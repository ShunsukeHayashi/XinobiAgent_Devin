# Chrome Extension Usage Guide for Devin API Monitoring

## Overview

This guide explains how to use the Chrome extension for monitoring Devin API interactions. The extension provides a user-friendly interface for capturing and analyzing API requests, authentication events, and session management.

## Installation

1. **Load the extension**:
   - Open Chrome and navigate to `chrome://extensions/`
   - Enable "Developer mode" in the top-right corner
   - Click "Load unpacked" and select the `devin_chrome_extension` directory

2. **Verify installation**:
   - The Devin API Monitor icon should appear in your Chrome toolbar
   - Click the icon to open the popup interface

## Using the DevTools Panel

1. **Open DevTools**:
   - Right-click on any page and select "Inspect" or press F12
   - Navigate to the "Devin API Monitor" panel

2. **Monitor API requests**:
   - The panel displays all API requests to `api.devin.ai`
   - Click on a request to view details
   - Use the filters to focus on specific request types

3. **Analyze authentication**:
   - The "Auth" tab shows authentication events
   - Bearer tokens are masked for security

4. **Track sessions**:
   - The "Sessions" tab displays session creation and updates
   - Click on a session to view message exchanges

## Using the Popup Interface

1. **Quick access**:
   - Click the Devin API Monitor icon in the toolbar
   - View a summary of recent API activity
   - Access configuration options

2. **Configure monitoring**:
   - Set the API domain to monitor
   - Configure logging level
   - Enable/disable response capture

## Exporting Data

1. **Export as JSON**:
   - Click the "Export" button in the DevTools panel
   - Choose a location to save the JSON file
   - The file contains all captured data

2. **Generate summary**:
   - Click the "Summary" button in the DevTools panel
   - View a summary of API interactions
   - Copy the summary to clipboard

## Advanced Features

### Network Request Filtering

The extension provides advanced filtering options for network requests:

1. **Domain filtering**:
   - Filter requests by domain (e.g., `api.devin.ai`)
   - Include or exclude specific subdomains

2. **Endpoint filtering**:
   - Filter requests by endpoint (e.g., `/sessions`, `/attachments`)
   - Group related endpoints for analysis

3. **Method filtering**:
   - Filter requests by HTTP method (GET, POST, DELETE)
   - Analyze patterns for specific operations

### Authentication Analysis

The extension provides detailed authentication analysis:

1. **Token usage tracking**:
   - Track when and how tokens are used
   - Monitor token expiration and refresh

2. **Authentication flow visualization**:
   - Visualize the complete authentication flow
   - Identify potential security issues

### Session Management

The extension provides comprehensive session management features:

1. **Session lifecycle tracking**:
   - Track session creation, updates, and termination
   - Analyze session duration and activity

2. **Message exchange visualization**:
   - Visualize message exchanges within sessions
   - Analyze conversation patterns

## Integration with Developer Console

The extension can be integrated with the Developer Console for advanced analysis:

1. **Console logging**:
   - Enable console logging for detailed analysis
   - Access captured data through console variables

2. **Custom analysis scripts**:
   - Write custom scripts to analyze captured data
   - Integrate with other analysis tools

## Troubleshooting

1. **Extension not working**:
   - Ensure the extension is enabled
   - Reload the page you're monitoring
   - Check the console for errors

2. **No data captured**:
   - Verify you're on a page that interacts with Devin API
   - Check the API domain configuration
   - Reload the extension

3. **Performance issues**:
   - Reduce the amount of data captured
   - Clear stored data regularly
   - Disable response capture for large responses

## Security Considerations

1. **Token masking**:
   - Bearer tokens are masked by default
   - Do not enable token capture in production environments

2. **Data handling**:
   - Exported data may contain sensitive information
   - Handle exported data securely
   - Clear stored data when no longer needed

3. **Permission management**:
   - The extension requires network request permissions
   - Review permissions before installation
   - Disable the extension when not in use

## Example Use Cases

### API Integration Development

When developing integrations with the Devin API:

1. Capture API requests and responses to understand the API structure
2. Analyze authentication flow to implement proper authentication
3. Monitor session management to implement session handling
4. Export data for documentation and testing

### API Monitoring

When monitoring the Devin API in production:

1. Track API usage patterns
2. Monitor authentication events
3. Analyze session lifecycle
4. Identify potential issues

### Debugging

When debugging issues with Devin API integration:

1. Capture API requests and responses
2. Analyze error responses
3. Monitor authentication flow
4. Track session state changes

## Conclusion

The Chrome extension provides a powerful tool for monitoring and analyzing Devin API interactions. By capturing API requests, authentication events, and session management, it enables detailed analysis of the API's behavior and integration patterns.

The extension's user-friendly interface and advanced features make it suitable for a wide range of use cases, from API integration development to production monitoring and debugging.
