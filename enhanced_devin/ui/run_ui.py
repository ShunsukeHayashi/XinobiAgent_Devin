#!/usr/bin/env python3
"""
Run script for Enhanced Devin UI.

This script provides a simple way to run the Enhanced Devin UI.
"""

import os
import sys
import argparse
import logging
from enhanced_devin.ui.gradio_app import launch_ui

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Run the Enhanced Devin UI."""
    # Parse arguments
    parser = argparse.ArgumentParser(description="Enhanced Devin UI")
    parser.add_argument("--api-key", help="API key for Devin API")
    parser.add_argument("--port", type=int, default=7860, help="Port to run the UI on")
    parser.add_argument("--host", default="0.0.0.0", help="Host to run the UI on")
    parser.add_argument("--share", action="store_true", help="Create a public URL")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    
    # Set up API key
    api_key = args.api_key or os.environ.get("DEVIN_API_KEY")
    
    # Launch the UI
    logger.info(f"Starting Enhanced Devin UI on port {args.port}")
    launch_ui(
        api_key=api_key,
        port=args.port,
        host=args.host,
        share=args.share,
        debug=args.debug
    )

if __name__ == "__main__":
    main()
