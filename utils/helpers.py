"""
Helper Utilities
================
WHY THIS FILE EXISTS:
    Small reusable functions that our tests use repeatedly.
    Instead of writing the same assertion 50 times in tests,
    we write it once here and call it everywhere.

WHAT YOU LEARN HERE:
    - @staticmethod  : method that doesn't need 'self' — call directly
    - assert         : pytest's way of checking things
    - Clean error messages make debugging 10x faster
"""

import logging

logger = logging.getLogger(__name__)


class Validators:
    """
    Reusable assertion helpers.

    Usage (no need to create an instance!):
        Validators.check_status(response, 200)
        Validators.check_key(response, "name")
    """

    @staticmethod
    def check_status(response, expected):
        """Assert the HTTP status code matches"""
        actual = response.status_code
        assert actual == expected, (
            f"Expected status {expected}, got {actual}. "
            f"Body: {response.text[:200]}"
        )
        logger.info(f"✅ Status code: {actual}")

    @staticmethod
    def check_key_exists(response, key):
        """Assert a key exists in the JSON response"""
        data = response.json()
        assert key in data, f"Key '{key}' not found. Available: {list(data.keys())}"
        logger.info(f"✅ Key '{key}' found in response")

    @staticmethod
    def check_value(response, key, expected):
        """Assert a JSON key has the expected value"""
        data = response.json()
        actual = data.get(key)
        assert actual == expected, f"Expected '{key}'={expected}, got {actual}"
        logger.info(f"✅ {key} = {expected}")


def generate_user_payload(first_name="Chandra", last_name="Shekar", age=28, role="user"):
    """
    Generate a JSON payload for creating users in DummyJSON.
    Centralizing this here keeps our test files clean and adheres to DRY.
    """
    return {
        "firstName": first_name,
        "lastName": last_name,
        "age": age,
        "role": role
    }
