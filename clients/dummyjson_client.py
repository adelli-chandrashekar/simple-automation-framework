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
from clients.base_api_client import BaseAPIClient

logger = logging.getLogger(__name__)


class APIClient(BaseAPIClient):
    """
    Simple HTTP client for our basic tests.
    INHERITS all generic HTTP methods (get, post, etc.) from BaseAPIClient!

    Usage:
        client = APIClient("https://dummyjson.com")
        client.get("/users/1")
    """

    def __init__(self, base_url, timeout=10):
        # 1. Call the parent class's constructor first!
        super().__init__(base_url, timeout)

        # 2. Add APIClient-specific setup (like default headers)
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        logger.info("APIClient setup complete.")

    # ── ONLY APIClient-specific methods go here ──

    def set_auth_token(self, token):
        """
        Store auth token in session headers.
        """
        self.session.headers["Authorization"] = f"Bearer {token}"
        logger.info("Auth token set in session headers")

