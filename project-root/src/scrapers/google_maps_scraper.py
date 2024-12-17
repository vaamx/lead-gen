import requests
import logging
from src.config.config import Config
from src.database.db_manager import get_db_session
from src.database.models import Lead

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GoogleMapsScraper:
    def __init__(self, query):
        self.query = query

    def run(self):
        try:
            url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={self.query}&key={Config.GOOGLE_MAPS_API_KEY}"
            r = requests.get(url)
            data = r.json()

            session = get_db_session()
            for place in data.get("results", []):
                lead = Lead(
                    platform="google_maps",
                    company_name=place.get("name"),
                    location=place.get("formatted_address"),
                    rating=place.get("rating")
                )
                session.add(lead)
            session.commit()
            session.close()
        except Exception as e:
            logger.error(f"Error in GoogleMapsScraper: {e}") 