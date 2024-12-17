import requests
from bs4 import BeautifulSoup
from src.database.db_manager import get_db_session
from src.database.models import Lead
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YelpScraper:
    def __init__(self, query):
        self.query = query

    def run(self):
        try:
            url = f"https://www.yelp.com/search?find_desc={self.query}"
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')

            session = get_db_session()
            for business in soup.select('.businessName__09f24__3Ml2X'):
                name = business.text.strip()
                location = business.find_next('address').text.strip()

                lead = Lead(
                    platform="yelp",
                    company_name=name,
                    location=location
                )
                session.add(lead)
            session.commit()
            session.close()
        except Exception as e:
            logger.error(f"Error in YelpScraper: {e}") 