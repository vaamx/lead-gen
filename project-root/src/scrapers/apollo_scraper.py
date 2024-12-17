import requests
import logging
from src.config.config import Config
from src.common.email_validator import validate_email
from src.database.db_manager import get_db_session
from src.database.models import Lead

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ApolloScraper:
    def __init__(self, query):
        self.query = query

    def run(self):
        try:
            url = f"https://api.apollo.io/v1/mixed_people/search?query={self.query}"
            r = requests.get(url) # Authentication, cookies, headers needed
            data = r.json()

            session = get_db_session()
            for person in data.get("people", []):
                email_info = validate_email(person["email"]) if person.get("email") else {"email":"", "status":"unknown"}
                lead = Lead(
                    platform="apollo",
                    first_name=person["first_name"],
                    last_name=person["last_name"],
                    job_title=person["title"],
                    company_name=person["company"]["name"],
                    linkedin_url=person.get("linkedin_url"),
                    email=email_info["email"],
                    email_status=email_info["status"],
                    company_website=person["company"].get("website_url"),
                    industry=person["company"].get("industry"),
                    location=person["company"].get("location")
                )
                session.add(lead)
            session.commit()
            session.close()
        except Exception as e:
            logger.error(f"Error in ApolloScraper: {e}") 