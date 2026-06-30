"""
Inventory Page
==============
The page you land on after a successful login in SauceDemo.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class InventoryPage(BasePage):
    # ── Locators ──
    HEADER_TITLE = (By.CLASS_NAME, "title")

    # ── Business Methods ──
    def is_header_displayed(self):
        """Verify we are on the inventory page by checking the header"""
        return self.is_element_displayed(self.HEADER_TITLE)
        
    def get_header_text(self):
        return self.get_text(self.HEADER_TITLE)
