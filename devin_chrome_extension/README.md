# Devin API Monitor Chrome Extension

## Overview

The Devin API Monitor is a Chrome extension designed to monitor and analyze interactions between applications and the Devin API. It provides detailed insights into API requests and responses, helping developers understand how Devin operates and integrates with applications.

## Features

- **API Request Monitoring**: Captures all requests to the Devin API
- **Request/Response Analysis**: Displays detailed information about requests and responses
- **DevTools Integration**: Adds a panel to Chrome DevTools for in-depth analysis
- **Filtering Capabilities**: Filter requests by endpoint type and HTTP method
- **Export Functionality**: Export captured requests for further analysis
- **Real-time Statistics**: View statistics about API usage

## Installation

### Development Installation

1. Clone this repository
2. Open Chrome and navigate to `chrome://extensions/`
3. Enable "Developer mode" in the top-right corner
4. Click "Load unpacked" and select the `devin_chrome_extension` directory
5. The extension should now be installed and active

## Usage

### Popup Interface

Click the extension icon in the Chrome toolbar to open the popup interface, which provides:

- Monitoring status
- Request statistics
- Quick actions (open DevTools panel, clear data, export data)

### DevTools Panel

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

## API Endpoints Monitored

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/sessions` | POST | Create a new Devin session |
| `/sessions` | GET | List all Devin sessions |
| `/session/{session_id}` | GET | Get details of a specific session |
| `/session/{session_id}/message` | POST | Send a message to a session |
| `/secrets` | GET | List all secrets |
| `/secrets/{secret_id}` | DELETE | Delete a secret |
| `/attachments` | POST | Upload a file |

## Architecture

The extension consists of the following components:

- **Background Script**: Intercepts and logs API requests
- **Content Script**: Injects code to monitor XHR and fetch requests
- **DevTools Panel**: Provides a UI for analyzing requests
- **Popup**: Provides quick access to statistics and actions

## Development

### Project Structure

```
devin_chrome_extension/
├── css/
│   ├── panel.css
│   └── popup.css
├── images/
│   ├── icon16.png
│   ├── icon48.png
│   └── icon128.png
├── js/
│   ├── background.js
│   ├── content.js
│   ├── devtools.js
│   ├── panel.js
│   └── popup.js
├── panel.html
├── popup.html
└── manifest.json
```

### Key Files

- `manifest.json`: Extension configuration
- `background.js`: Intercepts API requests
- `content.js`: Injects code to monitor XHR and fetch requests
- `devtools.js`: Creates the DevTools panel
- `panel.js`: Handles the DevTools panel UI
- `popup.js`: Handles the popup UI

## License

This project is licensed under the MIT License.
