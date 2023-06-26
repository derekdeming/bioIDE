import unittest
from unittest.mock import Mock, patch
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_wrapper import UniProtDatabase

class TestUniProtDatabase(unittest.TestCase):
    def setUp(self):
        self.uniprot = UniProtDatabase()

    @patch.object(UniProtDatabase, 'get')
    def test_search_proteins(self, mock_get):
        mock_get.return_value = Mock()
        self.uniprot.search_proteins('insulin')
        mock_get.assert_called_with('proteins?query=insulin&format=json')

    @patch.object(UniProtDatabase, 'get')
    def test_get_protein_by_accession(self, mock_get):
        mock_get.return_value = Mock()
        self.uniprot.get_protein_by_accession('P12345')
        mock_get.assert_called_with('proteins/P12345?format=json')

    @patch.object(UniProtDatabase, 'get')
    def test_get_protein_isoforms_by_accession(self, mock_get):
        mock_get.return_value = Mock()
        self.uniprot.get_protein_by_accession('P12345')
        mock_get.assert_called_with('proteins/P12345?format=json')

        # -------------------------------------

    def test_get_protein_sequence_by_accession(self):
        accession = "P12345"  # An example accession
        sequence = self.uniprot.get_protein_sequence_by_accession(accession)
        self.assertIsInstance(sequence, str)  # The sequence should be a string
        self.assertNotEqual(sequence, "")  # The sequence should not be empty

    def test_get_protein_features_by_accession(self):
        accession = "P12345"  # An example accession
        features = self.uniprot.get_protein_features_by_accession(accession)
        self.assertIsInstance(features, dict)  # The features should be a dictionary
        self.assertIn("features", features)  # The dictionary should contain a "features" key

    # def test_search_protein_features(self):
    #     query = "kinase"  # An example query
    #     results = self.uniprot.search_protein_features(query)
    #     self.assertIsInstance(results, dict)  # The results should be a dictionary
    #     self.assertIn("features", results)  # The dictionary should contain a "features" key

    # ... similar tests for the rest of the methods ...

if __name__ == '__main__':
    unittest.main()



    
