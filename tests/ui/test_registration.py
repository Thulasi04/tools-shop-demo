"""UI tests for user registration and form validations."""

import pytest
from pages.registration_page import RegistrationPage
from utils.helpers import generate_random_user


@pytest.mark.ui
@pytest.mark.smoke
def test_user_registration_with_valid_data(registration_page: RegistrationPage):
    """Verify that a new user can successfully register and is redirected to login."""
    new_user = generate_random_user()
    registration_page.load()
    registration_page.register_user(new_user)

    registration_page.wait_for_url_contains("auth/login", timeout=10000)
    assert "auth/login" in registration_page.get_url(), (
        f"Expected redirect to login page, current URL: {registration_page.get_url()}"
    )


@pytest.mark.ui
def test_registration_empty_form_validation(registration_page: RegistrationPage):
    """Verify that submitting an empty registration form displays validation errors."""
    registration_page.load()
    registration_page.submit()

    errors = registration_page.get_validation_errors()
    assert len(errors) > 0, "Validation errors should be displayed for empty form"
    combined_errors = " ".join(errors).lower()
    assert "required" in combined_errors, f"Expected 'required' in errors: {errors}"


@pytest.mark.ui
def test_registration_invalid_password_validation(registration_page: RegistrationPage):
    """Verify that entering an insufficient password triggers validation error."""
    invalid_user = generate_random_user()
    invalid_user["password"] = "123"  # Less than required 6/8 chars

    registration_page.load()
    registration_page.fill_registration_form(invalid_user)
    registration_page.submit()

    errors = registration_page.get_validation_errors()
    combined_errors = " ".join(errors).lower()
    assert "password" in combined_errors, f"Expected password error message, got: {errors}"
