"""
End-to-End API Tests (Users)
============================
THE SCENARIO:
    1. Auth session is set up in conftest.py (login once, reuse everywhere)
    2. Create a new user             → POST
    3. Read that user                → GET
    4. Update the user completely    → PUT
    5. Update the user partially     → PATCH
    6. Delete the user               → DELETE

WHAT YOU LEARN HERE:
    - @pytest.mark.api           : custom marker (run with: pytest -m api)
    - @pytest.mark.smoke         : tag critical tests
    - @pytest.mark.parametrize   : one test, many data sets
    - Test class (class TestXxx) : group related tests
    - Fixtures from conftest     : 'api_client' is injected automatically
"""

import pytest
import logging

from utils.helpers import Validators

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────
# TEST 1: LOGIN (Authentication check)
# ──────────────────────────────────────────────────────────────

@pytest.mark.api
@pytest.mark.smoke
class TestUserLogin:
    """POST /auth/login — test authentication separately"""

    def test_login_success(self, api_client, config):
        """Verify login works with valid credentials from config"""
        login_data = {
            "username": config.auth_username,
            "password": config.auth_password
        }
        
        # We test this specifically (even though conftest already logged in)
        # to ensure the login endpoint itself is working correctly.
        response = api_client.post("/auth/login", json=login_data)

        Validators.check_status(response, 200)
        Validators.check_key_exists(response, "accessToken")
        logger.info(f"Test login successful for: {response.json().get('username')}")

    def test_login_failure(self, api_client):
        """Verify login fails with bad credentials"""
        bad_data = {"username": "wrong", "password": "wrong"}
        response = api_client.post("/auth/login", json=bad_data)
        
        Validators.check_status(response, 400)


# ──────────────────────────────────────────────────────────────
# TEST 2: POST — Create User
# ──────────────────────────────────────────────────────────────

@pytest.mark.api
@pytest.mark.smoke
class TestCreateUser:
    """POST /users/add — create new users"""

    def test_create_single_user(self, api_client):
        """Create a single user and verify the response"""
        user_data = {
            "firstName": "Chandra",
            "lastName": "Shekar",
            "age": 28,
        }

        response = api_client.post("/users/add", json=user_data)

        Validators.check_status(response, 201)
        data = response.json()
        assert data["firstName"] == "Chandra"
        assert data["lastName"] == "Shekar"
        assert "id" in data, "Response should contain a generated 'id'"
        logger.info(f"Created user with id: {data['id']}")

    # PARAMETRIZE — One test definition, multiple test cases!
    @pytest.mark.parametrize("first_name, last_name, role", [
        ("Alice", "Smith", "admin"),
        ("Bob", "Johnson", "user"),
        ("Charlie", "Brown", "moderator"),
    ])
    def test_create_multiple_users(self, api_client, first_name, last_name, role):
        """Data-driven: create users with different roles"""
        user_data = {"firstName": first_name, "lastName": last_name, "role": role}

        response = api_client.post("/users/add", json=user_data)

        Validators.check_status(response, 201)
        data = response.json()
        assert data["firstName"] == first_name
        assert data["lastName"] == last_name


# ──────────────────────────────────────────────────────────────
# TEST 3: GET — Read User
# ──────────────────────────────────────────────────────────────

@pytest.mark.api
@pytest.mark.smoke
class TestGetUser:
    """GET /users — read users"""

    def test_get_user_by_id(self, api_client):
        """Get a specific user by ID"""
        response = api_client.get("/users/1")

        Validators.check_status(response, 200)
        Validators.check_key_exists(response, "firstName")
        Validators.check_value(response, "id", 1)

        data = response.json()
        assert "firstName" in data
        assert "email" in data
        assert "role" in data

    def test_get_all_users(self, api_client):
        """Get all users — should return paginated list"""
        response = api_client.get("/users")

        Validators.check_status(response, 200)
        data = response.json()
        logger.info(f"DATA: {data}")
        assert "users" in data
        assert len(data["users"]) > 0
        logger.info(f"Got {len(data['users'])} users in response")

    def test_get_nonexistent_user(self, api_client):
        """Verify 404 for a user that doesn't exist"""
        response = api_client.get("/users/999999")
        Validators.check_status(response, 404)

    # PARAMETRIZE — test multiple user IDs
    @pytest.mark.parametrize("user_id", [1, 2, 3])
    def test_get_multiple_users_by_id(self, api_client, user_id):
        """Data-driven: verify multiple users exist"""
        response = api_client.get(f"/users/{user_id}")
        Validators.check_status(response, 200)
        Validators.check_value(response, "id", user_id)


# ──────────────────────────────────────────────────────────────
# TEST 4: PUT and PATCH — Update User
# ──────────────────────────────────────────────────────────────

@pytest.mark.api
class TestUpdateUser:
    """PUT and PATCH /users — update users"""

    def test_put_update_user_full(self, api_client):
        """PUT = replace fields"""
        updated_data = {
            "firstName": "Chandra Updated",
            "lastName": "Shekar Updated",
            "age": 30
        }

        response = api_client.put("/users/1", json=updated_data)

        Validators.check_status(response, 200)
        data = response.json()
        assert data["firstName"] == "Chandra Updated"
        assert data["lastName"] == "Shekar Updated"
        logger.info("PUT full update successful")

    def test_patch_update_user_partial(self, api_client):
        """PATCH = update ONLY some fields"""
        partial_data = {"role": "superadmin"}

        response = api_client.patch("/users/1", json=partial_data)

        Validators.check_status(response, 200)
        assert response.json()["role"] == "superadmin"
        logger.info("PATCH partial update successful")


# ──────────────────────────────────────────────────────────────
# TEST 5: DELETE — Remove User
# ──────────────────────────────────────────────────────────────

@pytest.mark.api
class TestDeleteUser:
    """DELETE /users — remove a user"""

    def test_delete_user(self, api_client):
        """Delete a user and verify 200 OK + isDeleted flag"""
        response = api_client.delete("/users/1")

        Validators.check_status(response, 200)
        data = response.json()
        
        # dummyjson.com returns the deleted user data with an isDeleted flag
        assert data.get("isDeleted") is True
        assert data.get("id") == 1
        logger.info(f"User 1 deleted successfully at {data.get('deletedOn')}")
