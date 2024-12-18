import time
import logging
from random import uniform
from src.common.playwright_driver import PlaywrightDriver
from src.common.utils import random_delay
from src.common.proxy_manager import ProxyManager
from src.database.db_manager import get_db_session
from src.database.models import Lead

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LinkedInSalesNavigatorScraper:
    def __init__(self, persona):
        """
        Initializes the scraper with a persona configuration.

        :param persona: Dictionary containing search parameters for the persona.
        """
        self.persona = persona
        self.proxy = ProxyManager.get_random_proxy()

    def run(self):
        """
        Executes the scraper to fetch LinkedIn profiles based on persona filters.
        """
        logger.info(f"Starting scraper for persona: {self.persona['name']}...")
        try:
            with PlaywrightDriver(proxy=self.proxy, headless=True) as page:
                self.navigate_to_search(page)
                leads = self.extract_leads(page)

                if not leads:
                    logger.warning(f"No leads found for persona: {self.persona['name']}")
                    return

                self.save_to_database(leads)
                logger.info(f"Successfully saved {len(leads)} leads to the database for persona: {self.persona['name']}.")
        except Exception as e:
            logger.exception(f"An error occurred while scraping for persona {self.persona['name']}: {e}")
        finally:
            logger.info(f"Scraper completed for persona: {self.persona['name']}.")

    def navigate_to_search(self, page):
        """
        Navigate to LinkedIn Sales Navigator search page and apply persona filters.
        """
        logger.info(f"Navigating to LinkedIn Sales Navigator for persona: {self.persona['name']}...")
        page.goto("https://www.linkedin.com/sales/search/people")
        random_delay()

        # Apply query and persona filters
        page.fill("input[data-test-search-bar-input]", self.persona.get("query", ""))
        logger.info(f"Search query entered: {self.persona.get('query', '')}")

        filters = self.persona.get("filters", {})
        for filter_name, filter_value in filters.items():
            try:
                selector = self.get_filter_selector(filter_name)
                if selector:
                    page.fill(selector, filter_value)
                    logger.info(f"Applied filter - {filter_name}: {filter_value}")
            except Exception as e:
                logger.warning(f"Failed to apply filter {filter_name}: {e}")

        # Execute the search
        page.keyboard.press("Enter")
        random_delay()

    def get_filter_selector(self, filter_name):
        """
        Returns the CSS selector for a given filter.

        :param filter_name: Name of the filter (e.g., "location", "industry").
        :return: CSS selector string for the filter input.
        """
        filter_selectors = {
            "location": "input[data-test-location-input]",
            "industry": "input[data-test-industry-input]",
            "company_size": "input[data-test-company-size-input]",
            "job_roles": "input[data-test-title-input]"
        }
        return filter_selectors.get(filter_name)

    def extract_leads(self, page):
        """
        Extracts leads from search results.

        :param page: Playwright page object.
        :return: List of extracted leads.
        """
        logger.info("Extracting leads from search results...")
        leads = []
        result_cards = page.query_selector_all(".result-lockup")

        for idx, card in enumerate(result_cards):
            try:
                # Ensure that the expected elements exist before accessing them
                if not card:
                    logger.warning(f"Result card #{idx + 1} is None.")
                    continue
                first_name, last_name = self.parse_name(card)
                job_title = self.safe_query_text(card, ".result-lockup__highlight")
                company_name = self.safe_query_text(card, ".result-lockup__subtitle")
                profile_url = self.safe_query_attribute(card, ".result-lockup__name a", "href")

                if profile_url:
                    lead = {
                        "platform": "linkedin",
                        "persona": self.persona['name'],
                        "first_name": first_name,
                        "last_name": last_name,
                        "job_title": job_title,
                        "company_name": company_name,
                        "linkedin_url": profile_url,
                        "cta": self.persona.get("cta", ""),
                    }
                    leads.append(lead)
            except Exception as e:
                logger.warning(f"Failed to parse lead #{idx + 1}: {e}")

        logger.info(f"Extracted {len(leads)} leads.")
        return leads

    def parse_name(self, card):
        """
        Parse the name field into first and last name.

        :param card: Result card element.
        :return: Tuple of first and last name.
        """
        full_name = self.safe_query_text(card, ".result-lockup__name a")
        if full_name:
            parts = full_name.split(" ", 1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else ""
            return first_name, last_name
        return "", ""

    def safe_query_text(self, card, selector):
        """
        Safely query text content with a fallback for None.

        :param card: Result card element.
        :param selector: CSS selector for the text element.
        :return: Extracted text or an empty string.
        """
        element = card.query_selector(selector)
        return element.inner_text().strip() if element else ""

    def safe_query_attribute(self, card, selector, attribute):
        """
        Safely query an attribute with a fallback for None.

        :param card: Result card element.
        :param selector: CSS selector for the element.
        :param attribute: Attribute name to extract.
        :return: Extracted attribute value or None.
        """
        element = card.query_selector(selector)
        return element.get_attribute(attribute) if element else None

    def save_to_database(self, leads):
        """
        Save extracted leads to the database.

        :param leads: List of lead dictionaries to save.
        """
        logger.info("Saving leads to the database...")
        with get_db_session() as session:
            for lead in leads:
                try:
                    db_lead = Lead(**lead)
                    session.add(db_lead)
                except Exception as e:
                    logger.warning(f"Failed to save lead to database: {e}")
            session.commit()
        logger.info("Database transaction completed successfully.")


# Example usage with dynamic personas
if __name__ == "__main__":
    personas = [
        {
            "name": "Small Business Founders in AI Automation",
            "query": "CEO OR Founder OR CTO",
            "filters": {
                "location": "United States",
                "industry": "AI Automation",
                "company_size": "1-10",
            },
            "cta": "Let me show you how you can save 20+ hours per week."
        },
        {
            "name": "SaaS Executives",
            "query": "CEO OR COO OR Head of Operations",
            "filters": {
                "location": "Global",
                "industry": "SaaS",
                "company_size": "11-50",
            },
            "cta": "Get actionable insights to boost efficiency."
        }
    ]

    for persona in personas:
        scraper = LinkedInSalesNavigatorScraper(persona=persona)
        scraper.run()
