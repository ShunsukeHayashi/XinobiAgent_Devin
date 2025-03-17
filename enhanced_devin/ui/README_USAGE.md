# Enhanced Devin UI Usage Guide

This guide explains how to use the Enhanced Devin UI.

## Overview

The Enhanced Devin UI provides a web-based interface for interacting with the Enhanced Devin system. It allows you to:

- Create and manage sessions
- Send messages and upload files
- Execute tools
- Monitor API requests, performance metrics, and logs

## Interface

The UI is organized into tabs:

1. **Sessions**: Create and manage sessions
2. **Chat**: Send messages, upload files, and view responses
3. **Tools**: Execute tools and view tool details
4. **Monitoring**: View API requests, performance metrics, and logs

## Usage

### Sessions Tab

1. **Create a Session**:
   - Enter a name for the session in the "Session Name" field
   - Click "Create Session"

2. **Load a Session**:
   - Select a session from the "Active Sessions" dropdown
   - Click "Load Session"

3. **View Session Information**:
   - Session details are displayed in the "Session Information" section

### Chat Tab

1. **Send a Message**:
   - Type your message in the "Message" field
   - Click "Send Message"

2. **Upload a File**:
   - Click "Upload File"
   - Select a file from your computer
   - Click "Send Message"

3. **View Agent Actions**:
   - Agent actions are displayed in the "Agent Actions" section

4. **View Agent State**:
   - The current state of the agent is displayed in the "Agent State" section

### Tools Tab

1. **View Available Tools**:
   - Available tools are displayed in the "Available Tools" section

2. **Execute a Tool**:
   - Enter the tool name in the "Tool Name" field
   - Enter the parameters in the "Parameters (JSON)" field
   - Click "Execute Tool"

3. **View Tool Details**:
   - Select a tool from the "Available Tools" section
   - Tool details are displayed in the "Tool Details" section

### Monitoring Tab

1. **View API Requests**:
   - API requests are displayed in the "API Monitoring" tab

2. **View Performance Metrics**:
   - Performance metrics are displayed in the "Performance" tab

3. **View Logs**:
   - Logs are displayed in the "Logs" tab

## Examples

### Example 1: Creating a Session and Sending a Message

1. Go to the "Sessions" tab
2. Enter "My Session" in the "Session Name" field
3. Click "Create Session"
4. Go to the "Chat" tab
5. Enter "Hello, Enhanced Devin!" in the "Message" field
6. Click "Send Message"
7. View the response in the chat history

### Example 2: Executing a Tool

1. Go to the "Tools" tab
2. Enter "BashTool" in the "Tool Name" field
3. Enter `{"command": "ls -la"}` in the "Parameters (JSON)" field
4. Click "Execute Tool"
5. View the result in the "Execution Result" section
