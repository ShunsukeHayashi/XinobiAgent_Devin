/**
 * Page script for the Devin API Monitor extension.
 * 
 * This script is injected into the page to monitor XHR and fetch requests.
 */

(function() {
  // Check if the script is already injected
  if (window.__devinMonitorInjected) return;
  window.__devinMonitorInjected = true;
  
  console.log('Devin API Monitor page script injected');
  
  // Store original XMLHttpRequest
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
    if (this._url && this._url.includes('api.devin.ai')) {
      // Store request data
      this._requestBody = body;
      
      // Add event listener for load
      this.addEventListener('load', function() {
        // Create event with request and response data
        const event = new CustomEvent('devinApiRequest', {
          detail: {
            method: this._method,
            url: this._url,
            requestBody: this._requestBody,
            responseBody: this.responseText,
            status: this.status,
            timestamp: new Date().toISOString()
          }
        });
        
        // Dispatch event
        document.dispatchEvent(event);
      });
    }
    
    return originalXhrSend.apply(this, arguments);
  };
  
  // Store original fetch
  const originalFetch = window.fetch;
  
  // Override fetch
  window.fetch = async function(input, init) {
    // Get URL
    const url = typeof input === 'string' ? input : input.url;
    
    // Only monitor requests to the Devin API
    if (url && url.includes('api.devin.ai')) {
      // Store request data
      const method = init?.method || 'GET';
      const requestBody = init?.body;
      
      try {
        // Call original fetch
        const response = await originalFetch.apply(this, arguments);
        
        // Clone the response to read the body
        const clonedResponse = response.clone();
        const responseBody = await clonedResponse.text();
        
        // Create event with request and response data
        const event = new CustomEvent('devinApiRequest', {
          detail: {
            method: method,
            url: url,
            requestBody: requestBody,
            responseBody: responseBody,
            status: response.status,
            timestamp: new Date().toISOString()
          }
        });
        
        // Dispatch event
        document.dispatchEvent(event);
        
        return response;
      } catch (error) {
        // Create event with error data
        const event = new CustomEvent('devinApiRequest', {
          detail: {
            method: method,
            url: url,
            requestBody: requestBody,
            error: error.toString(),
            timestamp: new Date().toISOString()
          }
        });
        
        // Dispatch event
        document.dispatchEvent(event);
        
        throw error;
      }
    }
    
    // Call original fetch for non-Devin API requests
    return originalFetch.apply(this, arguments);
  };
  
  // Listen for devinApiRequest events
  document.addEventListener('devinApiRequest', function(event) {
    // Send the data to the content script
    window.postMessage({
      type: 'devinApiRequest',
      data: event.detail
    }, '*');
  });
  
  // Collect page information
  function collectPageInfo() {
    return {
      url: window.location.href,
      title: document.title,
      timestamp: new Date().toISOString()
    };
  }
  
  // Send page information to the content script
  window.postMessage({
    type: 'devinPageInfo',
    data: collectPageInfo()
  }, '*');
  
  console.log('Devin API Monitor page script initialized');
})();
