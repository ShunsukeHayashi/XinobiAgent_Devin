#!/usr/bin/env python3
"""
Test script for running the Enhanced Devin UI.
"""

import os
import sys
import logging

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the UI launcher
from enhanced_devin.ui.gradio_app import launch_ui

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Launch the UI with sharing enabled
    logger.info("Starting Enhanced Devin UI with public URL")
    launch_ui(share=True, debug=True)
