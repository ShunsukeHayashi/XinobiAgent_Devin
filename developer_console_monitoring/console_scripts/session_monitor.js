/**
 * Devin Session Monitor
 * 
 * This script monitors session-related API requests for the Devin API,
 * tracking session creation, updates, and messages.
 */

// Create the devinSession namespace
const devinSession = {
    // Configuration
    config: {
        apiDomain: 'api.devin.ai',
        logLevel: 'info', // 'debug', 'info', 'warn', 'error'
        maxStoredSessions: 20
    },
    
    // Storage for sessions
    sessions: {},
    
    // Initialize the monitor
    init: function() {
        console.log('Devin Session Monitor initialized');
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
                const method = options.method || 'GET';
                const requestBody = options.body || null;
                
                // Process request
                self._processRequest(method, url, requestBody);
                
                // Process response
                return originalFetch.apply(this, arguments)
                    .then(response => {
                        // Clone the response so we can read the body
                        const clonedResponse = response.clone();
                        
                        // Process the response
                        clonedResponse.text().then(responseBody => {
                            try {
                                const responseData = responseBody ? JSON.parse(responseBody) : {};
                                self._processResponse(method, url, responseData, requestBody);
                            } catch (error) {
                                self._log('error', 'Error processing response:', error);
                            }
                        });
                        
                        return response;
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
                
                const method = this._devinMonitorData.method;
                const url = this._devinMonitorData.url;
                
                // Process request
                self._processRequest(method, url, data);
                
                // Add response handler
                this.addEventListener('load', function() {
                    try {
                        const responseBody = this.responseText;
                        const responseData = responseBody ? JSON.parse(responseBody) : {};
                        self._processResponse(method, url, responseData, data);
                    } catch (error) {
                        self._log('error', 'Error processing XHR response:', error);
                    }
                });
            }
            
            return originalXHRSend.apply(this, arguments);
        };
    },
    
    // Process request
    _processRequest: function(method, url, body) {
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
            this._log('error', 'Error processing request:', error);
        }
    },
    
    // Process response
    _processResponse: function(method, url, responseData, requestBody) {
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
            this._log('error', 'Error processing response:', error);
        }
    },
    
    // Extract session ID from URL
    _extractSessionIdFromUrl: function(url) {
        const match = url.match(/\/session\/([^\/]+)/);
        return match ? match[1] : null;
    },
    
    // Utility functions
    _log: function(level, ...args) {
        const levels = {
            debug: 0,
            info: 1,
            warn: 2,
            error: 3
        };
        
        if (levels[level] >= levels[this.config.logLevel]) {
            console.log(`[Devin Session Monitor] [${level.toUpperCase()}]`, ...args);
        }
    },
    
    // Public API
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
    
    clearSessions: function() {
        this.sessions = {};
        this._log('info', 'Sessions cleared');
    },
    
    summarize: function() {
        const sessionCount = Object.keys(this.sessions).length;
        const messageCount = this.getMessages().length;
        
        // Count sessions by status
        const statusCounts = {};
        Object.values(this.sessions).forEach(session => {
            statusCounts[session.status] = (statusCounts[session.status] || 0) + 1;
        });
        
        return {
            sessionCount: sessionCount,
            messageCount: messageCount,
            byStatus: statusCounts,
            timestamp: new Date().toISOString()
        };
    },
    
    export: function() {
        const data = {
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
        a.setAttribute('download', `devin-session-monitor-export-${Date.now()}.json`);
        a.click();
        
        return data;
    },
    
    help: function() {
        console.log(`
Devin Session Monitor - Help
===========================

Available commands:

getSessions()           - Get all captured sessions
getSession(id)          - Get a specific session by ID
getCurrentSession()     - Get the most recent session
getMessages()           - Get all captured messages
getSessionMessages(id)  - Get messages for a specific session
clearSessions()         - Clear all captured sessions
summarize()             - Summarize all captured sessions
export()                - Export all data as JSON
help()                  - Show this help message

Configuration:
config.apiDomain        - Domain to monitor (default: 'api.devin.ai')
config.logLevel         - Log level (default: 'info')
        `);
    }
};

// Initialize the monitor
devinSession.init();

console.log('Devin Session Monitor loaded successfully');
