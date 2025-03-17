/**
 * Network monitor for the Devin API Monitor extension.
 * 
 * This script provides utilities for monitoring network requests.
 */

// Define the API base URL
const DEVIN_API_BASE_URL = 'https://api.devin.ai/v1';

// Network request monitor
class DevinNetworkMonitor {
  constructor() {
    this.requests = [];
    this.listeners = [];
    this.initialized = false;
  }

  // Initialize the monitor
  initialize() {
    if (this.initialized) return;
    
    // Set up listeners
    this.setupWebRequestListeners();
    this.setupMessageListeners();
    
    this.initialized = true;
    console.log('Devin Network Monitor initialized');
  }

  // Set up web request listeners
  setupWebRequestListeners() {
    // Listen for web requests to the Devin API
    chrome.webRequest.onBeforeRequest.addListener(
      this.handleBeforeRequest.bind(this),
      { urls: [`${DEVIN_API_BASE_URL}/*`] },
      ['requestBody']
    );

    // Listen for web request responses from the Devin API
    chrome.webRequest.onCompleted.addListener(
      this.handleRequestCompleted.bind(this),
      { urls: [`${DEVIN_API_BASE_URL}/*`] },
      ['responseHeaders']
    );
  }

  // Set up message listeners
  setupMessageListeners() {
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      if (request.action === 'getRequests') {
        sendResponse({ requests: this.requests });
      } else if (request.action === 'clearRequests') {
        this.clearRequests();
        sendResponse({ success: true });
      } else if (request.action === 'apiRequest') {
        this.handleApiRequest(request.data);
      }
      return true;
    });
  }

  // Handle before request event
  handleBeforeRequest(details) {
    // Extract request details
    const requestData = {
      id: details.requestId,
      url: details.url,
      method: details.method,
      timestamp: new Date().toISOString(),
      type: 'request',
      requestBody: details.requestBody
    };

    // Store the request
    this.requests.push(requestData);

    // Notify listeners
    this.notifyListeners('newRequest', requestData);

    // Log the request
    console.log('Devin API Request:', requestData);
    
    // Allow the request to proceed
    return { cancel: false };
  }

  // Handle request completed event
  handleRequestCompleted(details) {
    // Extract response details
    const responseData = {
      id: details.requestId,
      url: details.url,
      method: details.method,
      statusCode: details.statusCode,
      timestamp: new Date().toISOString(),
      type: 'response',
      responseHeaders: details.responseHeaders
    };

    // Store the response
    this.requests.push(responseData);

    // Notify listeners
    this.notifyListeners('newResponse', responseData);

    // Log the response
    console.log('Devin API Response:', responseData);
  }

  // Handle API request from content script
  handleApiRequest(data) {
    // Create a unique ID for the request
    const requestId = Date.now().toString();
    
    // Create request data
    const requestData = {
      id: requestId,
      url: data.url,
      method: data.method,
      timestamp: data.timestamp,
      type: 'request',
      requestBody: data.requestBody
    };
    
    // Create response data
    const responseData = {
      id: requestId,
      url: data.url,
      method: data.method,
      statusCode: data.status,
      timestamp: data.timestamp,
      type: 'response',
      responseBody: data.responseBody
    };
    
    // Store the request and response
    this.requests.push(requestData);
    this.requests.push(responseData);
    
    // Notify listeners
    this.notifyListeners('newRequest', requestData);
    this.notifyListeners('newResponse', responseData);
    
    // Log the request and response
    console.log('Devin API Request (from content):', requestData);
    console.log('Devin API Response (from content):', responseData);
  }

  // Add a listener
  addListener(callback) {
    this.listeners.push(callback);
  }

  // Remove a listener
  removeListener(callback) {
    const index = this.listeners.indexOf(callback);
    if (index !== -1) {
      this.listeners.splice(index, 1);
    }
  }

  // Notify all listeners
  notifyListeners(action, data) {
    this.listeners.forEach(listener => {
      try {
        listener(action, data);
      } catch (error) {
        console.error('Error in listener:', error);
      }
    });
  }

  // Clear all requests
  clearRequests() {
    this.requests = [];
    this.notifyListeners('requestsCleared');
  }

  // Get all requests
  getRequests() {
    return this.requests;
  }

  // Get requests by endpoint
  getRequestsByEndpoint(endpoint) {
    return this.requests.filter(req => {
      if (req.url) {
        return req.url.includes(endpoint);
      }
      return false;
    });
  }

  // Get requests by method
  getRequestsByMethod(method) {
    return this.requests.filter(req => req.method === method);
  }

  // Get requests by status code
  getRequestsByStatusCode(statusCode) {
    return this.requests.filter(req => {
      if (req.type === 'response') {
        return req.statusCode === statusCode;
      }
      return false;
    });
  }

  // Get session creation requests
  getSessionCreationRequests() {
    return this.requests.filter(req => {
      if (req.url && req.method === 'POST') {
        return req.url.endsWith('/sessions');
      }
      return false;
    });
  }

  // Get message sending requests
  getMessageSendingRequests() {
    return this.requests.filter(req => {
      if (req.url && req.method === 'POST') {
        return req.url.includes('/message');
      }
      return false;
    });
  }

  // Get session details requests
  getSessionDetailsRequests() {
    return this.requests.filter(req => {
      if (req.url && req.method === 'GET') {
        return req.url.includes('/session/') && !req.url.includes('/message');
      }
      return false;
    });
  }

  // Get file upload requests
  getFileUploadRequests() {
    return this.requests.filter(req => {
      if (req.url && req.method === 'POST') {
        return req.url.includes('/attachments');
      }
      return false;
    });
  }
}

// Create and export the monitor instance
const networkMonitor = new DevinNetworkMonitor();
networkMonitor.initialize();

// Export the monitor
window.devinNetworkMonitor = networkMonitor;
