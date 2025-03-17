# Enhanced Devin Gradio UI Usage Guide

This guide explains how to use the Enhanced Devin Gradio UI.

## Installation

Before running the UI, install the required dependencies:

```bash
pip install gradio matplotlib numpy psutil
```

## Running the UI

You can run the UI using one of the provided scripts:

```bash
# From the project root directory
python enhanced_devin/ui/run_ui.py --share
```

Or using the launcher:

```bash
python enhanced_devin/ui/launcher.py --share
```

Command line options:

- `--api-key`: API key for Devin API (can also be set via the `DEVIN_API_KEY` environment variable)
- `--port`: Port to run the UI on (default: 7860)
- `--host`: Host to run the UI on (default: 0.0.0.0)
- `--share`: Create a public URL using Gradio's sharing feature
- `--debug`: Enable debug mode

## Using the UI

The UI is organized into tabs:

### Sessions Tab

- Create new sessions with custom names
- Load existing sessions
- View session information

### Chat Tab

- Send messages to the agent
- Upload files
- View agent responses
- Monitor agent actions and state

### Tools Tab

- View available tools
- Select tools to view details
- Execute tools with custom parameters
- View tool execution results

### Monitoring Tab

#### API Monitoring

- View API requests
- Check request details

#### Performance

- View system metrics
- Check performance charts

#### Logs

- View log entries
- Filter logs by level and source
- View log details

## API Key

You can set the Devin API key in one of the following ways:

1. Via the UI: Enter the API key in the text box at the top of the UI
2. Via environment variable: Set the `DEVIN_API_KEY` environment variable
3. Via command line: Use the `--api-key` option when running the UI

## Usage Examples

### Creating a Session and Sending a Message

1. Go to the Sessions tab
2. Enter a name for the session and click "Create Session"
3. Go to the Chat tab
4. Enter a message and click "Send Message"
5. View the agent's response in the chat history

### Executing a Tool

1. Go to the Tools tab
2. Click "Refresh Tools" to view available tools
3. Select a tool from the list to view its details
4. Enter the tool name and parameters
5. Click "Execute Tool" to run the tool
6. View the execution result

### Monitoring API Requests

1. Go to the Monitoring tab
2. Select the API Monitoring sub-tab
3. Click "Refresh" to view recent API requests
4. Select a request to view its details

## Troubleshooting

If you encounter issues:

- Check the logs in the Monitoring tab
- Enable debug mode with the `--debug` flag
- Check the console output for error messages
