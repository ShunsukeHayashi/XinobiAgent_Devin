# Enhanced Devin UI

This directory contains the user interface for the Enhanced Devin system, implemented using Gradio.

## Overview

The Enhanced Devin UI provides a web-based interface for interacting with the Enhanced Devin system. It allows users to:

- Create and manage sessions
- Send messages and upload files
- Execute tools
- Monitor API requests, performance metrics, and logs

## Components

- `gradio_app.py`: Defines the `EnhancedDevinUI` class, which creates the Gradio interface
- `app.py`: Entry point for running the UI
- `__init__.py`: Package initialization file

## Usage

To run the UI, use the following command:

```bash
python -m enhanced_devin.ui.app --port 7860 --share
```

Command line options:

- `--api-key`: API key for Devin API (can also be set via the `DEVIN_API_KEY` environment variable)
- `--port`: Port to run the UI on (default: 7860)
- `--host`: Host to run the UI on (default: 0.0.0.0)
- `--share`: Create a public URL using Gradio's sharing feature
- `--debug`: Enable debug mode

## Interface

The UI is organized into tabs:

1. **Sessions**: Create and manage sessions
2. **Chat**: Send messages, upload files, and view responses
3. **Tools**: Execute tools and view tool details
4. **Monitoring**: View API requests, performance metrics, and logs

## Integration with Enhanced Devin

The UI integrates with the Enhanced Devin system through the following components:

- `EnhancedDevinAPIClient`: For API communication
- `APIMonitor`: For monitoring API requests
- `EventLogger`: For logging events
- `ToolRegistry`: For managing tools
