"""
Devin API Chat Tool Integration

This module provides a tool that can be used within a chat thread to interact with the Devin API.
It allows for creating Devin sessions, sending messages, and retrieving results directly within
a conversation context.
"""

import os
import json
import requests
from typing import Dict, Any, Optional, List, Union

class DevinTool:
    """
    A tool for interacting with the Devin API within a chat thread.
    
    This tool provides methods that can be called directly from a chat interface,
    allowing users to create Devin sessions, send messages, and retrieve results
    without leaving the conversation context.
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.devin.ai/v1"):
        """
        Initialize the Devin API tool.
        
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
        self.current_session_id = None
    
    def create_session(self, prompt: str, playbook_id: Optional[str] = None) -> Dict[str, Any]:
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
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        session_data = response.json()
        self.current_session_id = session_data.get("session_id")
        
        return {
            "status": "success",
            "message": f"Session created with ID: {self.current_session_id}",
            "session_id": self.current_session_id,
            "details": session_data
        }
    
    def send_message(self, message: str, session_id: Optional[str] = None) -> Dict[str, Any]:
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
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return {
            "status": "success",
            "message": "Message sent successfully",
            "details": response.json()
        }
    
    def get_session_status(self, session_id: Optional[str] = None) -> Dict[str, Any]:
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
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        return {
            "status": "success",
            "message": "Session status retrieved successfully",
            "details": response.json()
        }
    
    def list_sessions(self, limit: int = 10, offset: int = 0) -> Dict[str, Any]:
        """
        List all Devin sessions.
        
        Args:
            limit: Maximum number of sessions to return.
            offset: Number of sessions to skip.
            
        Returns:
            List of sessions.
        """
        url = f"{self.base_url}/sessions?limit={limit}&offset={offset}"
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        return {
            "status": "success",
            "message": f"Retrieved {limit} sessions starting from offset {offset}",
            "details": response.json()
        }
    
    def upload_file(self, file_path: str) -> Dict[str, Any]:
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
        
        with open(file_path, "rb") as file:
            files = {"file": (os.path.basename(file_path), file)}
            response = requests.post(url, headers={"Authorization": self.headers["Authorization"]}, files=files)
        
        response.raise_for_status()
        
        return {
            "status": "success",
            "message": "File uploaded successfully",
            "details": response.json()
        }
    
    def handle_command(self, command: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a command from a chat interface.
        
        Args:
            command: The command to execute.
            args: Arguments for the command.
            
        Returns:
            Command execution results.
        """
        commands = {
            "create_session": self.create_session,
            "send_message": self.send_message,
            "get_session_status": self.get_session_status,
            "list_sessions": self.list_sessions,
            "upload_file": self.upload_file
        }
        
        if command not in commands:
            return {
                "status": "error",
                "message": f"Unknown command: {command}. Available commands: {', '.join(commands.keys())}"
            }
        
        try:
            return commands[command](**args)
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error executing command {command}: {str(e)}"
            }

# Example of how to use the tool in a chat context
def process_tool_call(tool_call: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a tool call from a chat interface.
    
    Args:
        tool_call: Tool call details including the command and arguments.
        
    Returns:
        Tool call execution results.
    """
    try:
        # Extract command and arguments
        command = tool_call.get("command")
        args = tool_call.get("arguments", {})
        
        # Initialize the tool
        api_key = os.environ.get("DEVIN_API_KEY")
        tool = DevinTool(api_key=api_key)
        
        # Execute the command
        return tool.handle_command(command, args)
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error processing tool call: {str(e)}"
        }
