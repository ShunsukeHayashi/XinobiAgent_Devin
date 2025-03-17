/**
 * Devin Auth Monitor
 * 
 * This script monitors authentication-related events for the Devin API,
 * including token usage, storage, and headers.
 */

// Create the devinAuth namespace
const devinAuth = {
    // Configuration
    config: {
        logLevel: 'info', // 'debug', 'info', 'warn', 'error'
        captureTokens: false, // Set to true to capture actual tokens (security risk)
        maxStoredEvents: 100
    },
    
    // Storage for auth events
    events: [],
    
    // Initialize the monitor
    init: function() {
        console.log('Devin Auth Monitor initialized');
        
        // Monitor localStorage
        this._monitorStorage();
        
        // Monitor fetch headers
        this._monitorFetchHeaders();
        
        // Monitor XHR headers
        this._monitorXHRHeaders();
        
        return this;
    },
    
    // Monitor localStorage and sessionStorage
    _monitorStorage: function() {
        const originalSetItem = Storage.prototype.setItem;
        const originalGetItem = Storage.prototype.getItem;
        const self = this;
        
        // Monitor setItem
        Storage.prototype.setItem = function(key, value) {
            // Check if this is an auth-related key
            if (key.toLowerCase().includes('token') || 
                key.toLowerCase().includes('auth') || 
                key.toLowerCase().includes('devin')) {
                
                // Capture storage event
                const event = {
                    type: 'storage_set',
                    storage: this === localStorage ? 'localStorage' : 'sessionStorage',
                    key: key,
                    value: self.config.captureTokens ? value : self._maskToken(value),
                    timestamp: new Date().toISOString()
                };
                
                // Store event
                self._storeEvent(event);
                
                // Log event
                self._log('info', 'Storage set:', event.storage, key);
            }
            
            return originalSetItem.apply(this, arguments);
        };
        
        // Monitor getItem
        Storage.prototype.getItem = function(key) {
            // Check if this is an auth-related key
            if (key.toLowerCase().includes('token') || 
                key.toLowerCase().includes('auth') || 
                key.toLowerCase().includes('devin')) {
                
                const value = originalGetItem.call(this, key);
                
                // Capture storage event
                const event = {
                    type: 'storage_get',
                    storage: this === localStorage ? 'localStorage' : 'sessionStorage',
                    key: key,
                    value: self.config.captureTokens ? value : self._maskToken(value),
                    timestamp: new Date().toISOString()
                };
                
                // Store event
                self._storeEvent(event);
                
                // Log event
                self._log('debug', 'Storage get:', event.storage, key);
            }
            
            return originalGetItem.apply(this, arguments);
        };
    },
    
    // Monitor fetch headers
    _monitorFetchHeaders: function() {
        const originalFetch = window.fetch;
        const self = this;
        
        window.fetch = function(url, options = {}) {
            // Check if this request has auth headers
            if (options && options.headers) {
                // Check for Authorization header
                if (options.headers.Authorization || options.headers.authorization) {
                    const authHeader = options.headers.Authorization || options.headers.authorization;
                    
                    // Capture auth header event
                    const event = {
                        type: 'fetch_auth_header',
                        url: url,
                        method: options.method || 'GET',
                        header: 'Authorization',
                        value: self.config.captureTokens ? authHeader : self._maskToken(authHeader),
                        timestamp: new Date().toISOString()
                    };
                    
                    // Store event
                    self._storeEvent(event);
                    
                    // Log event
                    self._log('info', 'Fetch auth header:', event.method, url);
                }
                
                // Check for other auth-related headers
                for (const header in options.headers) {
                    if (header.toLowerCase().includes('token') || 
                        header.toLowerCase().includes('auth') || 
                        header.toLowerCase().includes('devin')) {
                        
                        // Skip if already captured as Authorization header
                        if (header === 'Authorization' || header === 'authorization') {
                            continue;
                        }
                        
                        // Capture auth header event
                        const event = {
                            type: 'fetch_auth_header',
                            url: url,
                            method: options.method || 'GET',
                            header: header,
                            value: self.config.captureTokens ? options.headers[header] : self._maskToken(options.headers[header]),
                            timestamp: new Date().toISOString()
                        };
                        
                        // Store event
                        self._storeEvent(event);
                        
                        // Log event
                        self._log('info', 'Fetch auth header:', event.method, url, header);
                    }
                }
            }
            
            return originalFetch.apply(this, arguments);
        };
    },
    
    // Monitor XHR headers
    _monitorXHRHeaders: function() {
        const originalSetRequestHeader = XMLHttpRequest.prototype.setRequestHeader;
        const self = this;
        
        XMLHttpRequest.prototype.setRequestHeader = function(header, value) {
            // Check if this is an auth-related header
            if (header.toLowerCase() === 'authorization' || 
                header.toLowerCase().includes('token') || 
                header.toLowerCase().includes('auth') || 
                header.toLowerCase().includes('devin')) {
                
                // Get request details
                const url = this._devinMonitorData ? this._devinMonitorData.url : 'unknown';
                const method = this._devinMonitorData ? this._devinMonitorData.method : 'unknown';
                
                // Capture auth header event
                const event = {
                    type: 'xhr_auth_header',
                    url: url,
                    method: method,
                    header: header,
                    value: self.config.captureTokens ? value : self._maskToken(value),
                    timestamp: new Date().toISOString()
                };
                
                // Store event
                self._storeEvent(event);
                
                // Log event
                self._log('info', 'XHR auth header:', method, url, header);
            }
            
            return originalSetRequestHeader.apply(this, arguments);
        };
    },
    
    // Utility functions
    _maskToken: function(token) {
        if (!token) return token;
        
        // Check if it's a Bearer token
        if (typeof token === 'string' && token.startsWith('Bearer ')) {
            const actualToken = token.substring(7);
            if (actualToken.length <= 8) return token;
            return 'Bearer ' + actualToken.substring(0, 4) + '...' + actualToken.substring(actualToken.length - 4);
        }
        
        // Regular token
        if (typeof token === 'string') {
            if (token.length <= 8) return token;
            return token.substring(0, 4) + '...' + token.substring(token.length - 4);
        }
        
        return token;
    },
    
    _log: function(level, ...args) {
        const levels = {
            debug: 0,
            info: 1,
            warn: 2,
            error: 3
        };
        
        if (levels[level] >= levels[this.config.logLevel]) {
            console.log(`[Devin Auth Monitor] [${level.toUpperCase()}]`, ...args);
        }
    },
    
    _storeEvent: function(event) {
        this.events.unshift(event);
        
        // Limit the number of stored events
        if (this.events.length > this.config.maxStoredEvents) {
            this.events = this.events.slice(0, this.config.maxStoredEvents);
        }
    },
    
    // Public API
    getEvents: function() {
        return this.events;
    },
    
    clearEvents: function() {
        this.events = [];
        this._log('info', 'Events cleared');
    },
    
    summarize: function() {
        // Count events by type
        const types = {};
        const headers = {};
        const storageKeys = {};
        
        this.events.forEach(event => {
            // Type
            types[event.type] = (types[event.type] || 0) + 1;
            
            // Headers
            if (event.type.includes('auth_header')) {
                headers[event.header] = (headers[event.header] || 0) + 1;
            }
            
            // Storage keys
            if (event.type.includes('storage')) {
                storageKeys[event.key] = (storageKeys[event.key] || 0) + 1;
            }
        });
        
        return {
            total: this.events.length,
            byType: types,
            byHeader: headers,
            byStorageKey: storageKeys,
            timestamp: new Date().toISOString()
        };
    },
    
    export: function() {
        const data = {
            events: this.events,
            summary: this.summarize(),
            exportTime: new Date().toISOString()
        };
        
        // Create download link
        const dataStr = JSON.stringify(data, null, 2);
        const blob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.setAttribute('href', url);
        a.setAttribute('download', `devin-auth-monitor-export-${Date.now()}.json`);
        a.click();
        
        return data;
    },
    
    help: function() {
        console.log(`
Devin Auth Monitor - Help
========================

Available commands:

getEvents()       - Get all captured auth events
clearEvents()     - Clear all captured events
summarize()       - Summarize all captured events
export()          - Export all data as JSON
help()            - Show this help message

Configuration:
config.logLevel      - Log level (default: 'info')
config.captureTokens - Whether to capture actual tokens (default: false)
        `);
    }
};

// Initialize the monitor
devinAuth.init();

console.log('Devin Auth Monitor loaded successfully');
