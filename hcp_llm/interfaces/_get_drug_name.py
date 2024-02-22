# -*- coding: utf-8 -*-
"""
Obtain drug name for a given brand.
"""

import requests

from ._Summarizer import SummarizerAI

def get_drug_name(config: dict, brand: str) -> str:
    """Get drug name from a given brand through rxnav API & using LLM to extract the specific name.

    :param config: Settings.
    :param brand: Commercial name of the drug.
    :return: String with the drug name.
    """

    base_url = "https://rxnav.nlm.nih.gov/REST/drugs.json?name="
    brand_lower = brand.lower().split(" ")[0]
    details = str(requests.get(f"{base_url}{brand_lower}").json()['drugGroup'])
    prompt_drug = f"""Give me a 1 word of the scientific name of the drug: {brand}: {details}"""

    model = SummarizerAI(config['openai_key'], prompt_drug, config['model'], config['temperature'])
    response = model.get_response()

    return response
