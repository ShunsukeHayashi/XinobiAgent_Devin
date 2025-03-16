# Devin API Tool Call Format

This document describes the format for using the Devin API as a tool call within a chat thread.

## Overview

The Devin API can be integrated as a tool call within a chat thread, allowing users to interact with Devin AI without leaving their conversation context. This document describes the format for these tool calls.

## Tool Call Format

A tool call to the Devin API has the following format:

```json
{
    "role": "tool",
    "name": "devin",
    "content": {
        "command": "create_session",
        "arguments": {
            "prompt": "Create a simple Python web server"
        }
    }
}
```

### Fields

- `role`: Always "tool" for a tool call
- `name`: "devin" for the Devin API tool
- `content`: A JSON object containing:
  - `command`: The command to execute
  - `arguments`: Arguments for the command

## Available Commands

### create_session

Create a new Devin session.

```json
{
    "command": "create_session",
    "arguments": {
        "prompt": "Create a simple Python web server",
        "playbook_id": "optional-playbook-id"
    }
}
```

#### Arguments

- `prompt` (required): The task description for Devin
- `playbook_id` (optional): Playbook ID to guide execution

### send_message

Send a message to an existing Devin session.

```json
{
    "command": "send_message",
    "arguments": {
        "message": "Add HTTPS support to the web server",
        "session_id": "session-123456"
    }
}
```

#### Arguments

- `message` (required): Message to send to Devin
- `session_id` (optional): Session ID to send the message to. If not provided, uses the current session.

### get_session_status

Get the status of a Devin session.

```json
{
    "command": "get_session_status",
    "arguments": {
        "session_id": "session-123456"
    }
}
```

#### Arguments

- `session_id` (optional): Session ID to check. If not provided, uses the current session.

### list_sessions

List all Devin sessions.

```json
{
    "command": "list_sessions",
    "arguments": {
        "limit": 10,
        "offset": 0
    }
}
```

#### Arguments

- `limit` (optional): Maximum number of sessions to return. Default: 10
- `offset` (optional): Number of sessions to skip. Default: 0

### upload_file

Upload a file to provide context for Devin.

```json
{
    "command": "upload_file",
    "arguments": {
        "file_path": "/path/to/file.py"
    }
}
```

#### Arguments

- `file_path` (required): Path to the file to upload

## Tool Result Format

The result of a tool call has the following format:

```json
{
    "role": "tool_result",
    "name": "devin",
    "content": {
        "status": "success",
        "message": "Session created with ID: session-123456",
        "session_id": "session-123456",
        "details": {
            "session_id": "session-123456",
            "created_at": "2025-03-16T00:00:00Z",
            "prompt": "Create a simple Python web server"
        }
    }
}
```

### Fields

- `role`: Always "tool_result" for a tool result
- `name`: "devin" for the Devin API tool
- `content`: A JSON object containing:
  - `status`: "success" or "error"
  - `message`: A human-readable message
  - `session_id`: The session ID (for create_session)
  - `details`: Additional details about the result

## Example Chat Thread

Here's an example of a complete chat thread with Devin API tool calls:

```json
[
    {
        "role": "user",
        "content": "I need to create a simple Python web server."
    },
    {
        "role": "assistant",
        "content": "I can help you with that. Let me use Devin AI to create a Python web server for you."
    },
    {
        "role": "tool",
        "name": "devin",
        "content": {
            "command": "create_session",
            "arguments": {
                "prompt": "Create a simple Python web server that serves static files from a directory"
            }
        }
    },
    {
        "role": "tool_result",
        "name": "devin",
        "content": {
            "status": "success",
            "message": "Session created with ID: session-123456",
            "session_id": "session-123456",
            "details": {
                "session_id": "session-123456",
                "created_at": "2025-03-16T00:00:00Z",
                "prompt": "Create a simple Python web server that serves static files from a directory"
            }
        }
    },
    {
        "role": "assistant",
        "content": "I've created a Devin AI session to help you build a Python web server. The session is now working on creating a web server that serves static files from a directory. Would you like to add any specific features to this web server?"
    },
    {
        "role": "user",
        "content": "Can you make it support HTTPS as well?"
    },
    {
        "role": "assistant",
        "content": "I'll ask Devin to add HTTPS support to the web server."
    },
    {
        "role": "tool",
        "name": "devin",
        "content": {
            "command": "send_message",
            "arguments": {
                "message": "Add HTTPS support to the web server",
                "session_id": "session-123456"
            }
        }
    },
    {
        "role": "tool_result",
        "name": "devin",
        "content": {
            "status": "success",
            "message": "Message sent successfully",
            "details": {
                "message_id": "message-123456",
                "created_at": "2025-03-16T00:05:00Z",
                "content": "Add HTTPS support to the web server"
            }
        }
    },
    {
        "role": "assistant",
        "content": "I've asked Devin to add HTTPS support to the web server. Devin is now working on your request. Is there anything else you'd like to add to the web server?"
    }
]
```

## Conclusion

This document describes the format for using the Devin API as a tool call within a chat thread. By following this format, you can integrate Devin AI capabilities into your chat interface, providing users with powerful programming assistance without leaving their conversation context.
