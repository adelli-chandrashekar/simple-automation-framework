"""
Login Page
==========
Child of BasePage.
Contains Locators (tuples) and Business Logic methods for the SauceDemo login page.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    # ── Locators ──
    # We use tuples: (By.ID, "string")
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON   = (By.ID, "login-button")
    ERROR_MESSAGE  = (By.XPATH, "//h3[@data-test='error']")

    # ── Business Methods ──
    def login(self, username, password):
        """Perform the login action"""
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        """Retrieve the text of the login error message"""
        return self.get_text(self.ERROR_MESSAGE)
