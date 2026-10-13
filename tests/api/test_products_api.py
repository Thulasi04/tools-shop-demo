"""API tests for product catalog, categories, brands, and product search."""

import pytest
from api.product_api import ProductAPI


@pytest.mark.api
@pytest.mark.smoke
def test_get_products_list_success(product_api: ProductAPI):
    """Verify that GET /products returns HTTP 200 and a populated list of products."""
    resp = product_api.get_products()
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"

    data = resp.json()
    assert "data" in data, "Response body should contain 'data' key"
    assert len(data["data"]) > 0, "Products list should not be empty"

    # Validate schema fields of first product item
    item = data["data"][0]
    required_fields = ["id", "name", "price", "description"]
    for field in required_fields:
        assert field in item, f"Product item missing required field '{field}'"


@pytest.mark.api
def test_get_products_pagination(product_api: ProductAPI):
    """Verify pagination parameters return page metadata."""
    resp = product_api.get_products(page=1)
    assert resp.status_code == 200

    data = resp.json()
    assert data.get("current_page") == 1, "Current page should equal 1"
    assert "total" in data, "Total count should be present"


@pytest.mark.api
@pytest.mark.smoke
def test_get_product_by_valid_id(product_api: ProductAPI, products_data: dict):
    """Verify fetching a specific product by its ID returns matching product details."""
    prod_id = products_data["known_product"]["id"]
    resp = product_api.get_product_by_id(prod_id)

    # In case product ID was reset, fetch dynamically from list
    if resp.status_code != 200:
        list_resp = product_api.get_products()
        prod_id = list_resp.json()["data"][0]["id"]
        resp = product_api.get_product_by_id(prod_id)

    assert resp.status_code == 200
    item = resp.json()
    assert item["id"] == prod_id
    assert "name" in item
    assert float(item["price"]) > 0


@pytest.mark.api
def test_get_product_by_nonexistent_id_returns_404(product_api: ProductAPI):
    """Verify fetching a non-existent product returns HTTP 404."""
    resp = product_api.get_product_by_id("00000000000000000000000000")
    assert resp.status_code == 404 or resp.status_code == 422, (
        f"Expected 404/422 for non-existent item, got {resp.status_code}"
    )


@pytest.mark.api
def test_search_products_api_returns_matching_results(product_api: ProductAPI, products_data: dict):
    """Verify GET /products/search?q={query} returns products matching search term."""
    query = products_data["search_terms"]["valid_term"]  # "Pliers"
    resp = product_api.search_products(query)
    assert resp.status_code == 200

    results = resp.json().get("data", [])
    assert len(results) > 0, f"Expected search results for '{query}'"
    assert any(query.lower() in p["name"].lower() for p in results)


@pytest.mark.api
def test_search_products_api_empty_for_unknown_term(product_api: ProductAPI, products_data: dict):
    """Verify searching for an unknown string returns an empty dataset."""
    query = products_data["search_terms"]["nonexistent_term"]
    resp = product_api.search_products(query)
    assert resp.status_code == 200

    results = resp.json().get("data", [])
    assert len(results) == 0, f"Expected 0 results for '{query}', got {len(results)}"


@pytest.mark.api
def test_get_categories_list(product_api: ProductAPI):
    """Verify GET /categories returns status 200 and category objects."""
    resp = product_api.get_categories()
    assert resp.status_code == 200

    categories = resp.json()
    assert isinstance(categories, list), "Categories should be a list"
    assert len(categories) > 0, "Categories list should not be empty"
    first_cat = categories[0]
    assert "id" in first_cat and "name" in first_cat, "Category must have 'id' and 'name'"


@pytest.mark.api
def test_get_brands_list(product_api: ProductAPI):
    """Verify GET /brands returns status 200 and brand objects."""
    resp = product_api.get_brands()
    assert resp.status_code == 200

    brands = resp.json()
    assert isinstance(brands, list), "Brands should be a list"
    assert len(brands) > 0, "Brands list should not be empty"
    first_brand = brands[0]
    assert "id" in first_brand and "name" in first_brand, "Brand must have 'id' and 'name'"


@pytest.mark.api
def test_products_api_response_time_under_threshold(product_api: ProductAPI):
    """Verify critical API endpoint responds within reasonable threshold (< 3 seconds)."""
    resp = product_api.get_products()
    assert resp.status_code == 200
    assert resp.elapsed.total_seconds() < 3.0, (
        f"API response time was {resp.elapsed.total_seconds():.2f}s, expected < 3.0s"
    )
