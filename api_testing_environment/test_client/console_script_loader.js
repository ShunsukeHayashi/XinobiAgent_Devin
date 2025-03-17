/**
 * Console Script Loader
 * 
 * This script loads the Developer Console monitoring scripts and initializes them.
 */

// Load API Monitor
function loadApiMonitor() {
    const script = document.createElement('script');
    script.src = '../../developer_console_monitoring/console_scripts/api_monitor.js';
    script.onload = function() {
        console.log('API Monitor loaded successfully');
    };
    script.onerror = function() {
        console.error('Failed to load API Monitor');
    };
    document.head.appendChild(script);
}

// Load Auth Monitor
function loadAuthMonitor() {
    const script = document.createElement('script');
    script.src = '../../developer_console_monitoring/console_scripts/auth_monitor.js';
    script.onload = function() {
        console.log('Auth Monitor loaded successfully');
    };
    script.onerror = function() {
        console.error('Failed to load Auth Monitor');
    };
    document.head.appendChild(script);
}

// Load Session Monitor
function loadSessionMonitor() {
    const script = document.createElement('script');
    script.src = '../../developer_console_monitoring/console_scripts/session_monitor.js';
    script.onload = function() {
        console.log('Session Monitor loaded successfully');
    };
    script.onerror = function() {
        console.error('Failed to load Session Monitor');
    };
    document.head.appendChild(script);
}

// Load Combined Monitor
function loadCombinedMonitor() {
    const script = document.createElement('script');
    script.src = '../../developer_console_monitoring/console_scripts/combined_monitor.js';
    script.onload = function() {
        console.log('Combined Monitor loaded successfully');
    };
    script.onerror = function() {
        console.error('Failed to load Combined Monitor');
    };
    document.head.appendChild(script);
}

// Initialize monitoring
function initializeMonitoring() {
    // Add buttons to the page
    const monitoringDiv = document.createElement('div');
    monitoringDiv.className = 'card';
    monitoringDiv.innerHTML = `
        <h2>Monitoring Tools</h2>
        <div>
            <button onclick="loadApiMonitor()">Load API Monitor</button>
            <button onclick="loadAuthMonitor()">Load Auth Monitor</button>
            <button onclick="loadSessionMonitor()">Load Session Monitor</button>
            <button onclick="loadCombinedMonitor()">Load Combined Monitor</button>
        </div>
        <div class="response" id="monitoringResponse"></div>
    `;
    
    // Add to the page
    const testScenariosTab = document.getElementById('TestScenarios');
    testScenariosTab.appendChild(monitoringDiv);
}

// Initialize when the page loads
window.addEventListener('load', initializeMonitoring);
