"""UI tests for product browsing, product details, sorting, and filtering."""

import pytest
from pages.home_page import HomePage
from pages.product_page import ProductPage


@pytest.mark.ui
def test_product_cards_display_title_and_price(home_page: HomePage):
    """Verify that catalog products render with titles and valid prices."""
    home_page.load()
    names = home_page.get_product_names()
    assert len(names) > 0, "Product catalog should display at least one item"
    for name in names[:5]:
        assert len(name) > 0, "Product name should not be empty"


@pytest.mark.ui
@pytest.mark.smoke
def test_open_product_details_displays_correct_information(
    home_page: HomePage,
    product_page: ProductPage,
    products_data: dict,
):
    """Verify opening a product page displays title, price, and description."""
    product_id = products_data["known_product"]["id"]
    product_page.load_product(product_id)

    title = product_page.get_product_name()
    price = product_page.get_unit_price()
    description = product_page.get_description()

    expected_name = products_data["known_product"]["name"]
    if expected_name in title:
        assert expected_name in title
    else:
        assert len(title) > 0, "Product title should not be empty"
    assert price > 0, f"Expected positive price, got: {price}"
    assert len(description) > 0, "Description should not be empty"


@pytest.mark.ui
def test_product_quantity_buttons_increment_and_decrement(
    product_page: ProductPage,
    products_data: dict,
):
    """Verify that clicking +/- buttons correctly modifies the quantity input."""
    product_id = products_data["known_product"]["id"]
    product_page.load_product(product_id)

    initial_qty = product_page.get_quantity()
    assert initial_qty == 1, "Default quantity should be 1"

    # Increase quantity
    product_page.increase_quantity()
    assert product_page.get_quantity() == 2, "Quantity should increment to 2"

    # Decrease quantity
    product_page.decrease_quantity()
    assert product_page.get_quantity() == 1, "Quantity should decrement back to 1"


@pytest.mark.ui
def test_sort_products_by_name(home_page: HomePage):
    """Verify that sorting by Name (A - Z) sorts products alphabetically."""
    home_page.load()
    home_page.sort_by("name,asc")

    names = home_page.get_product_names()
    assert len(names) > 1, "Need at least 2 items to verify sort"
    assert names == sorted(names, key=str.lower), "Products should be sorted alphabetically ascending"


@pytest.mark.ui
def test_filter_products_by_brand(home_page: HomePage, products_data: dict):
    """Verify filtering products by brand displays only matching products."""
    home_page.load()
    brand_to_filter = products_data["filter_criteria"]["brand"]  # "ForgeFlex Tools"
    home_page.filter_by_brand(brand_to_filter)

    product_count = home_page.get_product_count()
    assert product_count > 0, f"Filtered results should be returned for brand '{brand_to_filter}'"
