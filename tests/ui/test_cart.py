"""UI tests for shopping cart operations: adding, updating quantity, removal, and totals."""

import pytest
from pages.product_page import ProductPage
from pages.cart_page import CartPage


@pytest.mark.ui
@pytest.mark.smoke
def test_add_single_product_to_cart(product_page: ProductPage, products_data: dict):
    """Verify adding a product to cart displays success notification."""
    product_id = products_data["known_product"]["id"]
    product_page.load_product(product_id)
    product_page.add_to_cart()

    toast_text = product_page.get_toast_message()
    assert "Product added to shopping cart" in toast_text, (
        f"Expected add-to-cart confirmation, got: '{toast_text}'"
    )


@pytest.mark.ui
def test_cart_displays_correct_product_title_and_price(
    product_page: ProductPage,
    cart_page: CartPage,
    products_data: dict,
):
    """Verify product added to cart appears with expected name and price in cart table."""
    product_id = products_data["known_product"]["id"]
    expected_name = products_data["known_product"]["name"]

    product_page.load_product(product_id)
    product_page.add_to_cart()
    product_page.go_to_cart()

    cart_items = cart_page.get_product_titles()
    assert any(expected_name.lower() in item.lower() for item in cart_items), (
        f"Expected '{expected_name}' in cart items {cart_items}"
    )
    assert cart_page.get_cart_total() > 0, "Cart total should be greater than zero"


@pytest.mark.ui
def test_update_cart_quantity_recalculates_total(
    product_page: ProductPage,
    cart_page: CartPage,
    products_data: dict,
):
    """Verify that updating item quantity in cart recalculates line price and total."""
    product_id = products_data["known_product"]["id"]
    product_page.load_product(product_id)
    product_page.add_to_cart()
    product_page.go_to_cart()

    initial_total = cart_page.get_cart_total()

    # Update quantity from 1 to 2
    cart_page.update_quantity(index=0, new_quantity=2)
    new_total = cart_page.get_cart_total()

    assert new_total > initial_total, (
        f"New cart total ({new_total}) should be greater than initial total ({initial_total})"
    )


@pytest.mark.ui
def test_remove_product_from_cart(
    product_page: ProductPage,
    cart_page: CartPage,
    products_data: dict,
):
    """Verify that deleting an item from the cart removes its row."""
    product_id = products_data["known_product"]["id"]
    product_page.load_product(product_id)
    product_page.add_to_cart()
    product_page.go_to_cart()

    initial_count = cart_page.get_items_count()
    assert initial_count >= 1, "Cart should have at least 1 item before deletion"

    cart_page.remove_item(index=0)
    after_count = cart_page.get_items_count()

    assert after_count == initial_count - 1, (
        f"Item count after removal should be {initial_count - 1}, got {after_count}"
    )


@pytest.mark.ui
def test_empty_cart_view(cart_page: CartPage):
    """Verify navigating to checkout with empty cart displays 0 rows."""
    cart_page.load()
    assert cart_page.get_items_count() == 0, "Directly loaded cart should have 0 items"
