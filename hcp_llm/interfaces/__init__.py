"""
Interfaces
"""

from ._get_summary import get_summary_dict, generate_hcp_insights
from ._PubMedScrapper import PubMedScrapper
__all__: list[str] = [
    "generate_hcp_insights",
    "get_summary_dict",
    "PubMedScrapper"
]
