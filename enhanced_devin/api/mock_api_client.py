"""
Mock API Client for Enhanced Devin.

This module provides a mock API client for testing the Enhanced Devin UI
without requiring an actual API key.
"""

import asyncio
import logging
import uuid
import json
import time
from typing import Dict, List, Any, Optional, Union
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockDevinAPIClient:
    """
    Mock API Client for Enhanced Devin.
    
    This class provides a mock API client for testing the Enhanced Devin UI
    without requiring an actual API key.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the mock API client.
        
        Args:
            api_key: Optional API key (not used in mock)
        """
        self.sessions = {}
        self.messages = {}
        self.files = {}
        self.tools = {
            "bash": {
                "name": "bash",
                "description": "Execute bash commands",
                "version": "1.0.0",
                "author": "Enhanced Devin Team",
                "parameters": {
                    "command": "Command to execute"
                }
            },
            "python": {
                "name": "python",
                "description": "Execute Python code",
                "version": "1.0.0",
                "author": "Enhanced Devin Team",
                "parameters": {
                    "code": "Python code to execute"
                }
            },
            "google_search": {
                "name": "google_search",
                "description": "Search the web",
                "version": "1.0.0",
                "author": "Enhanced Devin Team",
                "parameters": {
                    "query": "Search query"
                }
            }
        }
        self.api_requests = []
        logger.info("Mock API client initialized")
    
    async def create_session(self, name: str) -> Dict[str, Any]:
        """Create a new session."""
        session_id = str(uuid.uuid4())
        created_at = datetime.now().isoformat()
        session = {
            "id": session_id,
            "name": name,
            "created_at": created_at,
            "status": "active"
        }
        self.sessions[session_id] = session
        self.messages[session_id] = []
        logger.info(f"Created session: {session_id}")
        return session
    
    async def get_sessions(self) -> List[Dict[str, Any]]:
        """Get all sessions."""
        return list(self.sessions.values())
    
    async def get_session(self, session_id: str) -> Dict[str, Any]:
        """Get a session by ID."""
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        return session
    
    async def send_message(self, session_id: str, content: str, files: Optional[List[str]] = None) -> Dict[str, Any]:
        """Send a message to a session."""
        if session_id not in self.sessions:
            raise ValueError(f"Session not found: {session_id}")
        
        message_id = str(uuid.uuid4())
        created_at = datetime.now().isoformat()
        message = {
            "id": message_id,
            "session_id": session_id,
            "content": content,
            "files": files or [],
            "created_at": created_at,
            "role": "user"
        }
        self.messages[session_id].append(message)
        
        # Generate a mock response
        await asyncio.sleep(1)  # Simulate processing time
        response_id = str(uuid.uuid4())
        response_created_at = datetime.now().isoformat()
        response = {
            "id": response_id,
            "session_id": session_id,
            "content": f"This is a mock response to: {content}",
            "files": [],
            "created_at": response_created_at,
            "role": "assistant"
        }
        self.messages[session_id].append(response)
        
        logger.info(f"Sent message to session {session_id}: {message_id}")
        return message
    
    async def get_messages(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all messages for a session."""
        if session_id not in self.sessions:
            raise ValueError(f"Session not found: {session_id}")
        return self.messages.get(session_id, [])
    
    async def get_tools(self) -> List[Dict[str, Any]]:
        """Get all available tools."""
        return list(self.tools.values())
    
    async def get_tool(self, tool_name: str) -> Dict[str, Any]:
        """Get a tool by name."""
        tool = self.tools.get(tool_name)
        if not tool:
            raise ValueError(f"Tool not found: {tool_name}")
        return tool
    
    async def execute_tool(self, session_id: str, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool."""
        if session_id not in self.sessions:
            raise ValueError(f"Session not found: {session_id}")
        
        if tool_name not in self.tools:
            raise ValueError(f"Tool not found: {tool_name}")
        
        execution_id = str(uuid.uuid4())
        created_at = datetime.now().isoformat()
        
        # Generate a mock result based on the tool
        result = None
        if tool_name == "bash":
            result = f"Executed bash command: {parameters.get('command', '')}\nOutput: Mock bash output"
        elif tool_name == "python":
            result = f"Executed Python code: {parameters.get('code', '')}\nOutput: Mock Python output"
        elif tool_name == "google_search":
            result = f"Searched for: {parameters.get('query', '')}\nResults: Mock search results"
        
        execution_result = {
            "id": execution_id,
            "session_id": session_id,
            "tool_name": tool_name,
            "parameters": parameters,
            "result": result,
            "created_at": created_at,
            "status": "completed"
        }
        
        logger.info(f"Executed tool {tool_name} in session {session_id}: {execution_id}")
        return execution_result
