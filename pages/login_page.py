"""Login Page Object for Practice Software Testing."""

from playwright.sync_api import Page, Locator
from pages.base_page import BasePage
from locators.login_locators import LoginLocators
from utils.logger import logger


class LoginPage(BasePage):
    """Page Object representing the customer login page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input: Locator = page.locator(LoginLocators.EMAIL_INPUT)
        self.password_input: Locator = page.locator(LoginLocators.PASSWORD_INPUT)
        self.login_button: Locator = page.locator(LoginLocators.LOGIN_BUTTON)
        self.error_message: Locator = page.locator(LoginLocators.ERROR_MESSAGE)
        self.register_link: Locator = page.locator(LoginLocators.REGISTER_LINK)
        self.forgot_password_link: Locator = page.locator(LoginLocators.FORGOT_PASSWORD_LINK)

    def load(self) -> "LoginPage":
        """Navigate to the login page."""
        self.navigate("/auth/login")
        self.page.wait_for_selector(LoginLocators.LOGIN_BUTTON, timeout=10000)
        return self

    def login(self, email: str, password: str) -> None:
        """Perform login action with provided credentials.

        Args:
            email: Account email.
            password: Account password.
        """
        logger.info(f"Attempting login for user: {email}")
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_message(self) -> str:
        """Get the text of the login error banner."""
        return self.get_text(self.error_message)

    def click_register(self) -> None:
        """Click the registration link to navigate to register page."""
        self.register_link.click()
