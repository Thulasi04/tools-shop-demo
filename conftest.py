"""Root conftest configuring test fixtures, hooks, failure screenshots, and reporting."""

import time
from typing import Dict, Any
import pytest
from utils.config import config as app_config
from utils.helpers import load_json
from utils.logger import logger

# Import all fixtures from fixture modules so they are globally discoverable
pytest_plugins = [
    "fixtures.ui_fixtures",
    "fixtures.api_fixtures",
]


@pytest.fixture(scope="session")
def users_data() -> Dict[str, Any]:
    """Provide users JSON test data."""
    return load_json(app_config.TEST_DATA_DIR / "users.json")


@pytest.fixture(scope="session")
def products_data() -> Dict[str, Any]:
    """Provide products JSON test data, dynamically synchronized with live catalog."""
    data = load_json(app_config.TEST_DATA_DIR / "products.json")
    try:
        import requests
        resp = requests.get(f"{app_config.API_BASE_URL}/products", timeout=5)
        if resp.status_code == 200:
            products = resp.json().get("data", [])
            # Prioritize in-stock 'Pliers', otherwise any in-stock product
            matched = next((p for p in products if p.get("name") == "Pliers" and p.get("in_stock")), None)
            if not matched:
                matched = next((p for p in products if p.get("in_stock")), None)
            if matched:
                data["known_product"]["id"] = matched["id"]
                data["known_product"]["name"] = matched["name"]
                data["known_product"]["price"] = float(matched["price"])
    except Exception as e:
        logger.warning(f"Using static test data, API product discovery fallback: {e}")
    return data


@pytest.fixture(scope="session")
def app_test_data() -> Dict[str, Any]:
    """Provide application navigation and checkout test data."""
    return load_json(app_config.TEST_DATA_DIR / "test_data.json")


def pytest_configure(config: pytest.Config) -> None:
    """Ensure report and screenshot directories exist before running tests."""
    app_config.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    app_config.FAILURES_DIR.mkdir(parents=True, exist_ok=True)
    app_config.PASSED_DIR.mkdir(parents=True, exist_ok=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """Hook to capture screenshots on UI test failures and attach to HTML report."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    # We only care about failure during the test call phase
    if report.when == "call" and report.failed:
        # Check if test had a Playwright page fixture
        page = item.funcargs.get("page")
        if page:
            timestamp = int(time.time())
            safe_name = item.name.replace("/", "_").replace(":", "_").replace("[", "_").replace("]", "_")
            screenshot_path = app_config.FAILURES_DIR / f"{safe_name}_{timestamp}.png"

            try:
                page.screenshot(path=str(screenshot_path), full_page=True)
                logger.error(f"Captured failure screenshot: {screenshot_path}")

                # Attach screenshot to pytest-html report if plugin is active
                try:
                    import pytest_html

                    image_extra = pytest_html.extras.image(str(screenshot_path))
                    extras = getattr(report, "extras", None)
                    if extras is not None:
                        extras.append(image_extra)
                    else:
                        report.extras = [image_extra]
                except Exception:
                    pass
            except Exception as e:
                logger.warning(f"Could not take failure screenshot: {e}")
