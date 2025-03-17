/**
 * Background script for the Devin API Monitor extension.
 * 
 * This script intercepts network requests to the Devin API and logs them.
 */

// Import the network monitor
importScripts('network_monitor.js');

// Define the API base URL
const DEVIN_API_BASE_URL = 'https://api.devin.ai/v1';

// Initialize storage for API requests
let apiRequests = [];

// Function to extract endpoint from URL
function extractEndpoint(url) {
  // Remove base URL
  const path = url.replace(DEVIN_API_BASE_URL, '');
  // Extract endpoint
  const endpoint = path.split('?')[0];
  return endpoint;
}

// Function to categorize request by endpoint
function categorizeRequest(url) {
  const endpoint = extractEndpoint(url);
  
  if (endpoint === '/sessions') {
    return 'sessions';
  } else if (endpoint.startsWith('/session/')) {
    if (endpoint.endsWith('/message')) {
      return 'message';
    } else {
      return 'session';
    }
  } else if (endpoint === '/secrets') {
    return 'secrets';
  } else if (endpoint.startsWith('/secrets/')) {
    return 'secret';
  } else if (endpoint === '/attachments') {
    return 'attachment';
  } else {
    return 'other';
  }
}

// Listen for tab updates to inject the page script
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url && 
      (tab.url.includes('app.devin.ai') || tab.url.includes('api.devin.ai'))) {
    // Inject the page script
    chrome.scripting.executeScript({
      target: { tabId: tabId },
      files: ['js/page_script.js']
    }).catch(error => {
      console.error('Error injecting page script:', error);
    });
  }
});

// Listen for messages from the content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'pageInfo') {
    // Store page info
    const tabId = sender.tab.id;
    chrome.storage.local.set({ [`pageInfo_${tabId}`]: message.data });
    sendResponse({ success: true });
  }
  return true;
});

console.log('Devin API Monitor background script loaded');
