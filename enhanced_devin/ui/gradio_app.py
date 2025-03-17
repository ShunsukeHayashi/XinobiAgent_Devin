"""
Gradio UI for Enhanced Devin.

This module provides a Gradio-based user interface for interacting with the
Enhanced Devin system.
"""

import os
import sys
import time
import json
import asyncio
import gradio as gr
from typing import Dict, List, Any, Optional, Union
import logging
from datetime import datetime
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedDevinUI:
    """Gradio UI for Enhanced Devin."""
    
    def __init__(self, api_key: Optional[str] = None, use_mock: bool = False):
        """Initialize the Enhanced Devin UI."""
        self.api_key = api_key or os.environ.get("DEVIN_API_KEY")
        self.use_mock = use_mock or not self.api_key
        
        if self.use_mock:
            # Import and use the mock API client
            from enhanced_devin.api.mock_api_client import MockDevinAPIClient
            self.client = MockDevinAPIClient()
            logger.info("Using mock API client")
        else:
            # Import and use the real API client if available
            try:
                from enhanced_devin.api.enhanced_api_client import EnhancedDevinAPIClient
                self.client = EnhancedDevinAPIClient(api_key=self.api_key)
                logger.info("Using real API client")
            except Exception as e:
                logger.error(f"Error initializing API client: {e}")
                logger.info("Falling back to mock API client")
                from enhanced_devin.api.mock_api_client import MockDevinAPIClient
                self.client = MockDevinAPIClient()
                self.use_mock = True
        
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
            
            # Mock mode indicator
            if self.use_mock:
                gr.Markdown("### Running in Mock Mode (No API Key)")
            
            # Tabs for different sections
            with gr.Tabs():
                # Session tab
                with gr.TabItem("Sessions"):
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
                    
                    # Session info
                    gr.Markdown("### Session Information")
                    self.session_info = gr.JSON(label="Session Details")
                
                # Chat tab
                with gr.TabItem("Chat"):
                    # Chat interface
                    with gr.Row():
                        with gr.Column(scale=3):
                            self.chat_history = gr.Chatbot(
                                label="Chat History",
                                height=500
                            )
                            with gr.Row():
                                self.message_input = gr.Textbox(
                                    label="Message",
                                    placeholder="Type your message here",
                                    lines=3
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
                
                # Tools tab
                with gr.TabItem("Tools"):
                    with gr.Row():
                        with gr.Column(scale=1):
                            gr.Markdown("### Available Tools")
                            self.tools_list = gr.Dataframe(
                                headers=["Name", "Version", "Author"],
                                datatype=["str", "str", "str"],
                                row_count=10,
                                col_count=(3, "fixed"),
                                height=300
                            )
                            self.refresh_tools_btn = gr.Button("Refresh Tools")
                        
                        with gr.Column(scale=2):
                            gr.Markdown("### Tool Details")
                            self.tool_details = gr.JSON(label="Selected Tool")
                            gr.Markdown("### Tool Execution")
                            with gr.Row():
                                self.tool_name_input = gr.Textbox(
                                    label="Tool Name",
                                    placeholder="Enter tool name"
                                )
                                self.tool_params_input = gr.Textbox(
                                    label="Parameters (JSON)",
                                    placeholder='{"param1": "value1", "param2": "value2"}',
                                    lines=3
                                )
                            self.execute_tool_btn = gr.Button("Execute Tool")
                            self.tool_result = gr.JSON(label="Execution Result")
            
            # Set up event handlers
            self.create_session_btn.click(self.create_session, inputs=[self.session_name_input], outputs=[self.sessions_dropdown, self.session_info])
            self.load_session_btn.click(self.load_session, inputs=[self.sessions_dropdown], outputs=[self.session_info, self.chat_history])
            self.refresh_sessions_btn.click(self.refresh_sessions, outputs=[self.sessions_dropdown])
            self.send_message_btn.click(self.send_message, inputs=[self.message_input], outputs=[self.chat_history, self.agent_actions, self.message_input])
            self.refresh_tools_btn.click(self.refresh_tools, outputs=[self.tools_list])
            self.tools_list.select(self.select_tool, outputs=[self.tool_details, self.tool_name_input])
            self.execute_tool_btn.click(self.execute_tool, inputs=[self.tool_name_input, self.tool_params_input], outputs=[self.tool_result])
    
    def create_session(self, session_name):
        """Create a new session."""
        if not session_name:
            return [], None
        
        try:
            # Create the session
            session = asyncio.run(self.client.create_session(session_name))
            self.sessions[session["id"]] = session
            self.current_session_id = session["id"]
            
            # Update the sessions dropdown
            sessions_list = list(self.sessions.values())
            sessions_dropdown = [(s["name"], s["id"]) for s in sessions_list]
            
            return sessions_dropdown, session
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            return [], None
    
    def refresh_sessions(self):
        """Refresh the sessions list."""
        try:
            # Get all sessions
            sessions = asyncio.run(self.client.get_sessions())
            self.sessions = {s["id"]: s for s in sessions}
            
            # Update the sessions dropdown
            sessions_dropdown = [(s["name"], s["id"]) for s in sessions]
            
            return sessions_dropdown
        except Exception as e:
            logger.error(f"Error refreshing sessions: {e}")
            return []
    
    def load_session(self, session_id):
        """Load a session."""
        if not session_id:
            return None, []
        
        try:
            # Get the session
            session = asyncio.run(self.client.get_session(session_id))
            self.current_session_id = session_id
            
            # Get the messages
            messages = asyncio.run(self.client.get_messages(session_id))
            
            # Format the chat history
            chat_history = []
            for message in messages:
                if message["role"] == "user":
                    chat_history.append([message["content"], None])
                elif message["role"] == "assistant":
                    if chat_history and chat_history[-1][1] is None:
                        chat_history[-1][1] = message["content"]
                    else:
                        chat_history.append([None, message["content"]])
            
            return session, chat_history
        except Exception as e:
            logger.error(f"Error loading session: {e}")
            return None, []
    
    def send_message(self, message):
        """Send a message."""
        if not self.current_session_id:
            return [], [], message
        
        if not message:
            return [], [], message
        
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
            
            # Format the agent actions
            agent_actions = [
                [datetime.now().strftime("%H:%M:%S"), "Send Message", "Completed"],
                [datetime.now().strftime("%H:%M:%S"), "Process Message", "Completed"],
                [datetime.now().strftime("%H:%M:%S"), "Generate Response", "Completed"]
            ]
            
            return chat_history, agent_actions, ""
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return [], [], message
    
    def refresh_tools(self):
        """Refresh the tools list."""
        try:
            # Get all tools
            tools = asyncio.run(self.client.get_tools())
            
            # Format the tools list
            tools_list = [[t["name"], t["version"], t["author"]] for t in tools]
            
            return tools_list
        except Exception as e:
            logger.error(f"Error refreshing tools: {e}")
            return []
    
    def select_tool(self, evt: gr.SelectData):
        """Select a tool."""
        try:
            # Get the tool name
            tool_name = evt.value[0]
            
            # Get the tool
            tool = asyncio.run(self.client.get_tool(tool_name))
            
            return tool, tool_name
        except Exception as e:
            logger.error(f"Error selecting tool: {e}")
            return None, ""
    
    def execute_tool(self, tool_name, params_json):
        """Execute a tool."""
        if not self.current_session_id:
            return None
        
        if not tool_name:
            return None
        
        try:
            # Parse the parameters
            parameters = json.loads(params_json) if params_json else {}
            
            # Execute the tool
            result = asyncio.run(self.client.execute_tool(self.current_session_id, tool_name, parameters))
            
            return result
        except Exception as e:
            logger.error(f"Error executing tool: {e}")
            return None

def launch_ui(api_key=None, port=7860, host="0.0.0.0", share=False, debug=False):
    """Launch the Enhanced Devin UI."""
    ui = EnhancedDevinUI(api_key=api_key, use_mock=True)
    ui.interface.launch(server_name=host, server_port=port, share=share, debug=debug)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Devin UI")
    parser.add_argument("--api-key", help="API key for Devin API")
    parser.add_argument("--port", type=int, default=7860, help="Port to run the UI on")
    parser.add_argument("--host", default="0.0.0.0", help="Host to run the UI on")
    parser.add_argument("--share", action="store_true", help="Create a public URL")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    
    launch_ui(
        api_key=args.api_key,
        port=args.port,
        host=args.host,
        share=args.share,
        debug=args.debug
    )
