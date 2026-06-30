import pytest
import logging
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

logger = logging.getLogger(__name__)

@pytest.mark.ui
@pytest.mark.smoke
class TestSauceDemoLogin:
    
    def test_login_success(self, driver):
        """Verify successful login with valid credentials"""
        logger.info("Initializing Page Objects")
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)
        
        logger.info("Attempting login as standard_user")
        login_page.login("standard_user", "secret_sauce")
        
        logger.info("Verifying successful redirect to inventory page")
        assert inventory_page.is_header_displayed(), "Inventory header should be visible"
        assert inventory_page.get_header_text() == "Products"
        logger.info("✅ Login successful")

    def test_login_locked_out_user(self, driver):
        """Verify error message for a locked out user"""
        login_page = LoginPage(driver)
        
        logger.info("Attempting login as locked_out_user")
        login_page.login("locked_out_user", "secret_sauce")
        
        error_msg = login_page.get_error_message()
        assert "locked out" in error_msg.lower()
        logger.info(f"✅ Verified error message: {error_msg}")

    def test_login_invalid_password(self, driver):
        """Verify error message for wrong password"""
        login_page = LoginPage(driver)
        
        logger.info("Attempting login with invalid password")
        login_page.login("standard_user", "wrong_password")
        
        error_msg = login_page.get_error_message()
        assert "do not match" in error_msg.lower()
        logger.info(f"✅ Verified error message: {error_msg}")
