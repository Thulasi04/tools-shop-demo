"""Locators for Multi-step Checkout Wizard."""


class CheckoutLocators:
    """Selectors for cart checkout wizard steps, shipping form, payment, and confirmation."""

    # Step 1: Cart proceed
    PROCEED_STEP_1 = "[data-test='proceed-1']"

    # Step 2: Sign-in / Guest
    PROCEED_STEP_2 = "[data-test='proceed-2']"
    GUEST_TAB = "a[href='#guest-tab']"
    GUEST_FIRST_NAME = "[data-test='guest-first-name']"
    GUEST_LAST_NAME = "[data-test='guest-last-name']"
    GUEST_EMAIL = "[data-test='guest-email']"
    GUEST_SUBMIT = "[data-test='guest-submit']"

    # Step 3: Address
    STREET_INPUT = "[data-test='street']"
    CITY_INPUT = "[data-test='city']"
    STATE_INPUT = "[data-test='state']"
    COUNTRY_SELECT = "[data-test='country']"
    POSTAL_CODE_INPUT = "[data-test='postal_code']"
    PROCEED_STEP_3 = "[data-test='proceed-3']"

    # Step 4: Payment
    PAYMENT_METHOD_SELECT = "[data-test='payment-method']"
    ACCOUNT_NAME_INPUT = "[data-test='account-name']"
    ACCOUNT_NUMBER_INPUT = "[data-test='account-number']"
    FINISH_BUTTON = "[data-test='finish']"

    # Order Confirmation
    SUCCESS_MESSAGE = ".alert, #order-confirmation, h2, h3"
