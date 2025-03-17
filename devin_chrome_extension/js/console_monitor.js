/**
 * Console monitor for the Devin API Monitor extension.
 * 
 * This script provides utilities for monitoring console output.
 */

// Console monitor class
class DevinConsoleMonitor {
  constructor() {
    this.logs = [];
    this.listeners = [];
    this.initialized = false;
    this.filter = 'devin';
  }

  // Initialize the monitor
  initialize() {
    if (this.initialized) return;
    
    // Set up console overrides
    this.setupConsoleOverrides();
    
    this.initialized = true;
    console.log('Devin Console Monitor initialized');
  }

  // Set up console overrides
  setupConsoleOverrides() {
    // Store original console methods
    const originalConsole = {
      log: console.log,
      info: console.info,
      warn: console.warn,
      error: console.error,
      debug: console.debug
    };

    // Override console.log
    console.log = (...args) => {
      // Call original method
      originalConsole.log.apply(console, args);
      
      // Process log
      this.processLog('log', args);
    };

    // Override console.info
    console.info = (...args) => {
      // Call original method
      originalConsole.info.apply(console, args);
      
      // Process log
      this.processLog('info', args);
    };

    // Override console.warn
    console.warn = (...args) => {
      // Call original method
      originalConsole.warn.apply(console, args);
      
      // Process log
      this.processLog('warn', args);
    };

    // Override console.error
    console.error = (...args) => {
      // Call original method
      originalConsole.error.apply(console, args);
      
      // Process log
      this.processLog('error', args);
    };

    // Override console.debug
    console.debug = (...args) => {
      // Call original method
      originalConsole.debug.apply(console, args);
      
      // Process log
      this.processLog('debug', args);
    };
  }

  // Process a log
  processLog(type, args) {
    // Check if the log contains the filter
    const logString = args.map(arg => {
      if (typeof arg === 'object') {
        try {
          return JSON.stringify(arg);
        } catch (e) {
          return String(arg);
        }
      }
      return String(arg);
    }).join(' ');
    
    // Only process logs that contain the filter
    if (this.filter && !logString.toLowerCase().includes(this.filter.toLowerCase())) {
      return;
    }
    
    // Create log object
    const log = {
      type: type,
      args: args,
      timestamp: new Date().toISOString()
    };
    
    // Store the log
    this.logs.push(log);
    
    // Notify listeners
    this.notifyListeners('newLog', log);
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

  // Clear all logs
  clearLogs() {
    this.logs = [];
    this.notifyListeners('logsCleared');
  }

  // Get all logs
  getLogs() {
    return this.logs;
  }

  // Set the filter
  setFilter(filter) {
    this.filter = filter;
  }

  // Get logs by type
  getLogsByType(type) {
    return this.logs.filter(log => log.type === type);
  }

  // Get logs containing a string
  getLogsByContent(content) {
    return this.logs.filter(log => {
      const logString = log.args.map(arg => {
        if (typeof arg === 'object') {
          try {
            return JSON.stringify(arg);
          } catch (e) {
            return String(arg);
          }
        }
        return String(arg);
      }).join(' ');
      
      return logString.toLowerCase().includes(content.toLowerCase());
    });
  }
}

// Create and export the monitor instance
const consoleMonitor = new DevinConsoleMonitor();
consoleMonitor.initialize();

// Export the monitor
window.devinConsoleMonitor = consoleMonitor;
