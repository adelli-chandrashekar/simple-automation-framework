"""
conftest.py — Pytest Auto-Discovery Magic
==========================================
WHY THIS FILE EXISTS:
    conftest.py is SPECIAL. Pytest finds it automatically.
    Any fixture defined here is available to ALL tests — no import needed!

    If you put a fixture in conftest.py:
        def test_something(api_client):   ← pytest injects it automatically
                                             No "from conftest import ..." needed!

WHAT YOU LEARN HERE:
    - Fixture scopes: session vs function
    - yield           : setup → give to test → teardown (guaranteed cleanup)
    - Fixture chaining: one fixture depends on another
    - Auth session     : authenticate ONCE, reuse the session in every test
    - Pytest hooks     : customize pytest behavior

FIXTURE SCOPES (when does pytest create/destroy the fixture?):
    scope="session"   → created ONCE for the entire test run
    scope="function"  → created fresh for EACH test (default)
"""

import os
import sys
import time
import logging
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Add project root to path so imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.config import Config
from clients.dummyjson_client import APIClient
from clients.github_client import GitHubClient

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────
# PYTEST HOOK: Add Custom Command Line Options
# ──────────────────────────────────────────────────────────────
def pytest_addoption(parser):
    """
    This is a built-in Pytest Hook. It allows us to add our own custom
    command line arguments when running tests.
    Example: pytest --env=staging
    """
    parser.addoption(
        "--env", action="store", default="dev", help="Environment to run tests against: dev or staging"
    )

# ──────────────────────────────────────────────────────────────
# FIXTURE 0: driver — UI Automation Browser
# ──────────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def driver(config):
    """
    Function-scoped: A new browser window opens for EACH test.
    We don't share the browser between tests to ensure clean state.
    """
    logger.info("Starting Chrome Browser...")
    
    service = ChromeService(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    
    # We MUST run invisibly in CI/CD because there is no physical monitor!
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    driver.get(config.ui_url)
    
    yield driver
    
    logger.info("Closing Chrome Browser...")
    driver.quit()


# ──────────────────────────────────────────────────────────────
# FIXTURE 1: config — Created ONCE, shared by all tests
# ──────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def config(request):
    """
    Session-scoped: ONE Config object for the whole test run.
    It reads the '--env' argument we passed in the command line using pytest_addoption.
    """
    env_name = request.config.getoption("--env")
    return Config(env=env_name)


# ──────────────────────────────────────────────────────────────
# FIXTURE 2: api_client — Created ONCE, session reused
# ──────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def api_client(config):
    """
    Session-scoped API client that authenticates ONCE and shares
    the session across ALL tests.

    THE KEY PATTERN — "Login once, reuse everywhere":
        1. Create the client with base URL
        2. Send POST /auth/login with credentials from config
        3. Extract the 'accessToken'
        4. Set token in session headers via client.set_auth_token()
        5. yield the client → all future requests carry the token!

    'yield' splits this function into SETUP and TEARDOWN:
        - Everything BEFORE yield = setup
        - Everything AFTER yield  = teardown (always runs, even on failure)
    """
    # SETUP
    client = APIClient(base_url=config.base_url, timeout=config.timeout)

    # ── REAL AUTHENTICATION ──
    login_data = {
        "username": config.auth_username,
        "password": config.auth_password
    }
    
    logger.info("Authenticating with DummyJSON...")
    response = client.post("/auth/login", json=login_data)
    
    if response.status_code == 200:
        token = response.json().get("accessToken")
        client.set_auth_token(token)
        logger.info("✅ Login successful. Auth session ready.")
    else:
        logger.error(f"❌ Login failed: {response.text}")
        pytest.fail("Failed to authenticate API client")

    yield client  # ← All tests use this authenticated client

    # TEARDOWN — runs after the last test finishes
    client.close()


# ──────────────────────────────────────────────────────────────
# FIXTURE 3: test_logger — Auto-logs each test start/end
# ──────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def test_logger(request):
    """
    autouse=True means this runs for EVERY test automatically.
    No test needs to ask for it — it just runs.
    """
    test_name = request.node.name
    logger.info(f"{'='*50}")
    logger.info(f"TEST START: {test_name}")
    logger.info(f"{'='*50}")

    yield  # ← test runs here

    logger.info(f"TEST END: {test_name}")
    logger.info(f"{'='*50}")


# ──────────────────────────────────────────────────────────────
# FIXTURE 4: github_client — Global OAuth Client
# ──────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def github_client(config):
    """
    Session-scoped GitHub OAuth client.
    Reads the token and URL from environments.json via the config fixture.
    """
    client = GitHubClient(
        base_url=config.get("github_api_url"),
        token=config.get("github_token")
    )

    yield client

    client.close()


# ──────────────────────────────────────────────────────────────
# PYTEST HOOKS
# ──────────────────────────────────────────────────────────────
#
# WHAT ARE HOOKS?
#   Hooks are special functions that pytest calls at specific moments.
#   You just define a function with the right name, and pytest calls it.
#

import time

def pytest_configure(config):
    """
    DEFAULT HOOK: runs BEFORE any tests are collected.
    Good for: creating directories, setting up global state.
    """
    os.makedirs("reports", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Dynamically create a new log file for EVERY run with a timestamp
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    log_file_path = os.path.join("logs", f"automation_{timestamp}.log")
    
    # Tell pytest to use this new file instead of the one in pytest.ini
    config.option.log_file = log_file_path


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    DEFAULT HOOK: runs AFTER all tests finish.
    Good for: printing a custom summary.
    """
    passed = len(terminalreporter.stats.get("passed", []))
    failed = len(terminalreporter.stats.get("failed", []))
    skipped = len(terminalreporter.stats.get("skipped", []))

    logger.info(f"\n{'='*50}")
    logger.info(f"CUSTOM SUMMARY")
    logger.info(f"  Passed:  {passed}")
    logger.info(f"  Failed:  {failed}")
    logger.info(f"  Skipped: {skipped}")
    logger.info(f"  Total:   {passed + failed + skipped}")
    logger.info(f"{'='*50}")
