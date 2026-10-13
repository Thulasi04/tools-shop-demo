"""Package containing locator classes for all application views."""

from locators.home_locators import HomeLocators
from locators.login_locators import LoginLocators
from locators.registration_locators import RegistrationLocators
from locators.product_locators import ProductLocators
from locators.cart_locators import CartLocators
from locators.checkout_locators import CheckoutLocators

__all__ = [
    "HomeLocators",
    "LoginLocators",
    "RegistrationLocators",
    "ProductLocators",
    "CartLocators",
    "CheckoutLocators",
]
