"""
WSGI configuration for Heroku deployment.
"""
import os
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.note_integration.web.app import NoteWebUI

# Create web UI instance with mock data
ui = NoteWebUI(use_mock=True)

# Create Gradio app
app = ui.create_ui().app

if __name__ == "__main__":
    app.run()
