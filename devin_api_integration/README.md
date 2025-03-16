# Devin API Integration

## Overview

This package provides integration with the Devin AI API, allowing you to create and manage Devin sessions programmatically. It includes a client for interacting with the API and an agent that provides higher-level functionality.

## Installation

```bash
# Clone the repository
git clone https://github.com/ShunsukeHayashi/XinobiAgent_Devin.git
cd XinobiAgent_Devin

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
import os
import asyncio
from devin_api_integration.src.devin_agent import DevinAgent

async def main():
    # Create the agent
    agent = DevinAgent(
        name="example_agent",
        description="Example agent for demonstrating Devin API integration",
        api_key=os.environ.get("DEVIN_API_KEY")
    )
    
    # Create a task
    prompt = "Create a simple Python function that calculates the Fibonacci sequence"
    session_id = await agent.create_task(prompt)
    
    print(f"Created task with session ID: {session_id}")
    
    # Get the status
    status = await agent.get_status()
    
    print(f"Session status: {status}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Using XinobiAgent Templates

```python
import os
import asyncio
from devin_api_integration.src.devin_agent import DevinAgent

async def main():
    # Create the agent
    agent = DevinAgent(
        name="xinobi_agent",
        description="Agent for demonstrating XinobiAgent template integration",
        api_key=os.environ.get("DEVIN_API_KEY")
    )
    
    # Create a template
    template_data = {
        "user_input": "I need a Python script that can download stock price data and create a chart",
        "fixed_goals": [
            "Create a Python script for downloading stock price data",
            "Generate a chart visualization of the data"
        ],
        "tasks": [
            "Set up the environment and required libraries",
            "Implement data download functionality",
            "Create chart visualization",
            "Add error handling and documentation"
        ]
    }
    
    # Create the task
    session_id = await agent.run_task_from_xinobi_template(template_data)
    
    print(f"Created task with session ID: {session_id}")

if __name__ == "__main__":
    asyncio.run(main())
```

## API Reference

### DevinAPIClient

The `DevinAPIClient` class provides methods for interacting with the Devin API:

- `create_session(prompt, playbook_id=None)`: Create a new Devin session
- `list_sessions(limit=10, offset=0)`: List all Devin sessions
- `get_session(session_id)`: Get details of a specific session
- `send_message(session_id, message)`: Send a message to a session
- `list_secrets()`: List all secrets
- `delete_secret(secret_id)`: Delete a secret
- `upload_file(file_path)`: Upload a file

### DevinAgent

The `DevinAgent` class provides higher-level functionality for interacting with Devin:

- `create_task(prompt, playbook_id=None)`: Create a new task for Devin
- `send_follow_up(message)`: Send a follow-up message to Devin
- `get_status()`: Get the status of the current session
- `upload_context_file(file_path)`: Upload a file to provide context for the task
- `format_prompt_from_xinobi_template(template_data)`: Format a prompt from a XinobiAgent template
- `run_task_from_xinobi_template(template_data, playbook_id=None)`: Run a task from a XinobiAgent template

## Examples

See the `examples` directory for more examples:

- `devin_agent_example.py`: Examples of using the DevinAgent
- `api_examples.md`: Examples of using the Devin API directly

## XinobiAgent Integration

This package integrates with the XinobiAgent framework by providing methods for formatting prompts from XinobiAgent templates. The `format_prompt_from_xinobi_template` method takes a template data dictionary and formats it into a prompt that can be sent to Devin.

The template data should include:

- `user_input`: The user's input
- `fixed_goals`: A list of goals to achieve
- `tasks`: A list of tasks to complete

The formatted prompt follows the XinobiAgent visual guidelines, using `◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢` as delimiters.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
