# Devin API Chat Tool Integration

This module provides a tool that can be used within a chat thread to interact with the Devin API, following the BaseTool interface from the XinobiAgent framework.

## Overview

The Devin Chat Tool allows you to interact with Devin AI directly within a chat thread, enabling you to create Devin sessions, send messages, and retrieve results without leaving the conversation context.

## Features

- Create Devin sessions
- Send messages to existing sessions
- Get session status
- List all sessions
- Upload files for context

## Installation

```bash
# Install the package
pip install -e .
```

## Usage

### As a Tool in a GenericAgent

```python
from app.agent.generic_agent import GenericAgent
from app.tool.collection import ToolCollection
from devin_api_integration.chat_tool.devin_chat_tool import DevinChatTool

# Create a tool collection with the Devin Chat Tool
tools = ToolCollection([
    DevinChatTool(api_key="your_api_key")
])

# Create a generic agent with the tool collection
agent = GenericAgent(
    name="devin_chat_agent",
    description="An agent that can use Devin AI to solve programming tasks",
    available_tools=tools
)

# Set the goal for the agent
goal = "Create a simple Python web server using Devin AI"
await agent.set_goal(goal)

# Run the agent
result = await agent.run()
```

### Direct Usage

```python
from devin_api_integration.chat_tool.devin_chat_tool import DevinChatTool

# Create the Devin Chat Tool
devin_tool = DevinChatTool(api_key="your_api_key")

# Create a session
create_result = await devin_tool.run(
    command="create_session",
    arguments={
        "prompt": "Create a simple Python web server"
    }
)

# Parse the result to get the session ID
import json
create_data = json.loads(create_result)
session_id = create_data.get("session_id")

# Send a follow-up message
message_result = await devin_tool.run(
    command="send_message",
    arguments={
        "message": "Make it serve static files from a directory",
        "session_id": session_id
    }
)
```

### In a Chat Thread

```python
import json
from devin_api_integration.chat_tool.devin_chat_tool import DevinChatTool

# Create the Devin Chat Tool
devin_tool = DevinChatTool(api_key="your_api_key")

# Simulate a chat thread
chat_thread = [
    {"role": "user", "content": "I need to create a simple Python web server."},
    {"role": "assistant", "content": "I can help you with that. Let me use Devin AI to create a Python web server for you."},
    {"role": "tool", "name": "devin", "content": json.dumps({
        "command": "create_session",
        "arguments": {
            "prompt": "Create a simple Python web server that serves static files from a directory"
        }
    })}
]

# Process the tool call
if chat_thread[-1]["role"] == "tool" and chat_thread[-1]["name"] == "devin":
    tool_call = json.loads(chat_thread[-1]["content"])
    tool_result = await devin_tool.run(
        command=tool_call["command"],
        arguments=tool_call["arguments"]
    )
    
    # Add the tool result to the chat thread
    chat_thread.append({
        "role": "tool_result",
        "name": "devin",
        "content": tool_result
    })
```

## API Reference

### DevinChatTool

```python
DevinChatTool(api_key=None, base_url="https://api.devin.ai/v1", **data)
```

#### Parameters

- `api_key` (Optional[str]): API key for authentication. If not provided, will look for DEVIN_API_KEY environment variable.
- `base_url` (str): Base URL for the Devin API.

#### Methods

```python
async run(command: str, arguments: Dict[str, Any]) -> str
```

Run the tool with the provided command and arguments.

##### Parameters

- `command` (str): The command to execute (create_session, send_message, get_session_status, list_sessions, upload_file)
- `arguments` (Dict[str, Any]): Arguments for the command

##### Returns

- `str`: The result of running the command as a JSON string

## Commands

### create_session

Create a new Devin session.

#### Arguments

- `prompt` (str): The task description for Devin.
- `playbook_id` (Optional[str]): Optional playbook ID to guide execution.

#### Returns

Session details including the session ID.

### send_message

Send a message to an existing Devin session.

#### Arguments

- `message` (str): Message to send to Devin.
- `session_id` (Optional[str]): Session ID to send the message to. If not provided, uses the current session.

#### Returns

Response details.

### get_session_status

Get the status of a Devin session.

#### Arguments

- `session_id` (Optional[str]): Session ID to check. If not provided, uses the current session.

#### Returns

Session status details.

### list_sessions

List all Devin sessions.

#### Arguments

- `limit` (int): Maximum number of sessions to return.
- `offset` (int): Number of sessions to skip.

#### Returns

List of sessions.

### upload_file

Upload a file to provide context for Devin.

#### Arguments

- `file_path` (str): Path to the file to upload.

#### Returns

Upload details including the attachment ID.

## Examples

See the `example_usage.py` file for complete examples of using the Devin Chat Tool.
