/**
 * Combined Devin API Monitor
 * 
 * This script combines the functionality of the API, Auth, and Session monitors
 * to provide comprehensive monitoring of Devin API interactions.
 */

// Configuration
const devin = {
    config: {
        apiDomain: 'api.devin.ai',
        logLevel: 'info', // 'debug', 'info', 'warn', 'error'
        captureResponses: true,
        captureTokens: false, // Set to true to capture actual tokens (security risk)
        maxStoredRequests: 100,
        maxStoredEvents: 100,
        maxStoredSessions: 20
    },
    
    // Storage
    requests: [],
    authEvents: [],
    sessions: {},
    
    // Initialization
    init: function() {
        console.log('Devin Combined Monitor initialized');
        console.log('Monitoring API domain:', this.config.apiDomain);
        
        // Initialize request monitoring
        this._initRequestMonitoring();
        
        // Initialize auth monitoring
        this._initAuthMonitoring();
        
        // Initialize session monitoring
        this._initSessionMonitoring();
        
        return this;
    },
    
    // API Request Monitoring
    _initRequestMonitoring: function() {
        const originalFetch = window.fetch;
        const originalXHROpen = XMLHttpRequest.prototype.open;
        const originalXHRSend = XMLHttpRequest.prototype.send;
        const self = this;
        
        // Override fetch
        window.fetch = function(url, options = {}) {
            // Only monitor requests to the Devin API
            if (typeof url === 'string' && url.includes(self.config.apiDomain)) {
                const requestId = self._generateId();
                const method = options.method || 'GET';
                const requestBody = options.body || null;
                
                // Capture request
                const request = {
                    id: requestId,
                    url: url,
                    method: method,
                    headers: options.headers || {},
                    body: requestBody,
                    timestamp: new Date().toISOString(),
                    type: 'fetch'
                };
                
                // Log request
                self._log('info', 'Fetch request:', request.method, request.url);
                
                // Store request
                self._storeRequest(request);
                
                // Process auth headers
                if (options.headers && options.headers.Authorization) {
                    self._processAuthHeader(method, url, options.headers.Authorization);
                }
                
                // Process session-related requests
                self._processSessionRequest(method, url, requestBody);
                
                // Make the actual request
                return originalFetch.apply(this, arguments)
                    .then(response => {
                        // Clone the response so we can read the body
                        const clonedResponse = response.clone();
                        
                        // Process the response
                        clonedResponse.text().then(responseBody => {
                            try {
                                const responseData = responseBody ? JSON.parse(responseBody) : {};
                                
                                // Capture response
                                const responseObj = {
                                    id: requestId,
                                    status: response.status,
                                    statusText: response.statusText,
                                    headers: self._getResponseHeaders(response),
                                    body: self.config.captureResponses ? responseBody : '[Response body not captured]',
                                    timestamp: new Date().toISOString(),
                                    duration: new Date() - new Date(request.timestamp)
                                };
                                
                                // Update request with response
                                self._updateRequestWithResponse(requestId, responseObj);
                                
                                // Process session-related responses
                                self._processSessionResponse(method, url, responseData, requestBody);
                                
                                // Log response
                                self._log('info', 'Fetch response:', response.status, url);
                            } catch (error) {
                                self._log('error', 'Error processing response:', error);
                            }
                        });
                        
                        return response;
                    })
                    .catch(error => {
                        // Capture error
                        const errorObj = {
                            id: requestId,
                            error: error.message,
                            timestamp: new Date().toISOString()
                        };
                        
                        // Update request with error
                        self._updateRequestWithError(requestId, errorObj);
                        
                        // Log error
                        self._log('error', 'Fetch error:', error.message, url);
                        
                        throw error;
                    });
            }
            
            // Pass through for non-Devin API requests
            return originalFetch.apply(this, arguments);
        };
        
        // Override XMLHttpRequest
        XMLHttpRequest.prototype.open = function(method, url, async, user, password) {
            this._devinMonitorData = {
                method: method,
                url: url
            };
            
            return originalXHROpen.apply(this, arguments);
        };
        
        XMLHttpRequest.prototype.send = function(data) {
            if (this._devinMonitorData && 
                typeof this._devinMonitorData.url === 'string' && 
                this._devinMonitorData.url.includes(self.config.apiDomain)) {
                
                const requestId = self._generateId();
                const method = this._devinMonitorData.method;
                const url = this._devinMonitorData.url;
                
                // Capture request
                const request = {
                    id: requestId,
                    url: url,
                    method: method,
                    body: data,
                    timestamp: new Date().toISOString(),
                    type: 'xhr'
                };
                
                // Store request ID on XHR object
                this._devinRequestId = requestId;
                
                // Store request
                self._storeRequest(request);
                
                // Process auth headers
                const authHeader = this.getRequestHeader('Authorization');
                if (authHeader) {
                    self._processAuthHeader(method, url, authHeader);
                }
                
                // Process session-related requests
                self._processSessionRequest(method, url, data);
                
                // Log request
                self._log('info', 'XHR request:', method, url);
                
                // Add response handler
                this.addEventListener('load', function() {
                    try {
                        const responseBody = this.responseText;
                        const responseData = responseBody ? JSON.parse(responseBody) : {};
                        
                        // Capture response
                        const responseObj = {
                            id: requestId,
                            status: this.status,
                            statusText: this.statusText,
                            body: self.config.captureResponses ? responseBody : '[Response body not captured]',
                            timestamp: new Date().toISOString(),
                            duration: new Date() - new Date(request.timestamp)
                        };
                        
                        // Update request with response
                        self._updateRequestWithResponse(requestId, responseObj);
                        
                        // Process session-related responses
                        self._processSessionResponse(method, url, responseData, data);
                        
                        // Log response
                        self._log('info', 'XHR response:', this.status, url);
                    } catch (error) {
                        self._log('error', 'Error processing XHR response:', error);
                    }
                });
                
                // Add error handler
                this.addEventListener('error', function(event) {
                    // Capture error
                    const errorObj = {
                        id: requestId,
                        error: 'Network error',
                        timestamp: new Date().toISOString()
                    };
                    
                    // Update request with error
                    self._updateRequestWithError(requestId, errorObj);
                    
                    // Log error
                    self._log('error', 'XHR error:', url);
                });
            }
            
            return originalXHRSend.apply(this, arguments);
        };
    },
    
    // Auth Monitoring
    _initAuthMonitoring: function() {
        const self = this;
        
        // Monitor localStorage
        const originalSetItem = Storage.prototype.setItem;
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
                self._storeAuthEvent(event);
                
                // Log event
                self._log('info', 'Storage set:', event.storage, key);
            }
            
            return originalSetItem.apply(this, arguments);
        };
        
        // Monitor localStorage.getItem
        const originalGetItem = Storage.prototype.getItem;
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
                self._storeAuthEvent(event);
                
                // Log event
                self._log('debug', 'Storage get:', event.storage, key);
            }
            
            return originalGetItem.apply(this, arguments);
        };
    },
    
    // Process auth header
    _processAuthHeader: function(method, url, authHeader) {
        // Capture auth header event
        const event = {
            type: 'request_header',
            method: method,
            url: url,
            header: 'Authorization',
            value: this.config.captureTokens ? authHeader : this._maskToken(authHeader),
            timestamp: new Date().toISOString()
        };
        
        // Store event
        this._storeAuthEvent(event);
        
        // Log event
        this._log('info', 'Auth header:', method, url);
    },
    
    // Session Monitoring
    _initSessionMonitoring: function() {
        // Session monitoring is handled by processing requests and responses
    },
    
    // Process session-related requests
    _processSessionRequest: function(method, url, body) {
        try {
            // Parse body if it's a string
            let bodyData = body;
            if (typeof body === 'string') {
                try {
                    bodyData = JSON.parse(body);
                } catch (e) {
                    // Not JSON, ignore
                    bodyData = null;
                }
            }
            
            // Session creation
            if (method === 'POST' && url.includes('/sessions') && bodyData) {
                this._log('debug', 'Session creation request detected');
            }
            
            // Message sending
            if (method === 'POST' && url.includes('/message') && bodyData) {
                const sessionId = this._extractSessionIdFromUrl(url);
                if (sessionId) {
                    this._log('debug', 'Message request detected for session:', sessionId);
                }
            }
        } catch (error) {
            this._log('error', 'Error processing session request:', error);
        }
    },
    
    // Process session-related responses
    _processSessionResponse: function(method, url, responseData, requestBody) {
        try {
            // Parse request body if it's a string
            let bodyData = requestBody;
            if (typeof requestBody === 'string') {
                try {
                    bodyData = JSON.parse(requestBody);
                } catch (e) {
                    // Not JSON, ignore
                    bodyData = null;
                }
            }
            
            // Session creation response
            if (method === 'POST' && url.includes('/sessions') && responseData.session_id) {
                const sessionId = responseData.session_id;
                
                // Create session object
                this.sessions[sessionId] = {
                    id: sessionId,
                    status: responseData.status || 'created',
                    created_at: new Date().toISOString(),
                    messages: [],
                    details: {
                        session_id: sessionId,
                        status: responseData.status || 'created',
                        prompt: bodyData ? bodyData.prompt : ''
                    }
                };
                
                this._log('info', 'Session created:', sessionId);
            }
            
            // Session details response
            if (method === 'GET' && url.includes('/session/') && !url.includes('/message')) {
                const sessionId = this._extractSessionIdFromUrl(url);
                if (sessionId && responseData) {
                    // Update session details
                    if (this.sessions[sessionId]) {
                        this.sessions[sessionId].details = responseData;
                        this._log('debug', 'Session details updated:', sessionId);
                    } else {
                        // Create session if it doesn't exist
                        this.sessions[sessionId] = {
                            id: sessionId,
                            status: responseData.status || 'unknown',
                            created_at: responseData.created_at || new Date().toISOString(),
                            messages: responseData.messages || [],
                            details: responseData
                        };
                        this._log('info', 'Session details captured:', sessionId);
                    }
                }
            }
            
            // Message response
            if (method === 'POST' && url.includes('/message')) {
                const sessionId = this._extractSessionIdFromUrl(url);
                if (sessionId && this.sessions[sessionId] && bodyData) {
                    // Add message to session
                    const message = {
                        session_id: sessionId,
                        direction: 'outgoing',
                        content: bodyData.message,
                        timestamp: new Date().toISOString(),
                        request_data: bodyData
                    };
                    
                    this.sessions[sessionId].messages.push(message);
                    this._log('info', 'Message sent:', sessionId);
                }
            }
        } catch (error) {
            this._log('error', 'Error processing session response:', error);
        }
    },
    
    // Extract session ID from URL
    _extractSessionIdFromUrl: function(url) {
        const match = url.match(/\/session\/([^\/]+)/);
        return match ? match[1] : null;
    },
    
    // Utility functions
    _generateId: function() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2, 5);
    },
    
    _getResponseHeaders: function(response) {
        const headers = {};
        if (response.headers && response.headers.forEach) {
            response.headers.forEach((value, name) => {
                headers[name] = value;
            });
        }
        return headers;
    },
    
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
            console.log(`[Devin Monitor] [${level.toUpperCase()}]`, ...args);
        }
    },
    
    _storeRequest: function(request) {
        this.requests.unshift(request);
        
        // Limit the number of stored requests
        if (this.requests.length > this.config.maxStoredRequests) {
            this.requests = this.requests.slice(0, this.config.maxStoredRequests);
        }
    },
    
    _updateRequestWithResponse: function(requestId, response) {
        const request = this.requests.find(req => req.id === requestId);
        if (request) {
            request.response = response;
        }
    },
    
    _updateRequestWithError: function(requestId, error) {
        const request = this.requests.find(req => req.id === requestId);
        if (request) {
            request.error = error;
        }
    },
    
    _storeAuthEvent: function(event) {
        this.authEvents.unshift(event);
        
        // Limit the number of stored events
        if (this.authEvents.length > this.config.maxStoredEvents) {
            this.authEvents = this.authEvents.slice(0, this.config.maxStoredEvents);
        }
    },
    
    // Public API
    getRequests: function() {
        return this.requests;
    },
    
    getRequest: function(id) {
        return this.requests.find(req => req.id === id);
    },
    
    getSessions: function() {
        return this.sessions;
    },
    
    getSession: function(id) {
        return this.sessions[id];
    },
    
    getCurrentSession: function() {
        // Get the most recently created session
        const sessionIds = Object.keys(this.sessions);
        if (sessionIds.length === 0) return null;
        
        let mostRecent = sessionIds[0];
        let mostRecentTime = new Date(this.sessions[mostRecent].created_at).getTime();
        
        for (let i = 1; i < sessionIds.length; i++) {
            const sessionTime = new Date(this.sessions[sessionIds[i]].created_at).getTime();
            if (sessionTime > mostRecentTime) {
                mostRecent = sessionIds[i];
                mostRecentTime = sessionTime;
            }
        }
        
        return this.sessions[mostRecent];
    },
    
    getMessages: function() {
        const messages = [];
        Object.values(this.sessions).forEach(session => {
            if (session.messages && session.messages.length > 0) {
                messages.push(...session.messages);
            }
        });
        return messages;
    },
    
    getSessionMessages: function(sessionId) {
        if (this.sessions[sessionId] && this.sessions[sessionId].messages) {
            return this.sessions[sessionId].messages;
        }
        return [];
    },
    
    getAuthEvents: function() {
        return this.authEvents;
    },
    
    analyze: function(requestId) {
        const request = this.getRequest(requestId);
        if (!request) {
            return { error: 'Request not found' };
        }
        
        // Extract endpoint type
        let endpoint = 'Unknown';
        if (request.url.includes('/sessions')) {
            endpoint = 'Session Creation';
        } else if (request.url.includes('/session/') && request.url.includes('/message')) {
            endpoint = 'Message Sending';
        } else if (request.url.includes('/session/')) {
            endpoint = 'Session Details';
        } else if (request.url.includes('/attachments')) {
            endpoint = 'File Attachment';
        }
        
        // Calculate timing
        const timing = {
            requestTime: request.timestamp
        };
        
        if (request.response) {
            timing.responseTime = request.response.timestamp;
            timing.duration = request.response.duration;
        }
        
        return {
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
            error: request.error || null,
            endpoint: endpoint,
            timing: timing
        };
    },
    
    summarize: function() {
        // Count requests by endpoint
        const endpoints = {};
        const methods = {};
        const statusCodes = {};
        let totalDuration = 0;
        let requestCount = 0;
        
        this.requests.forEach(request => {
            // Endpoint
            let endpoint = 'Unknown';
            if (request.url.includes('/sessions')) {
                endpoint = 'Session Creation';
            } else if (request.url.includes('/session/') && request.url.includes('/message')) {
                endpoint = 'Message Sending';
            } else if (request.url.includes('/session/')) {
                endpoint = 'Session Details';
            } else if (request.url.includes('/attachments')) {
                endpoint = 'File Attachment';
            }
            
            endpoints[endpoint] = (endpoints[endpoint] || 0) + 1;
            
            // Method
            methods[request.method] = (methods[request.method] || 0) + 1;
            
            // Status code
            if (request.response) {
                statusCodes[request.response.status] = (statusCodes[request.response.status] || 0) + 1;
                
                // Duration
                if (request.response.duration) {
                    totalDuration += request.response.duration;
                    requestCount++;
                }
            }
        });
        
        // Session stats
        const sessionCount = Object.keys(this.sessions).length;
        const messageCount = this.getMessages().length;
        
        // Auth stats
        const authEventTypes = {};
        this.authEvents.forEach(event => {
            authEventTypes[event.type] = (authEventTypes[event.type] || 0) + 1;
        });
        
        return {
            requestStats: {
                total: this.requests.length,
                byEndpoint: endpoints,
                byMethod: methods,
                byStatusCode: statusCodes,
                averageDuration: requestCount > 0 ? totalDuration / requestCount : 0
            },
            sessionStats: {
                sessionCount: sessionCount,
                messageCount: messageCount
            },
            authStats: {
                total: this.authEvents.length,
                byType: authEventTypes
            },
            timestamp: new Date().toISOString()
        };
    },
    
    clear: function() {
        this.requests = [];
        this.authEvents = [];
        this.sessions = {};
        this._log('info', 'Monitor data cleared');
    },
    
    export: function() {
        const data = {
            requests: this.requests,
            authEvents: this.authEvents,
            sessions: this.sessions,
            summary: this.summarize(),
            exportTime: new Date().toISOString()
        };
        
        // Create download link
        const dataStr = JSON.stringify(data, null, 2);
        const blob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.setAttribute('href', url);
        a.setAttribute('download', `devin-monitor-export-${Date.now()}.json`);
        a.click();
        
        return data;
    },
    
    help: function() {
        console.log(`
Devin Combined Monitor - Help
============================

Available commands:

getRequests()           - Get all captured API requests
getRequest(id)          - Get a specific request by ID
getSessions()           - Get all captured sessions
getSession(id)          - Get a specific session by ID
getCurrentSession()     - Get the most recent session
getMessages()           - Get all captured messages
getSessionMessages(id)  - Get messages for a specific session
getAuthEvents()         - Get all captured authentication events
analyze(id)             - Analyze a specific request
summarize()             - Summarize all captured data
clear()                 - Clear all captured data
export()                - Export all data as JSON
help()                  - Show this help message

Configuration:
config.apiDomain        - Domain to monitor (default: 'api.devin.ai')
config.logLevel         - Log level (default: 'info')
config.captureResponses - Whether to capture response bodies (default: true)
config.captureTokens    - Whether to capture actual tokens (default: false)
        `);
    }
};

// Initialize the monitor
devin.init();

console.log('Devin Combined Monitor loaded successfully');
