"""UI tests for product search and search reset functionality."""

import pytest
from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.smoke
def test_search_existing_product_returns_results(home_page: HomePage, products_data: dict):
    """Verify searching for an existing product displays matching product cards."""
    home_page.load()
    search_term = products_data["search_terms"]["valid_term"]  # "Pliers"
    home_page.search_product(search_term)

    product_names = home_page.get_product_names()
    assert len(product_names) > 0, f"Expected search results for '{search_term}'"
    assert any(search_term.lower() in name.lower() for name in product_names), (
        f"Expected at least one product matching '{search_term}', got: {product_names}"
    )


@pytest.mark.ui
def test_search_nonexistent_product_shows_empty_message(home_page: HomePage, products_data: dict):
    """Verify searching for a non-existent item displays the empty results message."""
    home_page.load()
    term = products_data["search_terms"]["nonexistent_term"]
    home_page.search_product(term)

    assert home_page.is_visible(home_page.no_results_message), "No results message should be visible"
    assert "There are no products found" in home_page.get_text(home_page.no_results_message)


@pytest.mark.ui
def test_search_reset_restores_catalog(home_page: HomePage, products_data: dict):
    """Verify that clicking the search reset button restores all products."""
    home_page.load()
    initial_count = home_page.get_product_count()

    # Search to filter list
    home_page.search_product(products_data["search_terms"]["valid_term"])
    filtered_count = home_page.get_product_count()

    # Reset search
    home_page.reset_search()
    restored_count = home_page.get_product_count()

    assert restored_count >= initial_count or restored_count > filtered_count, (
        "Catalog should be restored after clicking search reset"
    )


@pytest.mark.ui
def test_search_with_special_characters_handled_safely(home_page: HomePage, products_data: dict):
    """Verify searching with special characters does not cause application crash."""
    home_page.load()
    special_term = products_data["search_terms"]["special_characters"]
    home_page.search_product(special_term)

    # Application should remain functional and show no results or empty state
    assert home_page.is_visible(home_page.search_input), "Search input should remain accessible"
