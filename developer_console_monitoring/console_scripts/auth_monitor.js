/**
 * Devin API Authentication Monitor
 * 
 * This script monitors authentication-related interactions with the Devin API.
 * Copy and paste this entire script into the Console tab to activate monitoring.
 */

// Create the devinAuth namespace if it doesn't exist
window.devinAuth = window.devinAuth || {};

// Configuration
devinAuth.config = {
  apiDomain: 'api.devin.ai',
  appDomain: 'app.devin.ai',
  logLevel: 'info', // 'debug', 'info', 'warn', 'error'
  captureTokens: false // Set to true to capture tokens (security risk)
};

// Storage for captured auth events
devinAuth.events = [];

// Initialize the monitor
devinAuth.init = function() {
  console.log('%c Devin Auth Monitor Initialized ', 'background: #8e44ad; color: white; padding: 5px; border-radius: 3px;');
  console.log('Type devinAuth.help() for available commands');
  
  // Set up XHR monitoring
  devinAuth.setupXhrMonitoring();
  
  // Set up fetch monitoring
  devinAuth.setupFetchMonitoring();
  
  // Set up localStorage monitoring
  devinAuth.setupStorageMonitoring();
  
  return 'Devin Auth Monitor is now active';
};

// Set up XHR monitoring
devinAuth.setupXhrMonitoring = function() {
  const originalXhrOpen = XMLHttpRequest.prototype.open;
  const originalXhrSend = XMLHttpRequest.prototype.send;
  const originalXhrSetRequestHeader = XMLHttpRequest.prototype.setRequestHeader;
  
  // Override XMLHttpRequest.open
  XMLHttpRequest.prototype.open = function(method, url, async, user, password) {
    this._method = method;
    this._url = url;
    return originalXhrOpen.apply(this, arguments);
  };
  
  // Override XMLHttpRequest.setRequestHeader
  XMLHttpRequest.prototype.setRequestHeader = function(header, value) {
    // Only monitor requests to the Devin API
    if (this._url && this._url.includes(devinAuth.config.apiDomain)) {
      // Check for authentication headers
      if (header.toLowerCase() === 'authorization') {
        // Store auth header
        this._authHeader = {
          header: header,
          value: devinAuth.config.captureTokens ? value : devinAuth.maskToken(value)
        };
        
        // Create auth event
        const event = {
          type: 'request_header',
          method: this._method,
          url: this._url,
          header: header,
          value: devinAuth.config.captureTokens ? value : devinAuth.maskToken(value),
          timestamp: new Date().toISOString()
        };
        
        // Store the event
        devinAuth.storeEvent(event);
        
        // Log the event
        devinAuth.logEvent(event);
      }
    }
    
    return originalXhrSetRequestHeader.apply(this, arguments);
  };
  
  devinAuth.log('debug', 'XHR monitoring set up');
};

// Set up fetch monitoring
devinAuth.setupFetchMonitoring = function() {
  const originalFetch = window.fetch;
  
  // Override fetch
  window.fetch = async function(input, init) {
    // Get URL
    const url = typeof input === 'string' ? input : input.url;
    
    // Only monitor requests to the Devin API
    if (url && url.includes(devinAuth.config.apiDomain)) {
      // Check for authentication headers
      if (init && init.headers) {
        let authHeader = null;
        
        // Check for Authorization header
        if (init.headers instanceof Headers) {
          if (init.headers.has('Authorization')) {
            authHeader = {
              header: 'Authorization',
              value: init.headers.get('Authorization')
            };
          }
        } else if (Array.isArray(init.headers)) {
          const authHeaderEntry = init.headers.find(header => 
            Array.isArray(header) && header[0].toLowerCase() === 'authorization'
          );
          
          if (authHeaderEntry) {
            authHeader = {
              header: authHeaderEntry[0],
              value: authHeaderEntry[1]
            };
          }
        } else if (typeof init.headers === 'object') {
          for (const [key, value] of Object.entries(init.headers)) {
            if (key.toLowerCase() === 'authorization') {
              authHeader = {
                header: key,
                value: value
              };
              break;
            }
          }
        }
        
        // If auth header found, create event
        if (authHeader) {
          const event = {
            type: 'request_header',
            method: init.method || 'GET',
            url: url,
            header: authHeader.header,
            value: devinAuth.config.captureTokens ? authHeader.value : devinAuth.maskToken(authHeader.value),
            timestamp: new Date().toISOString()
          };
          
          // Store the event
          devinAuth.storeEvent(event);
          
          // Log the event
          devinAuth.logEvent(event);
        }
      }
    }
    
    // Call original fetch
    return originalFetch.apply(this, arguments);
  };
  
  devinAuth.log('debug', 'Fetch monitoring set up');
};

// Set up localStorage monitoring
devinAuth.setupStorageMonitoring = function() {
  const originalSetItem = Storage.prototype.setItem;
  const originalGetItem = Storage.prototype.getItem;
  const originalRemoveItem = Storage.prototype.removeItem;
  
  // Override setItem
  Storage.prototype.setItem = function(key, value) {
    // Check for auth-related keys
    if (devinAuth.isAuthKey(key)) {
      // Create event
      const event = {
        type: 'storage_set',
        storage: this === localStorage ? 'localStorage' : 'sessionStorage',
        key: key,
        value: devinAuth.config.captureTokens ? value : devinAuth.maskToken(value),
        timestamp: new Date().toISOString()
      };
      
      // Store the event
      devinAuth.storeEvent(event);
      
      // Log the event
      devinAuth.logEvent(event);
    }
    
    return originalSetItem.apply(this, arguments);
  };
  
  // Override getItem
  Storage.prototype.getItem = function(key) {
    // Check for auth-related keys
    if (devinAuth.isAuthKey(key)) {
      // Create event
      const event = {
        type: 'storage_get',
        storage: this === localStorage ? 'localStorage' : 'sessionStorage',
        key: key,
        timestamp: new Date().toISOString()
      };
      
      // Store the event
      devinAuth.storeEvent(event);
      
      // Log the event
      devinAuth.logEvent(event);
    }
    
    return originalGetItem.apply(this, arguments);
  };
  
  // Override removeItem
  Storage.prototype.removeItem = function(key) {
    // Check for auth-related keys
    if (devinAuth.isAuthKey(key)) {
      // Create event
      const event = {
        type: 'storage_remove',
        storage: this === localStorage ? 'localStorage' : 'sessionStorage',
        key: key,
        timestamp: new Date().toISOString()
      };
      
      // Store the event
      devinAuth.storeEvent(event);
      
      // Log the event
      devinAuth.logEvent(event);
    }
    
    return originalRemoveItem.apply(this, arguments);
  };
  
  devinAuth.log('debug', 'Storage monitoring set up');
};

// Check if a key is auth-related
devinAuth.isAuthKey = function(key) {
  const authKeywords = ['token', 'auth', 'jwt', 'bearer', 'session', 'credential'];
  
  return authKeywords.some(keyword => key.toLowerCase().includes(keyword));
};

// Mask a token
devinAuth.maskToken = function(token) {
  if (!token) return token;
  
  // Check if it's a Bearer token
  if (token.startsWith('Bearer ')) {
    const actualToken = token.substring(7);
    
    // Keep first and last 4 characters
    if (actualToken.length > 8) {
      return `Bearer ${actualToken.substring(0, 4)}...${actualToken.substring(actualToken.length - 4)}`;
    }
    
    return 'Bearer ***';
  }
  
  // Generic token masking
  if (token.length > 8) {
    return `${token.substring(0, 4)}...${token.substring(token.length - 4)}`;
  }
  
  return '***';
};

// Store an event
devinAuth.storeEvent = function(event) {
  devinAuth.events.push(event);
  
  // Limit the number of stored events
  if (devinAuth.events.length > 100) {
    devinAuth.events.shift();
  }
};

// Log an event
devinAuth.logEvent = function(event) {
  switch (event.type) {
    case 'request_header':
      devinAuth.log('info', `Auth Header: ${event.method} ${event.url} (${event.header}: ${event.value})`);
      break;
    case 'storage_set':
      devinAuth.log('info', `Storage Set: ${event.storage}.${event.key} = ${event.value}`);
      break;
    case 'storage_get':
      devinAuth.log('debug', `Storage Get: ${event.storage}.${event.key}`);
      break;
    case 'storage_remove':
      devinAuth.log('info', `Storage Remove: ${event.storage}.${event.key}`);
      break;
    default:
      devinAuth.log('debug', event);
  }
};

// Log a message
devinAuth.log = function(level, message) {
  const levels = {
    debug: 0,
    info: 1,
    warn: 2,
    error: 3
  };
  
  const configLevel = levels[devinAuth.config.logLevel] || 1;
  const messageLevel = levels[level] || 1;
  
  if (messageLevel >= configLevel) {
    switch (level) {
      case 'debug':
        console.debug('%c Devin Auth [DEBUG] ', 'background: #9b59b6; color: white; padding: 2px; border-radius: 2px;', message);
        break;
      case 'info':
        console.info('%c Devin Auth [INFO] ', 'background: #8e44ad; color: white; padding: 2px; border-radius: 2px;', message);
        break;
      case 'warn':
        console.warn('%c Devin Auth [WARN] ', 'background: #9b59b6; color: white; padding: 2px; border-radius: 2px;', message);
        break;
      case 'error':
        console.error('%c Devin Auth [ERROR] ', 'background: #8e44ad; color: white; padding: 2px; border-radius: 2px;', message);
        break;
      default:
        console.log('%c Devin Auth ', 'background: #8e44ad; color: white; padding: 2px; border-radius: 2px;', message);
    }
  }
};

// Help command
devinAuth.help = function() {
  console.log('%c Devin Auth Monitor Commands ', 'background: #8e44ad; color: white; padding: 5px; border-radius: 3px;');
  console.log('devinAuth.help() - Show this help message');
  console.log('devinAuth.getEvents() - Get all captured auth events');
  console.log('devinAuth.clear() - Clear all captured events');
  console.log('devinAuth.analyze() - Analyze auth patterns');
  console.log('devinAuth.export() - Export all captured events as JSON');
  console.log('devinAuth.config - View or modify configuration');
  
  return 'Type any of the above commands to use the Devin Auth Monitor';
};

// Get all events
devinAuth.getEvents = function() {
  return devinAuth.events;
};

// Clear all events
devinAuth.clear = function() {
  devinAuth.events = [];
  console.log('%c Devin Auth Monitor Cleared ', 'background: #8e44ad; color: white; padding: 5px; border-radius: 3px;');
  
  return 'All captured auth events have been cleared';
};

// Analyze auth patterns
devinAuth.analyze = function() {
  // Count event types
  const typeCounts = {};
  
  devinAuth.events.forEach(event => {
    if (!typeCounts[event.type]) {
      typeCounts[event.type] = 0;
    }
    
    typeCounts[event.type]++;
  });
  
  // Find auth storage keys
  const storageKeys = {};
  
  devinAuth.events.forEach(event => {
    if (event.type.startsWith('storage_') && event.key) {
      if (!storageKeys[event.key]) {
        storageKeys[event.key] = {
          count: 0,
          storage: event.storage
        };
      }
      
      storageKeys[event.key].count++;
    }
  });
  
  // Find auth header patterns
  const headerPatterns = {};
  
  devinAuth.events.forEach(event => {
    if (event.type === 'request_header') {
      const urlPath = new URL(event.url).pathname;
      
      if (!headerPatterns[urlPath]) {
        headerPatterns[urlPath] = {
          count: 0,
          methods: {}
        };
      }
      
      headerPatterns[urlPath].count++;
      
      if (!headerPatterns[urlPath].methods[event.method]) {
        headerPatterns[urlPath].methods[event.method] = 0;
      }
      
      headerPatterns[urlPath].methods[event.method]++;
    }
  });
  
  // Create analysis
  const analysis = {
    eventTypes: typeCounts,
    storageKeys: storageKeys,
    headerPatterns: headerPatterns,
    totalEvents: devinAuth.events.length
  };
  
  // Log analysis
  console.log('%c Auth Analysis ', 'background: #8e44ad; color: white; padding: 5px; border-radius: 3px;');
  console.log('Total Events:', analysis.totalEvents);
  console.log('Event Types:', analysis.eventTypes);
  console.log('Storage Keys:', analysis.storageKeys);
  console.log('Header Patterns:', analysis.headerPatterns);
  
  return analysis;
};

// Export all events
devinAuth.export = function() {
  const exportData = {
    timestamp: new Date().toISOString(),
    config: devinAuth.config,
    events: devinAuth.events
  };
  
  const dataStr = JSON.stringify(exportData, null, 2);
  const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);
  
  const exportFileDefaultName = `devin-auth-monitor-${new Date().toISOString().replace(/:/g, '-')}.json`;
  
  const linkElement = document.createElement('a');
  linkElement.setAttribute('href', dataUri);
  linkElement.setAttribute('download', exportFileDefaultName);
  linkElement.click();
  
  return `Exported ${devinAuth.events.length} events to ${exportFileDefaultName}`;
};

// Initialize the monitor
devinAuth.init();

console.log('%c Devin Auth Monitor Ready ', 'background: #8e44ad; color: white; padding: 5px; border-radius: 3px;');
console.log('Type devinAuth.help() for available commands');
