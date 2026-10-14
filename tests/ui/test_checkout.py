"""UI tests for multi-step checkout workflow and order completion."""

import pytest
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.checkout_page import CheckoutPage


@pytest.mark.ui
@pytest.mark.smoke
def test_end_to_end_checkout_with_logged_in_user(
    login_page: LoginPage,
    registered_user: dict,
    product_page: ProductPage,
    checkout_page: CheckoutPage,
    products_data: dict,
    app_test_data: dict,
):
    """Verify complete checkout journey from login to cart to payment confirmation."""
    # 1. Login user
    login_page.load()
    login_page.login(registered_user["email"], registered_user["password"])
    login_page.page.wait_for_selector("[data-test='nav-menu']", timeout=20000)

    # 2. Add product to cart
    product_id = products_data["known_product"]["id"]
    product_page.load_product(product_id)
    product_page.add_to_cart()

    # 3. Open cart and proceed through wizard
    product_page.go_to_cart()
    checkout_page.complete_step_1_cart()

    # 4. Step 2: Confirm logged in account
    checkout_page.complete_step_2_as_logged_in_user()

    # 5. Step 3: Enter shipping address
    address_data = app_test_data["checkout_data"]["address"]
    checkout_page.fill_step_3_address(address_data)

    # 6. Step 4: Choose payment method and confirm
    payment_method = app_test_data["checkout_data"]["payment_method"]
    checkout_page.complete_step_4_payment(payment_method)

    # 7. Assert order confirmation
    assert checkout_page.is_order_successful(), "Expected payment success confirmation"


@pytest.mark.ui
def test_checkout_cannot_proceed_with_empty_cart(checkout_page: CheckoutPage):
    """Verify that user cannot proceed when cart contains zero products."""
    checkout_page.load()
    # When cart is empty, proceed button should either be hidden or disabled
    assert not checkout_page.is_visible(checkout_page.proceed_step_1, timeout=2000), (
        "Proceed button should not be accessible on empty cart"
    )
