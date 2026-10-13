"""Helper utility functions for data generation, parsing, and JSON operations."""

import json
import random
import string
import time
from pathlib import Path
from typing import Any, Dict
from utils.config import config


def load_json(file_path: Path) -> Dict[str, Any]:
    """Load and parse a JSON file.

    Args:
        file_path: Absolute or relative Path object.

    Returns:
        dict: Parsed JSON data.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_unique_email(prefix: str = "auto_user") -> str:
    """Generate a unique email address with timestamp and random characters.

    Args:
        prefix: Email username prefix.

    Returns:
        str: Unique email address.
    """
    timestamp = int(time.time())
    random_str = "".join(random.choices(string.ascii_lowercase, k=4))
    return f"{prefix}_{timestamp}_{random_str}@example-test.com"


def generate_random_user() -> Dict[str, Any]:
    """Generate a realistic, unique user payload compatible with the API & UI schemas.

    Returns:
        dict: User registration payload.
    """
    first_names = ["Alex", "Jordan", "Taylor", "Morgan", "Sam", "Chris"]
    last_names = ["Miller", "Davis", "Wilson", "Anderson", "Taylor", "Thomas"]
    first = random.choice(first_names)
    last = random.choice(last_names)
    email = generate_unique_email(prefix=f"{first.lower()}.{last.lower()}")

    return {
        "first_name": first,
        "last_name": last,
        "dob": "1992-06-15",
        "address": {
            "street": "100 Automation Blvd",
            "house_number": "42",
            "city": "Sunnyvale",
            "state": "California",
            "country": "US",
            "postal_code": "94086",
        },
        "phone": "5551234567",
        "email": email,
        # Password meets complexity and avoids common breach list:
        # uppercase, lowercase, number, special symbol, min 8 chars
        "password": "PracticePassword987!",
    }


def parse_price(price_str: str) -> float:
    """Convert price strings like '$12.01' or '12.01' into float 12.01.

    Args:
        price_str: Formatted price string.

    Returns:
        float: Clean numeric price.
    """
    cleaned = price_str.replace("$", "").replace(",", "").strip()
    return float(cleaned)
