"""
Logger module for the XinobiAgent framework.

This module provides a configured logger for use throughout the application.
"""

import logging
import sys

# Configure the logger
logger = logging.getLogger("xinobiagent")
logger.setLevel(logging.INFO)

# Create console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Add formatter to console handler
console_handler.setFormatter(formatter)

# Add console handler to logger
logger.addHandler(console_handler)
