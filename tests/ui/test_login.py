"""UI tests for user authentication, login validation, and logout."""

import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.smoke
def test_login_with_valid_credentials(
    login_page: LoginPage,
    registered_user: dict,
    home_page: HomePage,
):
    """Verify that a registered user can log in and view their name in the user menu."""
    login_page.load()
    login_page.login(registered_user["email"], registered_user["password"])

    # Verify user menu becomes visible
    home_page.page.wait_for_selector("[data-test='nav-menu']", timeout=10000)
    assert home_page.is_user_logged_in(), "User menu should be visible after login"

    user_name = home_page.get_logged_in_user_name()
    expected_first = registered_user["first_name"]
    assert expected_first in user_name, f"Expected '{expected_first}' in nav title '{user_name}'"


@pytest.mark.ui
@pytest.mark.parametrize(
    "email,password",
    [
        ("nonexistent_user@example.com", "WrongPassword123!"),
        ("random_user_99@test.com", "InvalidPass888!"),
    ],
)
def test_login_with_invalid_credentials_shows_error(
    login_page: LoginPage,
    email: str,
    password: str,
):
    """Verify that incorrect credentials show the 'Invalid email or password' alert."""
    login_page.load()
    login_page.login(email, password)

    error = login_page.get_error_message()
    assert "Invalid email or password" in error, f"Expected error alert, got '{error}'"


@pytest.mark.ui
def test_login_empty_fields_validation(login_page: LoginPage):
    """Verify that submitting an empty login form does not navigate away."""
    login_page.load()
    login_page.login_button.click()

    # Form should remain on login page and not submit
    assert "login" in login_page.get_url(), "Should remain on login page when submitting empty form"


@pytest.mark.ui
def test_user_logout_flow(
    login_page: LoginPage,
    registered_user: dict,
    home_page: HomePage,
):
    """Verify that logging out revokes session and displays Sign In link."""
    login_page.load()
    login_page.login(registered_user["email"], registered_user["password"])

    home_page.page.wait_for_selector("[data-test='nav-menu']", timeout=10000)
    home_page.logout()

    assert home_page.is_visible(home_page.nav_sign_in), "Sign In button should be visible after logout"
