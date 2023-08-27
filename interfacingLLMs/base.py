import requests
from abc import ABC, abstractmethod

class BaseDatabase(ABC):
    def __init__(self, name, base_url):
        self.name = name
        self.base_url = base_url
        self.session = requests.Session()

    @abstractmethod
    def get_endpoint_url(self, endpoint):
        """
        Return the full URL for a given API endpoint.
        This method must be overridden by subclasses.
        """
        pass

    def get(self, endpoint, **kwargs):
        """
        Send a GET request to the given API endpoint.
        """
        url = self.get_endpoint_url(endpoint)
        response = self.session.get(url, **kwargs)
        response.raise_for_status()  # Raise an exception if the request failed
        return response # assuming the response is in JSON format

    def close(self):
        """
        Close the session.
        """
        self.session.close()