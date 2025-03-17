# Step-by-Step Guide for Monitoring Devin API Interactions

This guide provides detailed instructions for setting up and using the Chrome Developer Console to monitor Devin API interactions.

## Prerequisites

- Google Chrome browser
- Access to the Devin application (https://app.devin.ai)
- Basic understanding of HTTP requests and responses

## Setup Steps

### 1. Open the Devin Application

1. Navigate to https://app.devin.ai in Chrome
2. Log in to your Devin account

### 2. Open the Developer Console

1. Press F12 or Ctrl+Shift+I to open the Developer Tools
2. Navigate to the Network tab
3. Check the "Preserve log" checkbox
4. Check the "Disable cache" checkbox

### 3. Apply Network Filters

1. Enter `domain:api.devin.ai` in the filter box
2. This will show only requests to the Devin API

### 4. Set Up Console Monitoring

1. Navigate to the Console tab
2. Copy and paste the monitoring script from `console_scripts/api_monitor.js`
3. Press Enter to execute the script
4. You should see a message confirming that the monitor is active

### 5. Start Capturing Interactions

1. Return to the Devin application
2. Start interacting with Devin (create a session, send messages, etc.)
3. Switch back to the Network tab to see the captured requests
4. Switch to the Console tab to see the analyzed requests

## Monitoring Specific Interactions

### Session Creation

1. Apply the filter `url:sessions method:POST domain:api.devin.ai`
2. Create a new session in Devin
3. Observe the request and response

### Message Sending

1. Apply the filter `url:message method:POST domain:api.devin.ai`
2. Send a message in an existing Devin session
3. Observe the request and response

### File Upload

1. Apply the filter `url:attachments method:POST domain:api.devin.ai`
2. Upload a file in Devin
3. Observe the request and response

## Analyzing Captured Data

### Request Analysis

1. Click on a request in the Network tab
2. Navigate to the Headers tab to see request headers
3. Navigate to the Payload tab to see the request body
4. Navigate to the Preview tab to see a formatted version of the response

### Response Analysis

1. Click on a request in the Network tab
2. Navigate to the Response tab to see the raw response
3. Navigate to the Preview tab to see a formatted version of the response

### Using Console Commands

1. Navigate to the Console tab
2. Use the `devinApi.analyze(requestId)` command to analyze a specific request
3. Use the `devinApi.summarize()` command to see a summary of all captured requests

## Exporting Data for Further Analysis

### Exporting as HAR

1. Right-click on any request in the Network tab
2. Select "Save all as HAR with content"
3. Save the file to your computer

### Exporting Console Data

1. Navigate to the Console tab
2. Right-click in the console
3. Select "Save as..." to save the console output

## Troubleshooting

### No Requests Showing

1. Make sure you're on the Devin application
2. Check that the filter is correctly set to `domain:api.devin.ai`
3. Try refreshing the page and checking "Preserve log"

### Console Script Errors

1. Make sure you've copied the entire script
2. Check for any error messages in the console
3. Try refreshing the page and running the script again

## Next Steps

After capturing and analyzing Devin API interactions, you can:

1. Document the API endpoints and their parameters
2. Analyze the request and response formats
3. Identify patterns in the API usage
4. Create custom scripts for more detailed analysis
