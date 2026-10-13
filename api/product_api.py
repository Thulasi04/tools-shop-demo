"""Product and Catalog API client."""

from typing import Optional, Dict, Any
import requests
from api.base_api import BaseAPI


class ProductAPI(BaseAPI):
    """Client for product catalog, categories, and brands endpoints."""

    def get_products(
        self,
        page: Optional[int] = None,
        sort: Optional[str] = None,
        by_category_slug: Optional[str] = None,
        by_brand_slug: Optional[str] = None,
    ) -> requests.Response:
        """Fetch list of products with optional query filtering."""
        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if sort:
            params["sort"] = sort
        if by_category_slug:
            params["by_category_slug"] = by_category_slug
        if by_brand_slug:
            params["by_brand_slug"] = by_brand_slug

        return self.get("/products", params=params if params else None)

    def search_products(self, query: str) -> requests.Response:
        """Search products by query term."""
        return self.get("/products/search", params={"q": query})

    def get_product_by_id(self, product_id: str) -> requests.Response:
        """Retrieve details of a single product."""
        return self.get(f"/products/{product_id}")

    def get_related_products(self, product_id: str) -> requests.Response:
        """Retrieve related products for given product ID."""
        return self.get(f"/products/{product_id}/related")

    def get_categories(self) -> requests.Response:
        """Fetch list of product categories."""
        return self.get("/categories")

    def get_brands(self) -> requests.Response:
        """Fetch list of product brands."""
        return self.get("/brands")
