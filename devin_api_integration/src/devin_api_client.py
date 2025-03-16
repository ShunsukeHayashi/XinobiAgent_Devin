"""
Devin API Client for interacting with the Devin AI API.
"""

import os
import requests
from typing import Dict, Any, List, Optional, Union
import logging

# Configure logging
logger = logging.getLogger(__name__)

class DevinAPIClient:
    """
    Client for interacting with the Devin API.
    
    This client provides methods for all key Devin API endpoints, including
    session management, messaging, and file uploads.
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.devin.ai/v1"):
        """
        Initialize the Devin API client.
        
        Args:
            api_key: API key for authentication. If not provided, will look for DEVIN_API_KEY environment variable.
            base_url: Base URL for the Devin API.
        """
        self.api_key = api_key or os.environ.get("DEVIN_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set as DEVIN_API_KEY environment variable")
        
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def create_session(self, prompt: str, playbook_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new Devin session.
        
        Args:
            prompt: The task description for Devin.
            playbook_id: Optional playbook ID to guide execution.
            
        Returns:
            Response JSON containing session information.
            
        Raises:
            requests.exceptions.RequestException: If the request fails.
        """
        url = f"{self.base_url}/sessions"
        
        data = {
            "prompt": prompt
        }
        
        if playbook_id:
            data["playbook_id"] = playbook_id
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating session: {str(e)}")
            raise
    
    def list_sessions(self, limit: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
        """
        List all Devin sessions.
        
        Args:
            limit: Maximum number of sessions to return.
            offset: Offset for pagination.
            
        Returns:
            List of session information.
            
        Raises:
            requests.exceptions.RequestException: If the request fails.
        """
        url = f"{self.base_url}/sessions"
        params = {
            "limit": limit,
            "offset": offset
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error listing sessions: {str(e)}")
            raise
    
    def get_session(self, session_id: str) -> Dict[str, Any]:
        """
        Get details of a specific session.
        
        Args:
            session_id: ID of the session to get details for.
            
        Returns:
            Session details.
            
        Raises:
            requests.exceptions.RequestException: If the request fails.
        """
        url = f"{self.base_url}/session/{session_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting session {session_id}: {str(e)}")
            raise
    
    def send_message(self, session_id: str, message: str) -> Dict[str, Any]:
        """
        Send a message to a session.
        
        Args:
            session_id: ID of the session to send the message to.
            message: Message to send.
            
        Returns:
            Response JSON.
            
        Raises:
            requests.exceptions.RequestException: If the request fails.
        """
        url = f"{self.base_url}/session/{session_id}/message"
        
        data = {
            "message": message
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending message to session {session_id}: {str(e)}")
            raise
    
    def list_secrets(self) -> List[Dict[str, Any]]:
        """
        List all secrets.
        
        Returns:
            List of secret metadata.
            
        Raises:
            requests.exceptions.RequestException: If the request fails.
        """
        url = f"{self.base_url}/secrets"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error listing secrets: {str(e)}")
            raise
    
    def delete_secret(self, secret_id: str) -> Dict[str, Any]:
        """
        Delete a secret.
        
        Args:
            secret_id: ID of the secret to delete.
            
        Returns:
            Response JSON.
            
        Raises:
            requests.exceptions.RequestException: If the request fails.
        """
        url = f"{self.base_url}/secrets/{secret_id}"
        
        try:
            response = requests.delete(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error deleting secret {secret_id}: {str(e)}")
            raise
    
    def upload_file(self, file_path: str) -> Dict[str, Any]:
        """
        Upload a file.
        
        Args:
            file_path: Path to the file to upload.
            
        Returns:
            Response JSON containing attachment information.
            
        Raises:
            requests.exceptions.RequestException: If the request fails.
            FileNotFoundError: If the file does not exist.
        """
        url = f"{self.base_url}/attachments"
        
        # Remove Content-Type header for multipart/form-data
        headers = self.headers.copy()
        headers.pop("Content-Type", None)
        
        try:
            with open(file_path, "rb") as file:
                files = {
                    "file": (os.path.basename(file_path), file)
                }
                
                response = requests.post(url, headers=headers, files=files)
                response.raise_for_status()
                return response.json()
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Error uploading file {file_path}: {str(e)}")
            raise
