"""
Devin Agent for interacting with the Devin AI API.
"""

import os
import asyncio
import logging
from typing import Dict, Any, List, Optional, Union
from pydantic import BaseModel, Field

from devin_api_integration.src.devin_api_client import DevinAPIClient

# Configure logging
logger = logging.getLogger(__name__)


class DevinAgent(BaseModel):
    """
    Agent for interacting with Devin through the API.
    
    This agent provides methods for creating and managing Devin sessions,
    sending tasks, and retrieving results.
    """
    
    name: str = Field(description="Name of the agent")
    description: str = Field(description="Description of the agent's purpose")
    api_key: Optional[str] = Field(
        default=None,
        description="API key for authentication. If not provided, will look for DEVIN_API_KEY environment variable."
    )
    playbook_id: Optional[str] = Field(
        default=None,
        description="Default playbook ID to use for sessions."
    )
    
    # Internal state
    client: DevinAPIClient = Field(
        description="Devin API client"
    )
    session_id: Optional[str] = Field(
        default=None,
        description="Current session ID"
    )
    
    class Config:
        arbitrary_types_allowed = True
    
    def __init__(self, **data):
        # Initialize with default values
        if "client" not in data:
            api_key = data.get("api_key")
            data["client"] = DevinAPIClient(api_key=api_key)
        
        super().__init__(**data)
    
    async def create_task(self, prompt: str, playbook_id: Optional[str] = None) -> str:
        """
        Create a new task for Devin.
        
        Args:
            prompt: The task description for Devin.
            playbook_id: Optional playbook ID to guide execution. If not provided, will use the default playbook ID.
            
        Returns:
            The session ID of the created task.
            
        Raises:
            requests.exceptions.RequestException: If the request fails.
        """
        # Use the provided playbook ID or the default one
        playbook_id = playbook_id or self.playbook_id
        
        # Create a new session
        response = self.client.create_session(prompt, playbook_id)
        
        # Store the session ID
        session_id = response.get("session_id")
        if not session_id:
            raise ValueError("Failed to get session ID from response")
            
        self.session_id = session_id
        
        logger.info(f"Created Devin session with ID: {self.session_id}")
        
        # Since we've already validated session_id is not None, we can safely assert its type
        assert self.session_id is not None, "Session ID should not be None at this point"
        return self.session_id
    
    async def send_follow_up(self, message: str) -> bool:
        """
        Send a follow-up message to Devin.
        
        Args:
            message: Message to send.
            
        Returns:
            True if successful, False otherwise.
            
        Raises:
            ValueError: If no session is active.
            requests.exceptions.RequestException: If the request fails.
        """
        if not self.session_id:
            raise ValueError("No active session. Create a task first.")
        
        # Send the message
        response = self.client.send_message(self.session_id, message)
        
        logger.info(f"Sent follow-up message to session {self.session_id}")
        
        return True
    
    async def get_status(self) -> Dict[str, Any]:
        """
        Get the status of the current session.
        
        Returns:
            Session details.
            
        Raises:
            ValueError: If no session is active.
            requests.exceptions.RequestException: If the request fails.
        """
        if not self.session_id:
            raise ValueError("No active session. Create a task first.")
        
        # Get session details
        response = self.client.get_session(self.session_id)
        
        return response
    
    async def upload_context_file(self, file_path: str) -> str:
        """
        Upload a file to provide context for the task.
        
        Args:
            file_path: Path to the file to upload.
            
        Returns:
            The attachment ID.
            
        Raises:
            requests.exceptions.RequestException: If the request fails.
            FileNotFoundError: If the file does not exist.
            ValueError: If attachment ID is not found in response.
        """
        # Upload the file
        response = self.client.upload_file(file_path)
        
        attachment_id = response.get("attachment_id")
        if not attachment_id:
            raise ValueError("Failed to get attachment ID from response")
        
        logger.info(f"Uploaded file {file_path} with attachment ID: {attachment_id}")
        
        return attachment_id
    
    async def format_prompt_from_xinobi_template(self, template_data: Dict[str, Any]) -> str:
        """
        Format a prompt from a XinobiAgent template.
        
        Args:
            template_data: Template data to format.
            
        Returns:
            Formatted prompt.
        """
        # Extract user input
        user_input = template_data.get("user_input", "")
        
        # Extract goals
        goals = template_data.get("fixed_goals", [])
        goals_str = "\n".join([f"- {goal}" for goal in goals])
        
        # Extract tasks
        tasks = template_data.get("tasks", [])
        tasks_str = "\n".join([f"- {task}" for task in tasks])
        
        # Format the prompt
        prompt = f"""
◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢
User Input:

{user_input}

Goals:
{goals_str}

Tasks:
{tasks_str}
◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢
"""
        
        return prompt.strip()
    
    async def run_task_from_xinobi_template(self, template_data: Dict[str, Any], playbook_id: Optional[str] = None) -> str:
        """
        Run a task from a XinobiAgent template.
        
        Args:
            template_data: Template data to format.
            playbook_id: Optional playbook ID to guide execution. If not provided, will use the default playbook ID.
            
        Returns:
            The session ID of the created task.
            
        Raises:
            requests.exceptions.RequestException: If the request fails.
        """
        # Format the prompt
        prompt = await self.format_prompt_from_xinobi_template(template_data)
        
        # Create the task
        session_id = await self.create_task(prompt, playbook_id)
        
        return session_id
