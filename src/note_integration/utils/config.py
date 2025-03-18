import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# note.com credentials
NOTE_USERNAME = os.getenv("NOTE_USERNAME")
NOTE_PASSWORD = os.getenv("NOTE_PASSWORD")

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# note.com API endpoints
NOTE_BASE_URL = "https://note.com"
NOTE_API_BASE_URL = "https://note.com/api/v2"
NOTE_GRAPHQL_ENDPOINT = f"{NOTE_API_BASE_URL}/graphql"
NOTE_CREATORS_ENDPOINT = f"{NOTE_API_BASE_URL}/creators"
NOTE_NOTES_ENDPOINT = f"{NOTE_API_BASE_URL}/notes"
NOTE_EDITOR_URL = "https://editor.note.com/notes"

# Browser automation settings
HEADLESS = True  # Set to False for debugging

# Rate limiting settings
REQUEST_DELAY = 2  # seconds between requests

# SEO analysis settings
COMPETITOR_ANALYSIS_COUNT = 5  # Number of competitor articles to analyze

# Content generation settings
TARGET_CHAR_COUNT = 10000  # Target character count for generated articles
