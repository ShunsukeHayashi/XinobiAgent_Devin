#!/usr/bin/env python3
"""
Run script for Enhanced Devin Gradio UI with public URL.

This script runs the Enhanced Devin Gradio UI with a public URL for easy sharing.
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
    # Parse arguments
    parser = argparse.ArgumentParser(description="Run Enhanced Devin Gradio UI with public URL")
    parser.add_argument("--api-key", help="API key for Devin API")
    parser.add_argument("--port", type=int, default=7860, help="Port to run the UI on")
    parser.add_argument("--host", default="0.0.0.0", help="Host to run the UI on")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    
    # Set up API key
    api_key = args.api_key or os.environ.get("DEVIN_API_KEY")
    
    # Launch the integration with sharing enabled
    logger.info("Starting Enhanced Devin Gradio UI with public URL")
    launch_integration(
        api_key=api_key,
        port=args.port,
        host=args.host,
        share=True,
        debug=args.debug
    )
