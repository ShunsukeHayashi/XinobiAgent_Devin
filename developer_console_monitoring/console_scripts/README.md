# Devin API Console Scripts

This directory contains JavaScript scripts for monitoring Devin API interactions in the Chrome Developer Console.

## Available Scripts

- **api_monitor.js**: Monitors API requests and responses
- **auth_monitor.js**: Monitors authentication-related events
- **session_monitor.js**: Monitors session creation and message sending
- **combined_monitor.js**: Combines all monitoring functionality into a single script

## Usage

1. Open the Chrome Developer Console (F12 or Ctrl+Shift+I)
2. Copy and paste the entire content of one of the scripts into the Console tab
3. Press Enter to execute the script
4. Use the provided commands to interact with the monitor

## Available Commands

### API Monitor

```javascript
devinApi.help()           // Show help
devinApi.getRequests()    // Get all captured requests
devinApi.getRequest(id)   // Get a specific request by ID
devinApi.clear()          // Clear all captured requests
devinApi.analyze(id)      // Analyze a specific request
devinApi.summarize()      // Summarize all captured requests
devinApi.export()         // Export all captured requests as JSON
```

### Auth Monitor

```javascript
devinAuth.help()          // Show help
devinAuth.getEvents()     // Get all captured auth events
devinAuth.clear()         // Clear all captured events
devinAuth.analyze()       // Analyze auth patterns
devinAuth.export()        // Export all captured events as JSON
```

### Session Monitor

```javascript
devinSession.help()       // Show help
devinSession.getSessions() // Get all captured sessions
devinSession.getSession(id) // Get a specific session by ID
devinSession.getCurrentSession() // Get the current session
devinSession.getMessages() // Get all captured messages
devinSession.getSessionMessages(id) // Get messages for a specific session
devinSession.clear()      // Clear all captured sessions and messages
devinSession.export()     // Export all captured sessions and messages as JSON
```

### Combined Monitor

```javascript
devin.help()              // Show help
devin.getRequests()       // Get all captured requests
devin.getSessions()       // Get all captured sessions
devin.getMessages()       // Get all captured messages
devin.getAuthEvents()     // Get all captured auth events
devin.analyze(id)         // Analyze a specific request
devin.summarize()         // Summarize all captured requests
devin.export()            // Export all captured data
```

## Security Considerations

- By default, authentication tokens are masked to prevent accidental exposure
- To capture tokens (not recommended), set `config.captureTokens = true`
- Response bodies are captured by default, but this can be disabled by setting `config.captureResponses = false`
