"""
The `linkedin` package contains classes, functions, and utilities for scraping leads
and profiles from LinkedIn Sales Navigator. It provides interfaces for:
- Managing personas and their associated filters.
- Authenticating and simulating human-like interaction patterns to reduce detection.
- Executing the scraping process to retrieve leads and store them in a database.
"""

import logging

# Set up a basic logger for this module (optional, may be handled globally)
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# Public API imports:
from .scraper import LinkedInSalesNavigatorScraper
from .persona_definitions import IndustryPersonas, PersonaConfig
from .filters import CompanySize, Seniority, SalesNavigatorFilters
from .authenticator import authenticate
from .anti_detection import RateLimitManager

__all__ = [
    "LinkedInSalesNavigatorScraper",
    "IndustryPersonas",
    "PersonaConfig",
    "CompanySize",
    "Seniority",
    "SalesNavigatorFilters",
    "authenticate",
    "RateLimitManager"
]
