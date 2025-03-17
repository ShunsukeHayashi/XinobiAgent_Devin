/**
 * Devin API Monitor
 * 
 * This script monitors Devin API interactions in the Chrome Developer Console.
 * Copy and paste this entire script into the Console tab to activate monitoring.
 */

// Create the devinApi namespace if it doesn't exist
window.devinApi = window.devinApi || {};

// Configuration
devinApi.config = {
  apiDomain: 'api.devin.ai',
  appDomain: 'app.devin.ai',
  logLevel: 'info', // 'debug', 'info', 'warn', 'error'
  captureResponses: true,
  maxStoredRequests: 100
};

// Storage for captured requests
devinApi.requests = [];

// Initialize the monitor
devinApi.init = function() {
  console.log('%c Devin API Monitor Initialized ', 'background: #2c3e50; color: white; padding: 5px; border-radius: 3px;');
  console.log('Type devinApi.help() for available commands');
  
  // Set up XHR monitoring
  devinApi.setupXhrMonitoring();
  
  // Set up fetch monitoring
  devinApi.setupFetchMonitoring();
  
  return 'Devin API Monitor is now active';
};

// Set up XHR monitoring
devinApi.setupXhrMonitoring = function() {
  const originalXhrOpen = XMLHttpRequest.prototype.open;
  const originalXhrSend = XMLHttpRequest.prototype.send;
  
  // Override XMLHttpRequest.open
  XMLHttpRequest.prototype.open = function(method, url, async, user, password) {
    this._method = method;
    this._url = url;
    return originalXhrOpen.apply(this, arguments);
  };
  
  // Override XMLHttpRequest.send
  XMLHttpRequest.prototype.send = function(body) {
    // Only monitor requests to the Devin API
    if (this._url && this._url.includes(devinApi.config.apiDomain)) {
      // Store request data
      const requestId = Date.now().toString() + Math.random().toString(36).substring(2, 15);
      this._requestId = requestId;
      this._requestBody = body;
      this._requestTime = new Date();
      
      // Create request object
      const request = {
        id: requestId,
        url: this._url,
        method: this._method,
        body: body,
        timestamp: this._requestTime.toISOString(),
        type: 'xhr'
      };
      
      // Store the request
      devinApi.storeRequest(request);
      
      // Log the request
      devinApi.logRequest(request);
      
      // Add event listener for load
      this.addEventListener('load', function() {
        // Create response object
        const response = {
          id: requestId,
          status: this.status,
          statusText: this.statusText,
          body: devinApi.config.captureResponses ? this.responseText : '[Response body not captured]',
          timestamp: new Date().toISOString(),
          duration: new Date() - this._requestTime
        };
        
        // Store the response
        devinApi.storeResponse(requestId, response);
        
        // Log the response
        devinApi.logResponse(response);
      });
    }
    
    return originalXhrSend.apply(this, arguments);
  };
  
  devinApi.log('debug', 'XHR monitoring set up');
};

// Set up fetch monitoring
devinApi.setupFetchMonitoring = function() {
  const originalFetch = window.fetch;
  
  // Override fetch
  window.fetch = async function(input, init) {
    // Get URL
    const url = typeof input === 'string' ? input : input.url;
    
    // Only monitor requests to the Devin API
    if (url && url.includes(devinApi.config.apiDomain)) {
      // Store request data
      const requestId = Date.now().toString() + Math.random().toString(36).substring(2, 15);
      const method = init?.method || 'GET';
      const body = init?.body;
      const requestTime = new Date();
      
      // Create request object
      const request = {
        id: requestId,
        url: url,
        method: method,
        body: body,
        timestamp: requestTime.toISOString(),
        type: 'fetch'
      };
      
      // Store the request
      devinApi.storeRequest(request);
      
      // Log the request
      devinApi.logRequest(request);
      
      try {
        // Call original fetch
        const response = await originalFetch.apply(this, arguments);
        
        // Clone the response to read the body
        const clonedResponse = response.clone();
        let responseBody = '[Response body not captured]';
        
        if (devinApi.config.captureResponses) {
          try {
            responseBody = await clonedResponse.text();
          } catch (e) {
            responseBody = '[Error reading response body]';
          }
        }
        
        // Create response object
        const responseObj = {
          id: requestId,
          status: response.status,
          statusText: response.statusText,
          body: responseBody,
          timestamp: new Date().toISOString(),
          duration: new Date() - requestTime
        };
        
        // Store the response
        devinApi.storeResponse(requestId, responseObj);
        
        // Log the response
        devinApi.logResponse(responseObj);
        
        return response;
      } catch (error) {
        // Create error response
        const errorResponse = {
          id: requestId,
          error: error.toString(),
          timestamp: new Date().toISOString(),
          duration: new Date() - requestTime
        };
        
        // Store the error response
        devinApi.storeResponse(requestId, errorResponse);
        
        // Log the error
        devinApi.log('error', `Request ${requestId} failed: ${error}`);
        
        throw error;
      }
    }
    
    // Call original fetch for non-Devin API requests
    return originalFetch.apply(this, arguments);
  };
  
  devinApi.log('debug', 'Fetch monitoring set up');
};

// Store a request
devinApi.storeRequest = function(request) {
  // Find existing request or create new one
  const existingIndex = devinApi.requests.findIndex(req => req.id === request.id);
  
  if (existingIndex !== -1) {
    // Update existing request
    devinApi.requests[existingIndex] = {
      ...devinApi.requests[existingIndex],
      ...request
    };
  } else {
    // Add new request
    devinApi.requests.push({
      ...request,
      response: null
    });
    
    // Limit the number of stored requests
    if (devinApi.requests.length > devinApi.config.maxStoredRequests) {
      devinApi.requests.shift();
    }
  }
};

// Store a response
devinApi.storeResponse = function(requestId, response) {
  // Find the request
  const requestIndex = devinApi.requests.findIndex(req => req.id === requestId);
  
  if (requestIndex !== -1) {
    // Update the request with the response
    devinApi.requests[requestIndex].response = response;
  }
};

// Log a request
devinApi.logRequest = function(request) {
  const endpoint = devinApi.extractEndpoint(request.url);
  const method = request.method;
  
  devinApi.log('info', `${method} ${endpoint} (${request.id})`);
  devinApi.log('debug', request);
};

// Log a response
devinApi.logResponse = function(response) {
  const status = response.status;
  const duration = response.duration;
  
  if (status >= 200 && status < 300) {
    devinApi.log('info', `Response ${response.id}: ${status} (${duration}ms)`);
  } else {
    devinApi.log('warn', `Response ${response.id}: ${status} (${duration}ms)`);
  }
  
  devinApi.log('debug', response);
};

// Extract endpoint from URL
devinApi.extractEndpoint = function(url) {
  // Extract path
  const urlObj = new URL(url);
  const path = urlObj.pathname;
  
  return path;
};

// Categorize endpoint
devinApi.categorizeEndpoint = function(url) {
  const endpoint = devinApi.extractEndpoint(url);
  
  if (endpoint.endsWith('/sessions')) {
    return 'Session Creation';
  } else if (endpoint.includes('/session/')) {
    if (endpoint.endsWith('/message')) {
      return 'Message Sending';
    } else {
      return 'Session Details';
    }
  } else if (endpoint.endsWith('/secrets')) {
    return 'Secrets List';
  } else if (endpoint.includes('/secrets/')) {
    return 'Secret Management';
  } else if (endpoint.endsWith('/attachments')) {
    return 'File Upload';
  } else {
    return 'Other';
  }
};

// Log a message
devinApi.log = function(level, message) {
  const levels = {
    debug: 0,
    info: 1,
    warn: 2,
    error: 3
  };
  
  const configLevel = levels[devinApi.config.logLevel] || 1;
  const messageLevel = levels[level] || 1;
  
  if (messageLevel >= configLevel) {
    switch (level) {
      case 'debug':
        console.debug('%c Devin API [DEBUG] ', 'background: #95a5a6; color: white; padding: 2px; border-radius: 2px;', message);
        break;
      case 'info':
        console.info('%c Devin API [INFO] ', 'background: #3498db; color: white; padding: 2px; border-radius: 2px;', message);
        break;
      case 'warn':
        console.warn('%c Devin API [WARN] ', 'background: #f39c12; color: white; padding: 2px; border-radius: 2px;', message);
        break;
      case 'error':
        console.error('%c Devin API [ERROR] ', 'background: #e74c3c; color: white; padding: 2px; border-radius: 2px;', message);
        break;
      default:
        console.log('%c Devin API ', 'background: #2c3e50; color: white; padding: 2px; border-radius: 2px;', message);
    }
  }
};

// Help command
devinApi.help = function() {
  console.log('%c Devin API Monitor Commands ', 'background: #2c3e50; color: white; padding: 5px; border-radius: 3px;');
  console.log('devinApi.help() - Show this help message');
  console.log('devinApi.getRequests() - Get all captured requests');
  console.log('devinApi.getRequest(id) - Get a specific request by ID');
  console.log('devinApi.clear() - Clear all captured requests');
  console.log('devinApi.analyze(id) - Analyze a specific request');
  console.log('devinApi.summarize() - Summarize all captured requests');
  console.log('devinApi.export() - Export all captured requests as JSON');
  console.log('devinApi.config - View or modify configuration');
  
  return 'Type any of the above commands to use the Devin API Monitor';
};

// Get all requests
devinApi.getRequests = function() {
  return devinApi.requests;
};

// Get a specific request
devinApi.getRequest = function(id) {
  return devinApi.requests.find(req => req.id === id) || null;
};

// Clear all requests
devinApi.clear = function() {
  devinApi.requests = [];
  console.log('%c Devin API Monitor Cleared ', 'background: #2c3e50; color: white; padding: 5px; border-radius: 3px;');
  
  return 'All captured requests have been cleared';
};

// Analyze a request
devinApi.analyze = function(id) {
  const request = devinApi.getRequest(id);
  
  if (!request) {
    console.error(`Request with ID ${id} not found`);
    return null;
  }
  
  // Create analysis
  const analysis = {
    request: {
      id: request.id,
      url: request.url,
      method: request.method,
      timestamp: request.timestamp,
      body: request.body
    },
    response: request.response ? {
      status: request.response.status,
      statusText: request.response.statusText,
      timestamp: request.response.timestamp,
      duration: request.response.duration,
      body: request.response.body
    } : null,
    endpoint: devinApi.categorizeEndpoint(request.url),
    timing: request.response ? {
      duration: request.response.duration,
      requestTime: request.timestamp,
      responseTime: request.response.timestamp
    } : null
  };
  
  // Log analysis
  console.log('%c Request Analysis ', 'background: #2c3e50; color: white; padding: 5px; border-radius: 3px;');
  console.log('ID:', analysis.request.id);
  console.log('Endpoint:', analysis.endpoint);
  console.log('Method:', analysis.request.method);
  console.log('URL:', analysis.request.url);
  
  if (analysis.timing) {
    console.log('Duration:', analysis.timing.duration, 'ms');
  }
  
  if (analysis.response) {
    console.log('Status:', analysis.response.status, analysis.response.statusText);
  }
  
  console.log('Full Analysis:', analysis);
  
  return analysis;
};

// Summarize all requests
devinApi.summarize = function() {
  // Group requests by endpoint
  const endpoints = {};
  
  devinApi.requests.forEach(req => {
    const category = devinApi.categorizeEndpoint(req.url);
    
    if (!endpoints[category]) {
      endpoints[category] = {
        count: 0,
        methods: {},
        statuses: {},
        totalDuration: 0,
        avgDuration: 0
      };
    }
    
    endpoints[category].count++;
    
    // Count methods
    if (!endpoints[category].methods[req.method]) {
      endpoints[category].methods[req.method] = 0;
    }
    endpoints[category].methods[req.method]++;
    
    // Count statuses and calculate durations
    if (req.response) {
      if (!endpoints[category].statuses[req.response.status]) {
        endpoints[category].statuses[req.response.status] = 0;
      }
      endpoints[category].statuses[req.response.status]++;
      
      if (req.response.duration) {
        endpoints[category].totalDuration += req.response.duration;
      }
    }
  });
  
  // Calculate average durations
  Object.keys(endpoints).forEach(category => {
    if (endpoints[category].count > 0) {
      endpoints[category].avgDuration = endpoints[category].totalDuration / endpoints[category].count;
    }
  });
  
  // Log summary
  console.log('%c Request Summary ', 'background: #2c3e50; color: white; padding: 5px; border-radius: 3px;');
  console.log('Total Requests:', devinApi.requests.length);
  
  Object.keys(endpoints).forEach(category => {
    console.log(`\n${category}:`);
    console.log(`  Count: ${endpoints[category].count}`);
    console.log(`  Methods: `, endpoints[category].methods);
    console.log(`  Statuses: `, endpoints[category].statuses);
    console.log(`  Avg Duration: ${endpoints[category].avgDuration.toFixed(2)} ms`);
  });
  
  return endpoints;
};

// Export all requests
devinApi.export = function() {
  const exportData = {
    timestamp: new Date().toISOString(),
    config: devinApi.config,
    requests: devinApi.requests
  };
  
  const dataStr = JSON.stringify(exportData, null, 2);
  const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);
  
  const exportFileDefaultName = `devin-api-monitor-${new Date().toISOString().replace(/:/g, '-')}.json`;
  
  const linkElement = document.createElement('a');
  linkElement.setAttribute('href', dataUri);
  linkElement.setAttribute('download', exportFileDefaultName);
  linkElement.click();
  
  return `Exported ${devinApi.requests.length} requests to ${exportFileDefaultName}`;
};

// Initialize the monitor
devinApi.init();

console.log('%c Devin API Monitor Ready ', 'background: #27ae60; color: white; padding: 5px; border-radius: 3px;');
console.log('Type devinApi.help() for available commands');
