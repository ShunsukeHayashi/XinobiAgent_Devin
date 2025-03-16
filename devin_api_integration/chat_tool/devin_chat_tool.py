"""
Devin API Chat Tool Integration for XinobiAgent

This module provides a tool that can be used within a chat thread to interact with the Devin API,
following the BaseTool interface from the XinobiAgent framework.
"""

import os
import json
import requests
import asyncio
from typing import Dict, Any, Optional, List, Union

from app.tool.base import BaseTool


class DevinChatTool(BaseTool):
    """
    A tool for interacting with the Devin API within a chat thread.
    
    This tool follows the BaseTool interface from the XinobiAgent framework,
    allowing it to be used with the ToolCollection and GenericAgent classes.
    """
    
    name: str = "devin"
    description: str = "Interact with Devin AI to solve programming tasks"
    parameters: Dict[str, Any] = {
        "command": {
            "type": "string",
            "description": "The command to execute (create_session, send_message, get_session_status, list_sessions, upload_file)",
            "required": True
        },
        "arguments": {
            "type": "object",
            "description": "Arguments for the command",
            "required": True
        }
    }
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.devin.ai/v1", **data):
        """
        Initialize the Devin API tool.
        
        Args:
            api_key: API key for authentication. If not provided, will look for DEVIN_API_KEY environment variable.
            base_url: Base URL for the Devin API.
        """
        super().__init__(**data)
        self.api_key = api_key or os.environ.get("DEVIN_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set as DEVIN_API_KEY environment variable")
        
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.current_session_id = None
    
    async def run(self, command: str, arguments: Dict[str, Any]) -> str:
        """
        Run the tool with the provided command and arguments.
        
        Args:
            command: The command to execute
            arguments: Arguments for the command
            
        Returns:
            The result of running the command
        """
        commands = {
            "create_session": self._create_session,
            "send_message": self._send_message,
            "get_session_status": self._get_session_status,
            "list_sessions": self._list_sessions,
            "upload_file": self._upload_file
        }
        
        if command not in commands:
            return json.dumps({
                "status": "error",
                "message": f"Unknown command: {command}. Available commands: {', '.join(commands.keys())}"
            })
        
        try:
            result = await commands[command](**arguments)
            return json.dumps(result)
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Error executing command {command}: {str(e)}"
            })
    
    async def _create_session(self, prompt: str, playbook_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new Devin session.
        
        Args:
            prompt: The task description for Devin.
            playbook_id: Optional playbook ID to guide execution.
            
        Returns:
            Session details including the session ID.
        """
        url = f"{self.base_url}/sessions"
        
        payload = {
            "prompt": prompt
        }
        
        if playbook_id:
            payload["playbook_id"] = playbook_id
        
        # Use asyncio to run the blocking request in a thread pool
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: requests.post(url, headers=self.headers, json=payload)
        )
        response.raise_for_status()
        
        session_data = response.json()
        self.current_session_id = session_data.get("session_id")
        
        return {
            "status": "success",
            "message": f"Session created with ID: {self.current_session_id}",
            "session_id": self.current_session_id,
            "details": session_data
        }
    
    async def _send_message(self, message: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Send a message to an existing Devin session.
        
        Args:
            message: Message to send to Devin.
            session_id: Session ID to send the message to. If not provided, uses the current session.
            
        Returns:
            Response details.
        """
        session_id = session_id or self.current_session_id
        if not session_id:
            return {
                "status": "error",
                "message": "No session ID provided or no current session exists. Create a session first."
            }
        
        url = f"{self.base_url}/session/{session_id}/message"
        
        payload = {
            "message": message
        }
        
        # Use asyncio to run the blocking request in a thread pool
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: requests.post(url, headers=self.headers, json=payload)
        )
        response.raise_for_status()
        
        return {
            "status": "success",
            "message": "Message sent successfully",
            "details": response.json()
        }
    
    async def _get_session_status(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get the status of a Devin session.
        
        Args:
            session_id: Session ID to check. If not provided, uses the current session.
            
        Returns:
            Session status details.
        """
        session_id = session_id or self.current_session_id
        if not session_id:
            return {
                "status": "error",
                "message": "No session ID provided or no current session exists. Create a session first."
            }
        
        url = f"{self.base_url}/session/{session_id}"
        
        # Use asyncio to run the blocking request in a thread pool
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: requests.get(url, headers=self.headers)
        )
        response.raise_for_status()
        
        return {
            "status": "success",
            "message": "Session status retrieved successfully",
            "details": response.json()
        }
    
    async def _list_sessions(self, limit: int = 10, offset: int = 0) -> Dict[str, Any]:
        """
        List all Devin sessions.
        
        Args:
            limit: Maximum number of sessions to return.
            offset: Number of sessions to skip.
            
        Returns:
            List of sessions.
        """
        url = f"{self.base_url}/sessions?limit={limit}&offset={offset}"
        
        # Use asyncio to run the blocking request in a thread pool
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: requests.get(url, headers=self.headers)
        )
        response.raise_for_status()
        
        return {
            "status": "success",
            "message": f"Retrieved {limit} sessions starting from offset {offset}",
            "details": response.json()
        }
    
    async def _upload_file(self, file_path: str) -> Dict[str, Any]:
        """
        Upload a file to provide context for Devin.
        
        Args:
            file_path: Path to the file to upload.
            
        Returns:
            Upload details including the attachment ID.
        """
        if not os.path.exists(file_path):
            return {
                "status": "error",
                "message": f"File not found: {file_path}"
            }
        
        url = f"{self.base_url}/attachments"
        
        # Use asyncio to run the blocking request in a thread pool
        loop = asyncio.get_event_loop()
        
        async def upload():
            with open(file_path, "rb") as file:
                files = {"file": (os.path.basename(file_path), file)}
                return requests.post(url, headers={"Authorization": self.headers["Authorization"]}, files=files)
        
        response = await upload()
        response.raise_for_status()
        
        return {
            "status": "success",
            "message": "File uploaded successfully",
            "details": response.json()
        }
