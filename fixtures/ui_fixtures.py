"""UI fixtures providing Page Object Model instances using pytest-playwright built-in fixtures."""

import pytest
from typing import Dict, Any
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: Dict[str, Any]) -> Dict[str, Any]:
    """Launch arguments for browser instances to prevent bot challenge detection in CI."""
    args = list(browser_type_launch_args.get("args", []))
    for flag in ["--disable-blink-features=AutomationControlled", "--no-sandbox", "--disable-setuid-sandbox"]:
        if flag not in args:
            args.append(flag)
    return {
        **browser_type_launch_args,
        "args": args,
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: Dict[str, Any]) -> Dict[str, Any]:
    """Configure browser context options while respecting pytest-playwright CLI flags.

    CLI options such as --tracing, --video, and --screenshot from addopts or command line
    are preserved and managed automatically by the pytest-playwright plugin.
    """
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "user_agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/128.0.0.0 Safari/537.36"
        ),
        "locale": "en-US",
        "timezone_id": "America/New_York",
    }


@pytest.fixture(autouse=True)
def _configure_page(page: Page) -> None:
    """Mask navigator.webdriver on page instances so CI headless runners bypass Cloudflare challenges."""
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """)


@pytest.fixture(scope="function")
def home_page(page: Page) -> HomePage:
    """Fixture providing initialized HomePage POM using built-in page fixture."""
    return HomePage(page)


@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    """Fixture providing initialized LoginPage POM using built-in page fixture."""
    return LoginPage(page)


@pytest.fixture(scope="function")
def registration_page(page: Page) -> RegistrationPage:
    """Fixture providing initialized RegistrationPage POM using built-in page fixture."""
    return RegistrationPage(page)


@pytest.fixture(scope="function")
def product_page(page: Page) -> ProductPage:
    """Fixture providing initialized ProductPage POM using built-in page fixture."""
    return ProductPage(page)


@pytest.fixture(scope="function")
def cart_page(page: Page) -> CartPage:
    """Fixture providing initialized CartPage POM using built-in page fixture."""
    return CartPage(page)


@pytest.fixture(scope="function")
def checkout_page(page: Page) -> CheckoutPage:
    """Fixture providing initialized CheckoutPage POM using built-in page fixture."""
    return CheckoutPage(page)
