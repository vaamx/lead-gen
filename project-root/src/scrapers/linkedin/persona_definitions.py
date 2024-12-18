"""
Defines persona configurations for various industry niches and use cases,
providing reusable, parameterized Sales Navigator search criteria and associated metadata.

The `IndustryPersonas` class contains static methods returning `PersonaConfig` dictionaries
tailored to specific industries or targeting strategies.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from .filters import CompanySize, Seniority, SalesNavigatorFilters


@dataclass
class PersonaConfig:
    """
    Represents a persona configuration which includes:
    - A unique name identifying the persona or targeting strategy.
    - Pre-built search parameters (filters and keywords) for Sales Navigator.
    - A call-to-action message (CTA) to be used when reaching out to leads.
    - Optional tags for categorization or analytics purposes.

    This class enforces that the `name` and `search_params` fields are present and not empty.
    """
    name: str
    search_params: Dict[str, Any]
    cta: str
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Validate that all required fields are present."""
        if not self.name:
            raise ValueError("PersonaConfig requires a 'name' field.")
        if not self.search_params:
            raise ValueError("PersonaConfig requires 'search_params' to be defined.")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the persona configuration into a dictionary. Useful when passing configurations
        around without needing a full object.

        Returns:
            A dictionary containing all persona attributes.
        """
        return {
            "name": self.name,
            "search_params": self.search_params,
            "cta": self.cta,
            "tags": self.tags
        }


class IndustryPersonas:
    """
    Provides predefined persona configurations for various industries and targeting strategies.
    Each method returns a dictionary that can be directly passed to `PersonaConfig` or used
    as input to the scraper.

    These personas leverage the `SalesNavigatorFilters` class to create well-structured,
    detailed search parameters for LinkedIn Sales Navigator queries.
    """

    @staticmethod
    def ai_automation_persona() -> Dict[str, Any]:
        """
        Targets small to medium-sized companies in marketing, advertising, and IT sectors
        with a focus on automation and operational efficiency.
        """
        filters = SalesNavigatorFilters(
            company_sizes=[CompanySize.MICRO, CompanySize.SMALL, CompanySize.MEDIUM],
            industry_keywords=[
                "Marketing and Advertising",
                "Computer Software",
                "E-Commerce",
                "Digital Marketing",
                "Information Technology"
            ],
            job_titles=[
                "Marketing Director",
                "Digital Marketing Manager",
                "Operations Manager",
                "Agency Owner",
                "E-Commerce Manager",
                "Marketing Operations"
            ],
            seniority_levels=[Seniority.FOUNDER, Seniority.DIRECTOR, Seniority.MANAGER],
            keywords=["automation", "marketing automation", "operational efficiency"],
            locations=["United States", "United Kingdom", "Canada"]
        ).to_search_query()

        return {
            "name": "AI Automation Services",
            "search_params": filters,
            "cta": "Let me show you how you can save 20+ hours per week.",
            "tags": ["ai", "automation", "efficiency"]
        }

    @staticmethod
    def opscale_persona() -> Dict[str, Any]:
        """
        Targets medium to large companies using technology stacks like ERP/CRM and focusing
        on operational efficiency. Ideal for Ops leaders looking to streamline field operations.
        """
        filters = SalesNavigatorFilters(
            company_sizes=[CompanySize.MEDIUM, CompanySize.MEDIUM_LARGE, CompanySize.LARGE],
            industry_keywords=[
                "Software as a Service",
                "Logistics and Supply Chain",
                "Medical Devices",
                "Healthcare",
                "Field Services"
            ],
            job_titles=[
                "Operations Director",
                "Chief Operating Officer",
                "Head of Operations",
                "VP Operations",
                "Field Operations Manager"
            ],
            seniority_levels=[Seniority.CXO, Seniority.VP, Seniority.DIRECTOR],
            keywords=["operational efficiency", "process automation", "field operations"],
            locations=["United States", "Canada"],
            technologies_used=["ERP", "CRM", "Field Service Software"]
        ).to_search_query()

        return {
            "name": "Opscale AI Dashboard",
            "search_params": filters,
            "cta": "Get actionable insights to boost efficiency.",
            "tags": ["operations", "ai", "dashboard", "insights"]
        }

    @staticmethod
    def web3_persona() -> Dict[str, Any]:
        """
        Targets global blockchain and fintech companies, focusing on individuals involved
        in web3 technologies, smart contracts, NFTs, and DeFi.
        """
        filters = SalesNavigatorFilters(
            company_sizes=[CompanySize.MICRO, CompanySize.SMALL, CompanySize.MEDIUM],
            industry_keywords=[
                "Blockchain",
                "Cryptocurrency",
                "Financial Technology",
                "Computer Software",
                "Internet"
            ],
            job_titles=[
                "Founder",
                "CTO",
                "Blockchain Developer",
                "Smart Contract Developer",
                "Project Manager"
            ],
            seniority_levels=[Seniority.FOUNDER, Seniority.CXO, Seniority.HEAD],
            keywords=["smart contracts", "NFT", "web3", "blockchain", "defi"],
            locations=["Global"],
            active_last_30_days=True
        ).to_search_query()

        return {
            "name": "Smart Contract Services",
            "search_params": filters,
            "cta": "Let's audit your contracts before launch.",
            "tags": ["web3", "blockchain", "smart-contracts"]
        }

    @staticmethod
    def gaming_persona() -> Dict[str, Any]:
        """
        Targets small to medium-sized gaming and entertainment companies focusing on roles
        that influence game design, player retention, and monetization strategies.
        """
        filters = SalesNavigatorFilters(
            company_sizes=[CompanySize.SMALL, CompanySize.MEDIUM],
            industry_keywords=[
                "Gaming",
                "Computer Games",
                "Entertainment",
                "Mobile Games"
            ],
            job_titles=[
                "Game Producer",
                "Game Designer",
                "Product Manager",
                "Economy Designer",
                "Studio Head"
            ],
            seniority_levels=[Seniority.HEAD, Seniority.DIRECTOR, Seniority.MANAGER],
            keywords=["game economy", "player retention", "monetization"],
            locations=["Global"]
        ).to_search_query()

        return {
            "name": "Game Economy Design",
            "search_params": filters,
            "cta": "Optimize your game economy and boost player retention.",
            "tags": ["gaming", "economy", "retention"]
        }

    @staticmethod
    def bankero_persona() -> Dict[str, Any]:
        """
        Targets fintech-oriented businesses in Latin America, focusing on financial management
        and payment optimization roles like CFOs and Finance Managers.
        """
        filters = SalesNavigatorFilters(
            company_sizes=[CompanySize.MICRO, CompanySize.SMALL, CompanySize.MEDIUM],
            industry_keywords=[
                "Financial Services",
                "Financial Technology",
                "Professional Services",
                "Technology"
            ],
            job_titles=[
                "Business Owner",
                "Founder",
                "Finance Manager",
                "CFO",
                "Financial Controller"
            ],
            seniority_levels=[Seniority.FOUNDER, Seniority.CXO, Seniority.DIRECTOR],
            keywords=["cash flow", "financial management", "payments"],
            locations=["Mexico", "Brazil", "Colombia", "Argentina", "Chile"],
            regions=["Latin America"]
        ).to_search_query()

        return {
            "name": "Bankero FinTech",
            "search_params": filters,
            "cta": "Let us optimize your cash flow today.",
            "tags": ["fintech", "finance", "cashflow"]
        }
