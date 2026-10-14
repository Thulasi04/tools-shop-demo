"""Base API Client handling HTTP methods, sessions, and logging."""

import requests
from typing import Any, Dict, Optional
from utils.config import config
from utils.logger import logger


class BaseAPI:
    """Base API client wrapping requests.Session with logging and standardized execution."""

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = (base_url or config.API_BASE_URL).rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/128.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json, text/plain, */*",
        })
        self.timeout = config.API_TIMEOUT

    def set_auth_token(self, token: str) -> None:
        """Set Bearer authentication token for future requests."""
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def clear_auth_token(self) -> None:
        """Remove Authorization header."""
        self.session.headers.pop("Authorization", None)

    def _url(self, endpoint: str) -> str:
        """Format full endpoint URL."""
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"
        return f"{self.base_url}{endpoint}"

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """Execute HTTP GET request."""
        url = self._url(endpoint)
        logger.info(f"API GET -> {url} with params={params}")
        resp = self.session.get(url, params=params, timeout=self.timeout, **kwargs)
        logger.info(f"API GET <- Status {resp.status_code} in {resp.elapsed.total_seconds():.3f}s")
        return resp

    def post(self, endpoint: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """Execute HTTP POST request."""
        url = self._url(endpoint)
        logger.info(f"API POST -> {url}")
        resp = self.session.post(url, json=json, timeout=self.timeout, **kwargs)
        logger.info(f"API POST <- Status {resp.status_code} in {resp.elapsed.total_seconds():.3f}s")
        return resp

    def put(self, endpoint: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """Execute HTTP PUT request."""
        url = self._url(endpoint)
        logger.info(f"API PUT -> {url}")
        resp = self.session.put(url, json=json, timeout=self.timeout, **kwargs)
        logger.info(f"API PUT <- Status {resp.status_code} in {resp.elapsed.total_seconds():.3f}s")
        return resp

    def patch(self, endpoint: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """Execute HTTP PATCH request."""
        url = self._url(endpoint)
        logger.info(f"API PATCH -> {url}")
        resp = self.session.patch(url, json=json, timeout=self.timeout, **kwargs)
        logger.info(f"API PATCH <- Status {resp.status_code} in {resp.elapsed.total_seconds():.3f}s")
        return resp

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """Execute HTTP DELETE request."""
        url = self._url(endpoint)
        logger.info(f"API DELETE -> {url}")
        resp = self.session.delete(url, timeout=self.timeout, **kwargs)
        logger.info(f"API DELETE <- Status {resp.status_code} in {resp.elapsed.total_seconds():.3f}s")
        return resp
