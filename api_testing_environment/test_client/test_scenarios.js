/**
 * Test Scenarios for Devin API
 * 
 * This script provides predefined test scenarios for the Devin API.
 */

// Test Scenario 1: Complete Workflow
async function testCompleteWorkflow() {
    console.log('Running Test Scenario 1: Complete Workflow');
    
    // Step 1: Login
    const loginResponse = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: 'test@example.com',
            password: 'password123'
        })
    });
    
    const loginData = await loginResponse.json();
    const token = loginData.token;
    
    console.log('Step 1: Login completed', loginData);
    
    // Step 2: Create Session
    const createSessionResponse = await fetch(`${API_BASE_URL}/sessions`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            prompt: 'Create a React app with authentication'
        })
    });
    
    const sessionData = await createSessionResponse.json();
    const sessionId = sessionData.session_id;
    
    console.log('Step 2: Create Session completed', sessionData);
    
    // Step 3: Get Session Details
    const sessionDetailsResponse = await fetch(`${API_BASE_URL}/session/${sessionId}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    
    const sessionDetails = await sessionDetailsResponse.json();
    
    console.log('Step 3: Get Session Details completed', sessionDetails);
    
    // Step 4: Send Message
    const sendMessageResponse = await fetch(`${API_BASE_URL}/session/${sessionId}/message`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            message: 'Add a login page with JWT authentication'
        })
    });
    
    const messageData = await sendMessageResponse.json();
    
    console.log('Step 4: Send Message completed', messageData);
    
    // Step 5: Upload Attachment
    const uploadAttachmentResponse = await fetch(`${API_BASE_URL}/attachments`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            filename: 'auth-config.json',
            content_type: 'application/json',
            content: JSON.stringify({
                authProvider: 'jwt',
                tokenExpiration: '1h',
                refreshToken: true
            })
        })
    });
    
    const attachmentData = await uploadAttachmentResponse.json();
    
    console.log('Step 5: Upload Attachment completed', attachmentData);
    
    // Step 6: Get Updated Session Details
    const updatedSessionResponse = await fetch(`${API_BASE_URL}/session/${sessionId}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    
    const updatedSessionDetails = await updatedSessionResponse.json();
    
    console.log('Step 6: Get Updated Session Details completed', updatedSessionDetails);
    
    console.log('Test Scenario 1: Complete Workflow finished successfully');
    return {
        token,
        sessionId,
        sessionDetails: updatedSessionDetails
    };
}

// Test Scenario 2: Authentication Flow
async function testAuthenticationFlow() {
    console.log('Running Test Scenario 2: Authentication Flow');
    
    // Step 1: Login
    const loginResponse = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: 'test@example.com',
            password: 'password123'
        })
    });
    
    const loginData = await loginResponse.json();
    const token = loginData.token;
    
    console.log('Step 1: Login completed', loginData);
    
    // Step 2: Make authenticated request
    const authenticatedResponse = await fetch(`${API_BASE_URL}/sessions`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    
    const authenticatedData = await authenticatedResponse.json();
    
    console.log('Step 2: Authenticated request completed', authenticatedData);
    
    // Step 3: Make unauthenticated request (should fail)
    try {
        const unauthenticatedResponse = await fetch(`${API_BASE_URL}/sessions`, {
            method: 'GET'
        });
        
        const unauthenticatedData = await unauthenticatedResponse.json();
        
        console.log('Step 3: Unauthenticated request completed', unauthenticatedData);
    } catch (error) {
        console.log('Step 3: Unauthenticated request failed as expected', error);
    }
    
    console.log('Test Scenario 2: Authentication Flow finished successfully');
    return {
        token
    };
}

// Test Scenario 3: Session Management
async function testSessionManagement() {
    console.log('Running Test Scenario 3: Session Management');
    
    // Step 1: Login
    const loginResponse = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: 'test@example.com',
            password: 'password123'
        })
    });
    
    const loginData = await loginResponse.json();
    const token = loginData.token;
    
    console.log('Step 1: Login completed', loginData);
    
    // Step 2: Create multiple sessions
    const sessions = [];
    
    for (let i = 0; i < 3; i++) {
        const createSessionResponse = await fetch(`${API_BASE_URL}/sessions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                prompt: `Create a ${i === 0 ? 'React' : i === 1 ? 'Vue' : 'Angular'} app`
            })
        });
        
        const sessionData = await createSessionResponse.json();
        sessions.push(sessionData);
        
        console.log(`Step 2.${i+1}: Create Session ${i+1} completed`, sessionData);
    }
    
    // Step 3: Get details for each session
    for (let i = 0; i < sessions.length; i++) {
        const sessionDetailsResponse = await fetch(`${API_BASE_URL}/session/${sessions[i].session_id}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const sessionDetails = await sessionDetailsResponse.json();
        
        console.log(`Step 3.${i+1}: Get Session ${i+1} Details completed`, sessionDetails);
    }
    
    console.log('Test Scenario 3: Session Management finished successfully');
    return {
        token,
        sessions
    };
}

// Test Scenario 4: Message Exchange
async function testMessageExchange() {
    console.log('Running Test Scenario 4: Message Exchange');
    
    // Step 1: Login
    const loginResponse = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: 'test@example.com',
            password: 'password123'
        })
    });
    
    const loginData = await loginResponse.json();
    const token = loginData.token;
    
    console.log('Step 1: Login completed', loginData);
    
    // Step 2: Create session
    const createSessionResponse = await fetch(`${API_BASE_URL}/sessions`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            prompt: 'Create a React app'
        })
    });
    
    const sessionData = await createSessionResponse.json();
    const sessionId = sessionData.session_id;
    
    console.log('Step 2: Create Session completed', sessionData);
    
    // Step 3: Send multiple messages
    const messages = [
        'Add a login page',
        'Add a dashboard page',
        'Add a user profile page'
    ];
    
    for (let i = 0; i < messages.length; i++) {
        const sendMessageResponse = await fetch(`${API_BASE_URL}/session/${sessionId}/message`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                message: messages[i]
            })
        });
        
        const messageData = await sendMessageResponse.json();
        
        console.log(`Step 3.${i+1}: Send Message ${i+1} completed`, messageData);
    }
    
    // Step 4: Get session details with messages
    const sessionDetailsResponse = await fetch(`${API_BASE_URL}/session/${sessionId}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    
    const sessionDetails = await sessionDetailsResponse.json();
    
    console.log('Step 4: Get Session Details with messages completed', sessionDetails);
    
    console.log('Test Scenario 4: Message Exchange finished successfully');
    return {
        token,
        sessionId,
        sessionDetails
    };
}

// Export test scenarios
window.devinApiTests = {
    testCompleteWorkflow,
    testAuthenticationFlow,
    testSessionManagement,
    testMessageExchange
};
