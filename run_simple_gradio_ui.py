#!/usr/bin/env python3
"""
Run script for Simple Enhanced Devin Gradio UI.

This script runs the Simple Enhanced Devin Gradio UI with a public URL for easy sharing.
"""

import os
import sys
import logging

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the UI
from enhanced_devin.ui.simple_gradio_app import launch_simple_ui

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Simple Enhanced Devin UI")
    parser.add_argument("--port", type=int, default=7860, help="Port to run the UI on")
    parser.add_argument("--share", action="store_true", help="Create a public URL")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    
    # Launch the UI
    logger.info(f"Starting Simple Enhanced Devin UI on port {args.port}")
    launch_simple_ui(
        port=args.port,
        share=args.share,
        debug=args.debug
    )
