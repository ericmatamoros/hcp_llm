# -*- coding: utf-8 -*-
"""
Streamlit Application
"""

from datetime import datetime
import pandas as pd
import numpy as np
import streamlit as st


from hcp_llm.interfaces import (
    get_summary_dict,
    generate_hcp_insights,
    PubMedScrapper
)
from hcp_llm import general_settings, OpenAISettings


def hcp_interface(settings: dict):
    st.title("MedicalAid Summarizer")

    st.markdown("""
    The main purpose of this app is provided tailored brand-related insights that can be used by Healthcare Professionals to create
    informative marketing materials. The software uses PubMed to retrieve the articles and LLMs to make informed summaries and provide
    insightful data.
    """)

    st.sidebar.header("Input Details")
    # Dropdown for selecting the starting letter
    brand_options = sorted(['ENTRESTO', 'COSENTYX PSA', 'KISQALI', 'COSENTYX PSO', 'COSENTYX AXIAL SPA', 'KESIMPTA'])
    brand = st.sidebar.selectbox("Select Brand:", brand_options)

    if st.sidebar.button("Run"):
        with st.spinner("Retrieving data from PubMed. Please wait..."):
            # Run your scrapper with the selected brand
            scrapper = PubMedScrapper(query=f'{brand} efficiency')
            data = scrapper.get_data()
            st.success("Data Successfully retrived")

        data = data.sample(settings['sample_data'])

        if data.shape[0] != 0:
            overall_summary = {}

            with st.spinner("Gathering Insights from articles. Please wait..."):
                for ID in data.id:
                    df = data[data['id'] == ID]
                    summary = get_summary_dict(settings, brand, data.text.unique()[0])
                    overall_summary[ID] = summary
                general_response, positive_response, quantitative_response, side_effect_reponse = generate_hcp_insights(
                    settings, brand,  overall_summary
                )

            with st.expander(f"{brand} REPORT"):
                st.subheader("Description of drug:")
                st.write(general_response)
                st.write("")
                st.subheader("Positive Impact on Health:")
                st.write(positive_response)
                st.write("")
                st.subheader("Quantitative Improvement in Studies:")
                for quants in quantitative_response:
                    st.write(quants)
                st.write("")
                st.subheader("Reported side-effects:")
                for sides in side_effect_reponse:
                    st.write(sides)

            for ID in data.id:
                df = data[data['id'] == ID]
                summary = overall_summary[ID]

                # Use st.expander to create an expandable section for each article
                with st.expander(f"Article: {df.title[0]}"):
                    st.subheader("Details:")
                    # Display information in separate boxes inside the expander
                    st.write(f"Title: {df['title'].values[0]}")
                    st.write(f"PubMed Link: {df['pubmed_link'].values[0]}")
                    st.write(f"Authors: {df['author_names'].values[0]}")
                    st.write(f"Journal: {df['journal'].values[0]}")
                    st.write(f"Publication Date: {df['date_publication'].values[0]}")
                    st.subheader("Text Insights:")
                    keys_summary = list(summary.keys())
                    st.write(f"Summary: {summary[keys_summary[4]]}")
                    st.write(f"Positive Impact Reported: {summary[keys_summary[1]]}")
                    st.write(f"Impact over competitors: {summary[keys_summary[2]]}")
                    st.write(f"Side-effects: {summary[keys_summary[3]]}")
                    st.write(f"Potential cited articles: {summary[keys_summary[5]]}")
        else:
            st.warning("Didn't retrieve any data from PubMed. Re-phrase the query or check documentation.")

def main():
    st.set_page_config(page_title="MedicalAid Summarizer", page_icon="📈")

    settings = general_settings()
    settings['openai_key'] = OpenAISettings().openai_key

    hcp_interface(settings)

if __name__ == "__main__":
    main()