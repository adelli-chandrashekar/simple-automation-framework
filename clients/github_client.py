"""
OAuth API Client (GitHub)
=========================
WHY THIS FILE EXISTS:
    This demonstrates OAuth-style token-based authentication
    using GitHub's REST API.

    GitHub uses Personal Access Tokens (PATs), which are the result
    of an OAuth 2.0 flow. GitHub generates the token for you via
    their UI (Settings > Developer Settings > Personal Access Tokens).
    Your framework then uses this token exactly like an OAuth access_token.

THE OAUTH CONCEPT:
    1. You register your "app" (yourself) on GitHub's Auth Server (Settings page)
    2. GitHub gives you a token (PAT) — this IS the OAuth access_token
    3. You send this token as "Bearer <token>" in every API request
    4. GitHub's Resource Server (api.github.com) validates the token

KEY DESIGN DECISION:
    - URLs are NOT hardcoded here. They come from environments.json via Config.
    - This follows the same pattern as our api_client.py
"""

import logging
from clients.base_api_client import BaseAPIClient

logger = logging.getLogger(__name__)


class GitHubClient(BaseAPIClient):
    """
    GitHub API Client using OAuth Token (Personal Access Token).
    INHERITS all generic HTTP methods (get, post, etc.) from BaseAPIClient!

    Usage:
        client = GitHubClient(base_url="https://api.github.com", token="ghp_xxx")
        repos = client.get_my_repos()
    """

    def __init__(self, base_url, token, timeout=10):
        # 1. Call the parent class's constructor first!
        super().__init__(base_url, timeout)

        self.token = token

        # 2. Set the OAuth Bearer token in session headers
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        })
        logger.info("GitHubClient setup complete.")

    # ── ONLY GitHub-Specific Business Methods go here ──

    def get_authenticated_user(self):
        """Get the currently authenticated user's profile"""
        return self.get("/user")

    def get_my_repos(self):
        """List all repositories of the authenticated user"""
        return self.get("/user/repos", params={"sort": "updated", "per_page": 5})

    def get_repo(self, owner, repo_name):
        """Get details of a specific repository"""
        return self.get(f"/repos/{owner}/{repo_name}")

    def create_issue(self, owner, repo_name, title, body=""):
        """Create a new issue in a repository"""
        return self.post(f"/repos/{owner}/{repo_name}/issues", json={
            "title": title,
            "body": body
        })

    def close(self):
        """Close the session"""
        self.session.close()
        logger.info("GitHubClient session closed")
