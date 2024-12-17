import requests
from bs4 import BeautifulSoup
from src.database.db_manager import get_db_session
from src.database.models import Lead
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClutchScraper:
    def __init__(self, query):
        self.query = query

    def run(self):
        try:
            url = f"https://clutch.co/search?query={self.query}"
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')

            session = get_db_session()
            for company in soup.select('.search-result'):
                name = company.select_one('.company-name').text.strip()
                website = company.select_one('.website-link')['href']
                industry = company.select_one('.industry').text.strip()
                location = company.select_one('.location').text.strip()

                lead = Lead(
                    platform="clutch",
                    company_name=name,
                    company_website=website,
                    industry=industry,
                    location=location
                )
                session.add(lead)
            session.commit()
            session.close()
        except Exception as e:
            logger.error(f"Error in ClutchScraper: {e}") 