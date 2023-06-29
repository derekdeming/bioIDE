from .base import BaseDatabase

class UniProtDatabase(BaseDatabase):
    def __init__(self):
        super().__init__("UniProt", "https://www.ebi.ac.uk/proteins/api")

    def get_endpoint_url(self, endpoint):
        return f"{self.base_url}/{endpoint}"

# PROTEIN 0 --- QUERY FUNCTIONALITY ISN'T WORKING YET  
    # def search_proteins(self, query, format="json"):
    #     """
    #     Search UniProt entries
    #     """
    #     response = self.get(f"proteins?query={query}&format={format}")
    #     return response.text

# PROTEIN 1 
    def get_protein_by_accession(self, accession, format="json"):
        """
        Get UniProt entry by accession
        """
        return self.get(f"proteins/{accession}?format={format}").text

# PROTEIN 2 
    def get_protein_isoforms_by_accession(self, accession, format="json"):
        """
        Get UniProt isoform entries from parent entry accession
        """
        return self.get(f"proteins/{accession}/isoforms?format={format}").text

# PROTEIN 3
    def get_protein_sequence_by_accession(self, accession):
        """
        Get protein sequence by accession

        returns a string of the protein sequence
        """
        return self.get(f"proteins/{accession}", headers={"Accept": "text/x-fasta"}).text

# PROTEIN 4
    def get_protein_features_by_accession(self, accession, format="json"):
        """
        Get protein features by accession
        """
        return self.get(f"features/{accession}?format={format}").text

# PROTEIN 5 -- QUERY FUNCTIONALITY ISN'T WORKING YET
    def search_protein_features(self, query, format="json"):
        """
        Search protein sequence features in UniProt
        """
        return self.get(f"features?query={query}&format={format}")
    
# PROTEIN 6
    def get_protein_variants_by_accession(self, accession, format="json"):
        """
        Get natural variants by UniProt accession

        returns a list of dicts with keys: dict_keys(['accession', 'entryName', 'proteinName', 
        'geneName', 'organismName', 'proteinExistence', 'sequence', 'sequenceChecksum', 'sequenceVersion', 
        'taxid', 'features'])
        """
        response = self.get(f"variation/{accession}?format={format}")
        return response.text

# PROTEIN 7
    def get_proteomics_by_accession(self, accession, format="json"):
        """
        Get proteomics peptides mapped to UniProt by accession
        """
        return self.get(f"proteomics/{accession}?format={format}").text

# PROTEIN 8
    def get_antigen_by_accession(self, accession, format="json"):
        """
        Get antigen by UniProt accession
        """
        return self.get(f"antigen/{accession}?format={format}").text

# PROTEIN 9
    def get_mutagenesis_by_accession(self, accession, format="json"):
        """
        Get mutagenesis mapped to UniProt by accession
        """
        return self.get(f"mutagenesis/{accession}?format={format}").text