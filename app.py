# -*- coding: utf-8 -*-
"""
Streamlit Application
"""

from datetime import datetime
import pandas as pd
import numpy as np
import streamlit as st


from hcp_llm.interfaces import (
    get_drug_name,
    get_summary_dict,
    generate_hcp_insights,
    GenImager,
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
    # Select brabd
    brand_options = sorted(['ENTRESTO', 'COSENTYX PSA', 'KISQALI','KESIMPTA'])
    brand = st.sidebar.selectbox("Select Brand:", brand_options)

    # Obtain drug name & indication
    drug = get_drug_name(settings, brand.split(" ")[0])
    indication = st.sidebar.text_input("Indication:")
    early_year = st.sidebar.number_input("Retrieve articles from:", min_value=2000, max_value=datetime.now().year, step=1)
    brand_indication = f"{brand} used for {indication}"

    brand_text = f"{drug} AND {indication}".lower()

    keywords_input = st.sidebar.text_area("Enter keywords (one per line):", "")
    keywords_list = [keyword.strip() for keyword in keywords_input.split('\n') if keyword.strip()]

    if st.sidebar.button("Run"):
        with st.spinner("Retrieving data from PubMed. Please wait..."):
            # Run your scrapper with the selected brand
            scrapper = PubMedScrapper(query=brand_text)
            data = scrapper.get_data()
            st.success("Data Successfully retrived")

        if data.shape[0] != 0:
            # Filter by date of publication
            data = data[data['date_publication'].dt.year >= early_year]

            # Filter by keywords
            if len(keywords_list) != 0:
                text_column_lower = data['test'].str.lower()
                for keyword in keywords_list:
                    data[keyword] = text_column_lower.str.contains(keyword.lower())
                data = data[data[keywords_list].all(axis=1)]

            if settings['sample_data'] != -1:
                data = data.sample(settings['sample_data'])

            if data.shape[0] != 0:
                overall_summary = {}

                with st.spinner("Gathering Insights from articles. Please wait..."):
                    for ID in data.id:
                        df = data[data['id'] == ID]
                        text=  data.text.unique()[0]
                        tokens = text.split()
                        if len(tokens) > 16385:
                            text = " ".join(text.split()[-16300:])
                        
                        summary = get_summary_dict(settings, brand_indication, text)
                        overall_summary[ID] = summary
                    general_response, positive_response, quantitative_response, side_effect_reponse, articles = generate_hcp_insights(
                        settings, brand_indication,  overall_summary
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
                    st.subheader("Cited references:")
                    for sides in articles:
                        st.write(sides)

                    with st.spinner("Generating Image. Please wait..."):
                        image_prompt = f"""Generate real human image of the impact of {brand_indication} based on:
                            {general_response} - {positive_response}
                            No text on the image.
                            """
                        image_model = GenImager(settings['openai_key'], image_prompt, settings['model_image'])
                        images = image_model.get_image()
                        if len(images) != 0:
                            st.image(images)

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
        else:
            st.warning("Didn't retrieve any data from PubMed. Re-phrase the query or check documentation.")

def main():
    st.set_page_config(page_title="MedicalAid Summarizer", page_icon="📈")

    settings = general_settings()
    settings['openai_key'] = OpenAISettings().openai_key

    hcp_interface(settings)

if __name__ == "__main__":
    main()