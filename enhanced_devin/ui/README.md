# Enhanced Devin UI

This directory contains the user interface for the Enhanced Devin system, implemented using Gradio.

## Overview

The Enhanced Devin UI provides a web-based interface for interacting with the Enhanced Devin system. It allows users to:

- Create and manage sessions
- Send messages and upload files
- Execute tools
- Monitor API requests, performance metrics, and logs

## Documentation

The UI includes comprehensive documentation in both English and Japanese:

- [Usage Guide (English)](README_USAGE.md)
- [Usage Guide (Japanese)](README_USAGE_JA.md)
- [Installation Guide (English)](INSTALLATION.md)
- [Installation Guide (Japanese)](INSTALLATION_JA.md)
- [Verification Guide (English)](VERIFICATION.md)
- [Verification Guide (Japanese)](VERIFICATION_JA.md)
- [Troubleshooting Guide (English)](TROUBLESHOOTING.md)
- [Troubleshooting Guide (Japanese)](TROUBLESHOOTING_JA.md)
- [Screenshot Guide (English)](SCREENSHOTS.md)
- [Screenshot Guide (Japanese)](SCREENSHOTS_JA.md)
- [Simple UI Guide](README_SIMPLE.md)

## Running the UI

To run the UI, use the following command:

```bash
python run_simple_gradio_ui.py --share
```

This will start the UI and provide a public URL that can be accessed from any browser.

## Features

The UI includes the following features:

- Session management
- Chat interface
- File upload
- Tool execution
- API monitoring
- Performance monitoring
- Event logging

## Implementation

The UI is implemented using:

- Gradio: For the web interface
- MockDevinAPIClient: For testing without an actual API key
- EnhancedDevinAPIClient: For interacting with the Enhanced Devin API

## Testing

The UI can be tested without an actual API key by using the built-in MockDevinAPIClient.
