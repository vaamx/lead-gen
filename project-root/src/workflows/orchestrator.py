from src.scrapers.linkedin_sales_navigator_scraper import LinkedInSalesNavigatorScraper
from src.common.utils import deduplicate_records
from src.database.db_manager import get_db_session

# Import other scrapers as needed


def run_full_pipeline():
    # LinkedIn Scraper
    linkedin = LinkedInSalesNavigatorScraper(query="AI Solutions")
    linkedin.run()

    # TODO: Add other scrapers like Apollo, Clutch, Yelp, Google Maps

    # Deduplication logic if not done already
    session = get_db_session()
    leads = session.query().from_statement("SELECT * FROM leads").all()  # Example only; adjust as needed
    unique_leads = deduplicate_records(leads, "email")
    # This would require either re-inserting unique leads into another table or adjusting logic.
    # For demonstration, assume already handled at insert time.
    session.close()

    # Possibly trigger n8n workflow here, or output to Google Sheets/Airtable 