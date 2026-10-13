"""Locators for Shopping Cart Page."""


class CartLocators:
    """Selectors for cart line items, quantity adjustments, deletion, and totals."""

    ROWS = "table tbody tr"
    PRODUCT_TITLES = "[data-test='product-title']"
    QUANTITY_INPUTS = "[data-test='product-quantity']"
    PRODUCT_PRICES = "[data-test='product-price']"
    LINE_PRICES = "[data-test='line-price']"
    DELETE_BUTTONS = "table tbody tr a.btn-danger"
    CART_TOTAL = "[data-test='cart-total']"
    PROCEED_BUTTON = "[data-test='proceed-1']"
    CONTINUE_SHOPPING_BTN = "[data-test='continue-shopping']"
