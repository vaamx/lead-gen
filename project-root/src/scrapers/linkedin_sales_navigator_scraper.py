import time
import logging
from src.common.playwright_driver import PlaywrightDriver
from src.common.utils import random_delay
from src.common.proxy_manager import ProxyManager
from src.database.db_manager import get_db_session
from src.database.models import Lead

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LinkedInSalesNavigatorScraper:
    def __init__(self, query, location=None, industry=None, company_size=None):
        self.query = query
        self.location = location
        self.industry = industry
        self.company_size = company_size
        self.proxy = ProxyManager.get_random_proxy()

    def run(self):
        try:
            with PlaywrightDriver(proxy=self.proxy, headless=True) as page:
                page.goto("https://www.linkedin.com/sales/search/people")
                page.fill("input[data-test-search-bar-input]", self.query)

                # Fill in additional filters if provided
                if self.location:
                    page.fill("input[data-test-location-input]", self.location)
                if self.industry:
                    page.fill("input[data-test-industry-input]", self.industry)
                if self.company_size:
                    page.fill("input[data-test-company-size-input]", self.company_size)

                page.keyboard.press("Enter")
                random_delay()

                leads = []
                result_cards = page.query_selector_all(".result-lockup")
                for card in result_cards:
                    first_name, last_name = self.parse_name(card)
                    job_title = card.query_selector(".result-lockup__highlight").inner_text().strip()
                    company_name = card.query_selector(".result-lockup__subtitle").inner_text().strip()
                    profile_url = card.query_selector(".result-lockup__name a").get_attribute("href")

                    leads.append({
                        "platform": "linkedin",
                        "first_name": first_name,
                        "last_name": last_name,
                        "job_title": job_title,
                        "company_name": company_name,
                        "linkedin_url": profile_url,
                    })

                session = get_db_session()
                for lead in leads:
                    db_lead = Lead(**lead)
                    session.add(db_lead)
                session.commit()
                session.close()
                
                time.sleep(2)  # Rate limiting to avoid detection
        except Exception as e:
            logger.error(f"Error in LinkedInSalesNavigatorScraper: {e}")

    def parse_name(self, card):
        full_name = card.query_selector(".result-lockup__name a").inner_text().strip()
        parts = full_name.split(" ")
        return parts[0], " ".join(parts[1:])
        