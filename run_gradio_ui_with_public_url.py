#!/usr/bin/env python3
"""
Run script for Enhanced Devin Gradio UI with public URL.

This script runs the Enhanced Devin Gradio UI with a public URL.
"""

import os
import sys
import logging
import argparse

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the integration
from enhanced_devin.ui.gradio_ui_integration import launch_integration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Set up API key
    api_key = os.environ.get("DEVIN_API_KEY")
    
    # Launch the integration with sharing enabled
    logger.info("Starting Enhanced Devin Gradio UI with public URL")
    launch_integration(
        api_key=api_key,
        share=True,
        debug=True
    )
