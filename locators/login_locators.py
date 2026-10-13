"""Locators for Login Page."""


class LoginLocators:
    """Selectors for email, password, login submission, error banners, and links."""

    EMAIL_INPUT = "[data-test='email']"
    PASSWORD_INPUT = "[data-test='password']"
    LOGIN_BUTTON = "[data-test='login-submit']"
    ERROR_MESSAGE = "[data-test='login-error']"
    REGISTER_LINK = "[data-test='register-link']"
    FORGOT_PASSWORD_LINK = "[data-test='forgot-password-link']"
