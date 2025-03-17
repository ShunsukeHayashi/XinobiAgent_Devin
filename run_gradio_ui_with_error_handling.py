#!/usr/bin/env python3
"""
Run script for Enhanced Devin Gradio UI with error handling.

This script runs the Enhanced Devin Gradio UI with proper error handling.
"""

import os
import sys
import logging
import argparse
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Run the Enhanced Devin UI with error handling."""
    # Parse arguments
    parser = argparse.ArgumentParser(description="Enhanced Devin UI")
    parser.add_argument("--api-key", help="API key for Devin API")
    parser.add_argument("--port", type=int, default=7860, help="Port to run the UI on")
    parser.add_argument("--host", default="0.0.0.0", help="Host to run the UI on")
    parser.add_argument("--share", action="store_true", help="Create a public URL")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    
    # Set up logging level
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Add the project root to the path
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        # Import the UI
        from enhanced_devin.ui.gradio_app import EnhancedDevinUI
        
        # Set up API key
        api_key = args.api_key or os.environ.get("DEVIN_API_KEY")
        
        # Create the UI
        ui = EnhancedDevinUI(api_key=api_key)
        
        # Launch the UI
        logger.info(f"Starting Enhanced Devin UI on port {args.port}")
        ui.interface.launch(
            server_name=args.host,
            server_port=args.port,
            share=args.share,
            debug=args.debug
        )
    except ImportError as e:
        logger.error(f"Import error: {e}")
        logger.error("Please make sure all dependencies are installed:")
        logger.error("pip install gradio matplotlib numpy psutil aiohttp")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()
