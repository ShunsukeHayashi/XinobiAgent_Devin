/**
 * Popup script for the Devin API Monitor extension.
 * 
 * This script handles the popup UI and functionality.
 */

// DOM elements
const monitoringStatusEl = document.getElementById('monitoringStatus');
const requestCountEl = document.getElementById('requestCount');
const sessionCountEl = document.getElementById('sessionCount');
const messageCountEl = document.getElementById('messageCount');
const openDevToolsBtn = document.getElementById('openDevToolsBtn');
const clearDataBtn = document.getElementById('clearDataBtn');
const exportDataBtn = document.getElementById('exportDataBtn');

// Initialize the popup
function initPopup() {
  // Get request statistics
  chrome.runtime.sendMessage({ action: 'getRequests' }, function(response) {
    if (response && response.requests) {
      updateStatistics(response.requests);
    }
  });
  
  // Set up event listeners
  openDevToolsBtn.addEventListener('click', openDevTools);
  clearDataBtn.addEventListener('click', clearData);
  exportDataBtn.addEventListener('click', exportData);
}

// Update statistics
function updateStatistics(requests) {
  // Count total requests
  requestCountEl.textContent = requests.length;
  
  // Count sessions created
  const sessionCreations = requests.filter(req => {
    return req.url && req.url.endsWith('/sessions') && req.method === 'POST';
  });
  sessionCountEl.textContent = sessionCreations.length;
  
  // Count messages sent
  const messagesSent = requests.filter(req => {
    return req.url && req.url.includes('/message') && req.method === 'POST';
  });
  messageCountEl.textContent = messagesSent.length;
}

// Open DevTools panel
function openDevTools() {
  // Open DevTools if not already open
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    if (tabs.length > 0) {
      chrome.tabs.create({
        url: "chrome-devtools://devtools/bundled/devtools_app.html",
        active: true
      });
    }
  });
}

// Clear data
function clearData() {
  // Send message to background script
  chrome.runtime.sendMessage({ action: 'clearRequests' }, function(response) {
    if (response && response.success) {
      // Update statistics
      requestCountEl.textContent = '0';
      sessionCountEl.textContent = '0';
      messageCountEl.textContent = '0';
    }
  });
}

// Export data
function exportData() {
  // Get requests
  chrome.runtime.sendMessage({ action: 'getRequests' }, function(response) {
    if (response && response.requests) {
      // Create export data
      const exportData = {
        requests: response.requests,
        exportTime: new Date().toISOString()
      };
      
      // Convert to JSON
      const jsonData = JSON.stringify(exportData, null, 2);
      
      // Create blob
      const blob = new Blob([jsonData], { type: 'application/json' });
      
      // Create URL
      const url = URL.createObjectURL(blob);
      
      // Create download link
      const a = document.createElement('a');
      a.href = url;
      a.download = `devin-api-requests-${formatDateForFilename(new Date())}.json`;
      
      // Trigger download
      document.body.appendChild(a);
      a.click();
      
      // Clean up
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
  });
}

// Helper function to format date for filename
function formatDateForFilename(date) {
  return date.toISOString().replace(/:/g, '-').replace(/\..+/, '');
}

// Initialize the popup when the DOM is ready
document.addEventListener('DOMContentLoaded', initPopup);
