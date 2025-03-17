/**
 * Console integration for the Devin API Monitor extension.
 * 
 * This script provides utilities for integrating with the Chrome Developer Console.
 */

// Console integration class
class DevinConsoleIntegration {
  constructor() {
    this.initialized = false;
    this.commands = {};
  }

  // Initialize the integration
  initialize() {
    if (this.initialized) return;
    
    // Register commands
    this.registerCommands();
    
    this.initialized = true;
    console.log('Devin Console Integration initialized');
  }

  // Register console commands
  registerCommands() {
    // Register devin.help command
    this.registerCommand('devin.help', this.helpCommand, 'Show help for Devin API Monitor commands');
    
    // Register devin.requests command
    this.registerCommand('devin.requests', this.requestsCommand, 'Show captured API requests');
    
    // Register devin.sessions command
    this.registerCommand('devin.sessions', this.sessionsCommand, 'Show session creation requests');
    
    // Register devin.messages command
    this.registerCommand('devin.messages', this.messagesCommand, 'Show message sending requests');
    
    // Register devin.clear command
    this.registerCommand('devin.clear', this.clearCommand, 'Clear captured requests');
    
    // Register devin.analyze command
    this.registerCommand('devin.analyze', this.analyzeCommand, 'Analyze a specific request');
  }

  // Register a command
  registerCommand(name, callback, description) {
    // Store command
    this.commands[name] = {
      callback: callback.bind(this),
      description: description
    };
    
    // Define command in console
    window[name] = (...args) => {
      return this.commands[name].callback(...args);
    };
  }

  // Help command
  helpCommand() {
    console.log('Devin API Monitor Console Commands:');
    
    // List all commands
    Object.keys(this.commands).forEach(name => {
      console.log(`${name}: ${this.commands[name].description}`);
    });
    
    return 'Use these commands to interact with the Devin API Monitor';
  }

  // Requests command
  requestsCommand(filter) {
    // Get requests from network monitor
    const requests = window.devinNetworkMonitor?.getRequests() || [];
    
    // Filter requests if filter is provided
    const filteredRequests = filter
      ? requests.filter(req => JSON.stringify(req).includes(filter))
      : requests;
    
    // Log requests
    console.log(`Captured ${filteredRequests.length} requests:`);
    console.table(filteredRequests.map(req => ({
      id: req.id,
      method: req.method,
      url: req.url,
      type: req.type,
      timestamp: req.timestamp
    })));
    
    return filteredRequests;
  }

  // Sessions command
  sessionsCommand() {
    // Get session creation requests from network monitor
    const requests = window.devinNetworkMonitor?.getSessionCreationRequests() || [];
    
    // Log requests
    console.log(`Captured ${requests.length} session creation requests:`);
    console.table(requests.map(req => ({
      id: req.id,
      method: req.method,
      url: req.url,
      timestamp: req.timestamp
    })));
    
    return requests;
  }

  // Messages command
  messagesCommand() {
    // Get message sending requests from network monitor
    const requests = window.devinNetworkMonitor?.getMessageSendingRequests() || [];
    
    // Log requests
    console.log(`Captured ${requests.length} message sending requests:`);
    console.table(requests.map(req => ({
      id: req.id,
      method: req.method,
      url: req.url,
      timestamp: req.timestamp
    })));
    
    return requests;
  }

  // Clear command
  clearCommand() {
    // Clear requests in network monitor
    window.devinNetworkMonitor?.clearRequests();
    
    console.log('Cleared all captured requests');
    
    return true;
  }

  // Analyze command
  analyzeCommand(requestId) {
    // Get requests from network monitor
    const requests = window.devinNetworkMonitor?.getRequests() || [];
    
    // Find request and response
    const request = requests.find(req => req.id === requestId && req.type === 'request');
    const response = requests.find(req => req.id === requestId && req.type === 'response');
    
    if (!request) {
      console.error(`Request with ID ${requestId} not found`);
      return null;
    }
    
    // Create analysis
    const analysis = {
      request: {
        url: request.url,
        method: request.method,
        timestamp: request.timestamp,
        body: request.requestBody
      },
      response: response ? {
        statusCode: response.statusCode,
        timestamp: response.timestamp,
        body: response.responseBody
      } : null,
      endpoint: this.categorizeEndpoint(request.url),
      timing: response ? this.calculateTiming(request.timestamp, response.timestamp) : null
    };
    
    // Log analysis
    console.log('Request Analysis:');
    console.log(analysis);
    
    return analysis;
  }

  // Categorize endpoint
  categorizeEndpoint(url) {
    // Extract endpoint
    const match = url.match(/\/v1(\/[^?]*)/);
    const endpoint = match ? match[1] : '';
    
    if (endpoint === '/sessions') {
      return 'Session Creation';
    } else if (endpoint.startsWith('/session/')) {
      if (endpoint.endsWith('/message')) {
        return 'Message Sending';
      } else {
        return 'Session Details';
      }
    } else if (endpoint === '/secrets') {
      return 'Secrets List';
    } else if (endpoint.startsWith('/secrets/')) {
      return 'Secret Management';
    } else if (endpoint === '/attachments') {
      return 'File Upload';
    } else {
      return 'Other';
    }
  }

  // Calculate timing
  calculateTiming(requestTimestamp, responseTimestamp) {
    const requestTime = new Date(requestTimestamp);
    const responseTime = new Date(responseTimestamp);
    
    return {
      duration: responseTime - requestTime,
      requestTime: requestTimestamp,
      responseTime: responseTimestamp
    };
  }
}

// Create and export the integration instance
const consoleIntegration = new DevinConsoleIntegration();
consoleIntegration.initialize();

// Export the integration
window.devinConsoleIntegration = consoleIntegration;
