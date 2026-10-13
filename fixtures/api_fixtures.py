"""API fixtures for clients, authentication, and test entities."""

import pytest
from typing import Dict, Any, Generator
from api.base_api import BaseAPI
from api.product_api import ProductAPI
from api.user_api import UserAPI
from api.auth_api import AuthAPI
from api.order_api import OrderAPI
from utils.helpers import generate_random_user


@pytest.fixture(scope="session")
def api_client() -> BaseAPI:
    """Base API client instance."""
    return BaseAPI()


@pytest.fixture(scope="session")
def product_api() -> ProductAPI:
    """ProductAPI client instance."""
    return ProductAPI()


@pytest.fixture(scope="session")
def user_api() -> UserAPI:
    """UserAPI client instance."""
    return UserAPI()


@pytest.fixture(scope="session")
def auth_api() -> AuthAPI:
    """AuthAPI client instance."""
    return AuthAPI()


@pytest.fixture(scope="session")
def order_api() -> OrderAPI:
    """OrderAPI client instance."""
    return OrderAPI()


@pytest.fixture(scope="function")
def registered_user(user_api: UserAPI) -> Dict[str, Any]:
    """Create a verified fresh user in the application via API."""
    user_payload = generate_random_user()
    resp = user_api.register(user_payload)
    assert resp.status_code == 201, f"User registration fixture failed: {resp.text}"
    created_data = resp.json()
    user_payload["id"] = created_data.get("id")
    return user_payload


@pytest.fixture(scope="function")
def auth_token(auth_api: AuthAPI, registered_user: Dict[str, Any]) -> str:
    """Obtain Bearer token for the registered user."""
    resp = auth_api.login(registered_user["email"], registered_user["password"])
    assert resp.status_code == 200, f"Auth login fixture failed: {resp.text}"
    return resp.json()["access_token"]
