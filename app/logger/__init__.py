"""
Logging system for the agent framework.
"""

import logging
import sys
from typing import Optional


# Configure the logger
logger = logging.getLogger("agent_framework")
logger.setLevel(logging.INFO)

# Create console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(console_handler)


def setup_file_logging(log_file: str, level: Optional[int] = None) -> None:
    """
    Set up file logging.
    
    Args:
        log_file: Path to the log file
        level: Logging level (defaults to INFO if not specified)
    """
    if level is None:
        level = logging.INFO
        
    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(file_handler)
    logger.info(f"File logging set up at {log_file}")


__all__ = ["logger", "setup_file_logging"]
