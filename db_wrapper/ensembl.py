# ensembl.py
from .base import BaseDatabase
import requests

class EnsemblDatabase(BaseDatabase):
    def __init__(self):
        super().__init__('ensembl', 'https://rest.ensembl.org')
    
    def get_endpoint_url(self, endpoint):
        return f"{self.base_url}/{endpoint}"

    def get_sequence_by_id(self, id):
        response = self.get(f"sequence/id/{id}", headers={"Content-Type": "application/json"})
        return response.text

    def get_gene_by_id(self, id):
        response = self.get(f"lookup/id/{id}", headers={"Content-Type": "application/json"})
        return response.text
    