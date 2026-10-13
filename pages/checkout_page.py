"""Checkout Page Object implementing the multi-step checkout wizard."""

from typing import Dict, Any
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage
from locators.checkout_locators import CheckoutLocators
from utils.logger import logger


class CheckoutPage(BasePage):
    """Page Object for the checkout multi-step wizard."""

    def __init__(self, page: Page):
        super().__init__(page)
        # Step 1: Cart
        self.proceed_step_1: Locator = page.locator(CheckoutLocators.PROCEED_STEP_1)

        # Step 2: Sign-in / Guest
        self.proceed_step_2: Locator = page.locator(CheckoutLocators.PROCEED_STEP_2)
        self.guest_tab: Locator = page.locator(CheckoutLocators.GUEST_TAB)
        self.guest_first_name: Locator = page.locator(CheckoutLocators.GUEST_FIRST_NAME)
        self.guest_last_name: Locator = page.locator(CheckoutLocators.GUEST_LAST_NAME)
        self.guest_email: Locator = page.locator(CheckoutLocators.GUEST_EMAIL)
        self.guest_submit: Locator = page.locator(CheckoutLocators.GUEST_SUBMIT)

        # Step 3: Address
        self.street_input: Locator = page.locator(CheckoutLocators.STREET_INPUT)
        self.city_input: Locator = page.locator(CheckoutLocators.CITY_INPUT)
        self.state_input: Locator = page.locator(CheckoutLocators.STATE_INPUT)
        self.country_select: Locator = page.locator(CheckoutLocators.COUNTRY_SELECT)
        self.postal_code_input: Locator = page.locator(CheckoutLocators.POSTAL_CODE_INPUT)
        self.proceed_step_3: Locator = page.locator(CheckoutLocators.PROCEED_STEP_3)

        # Step 4: Payment
        self.payment_method_select: Locator = page.locator(CheckoutLocators.PAYMENT_METHOD_SELECT)
        self.account_name_input: Locator = page.locator(CheckoutLocators.ACCOUNT_NAME_INPUT)
        self.account_number_input: Locator = page.locator(CheckoutLocators.ACCOUNT_NUMBER_INPUT)
        self.finish_button: Locator = page.locator(CheckoutLocators.FINISH_BUTTON)

        # Order Confirmation
        self.success_message: Locator = page.locator(CheckoutLocators.SUCCESS_MESSAGE)

    def load(self) -> "CheckoutPage":
        """Load checkout page."""
        self.navigate("/checkout")
        self.page.wait_for_timeout(1000)
        return self

    def complete_step_1_cart(self) -> None:
        """Advance past Step 1."""
        logger.info("Proceeding from Step 1 (Cart)")
        self.proceed_step_1.click()
        self.page.wait_for_timeout(1000)

    def complete_step_2_as_logged_in_user(self) -> None:
        """Advance past Step 2 when user is already logged in."""
        logger.info("Proceeding from Step 2 (Logged-in user)")
        self.proceed_step_2.click()
        self.page.wait_for_timeout(1000)

    def fill_step_3_address(self, address: Dict[str, Any]) -> None:
        """Fill shipping address in Step 3 and proceed."""
        logger.info("Filling shipping address in Step 3")
        self.street_input.fill(address.get("street", "100 Automation Blvd"))
        self.city_input.fill(address.get("city", "Sunnyvale"))
        self.state_input.fill(address.get("state", "California"))
        self.country_select.select_option(value=address.get("country_value", "US"))
        self.postal_code_input.fill(address.get("postal_code", "94086"))
        self.proceed_step_3.click()
        self.page.wait_for_timeout(1000)

    def complete_step_4_payment(self, method: str = "cash-on-delivery") -> None:
        """Select payment method and confirm order."""
        logger.info(f"Selecting payment method: {method}")
        self.payment_method_select.select_option(value=method)
        self.page.wait_for_timeout(500)
        logger.info("Clicking finish button to submit order")
        self.finish_button.click()
        self.page.wait_for_timeout(3000)

    def is_order_successful(self) -> bool:
        """Verify if checkout success / payment confirmation text is present."""
        messages = [t.lower() for t in self.success_message.all_inner_texts()]
        return any("payment was successful" in m or "payment" in m for m in messages)
