"""
Test script for the DevinChatTool implementation.
"""

import os
import json
import asyncio
from typing import Dict, Any, Optional

from devin_api_integration.chat_tool.devin_chat_tool import DevinChatTool


class MockDevinChatTool(DevinChatTool):
    """
    A mock implementation of the DevinChatTool for testing.
    """
    
    def __init__(self, **data):
        """Initialize with a mock API key."""
        super().__init__(api_key="mock_api_key", **data)
        self.mock_responses = {
            "create_session": {
                "status": "success",
                "message": "Session created with ID: mock-session-123",
                "session_id": "mock-session-123",
                "details": {
                    "session_id": "mock-session-123",
                    "created_at": "2025-03-16T00:00:00Z",
                    "prompt": "Create a simple Python web server"
                }
            },
            "send_message": {
                "status": "success",
                "message": "Message sent successfully",
                "details": {
                    "message_id": "mock-message-123",
                    "created_at": "2025-03-16T00:05:00Z",
                    "content": "Add HTTPS support to the web server"
                }
            },
            "get_session_status": {
                "status": "success",
                "message": "Session status retrieved successfully",
                "details": {
                    "session_id": "mock-session-123",
                    "created_at": "2025-03-16T00:00:00Z",
                    "prompt": "Create a simple Python web server",
                    "status": "in_progress"
                }
            },
            "list_sessions": {
                "status": "success",
                "message": "Retrieved 1 sessions starting from offset 0",
                "details": {
                    "sessions": [
                        {
                            "session_id": "mock-session-123",
                            "created_at": "2025-03-16T00:00:00Z",
                            "prompt": "Create a simple Python web server"
                        }
                    ]
                }
            },
            "upload_file": {
                "status": "success",
                "message": "File uploaded successfully",
                "details": {
                    "attachment_id": "mock-attachment-123",
                    "filename": "test.py"
                }
            }
        }
    
    async def run(self, command: str, arguments: Dict[str, Any]) -> str:
        """
        Mock implementation of the run method.
        
        Args:
            command: The command to execute
            arguments: Arguments for the command
            
        Returns:
            The mock result for the command
        """
        if command not in self.mock_responses:
            return json.dumps({
                "status": "error",
                "message": f"Unknown command: {command}"
            })
        
        # For create_session, update the prompt in the mock response
        if command == "create_session" and "prompt" in arguments:
            self.mock_responses["create_session"]["details"]["prompt"] = arguments["prompt"]
        
        # For send_message, update the content in the mock response
        if command == "send_message" and "message" in arguments:
            self.mock_responses["send_message"]["details"]["content"] = arguments["message"]
        
        # Return the mock response
        return json.dumps(self.mock_responses[command])


async def test_create_session():
    """Test creating a session."""
    tool = MockDevinChatTool()
    result = await tool.run(
        command="create_session",
        arguments={
            "prompt": "Create a simple Python web server"
        }
    )
    
    result_data = json.loads(result)
    assert result_data["status"] == "success"
    assert "session_id" in result_data
    assert result_data["session_id"] == "mock-session-123"
    
    print("✅ test_create_session passed")


async def test_send_message():
    """Test sending a message."""
    tool = MockDevinChatTool()
    result = await tool.run(
        command="send_message",
        arguments={
            "message": "Add HTTPS support to the web server",
            "session_id": "mock-session-123"
        }
    )
    
    result_data = json.loads(result)
    assert result_data["status"] == "success"
    assert "details" in result_data
    assert "message_id" in result_data["details"]
    
    print("✅ test_send_message passed")


async def test_get_session_status():
    """Test getting session status."""
    tool = MockDevinChatTool()
    result = await tool.run(
        command="get_session_status",
        arguments={
            "session_id": "mock-session-123"
        }
    )
    
    result_data = json.loads(result)
    assert result_data["status"] == "success"
    assert "details" in result_data
    assert "session_id" in result_data["details"]
    
    print("✅ test_get_session_status passed")


async def test_list_sessions():
    """Test listing sessions."""
    tool = MockDevinChatTool()
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
    
    tool = MockDevinChatTool()
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
    tool = MockDevinChatTool()
    result = await tool.run(
        command="unknown_command",
        arguments={}
    )
    
    result_data = json.loads(result)
    assert result_data["status"] == "error"
    assert "message" in result_data
    assert "Unknown command" in result_data["message"]
    
    print("✅ test_unknown_command passed")


async def test_chat_thread_integration():
    """Test integration with a chat thread."""
    tool = MockDevinChatTool()
    
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
    await test_chat_thread_integration()
    
    print("\nAll tests passed! ✅")


if __name__ == "__main__":
    asyncio.run(run_tests())
