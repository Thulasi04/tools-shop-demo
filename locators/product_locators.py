"""Locators for Product Details Page."""


class ProductLocators:
    """Selectors for product details, pricing, quantity counter, and add-to-cart actions."""

    PRODUCT_NAME = "[data-test='product-name']"
    UNIT_PRICE = "[data-test='unit-price']"
    PRODUCT_DESCRIPTION = "[data-test='product-description']"
    QUANTITY_INPUT = "[data-test='quantity']"
    INCREASE_QUANTITY_BTN = "[data-test='increase-quantity']"
    DECREASE_QUANTITY_BTN = "[data-test='decrease-quantity']"
    ADD_TO_CART_BTN = "[data-test='add-to-cart']"
    ADD_TO_FAVORITES_BTN = "[data-test='add-to-favorites']"
    TOAST_ALERT = ".toast-message, [role='alert']"
    NAV_CART = "[data-test='nav-cart']"
