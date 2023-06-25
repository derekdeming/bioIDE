import requests
from xml.etree import ElementTree

class GeoDatabase:
    BASE_URL = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    
    def __init__(self, db):
        self.db = db
    
    def esearch(self, term):
        esearch_url = f"{self.BASE_URL}/esearch.fcgi"
        params = {"db": self.db, "term": term, "usehistory": "y"}
        response = requests.get(esearch_url, params=params)
        if response.status_code == 200:
            root = ElementTree.fromstring(response.content)
            count = int(root.find('Count').text)
            WebEnv = root.find('WebEnv').text
            query_key = root.find('QueryKey').text
            return count, WebEnv, query_key
        else:
            response.raise_for_status()

    def efetch(self, WebEnv, query_key, retstart, retmax):
        efetch_url = f"{self.BASE_URL}/efetch.fcgi"
        params = {
            "db": self.db,
            "WebEnv": WebEnv,
            "query_key": query_key,
            "retstart": retstart,
            "retmax": retmax
        }
        response = requests.get(efetch_url, params=params)
        if response.status_code == 200:
            return response.text
        else:
            response.raise_for_status()

    def fetch_records(self, term, retmax):
        count, WebEnv, query_key = self.esearch(term)
        for retstart in range(0, count, retmax):
            yield self.efetch(WebEnv, query_key, retstart, retmax)
