#!/usr/bin/env python3
"""
Run script for note.com integration web UI.
"""
import os
import sys
import argparse
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.note_integration.web.app import NoteWebUI

def main():
    """Main function to run the web UI."""
    parser = argparse.ArgumentParser(description="Run note.com integration web UI")
    parser.add_argument("--use-mock", action="store_true", help="Use mock data instead of real API")
    parser.add_argument("--no-mock", action="store_true", help="Don't use mock data")
    parser.add_argument("--no-share", action="store_true", help="Don't create a public URL")
    parser.add_argument("--port", type=int, default=None, help="Port to run the server on")
    args = parser.parse_args()
    
    # Set environment variables if not already set
    if not os.environ.get("NOTE_USERNAME"):
        os.environ["NOTE_USERNAME"] = "shunsuke_ai"
    
    if not os.environ.get("NOTE_PASSWORD"):
        os.environ["NOTE_PASSWORD"] = "Jin156762syun@"
    
    if not os.environ.get("OPENAI_API_KEY") and os.environ.get("API_Key"):
        api_key = os.environ.get("API_Key")
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
    
    # Determine mock mode
    use_mock = None
    if args.use_mock:
        use_mock = True
    elif args.no_mock:
        use_mock = False
    
    # Get port from environment variable for Heroku
    port = args.port
    if port is None:
        port = int(os.environ.get("PORT", 7860))
    
    # Create and run the web UI
    ui = NoteWebUI(use_mock=use_mock)
    app = ui.create_ui()
    app.launch(server_name="0.0.0.0", server_port=port, share=not args.no_share)

if __name__ == "__main__":
    main()
