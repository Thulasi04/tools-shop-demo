"""Registration Page Object for Practice Software Testing."""

from typing import Dict, Any, List
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage
from locators.registration_locators import RegistrationLocators
from utils.logger import logger


class RegistrationPage(BasePage):
    """Page Object representing the new user registration page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name_input: Locator = page.locator(RegistrationLocators.FIRST_NAME_INPUT)
        self.last_name_input: Locator = page.locator(RegistrationLocators.LAST_NAME_INPUT)
        self.dob_input: Locator = page.locator(RegistrationLocators.DOB_INPUT)
        self.country_select: Locator = page.locator(RegistrationLocators.COUNTRY_SELECT)
        self.postal_code_input: Locator = page.locator(RegistrationLocators.POSTAL_CODE_INPUT)
        self.house_number_input: Locator = page.locator(RegistrationLocators.HOUSE_NUMBER_INPUT)
        self.street_input: Locator = page.locator(RegistrationLocators.STREET_INPUT)
        self.city_input: Locator = page.locator(RegistrationLocators.CITY_INPUT)
        self.state_input: Locator = page.locator(RegistrationLocators.STATE_INPUT)
        self.phone_input: Locator = page.locator(RegistrationLocators.PHONE_INPUT)
        self.email_input: Locator = page.locator(RegistrationLocators.EMAIL_INPUT)
        self.password_input: Locator = page.locator(RegistrationLocators.PASSWORD_INPUT)
        self.submit_button: Locator = page.locator(RegistrationLocators.SUBMIT_BUTTON)
        self.validation_errors: Locator = page.locator(RegistrationLocators.VALIDATION_ERRORS)

    def load(self) -> "RegistrationPage":
        """Navigate to the registration page."""
        self.navigate("/auth/register")
        self.page.wait_for_selector(RegistrationLocators.SUBMIT_BUTTON, timeout=20000)
        return self

    def fill_registration_form(self, user: Dict[str, Any]) -> None:
        """Fill all fields in the registration form from user dictionary."""
        logger.info(f"Filling registration form for: {user.get('email')}")
        self.first_name_input.fill(user.get("first_name", ""))
        self.last_name_input.fill(user.get("last_name", ""))
        self.dob_input.fill(user.get("dob", "1990-01-01"))

        address = user.get("address", {})
        country = address.get("country", "US")
        self.country_select.select_option(value=country)

        self.postal_code_input.fill(address.get("postal_code", "90210"))
        self.house_number_input.fill(address.get("house_number", "10"))
        self.street_input.fill(address.get("street", "123 Main St"))
        self.city_input.fill(address.get("city", "Testville"))
        self.state_input.fill(address.get("state", "CA"))

        self.phone_input.fill(user.get("phone", "1234567890"))
        self.email_input.fill(user.get("email", ""))
        self.password_input.fill(user.get("password", ""))

    def submit(self) -> None:
        """Click the registration submit button."""
        logger.info("Submitting registration form")
        self.submit_button.click()

    def register_user(self, user: Dict[str, Any]) -> None:
        """Convenience method to fill form and submit."""
        self.fill_registration_form(user)
        self.submit()

    def get_validation_errors(self) -> List[str]:
        """Collect all visible validation error messages."""
        return [text.strip() for text in self.validation_errors.all_inner_texts() if text.strip()]
