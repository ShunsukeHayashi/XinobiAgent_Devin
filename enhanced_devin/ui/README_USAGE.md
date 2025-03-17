# Enhanced Devin UI Usage Guide

This guide explains how to use the Enhanced Devin UI to interact with the Enhanced Devin system.

## Overview

The Enhanced Devin UI provides a web-based interface for interacting with the Enhanced Devin system. It allows you to:

- Create and manage sessions
- Send messages and upload files
- View agent responses and actions

## Installation

Before using the UI, you need to install the required dependencies:

```bash
pip install gradio==5.21.0 aiohttp matplotlib numpy psutil
```

## Running the UI

To run the UI, use the following command:

```bash
python run_simple_gradio_ui.py --share
```

Command line options:

- `--api-key`: API key for Devin API (optional for demo)
- `--port`: Port to run the UI on (default: 7860)
- `--host`: Host to run the UI on (default: 0.0.0.0)
- `--share`: Create a public URL using Gradio's sharing feature
- `--debug`: Enable debug mode

## Using the UI

### Setting the API Key

1. Enter your Devin API key in the "API Key" field
2. Click "Set API Key"

Note: For demo purposes, you can use the UI without an API key. In this case, a mock API client will be used.

### Managing Sessions

1. Enter a name for the new session in the "Session Name" field
2. Click "Create Session"
3. To load an existing session, select it from the "Active Sessions" dropdown and click "Load Session"
4. To refresh the list of sessions, click "Refresh"

### Sending Messages

1. Type your message in the "Message" field
2. Optionally, upload files using the "Upload File" button
3. Click "Send Message"

### Viewing Agent Actions

The "Agent Actions" panel shows the actions taken by the agent in response to your messages. Each action includes:

- Time: When the action was taken
- Action: What the agent did
- Status: Whether the action was completed successfully

## Examples

### Example 1: Creating a Session and Sending a Message

1. Enter "My First Session" in the "Session Name" field
2. Click "Create Session"
3. Type "Hello, Enhanced Devin!" in the "Message" field
4. Click "Send Message"
5. View the agent's response in the chat history

### Example 2: Using the UI with a Public URL

1. Run the UI with the `--share` option:
   ```bash
   python run_simple_gradio_ui.py --share
   ```
2. Copy the public URL that is displayed in the console
3. Share the URL with others to allow them to access the UI

## Troubleshooting

### Issue: UI doesn't start

Make sure you have installed all the required dependencies:

```bash
pip install gradio==5.21.0 aiohttp matplotlib numpy psutil
```

### Issue: Can't connect to the UI

If you're running the UI on a remote server, make sure you're using the correct host and port:

```bash
python run_simple_gradio_ui.py --host 0.0.0.0 --port 7860
```

### Issue: UI is slow

Try running the UI in debug mode to see if there are any issues:

```bash
python run_simple_gradio_ui.py --debug
```

## Conclusion

The Enhanced Devin UI provides a simple and intuitive way to interact with the Enhanced Devin system. It allows you to create sessions, send messages, and view agent responses and actions.
