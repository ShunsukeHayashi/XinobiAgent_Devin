"""
Main application file for Enhanced Devin UI.

This module provides the entry point for running the Enhanced Devin UI.
"""

import os
import sys
import argparse
import logging
from enhanced_devin.ui.gradio_app import EnhancedDevinUI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Enhanced Devin UI")
    parser.add_argument("--api-key", help="API key for Devin API")
    parser.add_argument("--port", type=int, default=7860, help="Port to run the UI on")
    parser.add_argument("--host", default="0.0.0.0", help="Host to run the UI on")
    parser.add_argument("--share", action="store_true", help="Create a public URL")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    return parser.parse_args()

def main():
    """Run the Enhanced Devin UI."""
    args = parse_args()
    
    # Set up API key
    api_key = args.api_key or os.environ.get("DEVIN_API_KEY")
    
    # Create the UI
    ui = EnhancedDevinUI(api_key=api_key)
    
    # Set up logging level
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Launch the UI
    logger.info(f"Starting Enhanced Devin UI on port {args.port}")
    ui.interface.launch(
        server_name=args.host,
        server_port=args.port,
        share=args.share,
        debug=args.debug
    )

if __name__ == "__main__":
    main()
