"""Home Page Object for Practice Software Testing."""

from typing import List
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage
from locators.home_locators import HomeLocators
from utils.logger import logger


class HomePage(BasePage):
    """Page Object representing the storefront home page and product catalog."""

    def __init__(self, page: Page):
        super().__init__(page)
        # Navigation
        self.nav_home: Locator = page.locator(HomeLocators.NAV_HOME)
        self.nav_categories: Locator = page.locator(HomeLocators.NAV_CATEGORIES)
        self.nav_hand_tools: Locator = page.locator(HomeLocators.NAV_HAND_TOOLS)
        self.nav_power_tools: Locator = page.locator(HomeLocators.NAV_POWER_TOOLS)
        self.nav_special_tools: Locator = page.locator(HomeLocators.NAV_SPECIAL_TOOLS)
        self.nav_rentals: Locator = page.locator(HomeLocators.NAV_RENTALS)
        self.nav_contact: Locator = page.locator(HomeLocators.NAV_CONTACT)
        self.nav_sign_in: Locator = page.locator(HomeLocators.NAV_SIGN_IN)
        self.nav_cart: Locator = page.locator(HomeLocators.NAV_CART)
        self.user_menu: Locator = page.locator(HomeLocators.USER_MENU)
        self.sign_out_button: Locator = page.locator(HomeLocators.SIGN_OUT_BUTTON)

        # Search & Filter
        self.search_input: Locator = page.locator(HomeLocators.SEARCH_INPUT)
        self.search_submit_button: Locator = page.locator(HomeLocators.SEARCH_SUBMIT_BUTTON)
        self.search_reset_button: Locator = page.locator(HomeLocators.SEARCH_RESET_BUTTON)
        self.sort_dropdown: Locator = page.locator(HomeLocators.SORT_DROPDOWN)

        # Product elements
        self.product_cards: Locator = page.locator(HomeLocators.PRODUCT_CARDS)
        self.product_names: Locator = page.locator(HomeLocators.PRODUCT_NAMES)
        self.product_prices: Locator = page.locator(HomeLocators.PRODUCT_PRICES)
        self.no_results_message: Locator = page.locator(HomeLocators.NO_RESULTS_MESSAGE)

    def load(self) -> "HomePage":
        """Load the home page and wait for products to appear."""
        self.navigate("/")
        self.page.wait_for_selector(HomeLocators.PRODUCT_NAMES, timeout=10000)
        return self

    def search_product(self, term: str) -> None:
        """Search for a product term using the search form."""
        logger.info(f"Searching for product: '{term}'")
        self.search_input.fill(term)
        self.search_submit_button.click()
        self.page.wait_for_timeout(1000)

    def reset_search(self) -> None:
        """Click the search reset 'X' button."""
        logger.info("Resetting search")
        self.search_reset_button.click()
        self.page.wait_for_timeout(1000)

    def sort_by(self, sort_value: str) -> None:
        """Sort product catalog by given value (e.g., 'price,asc', 'name,desc')."""
        logger.info(f"Sorting products by: {sort_value}")
        self.sort_dropdown.select_option(value=sort_value)
        self.page.wait_for_timeout(1000)

    def filter_by_brand(self, brand_name: str) -> None:
        """Select a brand filter checkbox."""
        logger.info(f"Filtering by brand: {brand_name}")
        checkbox = self.page.locator(f"label:has-text('{brand_name}') input")
        checkbox.check()
        self.page.wait_for_timeout(1000)

    def filter_by_category(self, category_name: str) -> None:
        """Select a category filter checkbox."""
        logger.info(f"Filtering by category: {category_name}")
        checkbox = self.page.locator(f"label:has-text('{category_name}') input")
        checkbox.check()
        self.page.wait_for_timeout(1000)

    def get_product_names(self) -> List[str]:
        """Return list of product titles visible on current page."""
        return [text.strip() for text in self.product_names.all_inner_texts()]

    def get_product_count(self) -> int:
        """Return total count of visible product cards."""
        return self.product_names.count()

    def click_product_by_name(self, name: str) -> None:
        """Click on product card with matching name."""
        logger.info(f"Clicking product: {name}")
        self.page.locator(f"{HomeLocators.PRODUCT_NAMES}:has-text('{name}')").first.click()

    def click_first_product(self) -> None:
        """Click the first product card on the page."""
        self.product_names.first.click()

    def is_user_logged_in(self) -> bool:
        """Check if user profile menu is visible in navbar."""
        return self.is_visible(self.user_menu)

    def get_logged_in_user_name(self) -> str:
        """Retrieve user name from nav menu."""
        return self.get_text(self.user_menu)

    def logout(self) -> None:
        """Log out current user through user navigation menu."""
        logger.info("Logging out user")
        self.user_menu.click()
        self.sign_out_button.click()
        self.page.wait_for_selector(HomeLocators.NAV_SIGN_IN, timeout=5000)
