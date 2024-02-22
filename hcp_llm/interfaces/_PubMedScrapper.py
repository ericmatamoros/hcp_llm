# -*- coding: utf-8 -*-
"""
Gather article details from the PubMed API
"""
from datetime import datetime
import pandas as pd
import requests
import xml.etree.ElementTree as ET


class PubMedScrapper:
    """PubMedScrapper class used to retrieve text details for a specific drug."""
    def __init__(self, query: str) -> None:
        self._query = query

    def get_data(self) -> pd.DataFrame:
        """Get data from PubMed article based on a given query.
        
        :return: Dataframe with data properties & text.
        """

        IDs = _search_articles(self._query)

        data_list = []
        if len(IDs) != 0:
            for ID in IDs:
                data_list.append(_retrieve_pubmed_content(str(ID)))

            data = pd.concat(data_list)
        else:
            data = pd.DataFrame()

        return data


def _retrieve_pubmed_content(pubmed_id: str) -> pd.DataFrame:
        """Retrieve article details from a given PubMed ID.

        Columns include: ID, Title, Link, Authors, Publication, Journal & Article Content.
        
        :param pubmed_id: ID of PubMed.
        :return: Dataframe with content.
        """
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        base_summary = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'
        params = {"db": "pubmed", "id": pubmed_id,"retmode": "xml"}
        params_summary = {"db": "pubmed", "id": pubmed_id,"retmode": "json"}

        response = requests.get(base_url, params=params)
        response_summary = requests.get(base_summary, params=params_summary).json()
        if (response.status_code == 200) & (len(response_summary['result']) != 0):
            root = ET.fromstring(response.text)
            
            # Extracting information from the XML response
            pub_date = response_summary['result'][pubmed_id]['pubdate']
            pub_date = pub_date.replace("-", " ")
            try:
                if len(pub_date.split(" ")) == 3:
                    year_month = pd.to_datetime(datetime.strptime(pub_date, '%Y %b %d'))
                elif len(pub_date.split(" ")) == 2:
                    year_month = pd.to_datetime(datetime.strptime(pub_date, '%Y %b'))
                else:
                    year_month = pd.to_datetime(datetime.strptime(pub_date, '%Y'))
            except:
                year_month = pd.to_datetime(pub_date.split(" ")[0])
            try:
                journal = root.find(".//Title").text
            except:
                 journal = 'Unknown'

            return pd.DataFrame({
                "id": [pubmed_id],
                "title": [response_summary['result'][pubmed_id]['title']],
                "pubmed_link": f'https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/',
                'author_names': [';'.join([author['name'] for author in response_summary['result'][pubmed_id]['authors']])],
                "date_publication": [year_month],
                "journal": [journal],
                "text": response.text
            })
        else:
            return pd.DataFrame()

def _search_articles(query: str) -> list:
        """Search PubMed IDs for articles that match a specific query.

        :param query: String as a query search to filter the articles.
        :return: List of IDs found in PubMed regarding a specific input query.
        """
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {
            "db": "pubmed",
            "term": query,
            "retmode": "json"
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        # Extract the PubMed IDs from the response
        pubmed_ids = data.get("esearchresult", {}).get("idlist", [])
        return pubmed_ids
    

