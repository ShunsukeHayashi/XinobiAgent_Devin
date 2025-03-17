/**
 * Devin API Session Monitor
 * 
 * This script monitors session-related interactions with the Devin API.
 * Copy and paste this entire script into the Console tab to activate monitoring.
 */

// Create the devinSession namespace if it doesn't exist
window.devinSession = window.devinSession || {};

// Configuration
devinSession.config = {
  apiDomain: 'api.devin.ai',
  appDomain: 'app.devin.ai',
  logLevel: 'info', // 'debug', 'info', 'warn', 'error'
  captureResponses: true
};

// Storage for sessions
devinSession.sessions = {};
devinSession.messages = [];
devinSession.currentSessionId = null;

// Initialize the monitor
devinSession.init = function() {
  console.log('%c Devin Session Monitor Initialized ', 'background: #16a085; color: white; padding: 5px; border-radius: 3px;');
  console.log('Type devinSession.help() for available commands');
  
  // Set up XHR monitoring
  devinSession.setupXhrMonitoring();
  
  // Set up fetch monitoring
  devinSession.setupFetchMonitoring();
  
  // Extract current session ID from URL
  devinSession.extractSessionIdFromUrl();
  
  return 'Devin Session Monitor is now active';
};

// Set up XHR monitoring
devinSession.setupXhrMonitoring = function() {
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
    if (this._url && this._url.includes(devinSession.config.apiDomain)) {
      // Store request data
      this._requestBody = body;
      this._requestTime = new Date();
      
      // Check for session creation
      if (this._method === 'POST' && this._url.endsWith('/sessions')) {
        devinSession.handleSessionCreationRequest(this._url, this._method, body);
      }
      
      // Check for session details
      if (this._method === 'GET' && this._url.includes('/session/')) {
        devinSession.handleSessionDetailsRequest(this._url, this._method);
      }
      
      // Check for message sending
      if (this._method === 'POST' && this._url.includes('/session/') && this._url.endsWith('/message')) {
        devinSession.handleMessageSendingRequest(this._url, this._method, body);
      }
      
      // Add event listener for load
      this.addEventListener('load', function() {
        // Check for session creation response
        if (this._method === 'POST' && this._url.endsWith('/sessions')) {
          devinSession.handleSessionCreationResponse(this._url, this.responseText);
        }
        
        // Check for session details response
        if (this._method === 'GET' && this._url.includes('/session/')) {
          devinSession.handleSessionDetailsResponse(this._url, this.responseText);
        }
        
        // Check for message sending response
        if (this._method === 'POST' && this._url.includes('/session/') && this._url.endsWith('/message')) {
          devinSession.handleMessageSendingResponse(this._url, this.responseText);
        }
      });
    }
    
    return originalXhrSend.apply(this, arguments);
  };
  
  devinSession.log('debug', 'XHR monitoring set up');
};

// Set up fetch monitoring
devinSession.setupFetchMonitoring = function() {
  const originalFetch = window.fetch;
  
  // Override fetch
  window.fetch = async function(input, init) {
    // Get URL
    const url = typeof input === 'string' ? input : input.url;
    
    // Only monitor requests to the Devin API
    if (url && url.includes(devinSession.config.apiDomain)) {
      const method = init?.method || 'GET';
      const body = init?.body;
      
      // Check for session creation
      if (method === 'POST' && url.endsWith('/sessions')) {
        devinSession.handleSessionCreationRequest(url, method, body);
      }
      
      // Check for session details
      if (method === 'GET' && url.includes('/session/')) {
        devinSession.handleSessionDetailsRequest(url, method);
      }
      
      // Check for message sending
      if (method === 'POST' && url.includes('/session/') && url.endsWith('/message')) {
        devinSession.handleMessageSendingRequest(url, method, body);
      }
      
      try {
        // Call original fetch
        const response = await originalFetch.apply(this, arguments);
        
        // Clone the response to read the body
        const clonedResponse = response.clone();
        let responseBody = '';
        
        if (devinSession.config.captureResponses) {
          try {
            responseBody = await clonedResponse.text();
          } catch (e) {
            responseBody = '';
          }
        }
        
        // Check for session creation response
        if (method === 'POST' && url.endsWith('/sessions')) {
          devinSession.handleSessionCreationResponse(url, responseBody);
        }
        
        // Check for session details response
        if (method === 'GET' && url.includes('/session/')) {
          devinSession.handleSessionDetailsResponse(url, responseBody);
        }
        
        // Check for message sending response
        if (method === 'POST' && url.includes('/session/') && url.endsWith('/message')) {
          devinSession.handleMessageSendingResponse(url, responseBody);
        }
        
        return response;
      } catch (error) {
        devinSession.log('error', `Request to ${url} failed: ${error}`);
        throw error;
      }
    }
    
    // Call original fetch for non-Devin API requests
    return originalFetch.apply(this, arguments);
  };
  
  devinSession.log('debug', 'Fetch monitoring set up');
};

// Extract session ID from URL
devinSession.extractSessionIdFromUrl = function() {
  const url = window.location.href;
  const match = url.match(/\/session\/([^\/]+)/);
  
  if (match) {
    const sessionId = match[1];
    devinSession.currentSessionId = sessionId;
    
    devinSession.log('info', `Current session ID: ${sessionId}`);
    
    // Create session if it doesn't exist
    if (!devinSession.sessions[sessionId]) {
      devinSession.sessions[sessionId] = {
        id: sessionId,
        status: 'unknown',
        created_at: new Date().toISOString(),
        messages: [],
        details: {}
      };
    }
  }
};

// Handle session creation request
devinSession.handleSessionCreationRequest = function(url, method, body) {
  devinSession.log('info', `Session creation request: ${method} ${url}`);
  
  // Parse request body
  let requestData = {};
  
  try {
    if (body) {
      requestData = JSON.parse(body);
    }
  } catch (e) {
    devinSession.log('warn', `Failed to parse session creation request body: ${e}`);
  }
  
  devinSession.log('debug', 'Session creation request data:', requestData);
};

// Handle session creation response
devinSession.handleSessionCreationResponse = function(url, responseText) {
  devinSession.log('info', `Session creation response received`);
  
  // Parse response
  let responseData = {};
  
  try {
    if (responseText) {
      responseData = JSON.parse(responseText);
    }
  } catch (e) {
    devinSession.log('warn', `Failed to parse session creation response: ${e}`);
    return;
  }
  
  // Extract session ID
  if (responseData.session_id) {
    const sessionId = responseData.session_id;
    
    // Create session
    devinSession.sessions[sessionId] = {
      id: sessionId,
      status: responseData.status || 'created',
      created_at: new Date().toISOString(),
      messages: [],
      details: responseData
    };
    
    devinSession.currentSessionId = sessionId;
    
    devinSession.log('info', `Session created: ${sessionId}`);
    devinSession.log('debug', 'Session details:', devinSession.sessions[sessionId]);
  }
};

// Handle session details request
devinSession.handleSessionDetailsRequest = function(url, method) {
  // Extract session ID from URL
  const match = url.match(/\/session\/([^\/]+)/);
  
  if (match) {
    const sessionId = match[1];
    devinSession.log('info', `Session details request: ${method} ${url} (Session ID: ${sessionId})`);
  }
};

// Handle session details response
devinSession.handleSessionDetailsResponse = function(url, responseText) {
  // Extract session ID from URL
  const match = url.match(/\/session\/([^\/]+)/);
  
  if (!match) return;
  
  const sessionId = match[1];
  devinSession.log('info', `Session details response received for session ${sessionId}`);
  
  // Parse response
  let responseData = {};
  
  try {
    if (responseText) {
      responseData = JSON.parse(responseText);
    }
  } catch (e) {
    devinSession.log('warn', `Failed to parse session details response: ${e}`);
    return;
  }
  
  // Update session
  if (devinSession.sessions[sessionId]) {
    devinSession.sessions[sessionId].status = responseData.status || devinSession.sessions[sessionId].status;
    devinSession.sessions[sessionId].details = {
      ...devinSession.sessions[sessionId].details,
      ...responseData
    };
  } else {
    // Create session if it doesn't exist
    devinSession.sessions[sessionId] = {
      id: sessionId,
      status: responseData.status || 'unknown',
      created_at: responseData.created_at || new Date().toISOString(),
      messages: [],
      details: responseData
    };
  }
  
  devinSession.log('debug', 'Updated session details:', devinSession.sessions[sessionId]);
};

// Handle message sending request
devinSession.handleMessageSendingRequest = function(url, method, body) {
  // Extract session ID from URL
  const match = url.match(/\/session\/([^\/]+)\/message/);
  
  if (!match) return;
  
  const sessionId = match[1];
  devinSession.log('info', `Message sending request: ${method} ${url} (Session ID: ${sessionId})`);
  
  // Parse request body
  let requestData = {};
  
  try {
    if (body) {
      requestData = JSON.parse(body);
    }
  } catch (e) {
    devinSession.log('warn', `Failed to parse message sending request body: ${e}`);
  }
  
  // Create message
  const message = {
    session_id: sessionId,
    direction: 'outgoing',
    content: requestData.message || '',
    timestamp: new Date().toISOString(),
    request_data: requestData
  };
  
  // Add message to session
  if (devinSession.sessions[sessionId]) {
    devinSession.sessions[sessionId].messages.push(message);
  }
  
  // Add message to global messages
  devinSession.messages.push(message);
  
  devinSession.log('debug', 'Message sent:', message);
};

// Handle message sending response
devinSession.handleMessageSendingResponse = function(url, responseText) {
  // Extract session ID from URL
  const match = url.match(/\/session\/([^\/]+)\/message/);
  
  if (!match) return;
  
  const sessionId = match[1];
  devinSession.log('info', `Message sending response received for session ${sessionId}`);
  
  // Parse response
  let responseData = {};
  
  try {
    if (responseText) {
      responseData = JSON.parse(responseText);
    }
  } catch (e) {
    devinSession.log('warn', `Failed to parse message sending response: ${e}`);
  }
  
  devinSession.log('debug', 'Message response:', responseData);
};

// Log a message
devinSession.log = function(level, ...args) {
  const levels = {
    debug: 0,
    info: 1,
    warn: 2,
    error: 3
  };
  
  const configLevel = levels[devinSession.config.logLevel] || 1;
  const messageLevel = levels[level] || 1;
  
  if (messageLevel >= configLevel) {
    switch (level) {
      case 'debug':
        console.debug('%c Devin Session [DEBUG] ', 'background: #1abc9c; color: white; padding: 2px; border-radius: 2px;', ...args);
        break;
      case 'info':
        console.info('%c Devin Session [INFO] ', 'background: #16a085; color: white; padding: 2px; border-radius: 2px;', ...args);
        break;
      case 'warn':
        console.warn('%c Devin Session [WARN] ', 'background: #1abc9c; color: white; padding: 2px; border-radius: 2px;', ...args);
        break;
      case 'error':
        console.error('%c Devin Session [ERROR] ', 'background: #16a085; color: white; padding: 2px; border-radius: 2px;', ...args);
        break;
      default:
        console.log('%c Devin Session ', 'background: #16a085; color: white; padding: 2px; border-radius: 2px;', ...args);
    }
  }
};

// Help command
devinSession.help = function() {
  console.log('%c Devin Session Monitor Commands ', 'background: #16a085; color: white; padding: 5px; border-radius: 3px;');
  console.log('devinSession.help() - Show this help message');
  console.log('devinSession.getSessions() - Get all captured sessions');
  console.log('devinSession.getSession(id) - Get a specific session by ID');
  console.log('devinSession.getCurrentSession() - Get the current session');
  console.log('devinSession.getMessages() - Get all captured messages');
  console.log('devinSession.getSessionMessages(id) - Get messages for a specific session');
  console.log('devinSession.clear() - Clear all captured sessions and messages');
  console.log('devinSession.export() - Export all captured sessions and messages as JSON');
  console.log('devinSession.config - View or modify configuration');
  
  return 'Type any of the above commands to use the Devin Session Monitor';
};

// Get all sessions
devinSession.getSessions = function() {
  return devinSession.sessions;
};

// Get a specific session
devinSession.getSession = function(id) {
  return devinSession.sessions[id] || null;
};

// Get the current session
devinSession.getCurrentSession = function() {
  if (!devinSession.currentSessionId) {
    devinSession.extractSessionIdFromUrl();
  }
  
  return devinSession.getSession(devinSession.currentSessionId);
};

// Get all messages
devinSession.getMessages = function() {
  return devinSession.messages;
};

// Get messages for a specific session
devinSession.getSessionMessages = function(id) {
  const session = devinSession.getSession(id);
  
  if (!session) {
    return [];
  }
  
  return session.messages;
};

// Clear all sessions and messages
devinSession.clear = function() {
  devinSession.sessions = {};
  devinSession.messages = [];
  devinSession.currentSessionId = null;
  
  console.log('%c Devin Session Monitor Cleared ', 'background: #16a085; color: white; padding: 5px; border-radius: 3px;');
  
  return 'All captured sessions and messages have been cleared';
};

// Export all sessions and messages
devinSession.export = function() {
  const exportData = {
    timestamp: new Date().toISOString(),
    config: devinSession.config,
    sessions: devinSession.sessions,
    messages: devinSession.messages,
    currentSessionId: devinSession.currentSessionId
  };
  
  const dataStr = JSON.stringify(exportData, null, 2);
  const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);
  
  const exportFileDefaultName = `devin-session-monitor-${new Date().toISOString().replace(/:/g, '-')}.json`;
  
  const linkElement = document.createElement('a');
  linkElement.setAttribute('href', dataUri);
  linkElement.setAttribute('download', exportFileDefaultName);
  linkElement.click();
  
  return `Exported ${Object.keys(devinSession.sessions).length} sessions and ${devinSession.messages.length} messages to ${exportFileDefaultName}`;
};

// Initialize the monitor
devinSession.init();

console.log('%c Devin Session Monitor Ready ', 'background: #16a085; color: white; padding: 5px; border-radius: 3px;');
console.log('Type devinSession.help() for available commands');
