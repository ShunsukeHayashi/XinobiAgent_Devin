#!/usr/bin/env python3
"""
Run script for note.com integration web UI.
"""
import os
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.note_integration.web.app import main

if __name__ == "__main__":
    # Set environment variables if not already set
    if not os.environ.get("NOTE_USERNAME"):
        os.environ["NOTE_USERNAME"] = "shunsuke_ai"
    
    if not os.environ.get("NOTE_PASSWORD"):
        os.environ["NOTE_PASSWORD"] = "Jin156762syun@"
    
    if not os.environ.get("OPENAI_API_KEY") and os.environ.get("API_Key"):
        api_key = os.environ.get("API_Key")
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
    
    # Run the web UI
    main()
