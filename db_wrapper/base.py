import requests
import json
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
        return response

    def post(self, endpoint, data=None, json=None, **kwargs):
        """
        Send a POST request to the given API endpoint.
        """
        url = self.get_endpoint_url(endpoint)
        response = self.session.post(url, data=data, json=json, **kwargs)
        response.raise_for_status()  # Raise an exception if the request failed
        return response.json()

    def put(self, endpoint, data=None, **kwargs):
        """
        Send a PUT request to the given API endpoint.
        """
        url = self.get_endpoint_url(endpoint)
        response = self.session.put(url, data=data, **kwargs)
        response.raise_for_status()  # Raise an exception if the request failed
        return response.json()

    def delete(self, endpoint, **kwargs):
        """
        Send a DELETE request to the given API endpoint.
        """
        url = self.get_endpoint_url(endpoint)
        response = self.session.delete(url, **kwargs)
        response.raise_for_status()  # Raise an exception if the request failed
        return response.status_code  # Usually, there's no body in a DELETE response

    def close(self):
        """
        Close the session.
        """
        self.session.close()
