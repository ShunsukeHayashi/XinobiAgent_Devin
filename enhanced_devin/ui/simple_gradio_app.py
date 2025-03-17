"""
Simple Gradio UI for Enhanced Devin.

This module provides a simplified Gradio-based user interface for interacting with the
Enhanced Devin system.
"""

import os
import sys
import json
import asyncio
import gradio as gr
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleEnhancedDevinUI:
    """Simple Gradio UI for Enhanced Devin."""
    
    def __init__(self):
        """Initialize the Simple Enhanced Devin UI."""
        # Import the mock API client
        from enhanced_devin.api.mock_api_client import MockDevinAPIClient
        self.client = MockDevinAPIClient()
        logger.info("Using mock API client")
        
        self.current_session_id = None
        
        # Create the Gradio interface
        self.create_interface()
    
    def create_interface(self):
        """Create the Gradio interface."""
        with gr.Blocks(title="Enhanced Devin", theme=gr.themes.Soft()) as self.interface:
            # Header
            gr.Markdown("# Enhanced Devin")
            gr.Markdown("A superior version of Devin with enhanced capabilities")
            
            # Session creation
            with gr.Row():
                self.session_name_input = gr.Textbox(
                    label="Session Name",
                    placeholder="Enter a name for the new session"
                )
                self.create_session_btn = gr.Button("Create Session")
            
            # Session info
            self.session_info = gr.Textbox(label="Current Session", interactive=False)
            
            # Chat interface
            self.chat_history = gr.Chatbot(label="Chat History", height=400)
            
            # Message input
            with gr.Row():
                self.message_input = gr.Textbox(
                    label="Message",
                    placeholder="Type your message here",
                    lines=3
                )
                self.send_message_btn = gr.Button("Send Message")
            
            # Tool execution
            gr.Markdown("### Tool Execution")
            with gr.Row():
                self.tool_name_input = gr.Dropdown(
                    label="Tool",
                    choices=["bash", "python", "google_search"],
                    interactive=True
                )
                self.tool_params_input = gr.Textbox(
                    label="Parameters (JSON)",
                    placeholder='{"command": "ls -la"}',
                    lines=2
                )
            self.execute_tool_btn = gr.Button("Execute Tool")
            self.tool_result = gr.Textbox(label="Tool Result", lines=5)
            
            # Set up event handlers
            self.create_session_btn.click(self.create_session, inputs=[self.session_name_input], outputs=[self.session_info])
            self.send_message_btn.click(self.send_message, inputs=[self.message_input], outputs=[self.chat_history, self.message_input])
            self.execute_tool_btn.click(self.execute_tool, inputs=[self.tool_name_input, self.tool_params_input], outputs=[self.tool_result])
    
    def create_session(self, session_name):
        """Create a new session."""
        if not session_name:
            return "No session name provided"
        
        try:
            # Create the session
            session = asyncio.run(self.client.create_session(session_name))
            self.current_session_id = session["id"]
            
            return f"Session created: {session_name} (ID: {session['id']})"
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            return f"Error creating session: {str(e)}"
    
    def send_message(self, message):
        """Send a message."""
        if not self.current_session_id:
            return [["Please create a session first", None]], message
        
        if not message:
            return self.chat_history, message
        
        try:
            # Send the message
            sent_message = asyncio.run(self.client.send_message(self.current_session_id, message))
            
            # Get the messages
            messages = asyncio.run(self.client.get_messages(self.current_session_id))
            
            # Format the chat history
            chat_history = []
            for msg in messages:
                if msg["role"] == "user":
                    chat_history.append([msg["content"], None])
                elif msg["role"] == "assistant":
                    if chat_history and chat_history[-1][1] is None:
                        chat_history[-1][1] = msg["content"]
                    else:
                        chat_history.append([None, msg["content"]])
            
            return chat_history, ""
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return [[f"Error: {str(e)}", None]], message
    
    def execute_tool(self, tool_name, params_json):
        """Execute a tool."""
        if not self.current_session_id:
            return "Please create a session first"
        
        if not tool_name:
            return "No tool name provided"
        
        try:
            # Parse the parameters
            parameters = json.loads(params_json) if params_json else {}
            
            # Execute the tool
            result = asyncio.run(self.client.execute_tool(self.current_session_id, tool_name, parameters))
            
            return f"Tool execution result:\n{result['result']}"
        except Exception as e:
            logger.error(f"Error executing tool: {e}")
            return f"Error executing tool: {str(e)}"

def launch_simple_ui(port=7860, host="0.0.0.0", share=False, debug=False):
    """Launch the Simple Enhanced Devin UI."""
    ui = SimpleEnhancedDevinUI()
    ui.interface.launch(server_name=host, server_port=port, share=share, debug=debug)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Simple Enhanced Devin UI")
    parser.add_argument("--port", type=int, default=7860, help="Port to run the UI on")
    parser.add_argument("--host", default="0.0.0.0", help="Host to run the UI on")
    parser.add_argument("--share", action="store_true", help="Create a public URL")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    
    launch_simple_ui(
        port=args.port,
        host=args.host,
        share=args.share,
        debug=args.debug
    )
