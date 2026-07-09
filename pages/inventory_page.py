"""
Inventory Page
==============
The page you land on after a successful login in SauceDemo.
Demonstrates:
  - find_element vs find_elements
  - Multiple locator strategies (ID, CSS, XPath)
  - ActionChains for hover/tooltip
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class InventoryPage(BasePage):
    # ── Locators using DIFFERENT strategies ──
    HEADER_TITLE = (By.CLASS_NAME, "title")

    # XPath: relative path using tag + attribute
    PRODUCT_NAMES = (By.XPATH, "//div[@class='inventory_item_name']")

    # CSS Selector: class-based
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".inventory_item_price")

    # XPath: locating the Add to Cart button by text content
    ADD_TO_CART_FIRST = (By.XPATH, "(//button[contains(text(),'Add to cart')])[1]")

    # ID-based: the shopping cart badge
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    # ── Business Methods ──
    def is_header_displayed(self):
        """Verify we are on the inventory page by checking the header"""
        return self.is_element_displayed(self.HEADER_TITLE)

    def get_header_text(self):
        return self.get_text(self.HEADER_TITLE)

    def get_all_product_names(self):
        """
        find_elements (plural!) — returns a LIST of all matching elements.
        Unlike find_element which returns ONE element or throws an exception,
        find_elements returns an empty list if nothing is found.
        """
        elements = self.driver.find_elements(*self.PRODUCT_NAMES)
        names = [el.text for el in elements]
        logger.info(f"Found {len(names)} products: {names}")
        return names

    def get_all_product_prices(self):
        """Extract all product prices as a list of floats"""
        elements = self.driver.find_elements(*self.PRODUCT_PRICES)
        # Strip the "$" sign and convert to float
        prices = [float(el.text.replace("$", "")) for el in elements]
        logger.info(f"Product prices: {prices}")
        return prices

    def add_first_product_to_cart(self):
        """Click the first 'Add to cart' button"""
        self.click(self.ADD_TO_CART_FIRST)
        logger.info("Added first product to cart")

    def get_cart_count(self):
        """
        Get the number on the cart badge.
        Uses try/except because the badge doesn't exist when cart is empty.
        """
        try:
            badge = self.driver.find_element(*self.CART_BADGE)
            return int(badge.text)
        except NoSuchElementException:
            logger.info("Cart is empty — no badge displayed")
            return 0

    def hover_over_product(self, index=0):
        """
        ActionChains: Hover over a product to trigger any tooltip or effect.
        This demonstrates mouse actions in Selenium.
        """
        products = self.driver.find_elements(*self.PRODUCT_NAMES)
        if index < len(products):
            actions = ActionChains(self.driver)
            actions.move_to_element(products[index]).perform()
            logger.info(f"Hovered over product: {products[index].text}")
