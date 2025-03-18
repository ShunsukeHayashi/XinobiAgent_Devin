import requests
import logging
import time
from ..utils.config import (
    NOTE_API_BASE_URL, 
    NOTE_GRAPHQL_ENDPOINT, 
    NOTE_CREATORS_ENDPOINT,
    NOTE_NOTES_ENDPOINT,
    REQUEST_DELAY
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NoteAPI:
    """Handles API interactions with note.com."""
    
    def __init__(self, auth_token):
        self.auth_token = auth_token
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
    def _rate_limit(self):
        """Implement rate limiting to prevent detection."""
        time.sleep(REQUEST_DELAY)
    
    def get_creator_info(self, username):
        """Get creator information."""
        self._rate_limit()
        try:
            response = requests.get(
                f"{NOTE_CREATORS_ENDPOINT}/{username}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get creator info: {str(e)}")
            raise
    
    def get_notes_by_creator_id(self, creator_id):
        """Get notes by creator ID."""
        self._rate_limit()
        try:
            response = requests.get(
                f"{NOTE_NOTES_ENDPOINT}?creatorId={creator_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get notes by creator ID: {str(e)}")
            raise
    
    def get_notes_by_category(self, category, limit=10):
        """Get notes by category."""
        self._rate_limit()
        try:
            # GraphQL query to get notes by category
            query = """
            query GetNotesByCategory($category: String!, $limit: Int!) {
              notes(category: $category, limit: $limit) {
                id
                title
                body
                createdAt
                likeCount
                viewCount
                commentCount
                creator {
                  id
                  name
                }
              }
            }
            """
            variables = {
                "category": category,
                "limit": limit
            }
            
            response = requests.post(
                NOTE_GRAPHQL_ENDPOINT,
                headers=self.headers,
                json={"query": query, "variables": variables}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get notes by category: {str(e)}")
            raise
    
    def create_note(self, title, body, tags=None, category=None, is_public=True):
        """Create a new note."""
        self._rate_limit()
        try:
            # GraphQL mutation to create a new note
            mutation = """
            mutation CreateNote($input: CreateNoteInput!) {
              createNote(input: $input) {
                note {
                  id
                  title
                }
              }
            }
            """
            variables = {
                "input": {
                    "title": title,
                    "body": body,
                    "tags": tags or [],
                    "category": category,
                    "isPublic": is_public
                }
            }
            
            response = requests.post(
                NOTE_GRAPHQL_ENDPOINT,
                headers=self.headers,
                json={"query": mutation, "variables": variables}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to create note: {str(e)}")
            raise
