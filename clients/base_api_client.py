"""
Base API Client
===============
WHY THIS FILE EXISTS:
    This demonstrates the OOP concept of INHERITANCE (Don't Repeat Yourself).
    Both our standard API (DummyJSON) and our OAuth API (GitHub) need to
    make GET, POST, PATCH, and DELETE requests.
    
    Instead of writing these exact same methods twice in two different files,
    we put them ONCE in this BaseAPIClient. Then, both APIClient and GitHubClient
    will INHERIT from this class.

WHAT YOU LEARN HERE:
    - OOP Inheritance: Parent class (BaseAPIClient) and Child classes
    - DRY Principle (Don't Repeat Yourself)
"""

import logging
import requests

logger = logging.getLogger(__name__)


class BaseAPIClient:
    """
    Parent class for all API clients.
    Contains the generic HTTP methods that every API needs.
    """

    def __init__(self, base_url, timeout=10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        logger.info(f"BaseAPIClient created for: {self.base_url}")

    def get(self, endpoint, **kwargs):
        """Send a GET request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET {url}")
        response = self.session.get(url, timeout=self.timeout, **kwargs)
        logger.info(f"  → {response.status_code}")
        return response

    def post(self, endpoint, json=None, **kwargs):
        """Send a POST request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST {url}")
        response = self.session.post(url, json=json, timeout=self.timeout, **kwargs)
        logger.info(f"  → {response.status_code}")
        return response

    def put(self, endpoint, json=None, **kwargs):
        """Send a PUT request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PUT {url}")
        response = self.session.put(url, json=json, timeout=self.timeout, **kwargs)
        logger.info(f"  → {response.status_code}")
        return response

    def patch(self, endpoint, json=None, **kwargs):
        """Send a PATCH request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PATCH {url}")
        response = self.session.patch(url, json=json, timeout=self.timeout, **kwargs)
        logger.info(f"  → {response.status_code}")
        return response

    def delete(self, endpoint, **kwargs):
        """Send a DELETE request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"DELETE {url}")
        response = self.session.delete(url, timeout=self.timeout, **kwargs)
        logger.info(f"  → {response.status_code}")
        return response

    def close(self):
        """Close the session (cleanup)"""
        self.session.close()
        logger.info(f"Session closed for {self.base_url}")
