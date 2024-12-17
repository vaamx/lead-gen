import time
import logging
from src.common.playwright_driver import PlaywrightDriver
from src.common.utils import random_delay
from src.common.proxy_manager import ProxyManager
from src.common.email_validator import validate_email
from src.database.db_manager import get_db_session
from src.database.models import Lead

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LinkedInSalesNavigatorScraper:
    def __init__(self, query):
        self.query = query
        self.proxy = ProxyManager.get_random_proxy()

    def run(self):
        try:
            with PlaywrightDriver(proxy=self.proxy, headless=True) as page:
                page.goto("https://www.linkedin.com/sales/search/people")
                page.fill("input[data-test-search-bar-input]", self.query)
                page.keyboard.press("Enter")
                random_delay()

                leads = []
                result_cards = page.query_selector_all(".result-lockup")
                for card in result_cards:
                    first_name, last_name = self.parse_name(card)
                    job_title = card.query_selector(".result-lockup__highlight").inner_text().strip()
                    company_name = card.query_selector(".result-lockup__subtitle").inner_text().strip()
                    profile_url = card.query_selector(".result-lockup__name a").get_attribute("href")
                    email_data = validate_email(f"{first_name.lower()}@{company_name.lower().replace(' ','')}")

                    leads.append({
                        "platform":"linkedin",
                        "first_name": first_name,
                        "last_name": last_name,
                        "job_title": job_title,
                        "company_name": company_name,
                        "linkedin_url": profile_url,
                        "email": email_data["email"],
                        "email_status": email_data["status"]
                    })

                session = get_db_session()
                for lead in leads:
                    db_lead = Lead(**lead)
                    session.add(db_lead)
                session.commit()
                session.close()
        except Exception as e:
            logger.error(f"Error in LinkedInSalesNavigatorScraper: {e}")

    def parse_name(self, card):
        full_name = card.query_selector(".result-lockup__name a").inner_text().strip()
        parts = full_name.split(" ")
        return parts[0], " ".join(parts[1:]) 