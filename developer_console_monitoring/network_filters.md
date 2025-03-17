# Network Filters for Devin API Monitoring

This document provides guidance on setting up network filters in the Chrome Developer Console to effectively monitor Devin API interactions.

## Basic Filtering

### Domain Filtering

To focus only on Devin API requests, enter the following in the filter box:

```
domain:api.devin.ai
```

This will show only requests to the Devin API domain.

### Multiple Domain Filtering

To include both the API and the web application:

```
domain:api.devin.ai OR domain:app.devin.ai
```

### Method Filtering

To filter by HTTP method:

```
method:POST domain:api.devin.ai
```

This will show only POST requests to the Devin API.

## Advanced Filtering

### Endpoint Filtering

To filter by specific endpoints:

```
url:sessions domain:api.devin.ai
```

This will show only requests to the sessions endpoint.

### Combined Filters

To create more complex filters:

```
(url:sessions OR url:message) AND method:POST domain:api.devin.ai
```

This will show only POST requests to the sessions or message endpoints.

## Setting Up Persistent Logging

1. Open the Network tab in Chrome Developer Tools
2. Check the "Preserve log" checkbox
3. Check the "Disable cache" checkbox
4. Apply your desired filters

This will ensure that all matching requests are captured and preserved, even when navigating between pages.

## Custom Filter Presets

### Session Creation Filter

```
url:sessions method:POST domain:api.devin.ai
```

### Message Sending Filter

```
url:message method:POST domain:api.devin.ai
```

### File Upload Filter

```
url:attachments method:POST domain:api.devin.ai
```

### Session Details Filter

```
url:session/ method:GET domain:api.devin.ai
```

## Saving and Exporting Captured Requests

To save captured requests for later analysis:

1. Right-click on any request in the Network tab
2. Select "Save all as HAR with content"
3. Save the file to your computer

This will create a HAR file containing all captured requests and responses, which can be analyzed using various tools or imported into the Chrome Developer Tools of another browser.

## Filtering HAR Files

To filter a HAR file after importing it:

1. Import the HAR file into Chrome Developer Tools
2. Apply the filters described above
3. Right-click and select "Save all as HAR with content" to create a filtered HAR file

## Recommended Workflow

1. Apply the domain filter `domain:api.devin.ai`
2. Enable "Preserve log" and "Disable cache"
3. Start interacting with Devin
4. Use additional filters to focus on specific types of requests
5. Save the captured requests as a HAR file for later analysis
