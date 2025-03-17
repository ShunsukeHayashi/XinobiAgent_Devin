# Developer Console Usage Guide for Devin API Monitoring

## Overview

This guide explains how to use the Developer Console scripts for monitoring Devin API interactions. These scripts provide on-demand monitoring without requiring extension installation.

## Loading the Scripts

1. **Open Developer Console**:
   - Right-click on any page and select "Inspect" or press F12
   - Navigate to the "Console" tab

2. **Load API Monitor**:
   ```javascript
   fetch('https://raw.githubusercontent.com/ShunsukeHayashi/XinobiAgent_Devin/master/developer_console_monitoring/console_scripts/api_monitor.js')
     .then(response => response.text())
     .then(script => eval(script));
   ```

3. **Load Auth Monitor**:
   ```javascript
   fetch('https://raw.githubusercontent.com/ShunsukeHayashi/XinobiAgent_Devin/master/developer_console_monitoring/console_scripts/auth_monitor.js')
     .then(response => response.text())
     .then(script => eval(script));
   ```

4. **Load Session Monitor**:
   ```javascript
   fetch('https://raw.githubusercontent.com/ShunsukeHayashi/XinobiAgent_Devin/master/developer_console_monitoring/console_scripts/session_monitor.js')
     .then(response => response.text())
     .then(script => eval(script));
   ```

5. **Load Combined Monitor**:
   ```javascript
   fetch('https://raw.githubusercontent.com/ShunsukeHayashi/XinobiAgent_Devin/master/developer_console_monitoring/console_scripts/combined_monitor.js')
     .then(response => response.text())
     .then(script => eval(script));
   ```

## Configuration

1. **API Monitor Configuration**:
   ```javascript
   devinApi.config = {
       apiDomain: 'api.devin.ai',
       logLevel: 'info',
       captureResponses: true,
       maxStoredRequests: 100
   };
   ```

2. **Auth Monitor Configuration**:
   ```javascript
   devinAuth.config = {
       logLevel: 'info',
       captureTokens: false,
       maxStoredEvents: 100
   };
   ```

3. **Session Monitor Configuration**:
   ```javascript
   devinSession.config = {
       apiDomain: 'api.devin.ai',
       logLevel: 'info',
       maxStoredSessions: 20
   };
   ```

4. **Combined Monitor Configuration**:
   ```javascript
   devin.config = {
       apiDomain: 'api.devin.ai',
       logLevel: 'info',
       captureResponses: true,
       captureTokens: false,
       maxStoredRequests: 100,
       maxStoredEvents: 100,
       maxStoredSessions: 20
   };
   ```

## Using the Monitors

1. **Capture API Requests**:
   - Interact with Devin on the page
   - The monitors will automatically capture API requests

2. **View Captured Requests**:
   ```javascript
   // API Monitor
   const requests = devinApi.getRequests();
   console.table(requests);

   // Auth Monitor
   const events = devinAuth.getEvents();
   console.table(events);

   // Session Monitor
   const sessions = devinSession.getSessions();
   console.table(sessions);
   ```

3. **Generate Summaries**:
   ```javascript
   // API Monitor
   const apiSummary = devinApi.summarize();
   console.log(apiSummary);

   // Auth Monitor
   const authSummary = devinAuth.summarize();
   console.log(authSummary);

   // Session Monitor
   const sessionSummary = devinSession.summarize();
   console.log(sessionSummary);

   // Combined Monitor
   const summary = devin.summarize();
   console.log(summary);
   ```

4. **Export Data**:
   ```javascript
   // API Monitor
   const apiData = devinApi.export();
   console.log(JSON.stringify(apiData, null, 2));

   // Auth Monitor
   const authData = devinAuth.export();
   console.log(JSON.stringify(authData, null, 2));

   // Session Monitor
   const sessionData = devinSession.export();
   console.log(JSON.stringify(sessionData, null, 2));

   // Combined Monitor
   const data = devin.export();
   console.log(JSON.stringify(data, null, 2));
   ```

## Analyzing Data

1. **Request Patterns**:
   ```javascript
   // Get request frequency
   const frequency = devinApi.getRequestFrequency();
   console.table(frequency);

   // Get request types
   const types = devinApi.getRequestTypes();
   console.table(types);
   ```

2. **Authentication Analysis**:
   ```javascript
   // Get token usage
   const tokenUsage = devinAuth.getTokenUsage();
   console.table(tokenUsage);
   ```

3. **Session Analysis**:
   ```javascript
   // Get session lifecycle
   const lifecycle = devinSession.getSessionLifecycle('session-id');
   console.table(lifecycle);

   // Get message exchanges
   const messages = devinSession.getSessionMessages('session-id');
   console.table(messages);
   ```

## Advanced Usage

### Custom Filtering

You can apply custom filters to the captured data:

```javascript
// Filter requests by endpoint
const sessionRequests = devinApi.getRequests().filter(req => 
  req.url.includes('/session')
);
console.table(sessionRequests);

// Filter requests by method
const postRequests = devinApi.getRequests().filter(req => 
  req.method === 'POST'
);
console.table(postRequests);

// Filter requests by status code
const errorRequests = devinApi.getRequests().filter(req => 
  req.response && req.response.status >= 400
);
console.table(errorRequests);
```

### Custom Analysis

You can perform custom analysis on the captured data:

```javascript
// Analyze response times
const responseTimes = devinApi.getRequests().map(req => ({
  url: req.url,
  method: req.method,
  responseTime: req.responseTime
}));
console.table(responseTimes);

// Analyze request payload sizes
const payloadSizes = devinApi.getRequests().map(req => ({
  url: req.url,
  method: req.method,
  payloadSize: req.body ? JSON.stringify(req.body).length : 0
}));
console.table(payloadSizes);
```

### Real-time Monitoring

You can set up real-time monitoring with callbacks:

```javascript
// Set up request callback
devinApi.onRequest = (request) => {
  console.log(`New request to ${request.url}`);
};

// Set up response callback
devinApi.onResponse = (response) => {
  console.log(`Response from ${response.url}: ${response.status}`);
};

// Set up auth event callback
devinAuth.onEvent = (event) => {
  console.log(`Auth event: ${event.type}`);
};

// Set up session event callback
devinSession.onSessionUpdate = (session) => {
  console.log(`Session updated: ${session.id}`);
};
```

## Integration with Other Tools

### Export to File

You can export the captured data to a file:

```javascript
// Export to JSON file
const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(
  JSON.stringify(devin.export(), null, 2)
);
const downloadAnchorNode = document.createElement('a');
downloadAnchorNode.setAttribute("href", dataStr);
downloadAnchorNode.setAttribute("download", "devin_api_data.json");
document.body.appendChild(downloadAnchorNode);
downloadAnchorNode.click();
downloadAnchorNode.remove();
```

### Integration with Chrome Extension

You can integrate the Developer Console scripts with the Chrome extension:

```javascript
// Send data to Chrome extension
window.postMessage({
  type: 'DEVIN_API_DATA',
  data: devin.export()
}, '*');
```

## Security Considerations

1. **Token Masking**:
   - Bearer tokens are masked by default
   - Do not enable token capture in production environments
   - If you need to capture tokens for debugging, use a test account

2. **Data Handling**:
   - Exported data may contain sensitive information
   - Handle exported data securely
   - Clear sensitive data when no longer needed
   - Do not share exported data with unauthorized parties

3. **Script Execution**:
   - Be cautious when loading scripts from external sources
   - Review script content before execution
   - Use local copies of scripts when possible
   - Only load scripts from trusted sources

## Troubleshooting

1. **Scripts not loading**:
   - Check console for errors
   - Verify the script URLs
   - Try loading scripts from local copies

2. **No data captured**:
   - Verify you're on a page that interacts with Devin API
   - Check the API domain configuration
   - Ensure the scripts are loaded before interacting with Devin

3. **Configuration not applied**:
   - Ensure you set the configuration after loading the scripts
   - Check console for configuration errors
   - Verify the configuration object structure

## Conclusion

The Developer Console scripts provide a powerful and flexible way to monitor Devin API interactions without requiring extension installation. By loading these scripts in the Developer Console, you can capture and analyze API requests, authentication events, and session management in real-time.

The scripts offer comprehensive configuration options, data export capabilities, and advanced analysis features, making them suitable for a wide range of monitoring scenarios, from API integration development to debugging and performance analysis.
