"""API tests for carts, cart items, and invoices."""

import pytest
from api.order_api import OrderAPI
from api.product_api import ProductAPI


@pytest.mark.api
@pytest.mark.smoke
def test_create_cart_returns_cart_id(order_api: OrderAPI):
    """Verify POST /carts initializes a new cart and returns its UUID."""
    resp = order_api.create_cart()
    assert resp.status_code in (200, 201), f"Cart creation failed: {resp.text}"

    data = resp.json()
    assert "id" in data, "Cart response must contain 'id'"


@pytest.mark.api
def test_get_cart_by_id(order_api: OrderAPI):
    """Verify GET /carts/{cartId} returns cart details."""
    create_resp = order_api.create_cart()
    cart_id = create_resp.json()["id"]

    resp = order_api.get_cart(cart_id)
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"
    data = resp.json()
    assert data["id"] == cart_id


@pytest.mark.api
def test_add_item_to_cart_api(
    order_api: OrderAPI,
    product_api: ProductAPI,
    products_data: dict,
):
    """Verify adding an item to the cart via POST /carts/{cartId} succeeds."""
    create_resp = order_api.create_cart()
    cart_id = create_resp.json()["id"]

    prod_id = products_data["known_product"]["id"]
    # Check if known product exists or grab first from list
    p_check = product_api.get_product_by_id(prod_id)
    if p_check.status_code != 200:
        prod_id = product_api.get_products().json()["data"][0]["id"]

    resp = order_api.add_item_to_cart(cart_id, prod_id, quantity=1)
    assert resp.status_code in (200, 201), f"Add to cart failed: {resp.text}"


@pytest.mark.api
def test_delete_cart_api(order_api: OrderAPI):
    """Verify deleting a cart via DELETE /carts/{cartId} returns 200 or 204."""
    create_resp = order_api.create_cart()
    cart_id = create_resp.json()["id"]

    resp = order_api.delete_cart(cart_id)
    assert resp.status_code in (200, 204), f"Cart deletion failed: {resp.text}"


@pytest.mark.api
def test_get_invoices_unauthorized_without_token(order_api: OrderAPI):
    """Verify fetching invoices without Authorization header returns 401."""
    resp = order_api.get_invoices(token=None)
    assert resp.status_code == 401, f"Expected 401 Unauthorized, got {resp.status_code}"
