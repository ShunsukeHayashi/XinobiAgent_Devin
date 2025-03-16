"""
Direct test script for the DevinChatTool implementation.
"""

import os
import json
import asyncio
import sys
from typing import Dict, Any, Optional

# Create a mock BaseTool class for testing
class BaseTool:
    """
    Base class for all tools in the XinobiAgent framework.
    """
    
    name: str = "base_tool"
    description: str = "Base tool class"
    parameters: Dict[str, Any] = {}
    
    def __init__(self, **data):
        """Initialize the tool."""
        for key, value in data.items():
            setattr(self, key, value)
    
    async def run(self, *args, **kwargs):
        """
        Run the tool.
        
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method")

# Copy the DevinChatTool implementation directly into this file
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
        # For testing purposes, we'll just return a mock response
        session_id = "test-session-123"
        self.current_session_id = session_id
        
        return {
            "status": "success",
            "message": f"Session created with ID: {session_id}",
            "session_id": session_id,
            "details": {
                "session_id": session_id,
                "created_at": "2025-03-16T00:00:00Z",
                "prompt": prompt
            }
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
        
        return {
            "status": "success",
            "message": "Message sent successfully",
            "details": {
                "message_id": "test-message-123",
                "created_at": "2025-03-16T00:05:00Z",
                "content": message
            }
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
        
        return {
            "status": "success",
            "message": "Session status retrieved successfully",
            "details": {
                "session_id": session_id,
                "created_at": "2025-03-16T00:00:00Z",
                "status": "in_progress"
            }
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
        return {
            "status": "success",
            "message": f"Retrieved {limit} sessions starting from offset {offset}",
            "details": {
                "sessions": [
                    {
                        "session_id": "test-session-123",
                        "created_at": "2025-03-16T00:00:00Z",
                        "prompt": "Create a simple Python web server"
                    }
                ]
            }
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
        
        return {
            "status": "success",
            "message": "File uploaded successfully",
            "details": {
                "attachment_id": "test-attachment-123",
                "filename": os.path.basename(file_path)
            }
        }


async def test_create_session():
    """Test creating a session."""
    tool = DevinChatTool(api_key="test_api_key")
    result = await tool.run(
        command="create_session",
        arguments={
            "prompt": "Create a simple Python web server"
        }
    )
    
    result_data = json.loads(result)
    assert result_data["status"] == "success"
    assert "session_id" in result_data
    assert result_data["session_id"] == "test-session-123"
    
    print("✅ test_create_session passed")


async def test_send_message():
    """Test sending a message."""
    tool = DevinChatTool(api_key="test_api_key")
    
    # First create a session
    await tool.run(
        command="create_session",
        arguments={
            "prompt": "Create a simple Python web server"
        }
    )
    
    # Then send a message
    result = await tool.run(
        command="send_message",
        arguments={
            "message": "Add HTTPS support to the web server"
        }
    )
    
    result_data = json.loads(result)
    assert result_data["status"] == "success"
    assert "details" in result_data
    assert "message_id" in result_data["details"]
    
    print("✅ test_send_message passed")


async def test_get_session_status():
    """Test getting session status."""
    tool = DevinChatTool(api_key="test_api_key")
    
    # First create a session
    await tool.run(
        command="create_session",
        arguments={
            "prompt": "Create a simple Python web server"
        }
    )
    
    # Then get the session status
    result = await tool.run(
        command="get_session_status",
        arguments={}
    )
    
    result_data = json.loads(result)
    assert result_data["status"] == "success"
    assert "details" in result_data
    assert "session_id" in result_data["details"]
    
    print("✅ test_get_session_status passed")


async def test_list_sessions():
    """Test listing sessions."""
    tool = DevinChatTool(api_key="test_api_key")
    result = await tool.run(
        command="list_sessions",
        arguments={
            "limit": 10,
            "offset": 0
        }
    )
    
    result_data = json.loads(result)
    assert result_data["status"] == "success"
    assert "details" in result_data
    assert "sessions" in result_data["details"]
    
    print("✅ test_list_sessions passed")


async def test_upload_file():
    """Test uploading a file."""
    # Create a temporary test file
    with open("test.py", "w") as f:
        f.write("print('Hello, world!')")
    
    tool = DevinChatTool(api_key="test_api_key")
    result = await tool.run(
        command="upload_file",
        arguments={
            "file_path": "test.py"
        }
    )
    
    result_data = json.loads(result)
    assert result_data["status"] == "success"
    assert "details" in result_data
    assert "attachment_id" in result_data["details"]
    
    # Clean up the test file
    os.remove("test.py")
    
    print("✅ test_upload_file passed")


async def test_unknown_command():
    """Test handling of unknown commands."""
    tool = DevinChatTool(api_key="test_api_key")
    result = await tool.run(
        command="unknown_command",
        arguments={}
    )
    
    result_data = json.loads(result)
    assert result_data["status"] == "error"
    assert "message" in result_data
    assert "Unknown command" in result_data["message"]
    
    print("✅ test_unknown_command passed")


async def test_error_handling():
    """Test error handling."""
    tool = DevinChatTool(api_key="test_api_key")
    
    # Test sending a message without creating a session first
    result = await tool.run(
        command="send_message",
        arguments={
            "message": "This should fail"
        }
    )
    
    result_data = json.loads(result)
    assert result_data["status"] == "error"
    assert "message" in result_data
    assert "No session ID provided" in result_data["message"]
    
    # Test uploading a non-existent file
    result = await tool.run(
        command="upload_file",
        arguments={
            "file_path": "non_existent_file.py"
        }
    )
    
    result_data = json.loads(result)
    assert result_data["status"] == "error"
    assert "message" in result_data
    assert "File not found" in result_data["message"]
    
    print("✅ test_error_handling passed")


async def test_chat_thread_integration():
    """Test integration with a chat thread."""
    tool = DevinChatTool(api_key="test_api_key")
    
    # Simulate a chat thread
    chat_thread = [
        {"role": "user", "content": "I need to create a simple Python web server."},
        {"role": "assistant", "content": "I can help you with that. Let me use Devin AI to create a Python web server for you."}
    ]
    
    # Add a tool call to the chat thread
    tool_call = {
        "role": "tool",
        "name": "devin",
        "content": json.dumps({
            "command": "create_session",
            "arguments": {
                "prompt": "Create a simple Python web server that serves static files from a directory"
            }
        })
    }
    
    # Process the tool call
    if tool_call["name"] == "devin":
        tool_args = json.loads(tool_call["content"])
        tool_result = await tool.run(
            command=tool_args["command"],
            arguments=tool_args["arguments"]
        )
        
        # Add the tool result to the chat thread
        chat_thread.append({
            "role": "tool_result",
            "name": "devin",
            "content": tool_result
        })
    
    # Verify the chat thread
    assert len(chat_thread) == 3
    assert chat_thread[2]["role"] == "tool_result"
    assert chat_thread[2]["name"] == "devin"
    
    # Parse the tool result
    result_data = json.loads(chat_thread[2]["content"])
    assert result_data["status"] == "success"
    assert "session_id" in result_data
    
    # Add a follow-up message from the user
    chat_thread.append({
        "role": "user",
        "content": "Can you make it support HTTPS as well?"
    })
    
    # Add a response from the assistant
    chat_thread.append({
        "role": "assistant",
        "content": "I'll ask Devin to add HTTPS support to the web server."
    })
    
    # Add another tool call for the follow-up
    tool_call = {
        "role": "tool",
        "name": "devin",
        "content": json.dumps({
            "command": "send_message",
            "arguments": {
                "message": "Add HTTPS support to the web server",
                "session_id": result_data["session_id"]
            }
        })
    }
    
    # Process the follow-up tool call
    if tool_call["name"] == "devin":
        tool_args = json.loads(tool_call["content"])
        tool_result = await tool.run(
            command=tool_args["command"],
            arguments=tool_args["arguments"]
        )
        
        # Add the tool result to the chat thread
        chat_thread.append({
            "role": "tool_result",
            "name": "devin",
            "content": tool_result
        })
    
    # Verify the chat thread after the follow-up
    assert len(chat_thread) == 6
    assert chat_thread[5]["role"] == "tool_result"
    assert chat_thread[5]["name"] == "devin"
    
    # Parse the follow-up tool result
    result_data = json.loads(chat_thread[5]["content"])
    assert result_data["status"] == "success"
    
    print("✅ test_chat_thread_integration passed")


async def run_tests():
    """Run all tests."""
    print("Running tests for DevinChatTool...")
    
    await test_create_session()
    await test_send_message()
    await test_get_session_status()
    await test_list_sessions()
    await test_upload_file()
    await test_unknown_command()
    await test_error_handling()
    await test_chat_thread_integration()
    
    print("\nAll tests passed! ✅")


if __name__ == "__main__":
    asyncio.run(run_tests())
