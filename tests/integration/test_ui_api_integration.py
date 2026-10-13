"""Integration tests connecting API data setup with UI verification workflows."""

import pytest
from api.user_api import UserAPI
from api.product_api import ProductAPI
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.checkout_page import CheckoutPage
from utils.helpers import generate_random_user


@pytest.mark.integration
@pytest.mark.smoke
def test_user_created_via_api_can_login_in_ui(
    user_api: UserAPI,
    login_page: LoginPage,
    home_page: HomePage,
):
    """Integration Test 1: Seed a new user through the backend REST API,

    then launch the Playwright browser to log in and verify account status in UI.
    """
    # 1. API: Register user
    user_data = generate_random_user()
    resp = user_api.register(user_data)
    assert resp.status_code == 201, f"API user setup failed: {resp.text}"

    # 2. UI: Navigate to Login and sign in
    login_page.load()
    login_page.login(user_data["email"], user_data["password"])

    # 3. UI: Validate user session reflected in navigation menu
    home_page.page.wait_for_selector("[data-test='nav-menu']", timeout=10000)
    assert home_page.is_user_logged_in(), "User menu should appear after login"
    assert user_data["first_name"] in home_page.get_logged_in_user_name()


@pytest.mark.integration
def test_ui_product_details_match_api_catalog_data(
    product_api: ProductAPI,
    product_page: ProductPage,
):
    """Integration Test 2: Query product data from backend API,

    load the product in Playwright UI, and verify displayed information matches API.
    """
    # 1. API: Fetch products list
    list_resp = product_api.get_products()
    assert list_resp.status_code == 200
    api_product = list_resp.json()["data"][0]

    api_id = api_product["id"]
    api_name = api_product["name"]
    api_price = float(api_product["price"])

    # 2. UI: Navigate to product detail page
    product_page.load_product(api_id)

    # 3. UI: Assert UI display accurately matches API response
    ui_name = product_page.get_product_name()
    ui_price = product_page.get_unit_price()

    assert api_name in ui_name, f"UI name '{ui_name}' should match API name '{api_name}'"
    assert abs(ui_price - api_price) < 0.01, f"UI price {ui_price} should match API price {api_price}"


@pytest.mark.integration
def test_api_registered_user_completes_ui_checkout(
    user_api: UserAPI,
    product_api: ProductAPI,
    login_page: LoginPage,
    product_page: ProductPage,
    checkout_page: CheckoutPage,
    app_test_data: dict,
):
    """Integration Test 3: Create customer via API, log into UI, add item, and complete checkout."""
    # 1. API: Register customer
    user_data = generate_random_user()
    reg_resp = user_api.register(user_data)
    assert reg_resp.status_code == 201

    # 2. API: Grab active purchasable product ID (e.g. 'Pliers')
    prod_resp = product_api.get_products()
    products_list = prod_resp.json()["data"]
    purchasable_product_id = next(
        (p["id"] for p in products_list if p.get("name") == "Pliers"),
        products_list[1]["id"],
    )

    # 3. UI: Login
    login_page.load()
    login_page.login(user_data["email"], user_data["password"])
    login_page.page.wait_for_selector("[data-test='nav-menu']", timeout=10000)

    # 4. UI: Add product & navigate to cart
    product_page.load_product(purchasable_product_id)
    product_page.add_to_cart()
    product_page.go_to_cart()

    # 5. UI: Complete wizard
    checkout_page.complete_step_1_cart()
    checkout_page.complete_step_2_as_logged_in_user()
    checkout_page.fill_step_3_address(app_test_data["checkout_data"]["address"])
    checkout_page.complete_step_4_payment(app_test_data["checkout_data"]["payment_method"])

    # 6. Assert success
    assert checkout_page.is_order_successful(), "Expected payment success confirmation"
