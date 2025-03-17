# Devin API Testing Environment

This directory contains a testing environment for simulating Devin API interactions without requiring actual login credentials. The environment includes:

1. A mock server that simulates Devin API endpoints
2. Test scripts for generating API requests
3. Integration with the Developer Console monitoring scripts

## Setup

1. Start the mock server:
   ```
   cd test_server
   python mock_server.py
   ```

2. Open the test client in your browser:
   ```
   open test_client/index.html
   ```

3. Use the Developer Console monitoring scripts to capture and analyze the API interactions.

## Available Endpoints

The mock server simulates the following Devin API endpoints:

- `POST /v1/sessions`: Create a new session
- `GET /v1/session/{session_id}`: Get session details
- `POST /v1/session/{session_id}/message`: Send a message to a session
- `POST /v1/attachments`: Upload a file attachment

## Test Scenarios

The test client includes several test scenarios:

1. Session creation
2. Message sending
3. File upload
4. Authentication flow

Each scenario generates real API requests that can be captured and analyzed using the Developer Console monitoring scripts.
