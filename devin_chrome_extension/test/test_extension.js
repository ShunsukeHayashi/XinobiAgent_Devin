/**
 * Test script for the Devin API Monitor extension.
 * 
 * This script provides utilities for testing the extension.
 */

// Mock Devin API requests for testing
function mockDevinApiRequests() {
  console.log('Mocking Devin API requests...');
  
  // Mock session creation request
  mockRequest(
    'POST',
    'https://api.devin.ai/v1/sessions',
    {
      prompt: 'Create a simple React app',
      playbook_id: null
    },
    {
      session_id: 'session-123456',
      status: 'created'
    },
    200
  );
  
  // Mock session details request
  mockRequest(
    'GET',
    'https://api.devin.ai/v1/session/session-123456',
    null,
    {
      session_id: 'session-123456',
      status: 'running',
      created_at: new Date().toISOString(),
      prompt: 'Create a simple React app'
    },
    200
  );
  
  // Mock message sending request
  mockRequest(
    'POST',
    'https://api.devin.ai/v1/session/session-123456/message',
    {
      message: 'Add a login page'
    },
    {
      success: true
    },
    200
  );
  
  // Mock file upload request
  mockRequest(
    'POST',
    'https://api.devin.ai/v1/attachments',
    {
      file: 'mock-file-data'
    },
    {
      attachment_id: 'attachment-123456',
      url: 'https://api.devin.ai/v1/attachments/attachment-123456'
    },
    200
  );
  
  console.log('Mocked 4 Devin API requests');
}

// Mock a request
function mockRequest(method, url, requestBody, responseBody, statusCode) {
  // Create request ID
  const requestId = Date.now().toString() + Math.random().toString(36).substring(2, 15);
  
  // Create request event
  const requestEvent = new CustomEvent('devinApiRequest', {
    detail: {
      method: method,
      url: url,
      requestBody: requestBody ? JSON.stringify(requestBody) : null,
      timestamp: new Date().toISOString()
    }
  });
  
  // Create response event
  const responseEvent = new CustomEvent('devinApiRequest', {
    detail: {
      method: method,
      url: url,
      responseBody: responseBody ? JSON.stringify(responseBody) : null,
      status: statusCode,
      timestamp: new Date(Date.now() + 500).toISOString()
    }
  });
  
  // Dispatch request event
  document.dispatchEvent(requestEvent);
  
  // Dispatch response event after a delay
  setTimeout(() => {
    document.dispatchEvent(responseEvent);
  }, 500);
}

// Test the extension
function testExtension() {
  console.log('Testing Devin API Monitor extension...');
  
  // Mock API requests
  mockDevinApiRequests();
  
  // Test console commands
  setTimeout(() => {
    console.log('Testing console commands...');
    
    // Test help command
    console.log('Testing devin.help command:');
    if (typeof devin.help === 'function') {
      devin.help();
    } else {
      console.error('devin.help command not found');
    }
    
    // Test requests command
    console.log('Testing devin.requests command:');
    if (typeof devin.requests === 'function') {
      devin.requests();
    } else {
      console.error('devin.requests command not found');
    }
    
    // Test sessions command
    console.log('Testing devin.sessions command:');
    if (typeof devin.sessions === 'function') {
      devin.sessions();
    } else {
      console.error('devin.sessions command not found');
    }
    
    console.log('Test complete');
  }, 1000);
}

// Export test functions
window.testDevinExtension = {
  mockDevinApiRequests: mockDevinApiRequests,
  testExtension: testExtension
};

console.log('Devin API Monitor test script loaded');
