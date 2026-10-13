"""Locators for Registration Page."""


class RegistrationLocators:
    """Selectors for new user registration form inputs, buttons, and validation banners."""

    FIRST_NAME_INPUT = "[data-test='first-name']"
    LAST_NAME_INPUT = "[data-test='last-name']"
    DOB_INPUT = "[data-test='dob']"
    COUNTRY_SELECT = "[data-test='country']"
    POSTAL_CODE_INPUT = "[data-test='postal_code']"
    HOUSE_NUMBER_INPUT = "[data-test='house_number']"
    STREET_INPUT = "[data-test='street']"
    CITY_INPUT = "[data-test='city']"
    STATE_INPUT = "[data-test='state']"
    PHONE_INPUT = "[data-test='phone']"
    EMAIL_INPUT = "[data-test='email']"
    PASSWORD_INPUT = "[data-test='password']"
    SUBMIT_BUTTON = "[data-test='register-submit']"
    VALIDATION_ERRORS = ".alert, .invalid-feedback, .text-danger, .help-block"
