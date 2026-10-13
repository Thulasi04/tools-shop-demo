"""User API client."""

from typing import Dict, Any, Optional
import requests
from api.base_api import BaseAPI


class UserAPI(BaseAPI):
    """Client for user management, registration, and profile endpoints."""

    def register(self, user_data: Dict[str, Any]) -> requests.Response:
        """Register a new customer account."""
        return self.post("/users/register", json=user_data)

    def get_current_user(self, token: Optional[str] = None) -> requests.Response:
        """Fetch currently authenticated profile (/users/me)."""
        headers = {"Authorization": f"Bearer {token}"} if token else None
        return self.get("/users/me", headers=headers)

    def get_user_by_id(self, user_id: str, token: Optional[str] = None) -> requests.Response:
        """Retrieve user details by user ID (admin restricted)."""
        headers = {"Authorization": f"Bearer {token}"} if token else None
        return self.get(f"/users/{user_id}", headers=headers)
