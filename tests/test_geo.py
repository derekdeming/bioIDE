import unittest
from db_wrapper import GeoDBWrapper

class TestGeoDBWrapper(unittest.TestCase):
    def setUp(self):
        self.geodb = GeoDBWrapper()

    def test_get_study_ids(self):
        # Use a search term that is known to return some results
        search_term = 'cancer'
        ids = self.geodb.get_study_ids(search_term)
        # Check that the function returns the correct data
        self.assertIsInstance(ids, list)
        self.assertTrue(all(isinstance(i, str) for i in ids))

    def test_fetch_study_data(self):
        # Use a study ID that is known to exist
        study_id = 'GSE159451'
        data = self.geodb.fetch_study_data(study_id)
        # Check that the function returns the correct data
        self.assertIsInstance(data, dict)

    # ... additional tests for other methods ...

if __name__ == '__main__':
    unittest.main()
