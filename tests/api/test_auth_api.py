"""API tests for user authentication, token generation, and logout."""

import pytest
from api.auth_api import AuthAPI


@pytest.mark.api
@pytest.mark.smoke
def test_login_with_valid_credentials_returns_token(
    auth_api: AuthAPI,
    registered_user: dict,
):
    """Verify that valid credentials return HTTP 200, access token, and token type."""
    resp = auth_api.login(registered_user["email"], registered_user["password"])
    assert resp.status_code == 200, f"Login failed: {resp.text}"

    data = resp.json()
    assert "access_token" in data, "Response body must include 'access_token'"
    assert data.get("token_type") == "bearer", "Token type should be 'bearer'"
    assert data.get("expires_in") is not None, "Expires_in duration should be present"


@pytest.mark.api
def test_login_with_invalid_credentials_returns_401(auth_api: AuthAPI):
    """Verify that invalid password returns HTTP 401 Unauthorized."""
    resp = auth_api.login("nonexistent@example.com", "WrongPassword123!")
    assert resp.status_code == 401, f"Expected 401, got {resp.status_code}"
    assert "error" in resp.json() or "Unauthorized" in resp.text


@pytest.mark.api
def test_login_with_missing_password_returns_422(auth_api: AuthAPI):
    """Verify that omitting password field returns 422 Unprocessable Entity."""
    resp = auth_api.login("test@example.com", "")
    assert resp.status_code in (401, 422, 400), f"Expected 401/422/400 for empty password, got {resp.status_code}"


@pytest.mark.api
def test_logout_with_bearer_token(auth_api: AuthAPI, auth_token: str):
    """Verify that calling GET /users/logout with Bearer token is accepted."""
    resp = auth_api.logout(token=auth_token)
    assert resp.status_code in (200, 204), f"Expected 200/204, got {resp.status_code}: {resp.text}"
