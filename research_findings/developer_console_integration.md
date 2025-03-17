# Developer Console Integration for Devin API Monitoring

## Overview

This document outlines the approach for integrating the Devin API Monitor Chrome extension with the Chrome Developer Console. The integration provides developers with powerful tools for analyzing Devin API interactions directly from the console.

## Console Commands

The extension adds the following commands to the Chrome Developer Console:

| Command | Description |
|---------|-------------|
| `devin.help()` | Show help for Devin API Monitor commands |
| `devin.requests([filter])` | Show captured API requests, optionally filtered |
| `devin.sessions()` | Show session creation requests |
| `devin.messages()` | Show message sending requests |
| `devin.clear()` | Clear captured requests |
| `devin.analyze(requestId)` | Analyze a specific request |

## Integration Components

### 1. Console Integration Script

The `console_integration.js` script provides the core functionality for integrating with the Developer Console:

```javascript
// Register console commands
registerCommands() {
  // Register devin.help command
  this.registerCommand('devin.help', this.helpCommand, 'Show help for Devin API Monitor commands');
  
  // Register devin.requests command
  this.registerCommand('devin.requests', this.requestsCommand, 'Show captured API requests');
  
  // Register devin.sessions command
  this.registerCommand('devin.sessions', this.sessionsCommand, 'Show session creation requests');
  
  // Register devin.messages command
  this.registerCommand('devin.messages', this.messagesCommand, 'Show message sending requests');
  
  // Register devin.clear command
  this.registerCommand('devin.clear', this.clearCommand, 'Clear captured requests');
  
  // Register devin.analyze command
  this.registerCommand('devin.analyze', this.analyzeCommand, 'Analyze a specific request');
}
```

### 2. Console Monitor Script

The `console_monitor.js` script provides utilities for monitoring console output:

```javascript
// Process a log
processLog(type, args) {
  // Check if the log contains the filter
  const logString = args.map(arg => {
    if (typeof arg === 'object') {
      try {
        return JSON.stringify(arg);
      } catch (e) {
        return String(arg);
      }
    }
    return String(arg);
  }).join(' ');
  
  // Only process logs that contain the filter
  if (this.filter && !logString.toLowerCase().includes(this.filter.toLowerCase())) {
    return;
  }
  
  // Create log object
  const log = {
    type: type,
    args: args,
    timestamp: new Date().toISOString()
  };
  
  // Store the log
  this.logs.push(log);
  
  // Notify listeners
  this.notifyListeners('newLog', log);
}
```

### 3. DevTools Panel Integration

The DevTools panel provides a visual interface for analyzing API requests:

```javascript
// Create a sidebar pane for Devin API analysis
chrome.devtools.panels.elements.createSidebarPane(
  "Devin API",
  function(sidebar) {
    // Set sidebar content
    sidebar.setObject({ 
      title: "Devin API Monitor",
      description: "Select a network request to view details"
    });
    
    // Update sidebar when a network request is selected
    chrome.devtools.network.onRequestFinished.addListener(function(request) {
      if (request.request.url.includes('api.devin.ai')) {
        sidebar.setObject({
          title: "Devin API Request",
          url: request.request.url,
          method: request.request.method,
          status: request.response.status
        });
      }
    });
  }
);
```

## Usage Examples

### Viewing All Requests

```javascript
// Show all captured requests
devin.requests();

// Show requests containing 'session'
devin.requests('session');
```

### Analyzing Session Creation

```javascript
// Show session creation requests
devin.sessions();

// Analyze a specific session creation request
devin.analyze('request-123456');
```

### Monitoring Message Sending

```javascript
// Show message sending requests
devin.messages();

// Clear all captured requests
devin.clear();
```

## Implementation Considerations

### Performance

1. **Efficient Command Execution**:
   - Commands are designed to be lightweight
   - Results are formatted for readability
   - Large datasets are paginated

2. **Minimal Console Pollution**:
   - Commands are namespaced under `devin.*`
   - Only relevant information is logged
   - Clear formatting for easy reading

### User Experience

1. **Intuitive Commands**:
   - Simple, descriptive command names
   - Consistent parameter patterns
   - Helpful error messages

2. **Rich Output**:
   - Formatted tables for lists
   - Structured objects for details
   - Color-coded status indicators

## Testing

The extension includes a test page (`test.html`) that allows developers to:

1. Mock Devin API requests
2. Test console commands
3. Verify integration functionality

```javascript
// Mock a request
function mockRequest(method, url, requestBody, responseBody, statusCode) {
  // Create request ID
  const requestId = Date.now().toString() + Math.random().toString(36).substring(2, 15);
  
  // Create request event
  const requestEvent = new CustomEvent('devinApiRequest', {
    detail: {
      method: method,
      url: url,
      requestBody: requestBody ? JSON.stringify(requestBody) : null,
      timestamp: new Date().toISOString()
    }
  });
  
  // Create response event
  const responseEvent = new CustomEvent('devinApiRequest', {
    detail: {
      method: method,
      url: url,
      responseBody: responseBody ? JSON.stringify(responseBody) : null,
      status: statusCode,
      timestamp: new Date(Date.now() + 500).toISOString()
    }
  });
  
  // Dispatch events
  document.dispatchEvent(requestEvent);
  setTimeout(() => document.dispatchEvent(responseEvent), 500);
}
```

## Conclusion

The Developer Console integration provides a powerful interface for analyzing Devin API interactions. By combining the visual interface of the DevTools panel with the flexibility of console commands, developers can gain deep insights into how Devin operates.
