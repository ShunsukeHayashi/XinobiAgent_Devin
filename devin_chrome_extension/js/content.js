/**
 * Content script for the Devin API Monitor extension.
 * 
 * This script runs in the context of web pages and can interact with the page's DOM.
 */

console.log('Devin API Monitor content script loaded');

// Function to extract session ID from the page URL
function extractSessionId() {
  const url = window.location.href;
  const match = url.match(/\/session\/([^\/]+)/);
  return match ? match[1] : null;
}

// Listen for messages from the page script
window.addEventListener('message', function(event) {
  // Only accept messages from the same window
  if (event.source !== window) return;
  
  // Check if the message is from our page script
  if (event.data.type === 'devinApiRequest') {
    // Send the data to the background script
    chrome.runtime.sendMessage({
      action: 'apiRequest',
      data: event.data.data
    });
  } else if (event.data.type === 'devinPageInfo') {
    // Add session ID if available
    const pageInfo = event.data.data;
    pageInfo.sessionId = extractSessionId();
    
    // Send the page info to the background script
    chrome.runtime.sendMessage({
      action: 'pageInfo',
      data: pageInfo
    });
  }
});

// Listen for messages from the background script
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === 'getPageInfo') {
    // Extract information from the page
    const pageInfo = {
      url: window.location.href,
      title: document.title,
      sessionId: extractSessionId(),
      timestamp: new Date().toISOString()
    };
    
    // Send the information back
    sendResponse({ pageInfo: pageInfo });
  }
  // Return true to indicate that the response will be sent asynchronously
  return true;
});

// Inject the page script
function injectPageScript() {
  // Check if we're on a Devin page
  if (window.location.href.includes('app.devin.ai') || window.location.href.includes('api.devin.ai')) {
    console.log('Injecting page script');
    
    // Create script element
    const script = document.createElement('script');
    script.src = chrome.runtime.getURL('js/page_script.js');
    
    // Append the script to the document
    (document.head || document.documentElement).appendChild(script);
    
    // Remove the script after it has been loaded
    script.onload = function() {
      script.remove();
    };
  }
}

// Inject the page script when the content script loads
injectPageScript();

console.log('Devin API Monitor content script initialized');
