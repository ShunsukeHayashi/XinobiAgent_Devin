# Devin API Monitor Chrome Extension Installation Guide

This guide will walk you through the process of installing and using the Devin API Monitor Chrome extension for analyzing Devin API interactions.

## Installation Steps

### 1. Download the Extension

First, you need to download the extension files:

```bash
git clone https://github.com/ShunsukeHayashi/XinobiAgent_Devin.git
cd XinobiAgent_Devin
```

### 2. Load the Extension in Chrome

1. Open Google Chrome
2. Navigate to `chrome://extensions/`
3. Enable "Developer mode" by toggling the switch in the top-right corner
4. Click "Load unpacked"
5. Select the `devin_chrome_extension` directory from the cloned repository
6. The extension should now be installed and visible in your extensions list

### 3. Verify Installation

1. Look for the Devin API Monitor icon in your Chrome toolbar
2. Click the icon to open the popup interface
3. You should see the monitoring status and statistics

## Using the Extension

### Monitoring API Interactions

1. Navigate to the Devin application at `https://app.devin.ai/`
2. The extension will automatically start monitoring API interactions
3. You can view captured requests in the popup or DevTools panel

### Using the DevTools Panel

1. Open Chrome DevTools (F12 or Ctrl+Shift+I)
2. Navigate to the "Devin API" panel
3. View and analyze captured API requests

### Filtering Requests

Use the filters in the sidebar of the DevTools panel to filter requests by:

- Endpoint type (sessions, session details, messages, secrets, attachments)
- HTTP method (GET, POST, DELETE)

### Analyzing Requests

Click on a request in the list to view:

- Request details (URL, method, headers, body)
- Response details (status, headers, body)
- Analysis of the request/response

### Exporting Data

Click the "Export" button in the DevTools panel or popup to export captured requests as a JSON file.

## Troubleshooting

### Extension Not Capturing Requests

If the extension is not capturing API requests:

1. Make sure you're on the Devin application (`https://app.devin.ai/`)
2. Refresh the page to ensure the content script is injected
3. Check that the extension has the necessary permissions

### DevTools Panel Not Showing

If the Devin API panel is not showing in DevTools:

1. Close and reopen DevTools
2. Make sure the extension is enabled
3. Try reloading the extension from the extensions page

## Additional Resources

- [README.md](README.md) - General information about the extension
- [research_findings/](../research_findings/) - Documentation and analysis of the Devin API
