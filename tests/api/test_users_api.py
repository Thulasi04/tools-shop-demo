"""API tests for user registration, duplicate checks, and user profile."""

import pytest
from api.user_api import UserAPI
from utils.helpers import generate_random_user


@pytest.mark.api
@pytest.mark.smoke
def test_register_new_user_success(user_api: UserAPI):
    """Verify that registering a user with valid payload returns HTTP 201 and created user."""
    payload = generate_random_user()
    resp = user_api.register(payload)
    assert resp.status_code == 201, f"Expected 201 Created, got {resp.status_code}: {resp.text}"

    data = resp.json()
    assert "id" in data, "Created user should have an 'id'"
    assert data["email"] == payload["email"].lower()
    assert data["first_name"] == payload["first_name"]


@pytest.mark.api
def test_register_duplicate_email_fails(user_api: UserAPI, registered_user: dict):
    """Verify registering with already-used email address returns 422 Unprocessable Entity."""
    duplicate_payload = generate_random_user()
    duplicate_payload["email"] = registered_user["email"]

    resp = user_api.register(duplicate_payload)
    assert resp.status_code in (409, 422), f"Expected 409/422 for duplicate email, got {resp.status_code}"
    error_data = resp.json()
    assert "email" in str(error_data).lower()


@pytest.mark.api
def test_register_user_missing_required_fields_fails(user_api: UserAPI):
    """Verify submitting registration without email and password fails validation."""
    incomplete_payload = {
        "first_name": "Incomplete",
        "last_name": "User",
    }
    resp = user_api.register(incomplete_payload)
    assert resp.status_code == 422, f"Expected 422 for missing fields, got {resp.status_code}"


@pytest.mark.api
def test_get_current_user_profile_with_valid_token(
    user_api: UserAPI,
    auth_token: str,
    registered_user: dict,
):
    """Verify GET /users/me with Bearer token returns currently logged-in user details."""
    resp = user_api.get_current_user(token=auth_token)
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"

    profile = resp.json()
    assert profile["email"] == registered_user["email"].lower()
    assert profile["first_name"] == registered_user["first_name"]


@pytest.mark.api
def test_get_current_user_profile_without_token_returns_401(user_api: UserAPI):
    """Verify GET /users/me without Bearer header returns 401 Unauthorized."""
    resp = user_api.get_current_user(token=None)
    assert resp.status_code == 401, f"Expected 401 Unauthorized, got {resp.status_code}"
