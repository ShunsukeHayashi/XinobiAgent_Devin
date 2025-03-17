#!/usr/bin/env python3
"""
Test script for running the Enhanced Devin Gradio UI.

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
    # Parse arguments
    parser = argparse.ArgumentParser(description="Test Enhanced Devin Gradio UI")
    parser.add_argument("--api-key", help="API key for Devin API")
    parser.add_argument("--port", type=int, default=7860, help="Port to run the UI on")
    parser.add_argument("--host", default="0.0.0.0", help="Host to run the UI on")
    parser.add_argument("--share", action="store_true", help="Create a public URL")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    
    # Set up API key
    api_key = args.api_key or os.environ.get("DEVIN_API_KEY")
    
    # Launch the integration with sharing enabled by default
    logger.info("Starting Enhanced Devin Gradio UI")
    launch_integration(
        api_key=api_key,
        port=args.port,
        host=args.host,
        share=True if args.share is None else args.share,
        debug=True if args.debug is None else args.debug
    )
