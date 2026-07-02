from base.api_client import APIClient
import logging

logger = logging.getLogger(__name__)

class UsersClient(APIClient):
    """
    Users Service Client
    ====================
    Inherits from the Base APIClient. 
    This is the "Service Client Pattern" requested by the mentor.

    Instead of having 500 different endpoints (users, products, auth) 
    all inside the base api_client.py, we create a specific client 
    for the Users service.

    Usage:
        users = UsersClient("https://dummyjson.com")
        response = users.get_user_by_id(1)
        users.create_user({"firstName": "Chandra"})
    """

    def __init__(self, base_url, timeout=10):
        # Call the parent __init__ to set up the session and base URL
        super().__init__(base_url, timeout)
        # We can add a specific prefix for all user endpoints
        self.endpoint = "/users"

    def get_user_by_id(self, user_id):
        """Fetch a specific user"""
        logger.info(f"Fetching user with ID: {user_id}")
        # Uses the inherited self.get() method from the Base APIClient
        return self.get(f"{self.endpoint}/{user_id}")

    def create_user(self, payload):
        """Create a new user"""
        logger.info("Creating a new user")
        # Uses the inherited self.post() method from the Base APIClient
        return self.post(f"{self.endpoint}/add", json=payload)

    def delete_user(self, user_id):
        """Delete a user"""
        logger.info(f"Deleting user with ID: {user_id}")
        return self.delete(f"{self.endpoint}/{user_id}")
