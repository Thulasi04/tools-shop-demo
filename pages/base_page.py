"""Base Page Object providing reusable interactions and common navigation."""

from pathlib import Path
from playwright.sync_api import Page, Locator, expect
from utils.config import config
from utils.logger import logger


class BasePage:
    """Base class for all Page Objects in the framework."""

    def __init__(self, page: Page):
        self.page = page
        self.base_url = config.BASE_URL

    def navigate(self, path: str = "") -> None:
        """Navigate to a relative path or full URL.

        Args:
            path: Relative path (e.g. '/auth/login') or absolute URL.
        """
        target_url = path if path.startswith("http") else f"{self.base_url}{path}"
        logger.info(f"Navigating to: {target_url}")
        self.page.goto(target_url, wait_until="domcontentloaded")

    def get_title(self) -> str:
        """Get the current page title.

        Returns:
            str: Document title.
        """
        return self.page.title()

    def get_url(self) -> str:
        """Get the current page URL.

        Returns:
            str: Active URL.
        """
        return self.page.url

    def wait_for_url_contains(self, substring: str, timeout: int = 10000) -> None:
        """Wait until current URL contains the expected substring."""
        self.page.wait_for_url(lambda u: substring in u, timeout=timeout)

    def click(self, locator_or_selector: str | Locator) -> None:
        """Click on an element.

        Args:
            locator_or_selector: Selector string or Locator instance.
        """
        locator = self._get_locator(locator_or_selector)
        logger.info(f"Clicking on element: {locator_or_selector}")
        locator.click()

    def fill(self, locator_or_selector: str | Locator, text: str) -> None:
        """Fill an input field.

        Args:
            locator_or_selector: Selector string or Locator instance.
            text: Text to fill into the input.
        """
        locator = self._get_locator(locator_or_selector)
        logger.info(f"Filling element {locator_or_selector} with text")
        locator.fill(text)

    def get_text(self, locator_or_selector: str | Locator) -> str:
        """Retrieve inner text of an element.

        Args:
            locator_or_selector: Selector string or Locator instance.

        Returns:
            str: Inner text content trimmed.
        """
        locator = self._get_locator(locator_or_selector)
        return locator.inner_text().strip()

    def is_visible(self, locator_or_selector: str | Locator, timeout: int = 5000) -> bool:
        """Check if an element is visible within timeout.

        Args:
            locator_or_selector: Selector string or Locator instance.
            timeout: Timeout in milliseconds.

        Returns:
            bool: True if visible within timeout, False otherwise.
        """
        try:
            locator = self._get_locator(locator_or_selector)
            locator.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def select_option(self, locator_or_selector: str | Locator, value: str = None, label: str = None) -> None:
        """Select an option in a dropdown select element."""
        locator = self._get_locator(locator_or_selector)
        if value is not None:
            locator.select_option(value=value)
        elif label is not None:
            locator.select_option(label=label)

    def take_screenshot(self, filepath: str | Path) -> str:
        """Capture screenshot and save to designated filepath."""
        path_str = str(filepath)
        self.page.screenshot(path=path_str, full_page=True)
        logger.info(f"Saved screenshot: {path_str}")
        return path_str

    def _get_locator(self, locator_or_selector: str | Locator) -> Locator:
        """Helper to ensure we have a Playwright Locator."""
        if isinstance(locator_or_selector, Locator):
            return locator_or_selector
        return self.page.locator(locator_or_selector)
