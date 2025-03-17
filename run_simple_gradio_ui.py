#!/usr/bin/env python3
"""
Simple Gradio UI for Enhanced Devin.

This script provides a simplified Gradio UI for interacting with Enhanced Devin.
"""

import os
import sys
import argparse
import logging
import gradio as gr
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockDevinAPIClient:
    """Mock API client for testing without an actual API key."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the mock client."""
        self.api_key = api_key or "mock_api_key"
        self.sessions = {}
        self.current_session_id = None
    
    async def create_session(self, name: str) -> Dict[str, Any]:
        """Create a new session."""
        session_id = f"session_{len(self.sessions) + 1}"
        self.sessions[session_id] = {
            "id": session_id,
            "name": name,
            "created_at": "2025-03-17T10:00:00Z",
            "messages": []
        }
        self.current_session_id = session_id
        return self.sessions[session_id]
    
    async def list_sessions(self) -> List[Dict[str, Any]]:
        """List all sessions."""
        return list(self.sessions.values())
    
    async def get_session(self, session_id: str) -> Dict[str, Any]:
        """Get a session by ID."""
        return self.sessions.get(session_id, {})
    
    async def send_message(self, session_id: str, message: str, files: List[str] = None) -> Dict[str, Any]:
        """Send a message to a session."""
        if session_id not in self.sessions:
            return {"error": "Session not found"}
        
        message_id = f"message_{len(self.sessions[session_id]['messages']) + 1}"
        message_obj = {
            "id": message_id,
            "content": message,
            "role": "user",
            "created_at": "2025-03-17T10:05:00Z"
        }
        
        self.sessions[session_id]["messages"].append(message_obj)
        
        # Create a mock response
        response_id = f"response_{len(self.sessions[session_id]['messages']) + 1}"
        response_obj = {
            "id": response_id,
            "content": f"This is a mock response to: {message}",
            "role": "assistant",
            "created_at": "2025-03-17T10:06:00Z"
        }
        
        self.sessions[session_id]["messages"].append(response_obj)
        
        return response_obj

class SimpleEnhancedDevinUI:
    """
    Simple Gradio UI for Enhanced Devin.
    
    This class provides a simplified Gradio UI for interacting with Enhanced Devin.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Simple Enhanced Devin UI.
        
        Args:
            api_key: Optional API key for authentication
        """
        self.api_key = api_key
        self.client = MockDevinAPIClient(api_key=self.api_key)
        self.sessions = {}
        self.current_session_id = None
        
        # Create the Gradio interface
        self.create_interface()
    
    def create_interface(self):
        """Create the Gradio interface."""
        with gr.Blocks(title="Enhanced Devin", theme=gr.themes.Soft()) as self.interface:
            # Header
            gr.Markdown("# Enhanced Devin")
            gr.Markdown("A superior version of Devin with enhanced capabilities")
            
            # API Key input
            with gr.Row():
                self.api_key_input = gr.Textbox(
                    label="API Key",
                    placeholder="Enter your Devin API key (optional for demo)",
                    type="password",
                    value=self.api_key
                )
                self.set_api_key_btn = gr.Button("Set API Key")
            
            # Session management
            with gr.Row():
                with gr.Column(scale=2):
                    self.session_name_input = gr.Textbox(
                        label="Session Name",
                        placeholder="Enter a name for the new session"
                    )
                    self.create_session_btn = gr.Button("Create Session")
                
                with gr.Column(scale=3):
                    self.sessions_dropdown = gr.Dropdown(
                        label="Active Sessions",
                        choices=[],
                        interactive=True
                    )
                    with gr.Row():
                        self.load_session_btn = gr.Button("Load Session")
                        self.refresh_sessions_btn = gr.Button("Refresh")
            
            # Chat interface
            with gr.Row():
                with gr.Column(scale=3):
                    self.chat_history = gr.Chatbot(
                        label="Chat History",
                        height=400
                    )
                    with gr.Row():
                        self.message_input = gr.Textbox(
                            label="Message",
                            placeholder="Type your message here",
                            lines=3
                        )
                        self.file_upload = gr.File(
                            label="Upload File",
                            file_count="multiple"
                        )
                    self.send_message_btn = gr.Button("Send Message")
                
                with gr.Column(scale=2):
                    gr.Markdown("### Agent Actions")
                    self.agent_actions = gr.Dataframe(
                        headers=["Time", "Action", "Status"],
                        datatype=["str", "str", "str"],
                        row_count=10,
                        col_count=(3, "fixed"),
                        height=300
                    )
            
            # Set up event handlers
            self.set_api_key_btn.click(self.set_api_key, inputs=[self.api_key_input], outputs=[])
            self.create_session_btn.click(self.create_session, inputs=[self.session_name_input], outputs=[self.sessions_dropdown])
            self.load_session_btn.click(self.load_session, inputs=[self.sessions_dropdown], outputs=[self.chat_history])
            self.refresh_sessions_btn.click(self.refresh_sessions, outputs=[self.sessions_dropdown])
            self.send_message_btn.click(self.send_message, inputs=[self.message_input, self.file_upload], outputs=[self.chat_history, self.agent_actions, self.message_input])
    
    def set_api_key(self, api_key):
        """Set the API key."""
        self.api_key = api_key
        self.client = MockDevinAPIClient(api_key=self.api_key)
        return
    
    def create_session(self, name):
        """Create a new session."""
        import asyncio
        
        if not name:
            name = "New Session"
        
        # Create the session
        session = asyncio.run(self.client.create_session(name))
        
        # Update the sessions dropdown
        sessions = asyncio.run(self.client.list_sessions())
        session_names = [s["name"] for s in sessions]
        
        return gr.Dropdown(choices=session_names)
    
    def load_session(self, session_name):
        """Load a session."""
        import asyncio
        
        # Get the session ID
        sessions = asyncio.run(self.client.list_sessions())
        session = next((s for s in sessions if s["name"] == session_name), None)
        
        if not session:
            return gr.Chatbot(value=[])
        
        # Set the current session ID
        self.current_session_id = session["id"]
        
        # Get the session messages
        session = asyncio.run(self.client.get_session(self.current_session_id))
        messages = session.get("messages", [])
        
        # Format the messages for the chatbot
        chat_messages = []
        for i in range(0, len(messages), 2):
            if i + 1 < len(messages):
                chat_messages.append([messages[i]["content"], messages[i+1]["content"]])
        
        return gr.Chatbot(value=chat_messages)
    
    def refresh_sessions(self):
        """Refresh the sessions dropdown."""
        import asyncio
        
        # Get the sessions
        sessions = asyncio.run(self.client.list_sessions())
        session_names = [s["name"] for s in sessions]
        
        return gr.Dropdown(choices=session_names)
    
    def send_message(self, message, files):
        """Send a message."""
        import asyncio
        
        if not self.current_session_id:
            # Create a new session if none exists
            session = asyncio.run(self.client.create_session("New Session"))
            self.current_session_id = session["id"]
        
        # Send the message
        response = asyncio.run(self.client.send_message(self.current_session_id, message))
        
        # Update the chat history
        session = asyncio.run(self.client.get_session(self.current_session_id))
        messages = session.get("messages", [])
        
        # Format the messages for the chatbot
        chat_messages = []
        for i in range(0, len(messages), 2):
            if i + 1 < len(messages):
                chat_messages.append([messages[i]["content"], messages[i+1]["content"]])
        
        # Update the agent actions
        agent_actions = [
            ["2025-03-17 10:06:00", "Process Message", "Completed"],
            ["2025-03-17 10:06:01", "Generate Response", "Completed"]
        ]
        
        return gr.Chatbot(value=chat_messages), gr.Dataframe(value=agent_actions), gr.Textbox(value="")

def launch_ui(api_key=None, port=7860, host="0.0.0.0", share=False, debug=False):
    """
    Launch the Simple Enhanced Devin UI.
    
    Args:
        api_key: API key for authentication
        port: Port to run the UI on
        host: Host to run the UI on
        share: Whether to create a public URL
        debug: Whether to enable debug mode
    """
    # Set up logging level
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create the UI
    ui = SimpleEnhancedDevinUI(api_key=api_key)
    
    # Launch the UI
    logger.info(f"Starting Simple Enhanced Devin UI on port {port}")
    ui.interface.launch(
        server_name=host,
        server_port=port,
        share=share,
        debug=debug
    )

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="Simple Enhanced Devin UI")
    parser.add_argument("--api-key", help="API key for Devin API")
    parser.add_argument("--port", type=int, default=7860, help="Port to run the UI on")
    parser.add_argument("--host", default="0.0.0.0", help="Host to run the UI on")
    parser.add_argument("--share", action="store_true", help="Create a public URL")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    
    # Launch the UI
    launch_ui(
        api_key=args.api_key,
        port=args.port,
        host=args.host,
        share=args.share,
        debug=args.debug
    )
