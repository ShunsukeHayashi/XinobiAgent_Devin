#!/usr/bin/env python3
"""
Test script for Enhanced Devin Gradio integration.

This script tests the integration of Enhanced Devin with Gradio.
"""

import os
import sys
import logging
import argparse

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import the integration
from enhanced_devin.ui.gradio_ui_integration import launch_integration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Run the test script."""
    # Parse arguments
    parser = argparse.ArgumentParser(description="Test Enhanced Devin Gradio Integration")
    parser.add_argument("--api-key", help="API key for Devin API")
    parser.add_argument("--port", type=int, default=7860, help="Port to run the UI on")
    parser.add_argument("--host", default="0.0.0.0", help="Host to run the UI on")
    parser.add_argument("--share", action="store_true", help="Create a public URL")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    
    # Set up API key
    api_key = args.api_key or os.environ.get("DEVIN_API_KEY")
    
    # Launch the integration
    logger.info(f"Starting Enhanced Devin Gradio integration on port {args.port}")
    launch_integration(
        api_key=api_key,
        port=args.port,
        host=args.host,
        share=args.share,
        debug=args.debug
    )

if __name__ == "__main__":
    main()
