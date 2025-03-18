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
    parser.add_argument("--no-share", action="store_true", help="Don't create a public URL")
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
    
    # Create and run the web UI
    ui = NoteWebUI(use_mock=args.use_mock)
    app = ui.create_ui()
    app.launch(share=not args.no_share)

if __name__ == "__main__":
    main()
