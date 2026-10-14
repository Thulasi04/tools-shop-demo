"""Product Details Page Object."""

from playwright.sync_api import Page, Locator
from pages.base_page import BasePage
from locators.product_locators import ProductLocators
from utils.helpers import parse_price
from utils.logger import logger


class ProductPage(BasePage):
    """Page Object representing individual product detail pages."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.product_name: Locator = page.locator(ProductLocators.PRODUCT_NAME)
        self.unit_price: Locator = page.locator(ProductLocators.UNIT_PRICE)
        self.product_description: Locator = page.locator(ProductLocators.PRODUCT_DESCRIPTION)
        self.quantity_input: Locator = page.locator(ProductLocators.QUANTITY_INPUT)
        self.increase_quantity_btn: Locator = page.locator(ProductLocators.INCREASE_QUANTITY_BTN)
        self.decrease_quantity_btn: Locator = page.locator(ProductLocators.DECREASE_QUANTITY_BTN)
        self.add_to_cart_btn: Locator = page.locator(ProductLocators.ADD_TO_CART_BTN)
        self.add_to_favorites_btn: Locator = page.locator(ProductLocators.ADD_TO_FAVORITES_BTN)
        self.toast_alert: Locator = page.locator(ProductLocators.TOAST_ALERT)
        self.nav_cart: Locator = page.locator(ProductLocators.NAV_CART)

    def load_product(self, product_id: str) -> "ProductPage":
        """Navigate directly to product details by product ID with catalog fallback."""
        self.navigate(f"/product/{product_id}")
        try:
            self.page.wait_for_selector(ProductLocators.PRODUCT_NAME, timeout=20000)
        except Exception:
            logger.warning(f"Direct navigation to /product/{product_id} timed out; falling back to catalog click")
            self.navigate("/")
            self.page.wait_for_selector(".card, [data-test='product-name']", timeout=15000)
            self.page.locator(".card, a[href*='product/']").first.click()
            self.page.wait_for_selector(ProductLocators.PRODUCT_NAME, timeout=20000)
        return self

    def get_product_name(self) -> str:
        """Return the product name."""
        return self.get_text(self.product_name)

    def get_unit_price(self) -> float:
        """Return the numeric unit price."""
        return parse_price(self.get_text(self.unit_price))

    def get_description(self) -> str:
        """Return product description."""
        return self.get_text(self.product_description)

    def set_quantity(self, qty: int) -> None:
        """Directly type quantity into the quantity input."""
        logger.info(f"Setting product quantity to: {qty}")
        self.quantity_input.fill(str(qty))

    def increase_quantity(self) -> None:
        """Click the '+' button."""
        logger.info("Increasing quantity")
        self.increase_quantity_btn.click()

    def decrease_quantity(self) -> None:
        """Click the '-' button."""
        logger.info("Decreasing quantity")
        self.decrease_quantity_btn.click()

    def get_quantity(self) -> int:
        """Get current quantity input value."""
        return int(self.quantity_input.input_value() or "1")

    def add_to_cart(self) -> None:
        """Click Add to Cart button and wait for confirmation toast."""
        logger.info("Adding product to cart")
        self.page.wait_for_selector(f"{ProductLocators.ADD_TO_CART_BTN}:not([disabled])", timeout=10000)
        self.add_to_cart_btn.click()
        self.page.wait_for_selector(ProductLocators.TOAST_ALERT, timeout=6000)

    def get_toast_message(self) -> str:
        """Get text from toast alert notification."""
        return self.get_text(self.toast_alert)

    def go_to_cart(self) -> None:
        """Click cart link in navbar."""
        self.nav_cart.click()
        self.page.wait_for_selector("[data-test='proceed-1'], app-cart", timeout=10000)
