"""
Interfaces
"""

from ._get_drug_name import get_drug_name
from ._get_summary import get_summary_dict, generate_hcp_insights
from ._PubMedScrapper import PubMedScrapper
from ._GenImager import GenImager
__all__: list[str] = [
    "get_drug_name",
    "generate_hcp_insights",
    "get_summary_dict",
    "GenImager",
    "PubMedScrapper"
]
