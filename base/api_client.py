"""
API Client
==========
WHY THIS FILE EXISTS:
    Instead of writing requests.get(), requests.post() everywhere,
    we wrap them in a class. This gives us:
      - A base_url so we don't repeat "https://reqres.in" in every test
      - A session that keeps cookies and auth tokens alive
      - Logging so we can see what was sent and received

WHAT YOU LEARN HERE:
    - Class with __init__    : stores base_url and creates a session
    - Instance methods       : get(), post(), put(), patch(), delete()
    - requests.Session()     : reuses connections + keeps auth headers
    - Logging                : simple logging.info() for visibility
"""

import logging
import requests

logger = logging.getLogger(__name__)


class APIClient:
    """
    Simple HTTP client that wraps requests.Session.

    Usage:
        client = APIClient("https://reqres.in")
        response = client.get("/api/users/2")
        print(response.status_code)  # 200
        print(response.json())       # {...user data...}
    """

    def __init__(self, base_url, timeout=10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

        # Default headers — tell the server we're sending/expecting JSON
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        logger.info(f"APIClient created for: {self.base_url}")

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

    def set_auth_token(self, token):
        """
        Store auth token in session headers.
        Once set, EVERY future request from this client
        will automatically include this token — that's the
        power of requests.Session!
        """
        self.session.headers["Authorization"] = f"Bearer {token}"
        logger.info("Auth token set in session headers")

    def close(self):
        """Close the session (cleanup)"""
        self.session.close()
        logger.info("APIClient session closed")
