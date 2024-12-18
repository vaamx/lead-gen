"""
This module defines filter classes and enumerations for building LinkedIn Sales Navigator queries.
It provides strongly-typed structures for specifying company sizes, seniority levels, and filter
criteria that can be converted into a dictionary format for use with scraper logic.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Any


class CompanySize(Enum):
    """Enumerates possible company size categories for targeting on LinkedIn Sales Navigator."""
    MICRO = "1-10"
    SMALL = "11-50"
    MEDIUM = "51-200"
    MEDIUM_LARGE = "201-500"
    LARGE = "501-1000"
    ENTERPRISE = "1001+"


class Seniority(Enum):
    """Enumerates possible seniority levels for roles within a company."""
    CXO = "CXO"
    FOUNDER = "FOUNDER"
    VP = "VP"
    DIRECTOR = "Director"
    MANAGER = "Manager"
    HEAD = "Head"


@dataclass
class SalesNavigatorFilters:
    """
    Represents a set of filtering criteria for LinkedIn Sales Navigator queries.
    
    Attributes:
        company_sizes: A list of target company sizes.
        industry_keywords: Target industries (as keywords) that the companies operate in.
        job_titles: Job titles to match on target profiles.
        seniority_levels: A list of seniority levels to filter profiles by.
        keywords: Additional keywords to refine the search.
        locations: A list of geographic locations to target (e.g., "United States").
        company_headcount_growth: Optional headcount growth criterion (e.g., "Growing").
        company_revenue: Optional list of company revenue brackets.
        technologies_used: Optional list of technologies that target companies should use.
        regions: Optional list of more granular regions.
        posted_content: Whether to filter for profiles that posted content recently.
        active_last_30_days: Whether to filter for profiles that have been active within the last 30 days.
    """
    company_sizes: List[CompanySize] = field(default_factory=list)
    industry_keywords: List[str] = field(default_factory=list)
    job_titles: List[str] = field(default_factory=list)
    seniority_levels: List[Seniority] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    locations: List[str] = field(default_factory=list)
    company_headcount_growth: Optional[str] = "Growing"
    company_revenue: Optional[List[str]] = None
    technologies_used: Optional[List[str]] = None
    regions: Optional[List[str]] = None
    posted_content: Optional[bool] = True
    active_last_30_days: Optional[bool] = True

    def __post_init__(self) -> None:
        """Validate that required fields are properly populated and types are correct."""
        if not self.job_titles and not self.keywords:
            raise ValueError(
                "At least one job title or keyword must be provided to construct a meaningful query."
            )
        if not self.locations:
            raise ValueError(
                "At least one location must be provided for Sales Navigator filtering."
            )
        # Additional validation can be added here as needed.

    def to_search_query(self) -> Dict[str, Any]:
        """
        Convert filter criteria into a structured dictionary format.
        
        Returns:
            A dictionary that can be used to apply these filters in a Sales Navigator search.
        """
        # Build the keyword query (job titles OR'ed together, keywords AND'ed together)
        query_parts = []

        if self.job_titles:
            title_query = " OR ".join(f'"{title}"' for title in self.job_titles)
            query_parts.append(f"({title_query})")

        if self.keywords:
            keyword_query = " AND ".join(f'"{keyword}"' for keyword in self.keywords)
            query_parts.append(keyword_query)

        final_keywords = " AND ".join(query_parts) if query_parts else ""

        return {
            "keywords": final_keywords,
            "filterGroups": {
                "company": {
                    "size": [size.value for size in self.company_sizes],
                    "industry": self.industry_keywords,
                    "headcountGrowth": self.company_headcount_growth,
                    "technologies": self.technologies_used or []
                },
                "profile": {
                    "seniority": [level.value for level in self.seniority_levels],
                    "postedContent": self.posted_content,
                    "activeLastDays": 30 if self.active_last_30_days else None
                },
                "location": {
                    "regions": self.regions or [],
                    "locations": self.locations
                }
            }
        }
