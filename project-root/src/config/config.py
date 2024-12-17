import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Proxies
    PROXY_LIST = os.getenv("PROXY_LIST", "").split(",")  # List of proxies

    # Captcha
    CAPTCHA_API_KEY = os.getenv("CAPTCHA_API_KEY")
    CAPTCHA_PROVIDER_URL = "http://2captcha.com/..."

    # Hunter.io
    HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")

    # Truemail
    TRUEMAIL_API_KEY = os.getenv("TRUEMAIL_API_KEY")

    # Databases
    DB_URI = os.getenv("DB_URI", "postgresql://user:pass@localhost:5432/leads")

    # Rate limits & Delays
    REQUEST_DELAY_MIN = 1
    REQUEST_DELAY_MAX = 5

    # User Agents
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
        "Mozilla/5.0 (X11; Linux x86_64)..."
    ] 