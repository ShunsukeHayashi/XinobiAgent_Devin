#!/usr/bin/env python3
"""
Mock server for simulating Devin API interactions.
This server provides endpoints that mimic the behavior of the Devin API.
"""

import json
import time
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Store sessions and attachments in memory
sessions = {}
attachments = {}

class MockDevinAPIHandler(BaseHTTPRequestHandler):
    """Handler for mock Devin API requests."""
    
    def _set_headers(self, status_code=200, content_type='application/json'):
        """Set response headers."""
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS."""
        self._set_headers()
    
    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Check authorization
        if not self._check_auth():
            return
        
        # Session details endpoint
        if path.startswith('/v1/session/'):
            session_id = path.split('/')[-1]
            if session_id in sessions:
                self._set_headers()
                self.wfile.write(json.dumps(sessions[session_id]).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': 'Session not found'}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Endpoint not found'}).encode())
    
    def do_POST(self):
        """Handle POST requests."""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(post_data) if post_data else {}
        except json.JSONDecodeError:
            data = {}
        
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Check authorization except for login
        if not path.startswith('/v1/auth/login') and not self._check_auth():
            return
        
        # Sessions endpoint
        if path == '/v1/sessions':
            session_id = f"session-{uuid.uuid4().hex[:8]}"
            sessions[session_id] = {
                'session_id': session_id,
                'status': 'created',
                'created_at': time.strftime('%Y-%m-%dT%H:%M:%S.%fZ', time.gmtime()),
                'prompt': data.get('prompt', '')
            }
            self._set_headers()
            self.wfile.write(json.dumps({
                'session_id': session_id,
                'status': 'created'
            }).encode())
        
        # Message endpoint
        elif path.startswith('/v1/session/') and path.endswith('/message'):
            session_id = path.split('/')[-2]
            if session_id in sessions:
                # Update session with message
                if 'messages' not in sessions[session_id]:
                    sessions[session_id]['messages'] = []
                
                sessions[session_id]['messages'].append({
                    'id': f"msg-{uuid.uuid4().hex[:8]}",
                    'content': data.get('message', ''),
                    'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S.%fZ', time.gmtime()),
                    'role': 'user'
                })
                
                # Simulate processing time
                time.sleep(0.5)
                
                # Add mock response from Devin
                sessions[session_id]['messages'].append({
                    'id': f"msg-{uuid.uuid4().hex[:8]}",
                    'content': f"I'll help you with: {data.get('message', '')}",
                    'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S.%fZ', time.gmtime()),
                    'role': 'assistant'
                })
                
                self._set_headers()
                self.wfile.write(json.dumps({'success': True}).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': 'Session not found'}).encode())
        
        # Attachments endpoint
        elif path == '/v1/attachments':
            attachment_id = f"attachment-{uuid.uuid4().hex[:8]}"
            attachments[attachment_id] = {
                'attachment_id': attachment_id,
                'created_at': time.strftime('%Y-%m-%dT%H:%M:%S.%fZ', time.gmtime()),
                'filename': data.get('filename', 'unknown.txt'),
                'content_type': data.get('content_type', 'text/plain')
            }
            self._set_headers()
            self.wfile.write(json.dumps({
                'attachment_id': attachment_id,
                'url': f"https://api.devin.ai/v1/attachments/{attachment_id}"
            }).encode())
        
        # Login endpoint
        elif path == '/v1/auth/login':
            self._set_headers()
            self.wfile.write(json.dumps({
                'token': 'mock-token-12345',
                'expires_in': 3600
            }).encode())
        
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Endpoint not found'}).encode())
    
    def _check_auth(self):
        """Check if the request has valid authorization."""
        auth_header = self.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            self._set_headers(401)
            self.wfile.write(json.dumps({'error': 'Unauthorized'}).encode())
            return False
        return True

def run_server(port=8000):
    """Run the mock server."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, MockDevinAPIHandler)
    print(f"Starting mock Devin API server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
