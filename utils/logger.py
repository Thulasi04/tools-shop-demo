"""Logging utility for the automation framework."""

import logging
import sys
from utils.config import config


def get_logger(name: str = "framework") -> logging.Logger:
    """Create and configure a standardized logger instance.

    Args:
        name: Name of the logger, typically __name__ or module identifier.

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler in reports directory
        log_file = config.REPORTS_DIR / "execution.log"
        config.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


logger = get_logger("automation")
