"""Locators for Home Page and storefront navigation."""


class HomeLocators:
    """Selectors for header navigation, search bar, sort options, and catalog."""

    NAV_HOME = "[data-test='nav-home']"
    NAV_CATEGORIES = "[data-test='nav-categories']"
    NAV_HAND_TOOLS = "[data-test='nav-hand-tools']"
    NAV_POWER_TOOLS = "[data-test='nav-power-tools']"
    NAV_SPECIAL_TOOLS = "[data-test='nav-special-tools']"
    NAV_RENTALS = "[data-test='nav-rentals']"
    NAV_CONTACT = "[data-test='nav-contact']"
    NAV_SIGN_IN = "[data-test='nav-sign-in']"
    NAV_CART = "[data-test='nav-cart']"
    USER_MENU = "[data-test='nav-menu']"
    SIGN_OUT_BUTTON = "[data-test='nav-sign-out']"

    SEARCH_INPUT = "[data-test='search-query']"
    SEARCH_SUBMIT_BUTTON = "[data-test='search-submit']"
    SEARCH_RESET_BUTTON = "[data-test='search-reset']"
    SORT_DROPDOWN = "[data-test='sort']"

    PRODUCT_CARDS = "a.card"
    PRODUCT_NAMES = "[data-test='product-name']"
    PRODUCT_PRICES = "[data-test='product-price']"
    NO_RESULTS_MESSAGE = "[data-test='no-results']"
