"""UI tests for Home page layout, title, and primary navigation."""

import pytest
from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.smoke
def test_home_page_loads_with_correct_title(home_page: HomePage, app_test_data: dict):
    """Verify that the home page loads successfully with the expected page title."""
    home_page.load()
    expected_title = app_test_data["app_info"]["title"]
    actual_title = home_page.get_title()
    assert expected_title in actual_title, f"Expected '{expected_title}' in '{actual_title}'"


@pytest.mark.ui
def test_home_page_navigation_elements_are_visible(home_page: HomePage):
    """Verify all primary navigation items are present in the header."""
    home_page.load()
    assert home_page.is_visible(home_page.nav_home), "Home nav link should be visible"
    assert home_page.is_visible(home_page.nav_categories), "Categories dropdown should be visible"
    assert home_page.is_visible(home_page.nav_contact), "Contact nav link should be visible"
    assert home_page.is_visible(home_page.nav_sign_in), "Sign in link should be visible"


@pytest.mark.ui
def test_navigation_to_hand_tools_category(home_page: HomePage):
    """Verify navigating to Hand Tools displays relevant category page."""
    home_page.load()
    home_page.click(home_page.nav_categories)
    home_page.click(home_page.nav_hand_tools)
    home_page.wait_for_url_contains("hand-tools")
    assert "hand-tools" in home_page.get_url(), "URL should contain 'hand-tools'"
    home_page.page.wait_for_selector("a.card, [data-test='product-name']", timeout=10000)
    assert home_page.get_product_count() > 0, "Products should be listed in Hand Tools category"


@pytest.mark.ui
def test_navigation_to_contact_page(home_page: HomePage):
    """Verify navigating to Contact link opens the contact form page."""
    home_page.load()
    home_page.click(home_page.nav_contact)
    home_page.wait_for_url_contains("contact")
    assert "contact" in home_page.get_url(), "URL should contain 'contact'"
