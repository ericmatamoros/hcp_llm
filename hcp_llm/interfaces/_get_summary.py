# -*- coding: utf-8 -*-
"""
Use LLM to gather a summary of the text.
"""

import json
from ._Summarizer import SummarizerAI

def get_summary_dict(config: dict, brand: str, text: str) -> dict:
    """Obtain summary of a provided scientific article.

    Provides a dictionary with:

    * General description of the drug
    * Specific positive effects on patient's health
    * Examples of improved efficiency over competitors
    * Potential reported side-effects
    *
    
    :param config: Settings.
    :param brand: Name of the specific drug to be fetched.
    :param text: Input text to be analysed.
    :return: Dictionary with different summary & insights obtained from the text.
    """

    prompt = f"""Return a dictionary that has the following keys: A, B, C, D, E, F and for each key the value should be:
    A) General description of what's {brand} drug used for including the profile of disease person or the molecular drug it targets (all in same sentence).
    B) Positive effects or impact of the drug {brand} on the health of the patients.
    C) Provide exact examples of improved efficiency over its competitors of drug {brand} in the trials performed. Give quantitative details if provided and any mentioned study.
    D) Side effects of {brand}. Give quantitative details if provided and any mentioned study. 
    E) Provide an overall summary of the article about {brand}. The summary should contain information of what was the study about, the methodology and results obtained.
    F) List other scientific literature mentioned on the text regarding the {brand}. Citations must include authors, article name & year.
    The text to be examined is: {text}"""

    model = SummarizerAI(config['openai_key'], prompt, config['model'], config['temperature'])
    response = model.get_response()

    output_dict = json.loads(response)
    return output_dict


def generate_hcp_insights(config: dict, brand: str,  overall_summary: dict) -> tuple:
    """Generate overall insights for HCP based on article-based summaries.
    
    :param config: Settings.
    :param brand: Name of the specific drug to be fetched.
    :param overall_summary: Summary per fetched article ID coming from 'get_summary_dict'.
    :return: Tuple with different generated summaries.
    """

    ids = list(overall_summary.keys())
    general = '\n'.join([overall_summary[x]['A'] for x in ids])
    positive_impact = '\n'.join([overall_summary[x]['B'] for x in ids])
    quantitative_examples = '\n'.join([overall_summary[x]['C'] for x in ids])
    side_effects = '\n'.join([overall_summary[x]['D'] for x in ids])
    articles =  '\n'.join([overall_summary[x]['E'] for x in ids])

    model = SummarizerAI(
        config['openai_key'],
        f"Here you have different summaries on the usage of {brand}, please make a final summary based on this texts: {general}" ,
        config['model'], config['temperature'])
    general_response = model.get_response()

    model = SummarizerAI(
        config['openai_key'],
        f"List positive effects of {brand} on patients health from: {positive_impact}." ,
        config['model'], config['temperature'])
    positive_response = model.get_response()

    model = SummarizerAI(
        config['openai_key'],
        f"Give a list with the different exact quantitative advantage of {brand} on the molecular experiements or patients health over its competitors from: {quantitative_examples}",
        config['model'], config['temperature'])
    quantitative_response = model.get_response().split("\n")

    model = SummarizerAI(
        config['openai_key'],
        f"Give a direct numeric list the different side-effects reported of {brand} from: {side_effects}. If there were no side-effects reported overall do not mention it.",
        config['model'], config['temperature'])
    side_effect_reponse = model.get_response().split("\n")

    model = SummarizerAI(
        config['openai_key'],
        f"Cite scientific literature/articles on: {articles}",
        config['model'], config['temperature'])
    articles = model.get_response().split("\n")

    return general_response, positive_response, quantitative_response, side_effect_reponse, articles