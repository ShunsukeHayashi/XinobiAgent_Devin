/**
 * DevTools script for the Devin API Monitor extension.
 * 
 * This script creates a new panel in the DevTools.
 */

console.log('Devin API Monitor DevTools script loaded');

// Create a new panel in DevTools
chrome.devtools.panels.create(
  "Devin API",
  null,
  "panel.html",
  function(panel) {
    // Panel created
    console.log("Devin API panel created");
    
    // Add panel shown event listener
    panel.onShown.addListener(function(window) {
      // Panel is shown
      console.log("Devin API panel shown");
      
      // Initialize the panel
      if (window.initPanel) {
        window.initPanel();
      }
    });
    
    // Add panel hidden event listener
    panel.onHidden.addListener(function() {
      // Panel is hidden
      console.log("Devin API panel hidden");
    });
  }
);

// Create a new network request sidebar pane
chrome.devtools.network.onRequestFinished.addListener(function(request) {
  // Check if the request is to the Devin API
  if (request.request.url.includes('api.devin.ai')) {
    // Get the request and response details
    const requestDetails = {
      url: request.request.url,
      method: request.request.method,
      headers: request.request.headers,
      body: request.request.postData?.text || '',
      timestamp: new Date().toISOString()
    };
    
    const responseDetails = {
      status: request.response.status,
      statusText: request.response.statusText,
      headers: request.response.headers,
      timestamp: new Date().toISOString()
    };
    
    // Get the response body
    request.getContent(function(content, encoding) {
      responseDetails.body = content;
      
      // Send the details to the panel
      chrome.runtime.sendMessage({
        action: 'networkRequest',
        request: requestDetails,
        response: responseDetails
      });
    });
  }
});

// Create a sidebar pane for Devin API analysis
chrome.devtools.panels.elements.createSidebarPane(
  "Devin API",
  function(sidebar) {
    // Set sidebar content
    sidebar.setObject({ 
      title: "Devin API Monitor",
      description: "Select a network request to view details"
    });
    
    // Update sidebar when a network request is selected
    chrome.devtools.network.onRequestFinished.addListener(function(request) {
      if (request.request.url.includes('api.devin.ai')) {
        sidebar.setObject({
          title: "Devin API Request",
          url: request.request.url,
          method: request.request.method,
          status: request.response.status
        });
      }
    });
  }
);

console.log('Devin API Monitor DevTools script initialized');
