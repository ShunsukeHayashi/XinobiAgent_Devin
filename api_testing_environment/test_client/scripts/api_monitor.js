/**
 * Devin API Monitor
 * 
 * This script monitors API requests to the Devin API,
 * capturing request and response data for analysis.
 */

// Create the devinApi namespace
const devinApi = {
    // Configuration
    config: {
        apiDomain: 'api.devin.ai',
        logLevel: 'info', // 'debug', 'info', 'warn', 'error'
        captureResponses: true,
        maxStoredRequests: 100
    },
    
    // Storage for requests
    requests: [],
    
    // Initialize the monitor
    init: function() {
        console.log('Devin API Monitor initialized');
        console.log('Monitoring API domain:', this.config.apiDomain);
        
        // Monitor fetch requests
        this._monitorFetch();
        
        // Monitor XHR requests
        this._monitorXHR();
        
        return this;
    },
    
    // Monitor fetch requests
    _monitorFetch: function() {
        const originalFetch = window.fetch;
        const self = this;
        
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
                
                // Make the actual request
                return originalFetch.apply(this, arguments)
                    .then(response => {
                        // Clone the response so we can read the body
                        const clonedResponse = response.clone();
                        
                        // Process the response
                        clonedResponse.text().then(responseBody => {
                            try {
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
    },
    
    // Monitor XHR requests
    _monitorXHR: function() {
        const originalXHROpen = XMLHttpRequest.prototype.open;
        const originalXHRSend = XMLHttpRequest.prototype.send;
        const self = this;
        
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
                
                // Log request
                self._log('info', 'XHR request:', method, url);
                
                // Add response handler
                this.addEventListener('load', function() {
                    try {
                        const responseBody = this.responseText;
                        
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
    
    _log: function(level, ...args) {
        const levels = {
            debug: 0,
            info: 1,
            warn: 2,
            error: 3
        };
        
        if (levels[level] >= levels[this.config.logLevel]) {
            console.log(`[Devin API Monitor] [${level.toUpperCase()}]`, ...args);
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
    
    // Public API
    getRequests: function() {
        return this.requests;
    },
    
    getRequest: function(id) {
        return this.requests.find(req => req.id === id);
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
        
        return {
            total: this.requests.length,
            byEndpoint: endpoints,
            byMethod: methods,
            byStatusCode: statusCodes,
            averageDuration: requestCount > 0 ? totalDuration / requestCount : 0,
            timestamp: new Date().toISOString()
        };
    },
    
    clear: function() {
        this.requests = [];
        this._log('info', 'Requests cleared');
    },
    
    export: function() {
        const data = {
            requests: this.requests,
            summary: this.summarize(),
            exportTime: new Date().toISOString()
        };
        
        // Create download link
        const dataStr = JSON.stringify(data, null, 2);
        const blob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.setAttribute('href', url);
        a.setAttribute('download', `devin-api-monitor-export-${Date.now()}.json`);
        a.click();
        
        return data;
    },
    
    help: function() {
        console.log(`
Devin API Monitor - Help
=======================

Available commands:

getRequests()       - Get all captured API requests
getRequest(id)      - Get a specific request by ID
analyze(id)         - Analyze a specific request
summarize()         - Summarize all captured requests
clear()             - Clear all captured requests
export()            - Export all data as JSON
help()              - Show this help message

Configuration:
config.apiDomain        - Domain to monitor (default: 'api.devin.ai')
config.logLevel         - Log level (default: 'info')
config.captureResponses - Whether to capture response bodies (default: true)
        `);
    }
};

// Initialize the monitor
devinApi.init();

console.log('Devin API Monitor loaded successfully');
