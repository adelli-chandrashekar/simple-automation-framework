"""
OAuth 2.0 Tests — GitHub API (Test Pyramid Structure)
======================================================
This file demonstrates the TEST PYRAMID in action:

    Layer 1: UNIT TESTS        — Test individual functions in isolation
    Layer 2: INTEGRATION TESTS — Test token + single API call together
    Layer 3: E2E TESTS         — Full flow: Auth → Create → Read → Verify → Cleanup

THE OAUTH FLOW:
    GitHub Settings (Auth Server)  →  Generates a PAT (access_token)
    Our Framework (Client)         →  Uses Bearer token in headers
    api.github.com (Resource Server) → Returns protected data

URLs come from environments.json — nothing is hardcoded in this file!
"""

import pytest
import logging

from clients.github_client import GitHubClient

logger = logging.getLogger(__name__)


# ==============================================================
# LAYER 1: UNIT TESTS (The Foundation — Fast, Isolated)
# ==============================================================
# These test the client's internal logic WITHOUT making real API calls.
# In a real framework, you would use mocking (unittest.mock) here.

@pytest.mark.oauth
class TestUnitOAuthClient:
    """Unit tests — verify the client object is constructed correctly"""

    def test_client_has_token(self, github_client):
        """UNIT: Verify the token was set in the client"""
        assert github_client.token is not None, "Token should not be None"
        assert len(github_client.token) > 0, "Token should not be empty"
        logger.info("UNIT: Token is present in the client")

    def test_client_has_auth_header(self, github_client):
        """UNIT: Verify the Bearer token is in session headers"""
        auth_header = github_client.session.headers.get("Authorization")
        assert auth_header is not None, "Authorization header should be set"
        assert auth_header.startswith("Bearer "), "Should use Bearer token scheme"
        logger.info("UNIT: Authorization header is correctly formatted")

    def test_client_base_url(self, github_client):
        """UNIT: Verify the base URL was loaded from config"""
        assert "github.com" in github_client.base_url, "Base URL should point to GitHub"
        logger.info(f"UNIT: Base URL is {github_client.base_url}")


# ==============================================================
# LAYER 2: INTEGRATION TESTS (The Walls — Token + Single API Call)
# ==============================================================
# These test that the token actually works against a real API.
# Each test makes ONE API call and verifies the response.

@pytest.mark.oauth
class TestIntegrationGitHubAPI:
    """Integration tests — verify token works with real GitHub API"""

    def test_authenticated_user(self, github_client):
        """INTEGRATION: Verify the token gives us access to user profile"""
        response = github_client.get_authenticated_user()

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "login" in data, "Response should contain GitHub username"
        assert "email" in data, "Response should contain email"
        logger.info(f"INTEGRATION: Authenticated as: {data['login']}")

    def test_list_my_repos(self, github_client):
        """INTEGRATION: Verify we can list the user's repositories"""
        response = github_client.get_my_repos()

        assert response.status_code == 200
        repos = response.json()
        assert isinstance(repos, list), "Should return a list of repos"
        logger.info(f"INTEGRATION: Found {len(repos)} repositories")

        for repo in repos[:3]:
            logger.info(f"  Repo: {repo['name']} | Stars: {repo.get('stargazers_count', 0)}")

    def test_get_specific_repo(self, github_client):
        """INTEGRATION: Fetch our automation framework repo details"""
        response = github_client.get_repo(
            "adelli-chandrashekar", "simple-automation-framework"
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "simple-automation-framework"
        logger.info(f"INTEGRATION: Repo '{data['name']}' has {data.get('stargazers_count', 0)} stars")


# ==============================================================
# LAYER 3: E2E TEST (The Roof — Full Lifecycle Flow)
# ==============================================================
# This tests the complete flow: Auth → Create → Read → Verify → Cleanup
# This is the single E2E flow the reviewer asked for!

@pytest.mark.oauth
class TestE2EGitHubLifecycle:
    """
    End-to-End test: Full lifecycle using OAuth token.
    CREATE an issue → READ it back → VERIFY data → CLOSE it
    All in one test, proving real-world integration.
    """

    def test_issue_lifecycle(self, github_client):
        """E2E: Create an issue, read it, verify it, then close it"""

        owner = "adelli-chandrashekar"
        repo = "simple-automation-framework"

        # 1. CREATE — open a new issue
        create_resp = github_client.create_issue(
            owner, repo,
            title="[Automated] OAuth 2.0 Test Issue",
            body="This issue was created by the automation framework to test OAuth 2.0 E2E flow."
        )
        assert create_resp.status_code == 201, f"Expected 201, got {create_resp.status_code}"
        issue_data = create_resp.json()
        issue_number = issue_data["number"]
        logger.info(f"E2E: CREATED issue #{issue_number}")

        # 2. READ — fetch the same issue we just created
        get_resp = github_client.get(f"/repos/{owner}/{repo}/issues/{issue_number}")
        assert get_resp.status_code == 200
        read_data = get_resp.json()
        assert read_data["title"] == "[Automated] OAuth 2.0 Test Issue"
        assert read_data["state"] == "open"
        logger.info(f"E2E: READ issue #{issue_number} — title verified")

        # 3. UPDATE — close the issue (PATCH)
        close_resp = github_client.patch(
            f"/repos/{owner}/{repo}/issues/{issue_number}",
            json={"state": "closed"}
        )
        assert close_resp.status_code == 200
        assert close_resp.json()["state"] == "closed"
        logger.info(f"E2E: CLOSED issue #{issue_number} — Full lifecycle complete!")
