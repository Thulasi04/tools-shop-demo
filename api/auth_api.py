"""Authentication API client."""

from typing import Optional
import requests
from api.base_api import BaseAPI


class AuthAPI(BaseAPI):
    """Client for user authentication and session endpoints."""

    def login(self, email: str, password: str) -> requests.Response:
        """Authenticate user credentials and obtain bearer JWT token."""
        payload = {"email": email, "password": password}
        return self.post("/users/login", json=payload)

    def logout(self, token: Optional[str] = None) -> requests.Response:
        """Invalidate session / logout user."""
        headers = {"Authorization": f"Bearer {token}"} if token else None
        return self.get("/users/logout", headers=headers)

    def get_token(self, email: str, password: str) -> Optional[str]:
        """Convenience method to retrieve JWT token directly on successful login."""
        resp = self.login(email, password)
        if resp.status_code == 200:
            return resp.json().get("access_token")
        return None
