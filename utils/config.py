"""Configuration module for the E-Commerce Automation Framework."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if available
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")


class Config:
    """Central configuration management class."""

    # Application URLs
    BASE_URL: str = os.getenv("BASE_URL", "https://practicesoftwaretesting.com").rstrip("/")
    API_BASE_URL: str = os.getenv("API_BASE_URL", "https://api.practicesoftwaretesting.com").rstrip("/")

    # Playwright Browser Options
    HEADLESS: bool = os.getenv("HEADLESS", "True").lower() in ("true", "1", "yes")
    SLOW_MO: int = int(os.getenv("SLOW_MO", "0"))
    DEFAULT_TIMEOUT: int = int(os.getenv("DEFAULT_TIMEOUT", "15000"))

    # Project Directories
    PROJECT_ROOT: Path = PROJECT_ROOT
    REPORTS_DIR: Path = PROJECT_ROOT / "reports"
    SCREENSHOTS_DIR: Path = PROJECT_ROOT / "reports" / "screenshots"
    FAILURES_DIR: Path = SCREENSHOTS_DIR / "failures"
    PASSED_DIR: Path = SCREENSHOTS_DIR / "passed"
    TEST_DATA_DIR: Path = PROJECT_ROOT / "test_data"

    # API Request defaults
    API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "10"))


config = Config()
