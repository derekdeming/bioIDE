### BioRxiv api 

# https://api.biorxiv.org/

# The format of the endpoint is https://api.biorxiv.org/details/[server]/[interval]/[cursor]/[format] or https://api.biorxiv.org/details/[server]/[DOI]/na/[format]

from .base import BaseDatabase

class BiorxivDatabase(BaseDatabase):
    """
    A wrapper for the BioRxiv API.

    This class provides methods to fetch details, preprint publications, published articles from the BioRxiv API.
    """

    def __init__(self):
        """
        Initialize the BiorxivDatabase instance.
        
        Sets the name of the database to 'Biorxiv' and the base URL to 'https://api.biorxiv.org'.
        """
        super().__init__('Biorxiv', 'https://api.biorxiv.org')

    def get_endpoint_url(self, endpoint):
        """
        Return the full URL for a given API endpoint.

        Args:
            endpoint (str): The endpoint of the API.

        Returns:
            str: The full URL for the given API endpoint.
        """
        return f"{self.base_url}/{endpoint}"

    def fetch_data(self, interval: str = None):
        if interval is None:
            interval = "2021-06-01/2021-06-05" 
        response = self.fetch_details(server="biorxiv", interval=interval)
        papers = response.json()['collection']
        return papers
    
    def fetch_details(self, server, interval, cursor=0, format='json', params=None):
        """
        Fetch details from the BioRxiv API.

        Args:
            server (str): The server name.
            interval (str): The interval.
            cursor (int, optional): The cursor. Defaults to 0.
            format (str, optional): The format of the response. Defaults to 'json'.

        Returns:
            dict: The response from the API as a dictionary.
        """
        endpoint = f"details/{server}/{interval}/{cursor}/{format}"
        return self.get(endpoint, params=params)

    def fetch_preprint_publications(self, server, interval, cursor=0, format='json'):
        """
        Fetch preprint publications from the BioRxiv API.

        Args:
            server (str): The server name.
            interval (str): The interval.
            cursor (int, optional): The cursor. Defaults to 0.
            format (str, optional): The format of the response. Defaults to 'json'.

        Returns:
            dict: The response from the API as a dictionary.
        """
        endpoint = f"pubs/{server}/{interval}/{cursor}/{format}"
        return self.get(endpoint)

    def fetch_published_articles(self, interval, cursor=0, format='json'):
        """
        Fetch published articles from the BioRxiv API.

        Args:
            interval (str): The interval.
            cursor (int, optional): The cursor. Defaults to 0.
            format (str, optional): The format of the response. Defaults to 'json'.

        Returns:
            dict: The response from the API as a dictionary.
        """
        endpoint = f"pub/{interval}/{cursor}/{format}"
        return self.get(endpoint)

    def fetch_summary_statistics(self, interval, format='json'):
        """
        Fetch summary statistics from the BioRxiv API.

        Args:
            interval (str): The interval.
            format (str, optional): The format of the response. Defaults to 'json'.

        Returns:
            dict: The response from the API as a dictionary.
        """
        endpoint = f"sum/{interval}"
        return self.get(endpoint)

    def fetch_usage_statistics(self, interval, format='json'):
        """
        Fetch usage statistics from the BioRxiv API.

        Args:
            interval (str): The interval.
            format (str, optional): The format of the response. Defaults to 'json'.

        Returns:
            dict: The response from the API as a dictionary.
        """
        endpoint = f"usage/{interval}/{format}"
        return self.get(endpoint)

