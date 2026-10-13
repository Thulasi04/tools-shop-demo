"""Cart Page Object representing the shopping cart view."""

from typing import List
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage
from locators.cart_locators import CartLocators
from utils.helpers import parse_price
from utils.logger import logger


class CartPage(BasePage):
    """Page Object for managing cart items, quantities, and totals."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.rows: Locator = page.locator(CartLocators.ROWS)
        self.product_titles: Locator = page.locator(CartLocators.PRODUCT_TITLES)
        self.quantity_inputs: Locator = page.locator(CartLocators.QUANTITY_INPUTS)
        self.product_prices: Locator = page.locator(CartLocators.PRODUCT_PRICES)
        self.line_prices: Locator = page.locator(CartLocators.LINE_PRICES)
        self.delete_buttons: Locator = page.locator(CartLocators.DELETE_BUTTONS)
        self.cart_total: Locator = page.locator(CartLocators.CART_TOTAL)
        self.proceed_button: Locator = page.locator(CartLocators.PROCEED_BUTTON)
        self.continue_shopping_btn: Locator = page.locator(CartLocators.CONTINUE_SHOPPING_BTN)

    def load(self) -> "CartPage":
        """Navigate directly to the cart / checkout view."""
        self.navigate("/checkout")
        self.page.wait_for_timeout(1000)
        return self

    def get_items_count(self) -> int:
        """Return the count of rows currently in the cart."""
        return self.product_titles.count()

    def get_product_titles(self) -> List[str]:
        """Return list of product names in the cart."""
        return [t.strip() for t in self.product_titles.all_inner_texts()]

    def update_quantity(self, index: int, new_quantity: int) -> None:
        """Update quantity of item at index and press Enter to save."""
        logger.info(f"Updating quantity of cart item {index} to {new_quantity}")
        qty_input = self.quantity_inputs.nth(index)
        qty_input.fill(str(new_quantity))
        qty_input.press("Enter")
        self.page.wait_for_timeout(1500)

    def remove_item(self, index: int = 0) -> None:
        """Click delete button for the item at given index."""
        logger.info(f"Removing item at index {index} from cart")
        self.delete_buttons.nth(index).click()
        self.page.wait_for_timeout(1500)

    def get_cart_total(self) -> float:
        """Retrieve total cart cost."""
        raw_total = self.get_text(self.cart_total)
        return parse_price(raw_total)

    def get_line_price(self, index: int = 0) -> float:
        """Retrieve line price for item at index."""
        raw_price = self.get_text(self.line_prices.nth(index))
        return parse_price(raw_price)

    def proceed_to_checkout(self) -> None:
        """Click proceed to checkout button (Step 1)."""
        logger.info("Proceeding to checkout step 1")
        self.proceed_button.click()
        self.page.wait_for_timeout(1000)
