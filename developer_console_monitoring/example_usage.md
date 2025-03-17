# Example Usage of Devin API Monitoring

This document provides examples of how to use the Devin API monitoring tools in various scenarios.

## Basic Monitoring

### Capturing All API Requests

1. Open the Chrome Developer Console (F12 or Ctrl+Shift+I)
2. Copy and paste the content of `console_scripts/api_monitor.js` into the Console tab
3. Press Enter to execute the script
4. Interact with Devin to generate API requests
5. View captured requests with `devinApi.getRequests()`

```javascript
// Example output
[
  {
    "id": "16798765432123abc",
    "url": "https://api.devin.ai/v1/sessions",
    "method": "POST",
    "body": "{\"prompt\":\"Create a React app\"}",
    "timestamp": "2025-03-17T06:15:23.456Z",
    "type": "xhr",
    "response": {
      "id": "16798765432123abc",
      "status": 200,
      "statusText": "OK",
      "body": "{\"session_id\":\"session-123456\",\"status\":\"created\"}",
      "timestamp": "2025-03-17T06:15:24.123Z",
      "duration": 667
    }
  }
]
```

### Analyzing a Specific Request

1. Capture requests as described above
2. Get the ID of the request you want to analyze
3. Use `devinApi.analyze(id)` to get detailed information about the request

```javascript
devinApi.analyze("16798765432123abc");

// Example output
{
  "request": {
    "id": "16798765432123abc",
    "url": "https://api.devin.ai/v1/sessions",
    "method": "POST",
    "timestamp": "2025-03-17T06:15:23.456Z",
    "body": "{\"prompt\":\"Create a React app\"}"
  },
  "response": {
    "status": 200,
    "statusText": "OK",
    "timestamp": "2025-03-17T06:15:24.123Z",
    "duration": 667,
    "body": "{\"session_id\":\"session-123456\",\"status\":\"created\"}"
  },
  "endpoint": "Session Creation",
  "timing": {
    "duration": 667,
    "requestTime": "2025-03-17T06:15:23.456Z",
    "responseTime": "2025-03-17T06:15:24.123Z"
  }
}
```

## Session Monitoring

### Tracking Session Creation and Messages

1. Open the Chrome Developer Console (F12 or Ctrl+Shift+I)
2. Copy and paste the content of `console_scripts/session_monitor.js` into the Console tab
3. Press Enter to execute the script
4. Create a new Devin session and send messages
5. View captured sessions with `devinSession.getSessions()`

```javascript
// Example output
{
  "session-123456": {
    "id": "session-123456",
    "status": "running",
    "created_at": "2025-03-17T06:15:24.123Z",
    "messages": [
      {
        "session_id": "session-123456",
        "direction": "outgoing",
        "content": "Add a login page",
        "timestamp": "2025-03-17T06:20:15.789Z",
        "request_data": {
          "message": "Add a login page"
        }
      }
    ],
    "details": {
      "session_id": "session-123456",
      "status": "running",
      "created_at": "2025-03-17T06:15:24.123Z",
      "prompt": "Create a React app"
    }
  }
}
```

### Viewing Messages for a Specific Session

```javascript
devinSession.getSessionMessages("session-123456");

// Example output
[
  {
    "session_id": "session-123456",
    "direction": "outgoing",
    "content": "Add a login page",
    "timestamp": "2025-03-17T06:20:15.789Z",
    "request_data": {
      "message": "Add a login page"
    }
  }
]
```

## Authentication Monitoring

### Tracking Authentication Events

1. Open the Chrome Developer Console (F12 or Ctrl+Shift+I)
2. Copy and paste the content of `console_scripts/auth_monitor.js` into the Console tab
3. Press Enter to execute the script
4. Interact with Devin to generate authentication events
5. View captured events with `devinAuth.getEvents()`

```javascript
// Example output
[
  {
    "type": "request_header",
    "method": "POST",
    "url": "https://api.devin.ai/v1/sessions",
    "header": "Authorization",
    "value": "Bearer abcd...wxyz",
    "timestamp": "2025-03-17T06:15:23.456Z"
  },
  {
    "type": "storage_set",
    "storage": "localStorage",
    "key": "devin_token",
    "value": "abcd...wxyz",
    "timestamp": "2025-03-17T06:15:22.123Z"
  }
]
```

### Analyzing Authentication Patterns

```javascript
devinAuth.analyze();

// Example output
{
  "eventTypes": {
    "request_header": 5,
    "storage_set": 1,
    "storage_get": 3
  },
  "storageKeys": {
    "devin_token": {
      "count": 4,
      "storage": "localStorage"
    }
  },
  "headerPatterns": {
    "/v1/sessions": {
      "count": 1,
      "methods": {
        "POST": 1
      }
    },
    "/v1/session/session-123456": {
      "count": 3,
      "methods": {
        "GET": 2,
        "POST": 1
      }
    }
  },
  "totalEvents": 9
}
```

## Combined Monitoring

### Using the Combined Monitor

1. Open the Chrome Developer Console (F12 or Ctrl+Shift+I)
2. Copy and paste the content of `console_scripts/combined_monitor.js` into the Console tab
3. Press Enter to execute the script
4. Interact with Devin to generate API requests, authentication events, and sessions
5. Use the various commands to analyze the captured data

```javascript
// Get all requests
devin.getRequests();

// Get all sessions
devin.getSessions();

// Get all messages
devin.getMessages();

// Get all authentication events
devin.getAuthEvents();

// Analyze a specific request
devin.analyze("16798765432123abc");

// Summarize all requests
devin.summarize();

// Export all data
devin.export();
```

## Exporting Data for Further Analysis

All monitoring scripts provide an export function that saves the captured data as a JSON file:

```javascript
// Export API requests
devinApi.export();

// Export authentication events
devinAuth.export();

// Export sessions and messages
devinSession.export();

// Export all data (combined monitor)
devin.export();
```

The exported JSON files can be imported into other tools for further analysis.
