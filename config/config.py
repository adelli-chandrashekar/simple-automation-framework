"""
Config Module
=============
WHY THIS FILE EXISTS:
    Every test needs to know WHERE to hit the API.
    Instead of hardcoding "https://reqres.in" in every test file,
    we load it ONCE from environments.json and share it everywhere.

WHAT YOU LEARN HERE:
    - __init__   : constructor — runs when you do Config()
    - @property  : makes a method look like a simple attribute
    - json.load  : reads a JSON file into a Python dictionary
"""

import os
import json


class Config:
    """
    Loads settings from environments.json.

    Usage:
        config = Config()           # loads "dev" environment by default
        config = Config("staging")  # loads "staging" environment
        print(config.base_url)      # "https://reqres.in"
    """

    def __init__(self, env=None):
        # Which environment? Check ENV variable, or default to "dev"
        self.env = env or os.environ.get("ENV", "dev")

        # Build path to environments.json (same folder as this file)
        config_file = os.path.join(os.path.dirname(__file__), "environments.json")

        # Load the JSON file into a Python dict
        with open(config_file, "r") as f:
            all_envs = json.load(f)

        # Pick our environment's settings (fall back to "dev" if not found)
        self._settings = all_envs.get(self.env, all_envs["dev"])

    @property
    def base_url(self):
        """The base URL for the API"""
        return self._settings.get("base_url")
        
    @property
    def ui_url(self):
        """The base URL for the UI tests"""
        return self._settings.get("ui_url")

    @property
    def timeout(self):
        """Request timeout in seconds"""
        return self._settings.get("timeout", 10)

    @property
    def auth_username(self):
        """Username for authentication"""
        return self._settings.get("auth_username")

    @property
    def auth_password(self):
        """Password for authentication"""
        return self._settings.get("auth_password")

    def get(self, key, default=None):
        """Get any setting by key name"""
        return self._settings.get(key, default)

    def __repr__(self):
        return f"Config(env='{self.env}', base_url='{self.base_url}')"
