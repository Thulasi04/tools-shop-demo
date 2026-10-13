"""Cart and Order/Invoice API client."""

from typing import Dict, Any, Optional
import requests
from api.base_api import BaseAPI


class OrderAPI(BaseAPI):
    """Client for cart operations and invoices/orders."""

    def create_cart(self) -> requests.Response:
        """Initialize a new shopping cart."""
        return self.post("/carts")

    def get_cart(self, cart_id: str) -> requests.Response:
        """Retrieve cart items and details by cart ID."""
        return self.get(f"/carts/{cart_id}")

    def add_item_to_cart(self, cart_id: str, product_id: str, quantity: int = 1) -> requests.Response:
        """Add a product item to the specified cart."""
        payload = {"product_id": product_id, "quantity": quantity}
        return self.post(f"/carts/{cart_id}", json=payload)

    def update_item_quantity(self, cart_id: str, product_id: str, quantity: int) -> requests.Response:
        """Update quantity of a product in the cart."""
        payload = {"product_id": product_id, "quantity": quantity}
        return self.put(f"/carts/{cart_id}/product/quantity", json=payload)

    def remove_item_from_cart(self, cart_id: str, product_id: str) -> requests.Response:
        """Remove a product from the cart."""
        return self.delete(f"/carts/{cart_id}/product/{product_id}")

    def delete_cart(self, cart_id: str) -> requests.Response:
        """Delete an entire cart."""
        return self.delete(f"/carts/{cart_id}")

    def get_invoices(self, token: Optional[str] = None) -> requests.Response:
        """Fetch list of user invoices."""
        headers = {"Authorization": f"Bearer {token}"} if token else None
        return self.get("/invoices", headers=headers)

    def create_guest_invoice(self, invoice_data: Dict[str, Any]) -> requests.Response:
        """Create order/invoice for a guest checkout."""
        return self.post("/invoices/guest", json=invoice_data)
