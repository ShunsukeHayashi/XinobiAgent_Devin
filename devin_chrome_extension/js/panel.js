/**
 * Panel script for the Devin API Monitor extension.
 * 
 * This script handles the DevTools panel UI and functionality.
 */

// Store requests and responses
let requests = [];
let selectedRequestId = null;

// DOM elements
const requestListEl = document.getElementById('requestList');
const clearBtn = document.getElementById('clearBtn');
const exportBtn = document.getElementById('exportBtn');
const tabBtns = document.querySelectorAll('.tab-btn');
const tabPanes = document.querySelectorAll('.tab-pane');
const filterEndpointCheckboxes = document.querySelectorAll('.filter-endpoint');
const filterMethodCheckboxes = document.querySelectorAll('.filter-method');

// Request detail elements
const requestUrlEl = document.querySelector('.request-url');
const requestMethodEl = document.querySelector('.request-method');
const requestTimestampEl = document.querySelector('.request-timestamp');
const requestBodyEl = document.querySelector('.request-body');
const responseStatusEl = document.querySelector('.response-status');
const responseTimestampEl = document.querySelector('.response-timestamp');
const responseBodyEl = document.querySelector('.response-body');
const requestHeadersEl = document.querySelector('.request-headers');
const responseHeadersEl = document.querySelector('.response-headers');
const endpointInfoEl = document.querySelector('.endpoint-info');
const sessionInfoEl = document.querySelector('.session-info');
const timingInfoEl = document.querySelector('.timing-info');

// Initialize the panel
function initPanel() {
  // Load existing requests
  chrome.runtime.sendMessage({ action: 'getRequests' }, function(response) {
    if (response && response.requests) {
      requests = response.requests;
      updateRequestList();
    }
  });
  
  // Set up event listeners
  clearBtn.addEventListener('click', clearRequests);
  exportBtn.addEventListener('click', exportRequests);
  
  // Tab switching
  tabBtns.forEach(btn => {
    btn.addEventListener('click', function() {
      // Remove active class from all buttons
      tabBtns.forEach(b => b.classList.remove('active'));
      // Add active class to clicked button
      this.classList.add('active');
      
      // Hide all tab panes
      tabPanes.forEach(pane => pane.classList.remove('active'));
      // Show the selected tab pane
      const tabId = this.getAttribute('data-tab');
      document.getElementById(`${tabId}Tab`).classList.add('active');
    });
  });
  
  // Filter change events
  filterEndpointCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', updateRequestList);
  });
  
  filterMethodCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', updateRequestList);
  });
  
  // Listen for new requests
  chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === 'newRequest' || message.action === 'newResponse') {
      // Add the request or response to the list
      if (message.action === 'newRequest') {
        requests.push(message.request);
      } else {
        requests.push(message.response);
      }
      
      // Update the UI
      updateRequestList();
    } else if (message.action === 'networkRequest') {
      // Add the network request to the list
      const requestId = Date.now().toString();
      
      // Add request
      requests.push({
        id: requestId,
        url: message.request.url,
        method: message.request.method,
        headers: message.request.headers,
        body: message.request.body,
        timestamp: message.request.timestamp,
        type: 'request'
      });
      
      // Add response
      requests.push({
        id: requestId,
        url: message.request.url,
        method: message.request.method,
        statusCode: message.response.status,
        statusText: message.response.statusText,
        headers: message.response.headers,
        body: message.response.body,
        timestamp: message.response.timestamp,
        type: 'response'
      });
      
      // Update the UI
      updateRequestList();
    }
  });
}

// Update the request list
function updateRequestList() {
  // Clear the list
  requestListEl.innerHTML = '';
  
  // Get active filters
  const activeEndpoints = Array.from(filterEndpointCheckboxes)
    .filter(cb => cb.checked)
    .map(cb => cb.value);
  
  const activeMethods = Array.from(filterMethodCheckboxes)
    .filter(cb => cb.checked)
    .map(cb => cb.value);
  
  // Group requests by ID
  const requestGroups = {};
  
  requests.forEach(req => {
    if (!requestGroups[req.id]) {
      requestGroups[req.id] = {
        request: null,
        response: null
      };
    }
    
    if (req.type === 'request') {
      requestGroups[req.id].request = req;
    } else if (req.type === 'response') {
      requestGroups[req.id].response = req;
    }
  });
  
  // Create list items for each request group
  Object.keys(requestGroups).forEach(id => {
    const group = requestGroups[id];
    
    // Skip if no request
    if (!group.request) return;
    
    // Get request details
    const url = group.request.url;
    const method = group.request.method;
    
    // Categorize the request
    const category = categorizeRequest(url);
    
    // Skip if not in active filters
    if (!activeEndpoints.includes(category) || !activeMethods.includes(method)) {
      return;
    }
    
    // Create list item
    const listItem = document.createElement('div');
    listItem.className = 'list-item';
    listItem.setAttribute('data-id', id);
    
    // Add status indicator
    const statusIndicator = document.createElement('span');
    statusIndicator.className = 'status-indicator';
    
    if (group.response) {
      const statusCode = group.response.statusCode;
      if (statusCode >= 200 && statusCode < 300) {
        statusIndicator.className += ' success';
      } else if (statusCode >= 400) {
        statusIndicator.className += ' error';
      } else {
        statusIndicator.className += ' warning';
      }
    } else {
      statusIndicator.className += ' pending';
    }
    
    // Add method badge
    const methodBadge = document.createElement('span');
    methodBadge.className = `method-badge ${method.toLowerCase()}`;
    methodBadge.textContent = method;
    
    // Add endpoint
    const endpointEl = document.createElement('span');
    endpointEl.className = 'endpoint';
    endpointEl.textContent = extractEndpoint(url);
    
    // Add timestamp
    const timestampEl = document.createElement('span');
    timestampEl.className = 'timestamp';
    timestampEl.textContent = formatTimestamp(group.request.timestamp);
    
    // Add status code if available
    if (group.response) {
      const statusCodeEl = document.createElement('span');
      statusCodeEl.className = 'status-code';
      statusCodeEl.textContent = group.response.statusCode;
      listItem.appendChild(statusCodeEl);
    }
    
    // Assemble list item
    listItem.appendChild(statusIndicator);
    listItem.appendChild(methodBadge);
    listItem.appendChild(endpointEl);
    listItem.appendChild(timestampEl);
    
    // Add click handler
    listItem.addEventListener('click', function() {
      // Remove active class from all list items
      document.querySelectorAll('.list-item').forEach(item => {
        item.classList.remove('active');
      });
      
      // Add active class to clicked item
      this.classList.add('active');
      
      // Set selected request ID
      selectedRequestId = this.getAttribute('data-id');
      
      // Show request details
      showRequestDetails(selectedRequestId);
    });
    
    // Add to list
    requestListEl.appendChild(listItem);
  });
  
  // Select first item if none selected
  if (requestListEl.children.length > 0 && !selectedRequestId) {
    const firstItem = requestListEl.children[0];
    firstItem.classList.add('active');
    selectedRequestId = firstItem.getAttribute('data-id');
    showRequestDetails(selectedRequestId);
  }
}

// Show request details
function showRequestDetails(requestId) {
  // Find request and response
  const requestGroup = {};
  
  requests.forEach(req => {
    if (req.id === requestId) {
      if (req.type === 'request') {
        requestGroup.request = req;
      } else if (req.type === 'response') {
        requestGroup.response = req;
      }
    }
  });
  
  // Show request details
  if (requestGroup.request) {
    const req = requestGroup.request;
    
    requestUrlEl.textContent = req.url;
    requestMethodEl.textContent = req.method;
    requestTimestampEl.textContent = formatTimestamp(req.timestamp);
    
    // Format request body if available
    if (req.requestBody) {
      try {
        const bodyObj = JSON.parse(req.requestBody);
        requestBodyEl.textContent = JSON.stringify(bodyObj, null, 2);
      } catch (e) {
        requestBodyEl.textContent = req.requestBody;
      }
    } else {
      requestBodyEl.textContent = 'No request body';
    }
    
    // Format request headers if available
    if (req.headers) {
      requestHeadersEl.textContent = formatHeaders(req.headers);
    } else {
      requestHeadersEl.textContent = 'No request headers';
    }
  }
  
  // Show response details
  if (requestGroup.response) {
    const res = requestGroup.response;
    
    responseStatusEl.textContent = `${res.statusCode} ${res.statusText || ''}`;
    responseTimestampEl.textContent = formatTimestamp(res.timestamp);
    
    // Format response body if available
    if (res.body) {
      try {
        const bodyObj = JSON.parse(res.body);
        responseBodyEl.textContent = JSON.stringify(bodyObj, null, 2);
      } catch (e) {
        responseBodyEl.textContent = res.body;
      }
    } else {
      responseBodyEl.textContent = 'No response body';
    }
    
    // Format response headers if available
    if (res.headers) {
      responseHeadersEl.textContent = formatHeaders(res.headers);
    } else {
      responseHeadersEl.textContent = 'No response headers';
    }
  } else {
    responseStatusEl.textContent = 'No response';
    responseTimestampEl.textContent = '';
    responseBodyEl.textContent = 'No response body';
    responseHeadersEl.textContent = 'No response headers';
  }
  
  // Show analysis
  showAnalysis(requestGroup);
}

// Show analysis
function showAnalysis(requestGroup) {
  if (!requestGroup.request) return;
  
  const req = requestGroup.request;
  const res = requestGroup.response;
  
  // Endpoint info
  const endpoint = extractEndpoint(req.url);
  const category = categorizeRequest(req.url);
  
  let endpointInfo = `<h4>Endpoint: ${endpoint}</h4>`;
  endpointInfo += `<p>Category: ${category}</p>`;
  
  // Add endpoint-specific info
  if (category === 'sessions' && req.method === 'POST') {
    endpointInfo += `<p>Creating a new Devin session</p>`;
    
    // Extract prompt from request body
    if (req.requestBody) {
      try {
        const bodyObj = JSON.parse(req.requestBody);
        if (bodyObj.prompt) {
          endpointInfo += `<p>Prompt: ${bodyObj.prompt}</p>`;
        }
      } catch (e) {}
    }
  } else if (category === 'session') {
    const sessionId = extractSessionId(req.url);
    endpointInfo += `<p>Getting details for session: ${sessionId}</p>`;
  } else if (category === 'message') {
    const sessionId = extractSessionId(req.url);
    endpointInfo += `<p>Sending message to session: ${sessionId}</p>`;
    
    // Extract message from request body
    if (req.requestBody) {
      try {
        const bodyObj = JSON.parse(req.requestBody);
        if (bodyObj.message) {
          endpointInfo += `<p>Message: ${bodyObj.message}</p>`;
        }
      } catch (e) {}
    }
  }
  
  endpointInfoEl.innerHTML = endpointInfo;
  
  // Session info
  let sessionInfo = '<h4>Session Information</h4>';
  
  if (res && res.body) {
    try {
      const bodyObj = JSON.parse(res.body);
      
      if (bodyObj.session_id) {
        sessionInfo += `<p>Session ID: ${bodyObj.session_id}</p>`;
      }
      
      if (bodyObj.status) {
        sessionInfo += `<p>Status: ${bodyObj.status}</p>`;
      }
      
      if (bodyObj.created_at) {
        sessionInfo += `<p>Created: ${formatTimestamp(bodyObj.created_at)}</p>`;
      }
    } catch (e) {}
  }
  
  sessionInfoEl.innerHTML = sessionInfo;
  
  // Timing info
  let timingInfo = '<h4>Timing Information</h4>';
  
  if (req.timestamp && res && res.timestamp) {
    const requestTime = new Date(req.timestamp);
    const responseTime = new Date(res.timestamp);
    const duration = responseTime - requestTime;
    
    timingInfo += `<p>Request Time: ${formatTimestamp(req.timestamp)}</p>`;
    timingInfo += `<p>Response Time: ${formatTimestamp(res.timestamp)}</p>`;
    timingInfo += `<p>Duration: ${duration}ms</p>`;
  }
  
  timingInfoEl.innerHTML = timingInfo;
}

// Clear requests
function clearRequests() {
  // Clear requests array
  requests = [];
  
  // Clear selected request ID
  selectedRequestId = null;
  
  // Update UI
  updateRequestList();
  
  // Clear request details
  requestUrlEl.textContent = '';
  requestMethodEl.textContent = '';
  requestTimestampEl.textContent = '';
  requestBodyEl.textContent = '';
  responseStatusEl.textContent = '';
  responseTimestampEl.textContent = '';
  responseBodyEl.textContent = '';
  requestHeadersEl.textContent = '';
  responseHeadersEl.textContent = '';
  endpointInfoEl.innerHTML = '';
  sessionInfoEl.innerHTML = '';
  timingInfoEl.innerHTML = '';
  
  // Send message to background script
  chrome.runtime.sendMessage({ action: 'clearRequests' });
}

// Export requests
function exportRequests() {
  // Create export data
  const exportData = {
    requests: requests,
    exportTime: new Date().toISOString()
  };
  
  // Convert to JSON
  const jsonData = JSON.stringify(exportData, null, 2);
  
  // Create blob
  const blob = new Blob([jsonData], { type: 'application/json' });
  
  // Create URL
  const url = URL.createObjectURL(blob);
  
  // Create download link
  const a = document.createElement('a');
  a.href = url;
  a.download = `devin-api-requests-${formatDateForFilename(new Date())}.json`;
  
  // Trigger download
  document.body.appendChild(a);
  a.click();
  
  // Clean up
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// Helper functions
function formatTimestamp(timestamp) {
  if (!timestamp) return '';
  
  const date = new Date(timestamp);
  return date.toLocaleTimeString();
}

function formatDateForFilename(date) {
  return date.toISOString().replace(/:/g, '-').replace(/\..+/, '');
}

function formatHeaders(headers) {
  if (!headers) return '';
  
  if (Array.isArray(headers)) {
    return headers.map(h => `${h.name}: ${h.value}`).join('\n');
  } else if (typeof headers === 'object') {
    return Object.keys(headers).map(key => `${key}: ${headers[key]}`).join('\n');
  }
  
  return headers.toString();
}

function extractEndpoint(url) {
  // Remove base URL
  const baseUrl = 'https://api.devin.ai/v1';
  const path = url.replace(baseUrl, '');
  
  // Extract endpoint
  const endpoint = path.split('?')[0];
  return endpoint;
}

function extractSessionId(url) {
  const match = url.match(/\/session\/([^\/]+)/);
  return match ? match[1] : '';
}

function categorizeRequest(url) {
  const endpoint = extractEndpoint(url);
  
  if (endpoint === '/sessions') {
    return 'sessions';
  } else if (endpoint.startsWith('/session/')) {
    if (endpoint.endsWith('/message')) {
      return 'message';
    } else {
      return 'session';
    }
  } else if (endpoint === '/secrets') {
    return 'secrets';
  } else if (endpoint.startsWith('/secrets/')) {
    return 'secret';
  } else if (endpoint === '/attachments') {
    return 'attachment';
  } else {
    return 'other';
  }
}

// Initialize the panel when the DOM is ready
document.addEventListener('DOMContentLoaded', initPanel);
