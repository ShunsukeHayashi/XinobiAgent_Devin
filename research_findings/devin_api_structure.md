# Devin API Structure Research

## API Overview

The Devin API provides programmatic access to Devin's AI agent capabilities, allowing developers to integrate Devin's functionality into their applications and workflows. The API follows RESTful principles and uses Bearer Authentication for security.

## Authentication

All API requests require authentication using Bearer tokens:
```
Authorization: Bearer YOUR_API_TOKEN
```

The API key can be provided directly or through the `DEVIN_API_KEY` environment variable.

## Base URL

The default base URL for the API is `https://api.devin.ai/v1`.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/sessions` | POST | Create a new Devin session |
| `/sessions` | GET | List all Devin sessions |
| `/session/{session_id}` | GET | Get details of a specific session |
| `/session/{session_id}/message` | POST | Send a message to a session |
| `/secrets` | GET | List all secrets |
| `/secrets/{secret_id}` | DELETE | Delete a secret |
| `/attachments` | POST | Upload a file |

## Request/Response Formats

### Create Session

**Request:**
```json
{
  "prompt": "Create a to-do list app using Vue",
  "playbook_id": "playbook-e40fe364a84a45f78a86d1f60d7ea1fd" // Optional
}
```

**Response:**
```json
{
  "session_id": "session-123456"
}
```

### Send Message

**Request:**
```json
{
  "message": "Add a pagination feature to the Vue app"
}
```

**Response:**
```json
{
  "success": true
}
```

### Get Session Details

**Response:**
```json
{
  "session_id": "session-123456",
  "status": "running",
  "created_at": "2023-01-01T00:00:00Z",
  "prompt": "Create a to-do list app using Vue",
  "messages": [
    {
      "role": "user",
      "content": "Add a pagination feature to the Vue app"
    },
    {
      "role": "assistant",
      "content": "I'll add a pagination feature to the Vue app."
    }
  ]
}
```

## Integration Patterns

### Direct API Integration

```python
import requests
import os

api_key = os.environ.get("DEVIN_API_KEY")
base_url = "https://api.devin.ai/v1"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.post(
    f"{base_url}/sessions",
    headers=headers,
    json={"prompt": "Create a to-do list app using Vue"}
)

session_id = response.json().get("session_id")
```

### Client Library Integration

```python
from devin_api_integration.src.devin_api_client import DevinAPIClient

client = DevinAPIClient(api_key=os.environ.get("DEVIN_API_KEY"))
session_id = client.create_session("Create a to-do list app using Vue")
```

### Agent-Based Integration

```python
from devin_api_integration.src.devin_agent import DevinAgent

agent = DevinAgent(
    name="example_agent",
    description="Example agent for demonstrating Devin API integration",
    api_key=os.environ.get("DEVIN_API_KEY")
)

session_id = await agent.create_task("Create a to-do list app using Vue")
```

## XinobiAgent Integration

The Devin API can be integrated with the XinobiAgent framework through template conversion:

```python
template_data = {
    "user_input": "Create a Python web scraper",
    "fixed_goals": ["Scrape website data", "Save results"],
    "tasks": ["Set up libraries", "Implement scraping logic"]
}

prompt = await agent.format_prompt_from_xinobi_template(template_data)
session_id = await agent.run_task_from_xinobi_template(template_data)
```

## Network Request Patterns

Based on the implementation, the following network request patterns can be observed:

1. **Session Creation**: POST request to `/sessions` with JSON payload containing prompt and optional playbook_id
2. **Message Sending**: POST request to `/session/{session_id}/message` with JSON payload containing message
3. **Session Retrieval**: GET request to `/session/{session_id}`
4. **File Upload**: POST request to `/attachments` with multipart/form-data containing file

These patterns are important for monitoring API interactions through a Chrome extension.

## Security Considerations

1. **API Key Management**: Store API keys securely using environment variables
2. **Data Privacy**: Be mindful of sensitive data in prompts and uploads
3. **Error Handling**: Implement proper error handling for API requests
