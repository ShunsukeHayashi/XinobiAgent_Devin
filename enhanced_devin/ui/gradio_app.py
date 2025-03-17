"""
Gradio UI for Enhanced Devin.

This module provides a Gradio-based user interface for interacting with the
Enhanced Devin system. It allows users to create sessions, send messages,
upload files, and view agent responses and actions.
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

# Import Enhanced Devin components
from enhanced_devin.api.enhanced_api_client import EnhancedDevinAPIClient
from enhanced_devin.monitoring.api_monitor import APIMonitor
from enhanced_devin.monitoring.event_logger import EventLogger
from enhanced_devin.tools.tool_registry import ToolRegistry

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create event logger
event_logger = EventLogger(log_file="enhanced_devin_ui.log")

# Create API monitor
api_monitor = APIMonitor()

class EnhancedDevinUI:
    """
    Gradio UI for Enhanced Devin.
    
    This class provides a Gradio-based user interface for interacting with the
    Enhanced Devin system.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Enhanced Devin UI.
        
        Args:
            api_key: Optional API key for authentication
        """
        self.api_key = api_key or os.environ.get("DEVIN_API_KEY")
        self.client = EnhancedDevinAPIClient(api_key=self.api_key)
        self.api_monitor = APIMonitor()
        self.event_logger = EventLogger(log_file="enhanced_devin_ui.log")
        self.tool_registry = ToolRegistry()
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
                    placeholder="Enter your Devin API key",
                    type="password",
                    value=self.api_key
                )
                self.set_api_key_btn = gr.Button("Set API Key")
            
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
                    with gr.Box():
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
                            gr.Markdown("### Agent State")
                            self.agent_state = gr.JSON(label="Current State")
                
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
                
                # Monitoring tab
                with gr.TabItem("Monitoring"):
                    with gr.Tabs():
                        with gr.TabItem("API Monitoring"):
                            with gr.Row():
                                self.api_requests = gr.Dataframe(
                                    headers=["Time", "Method", "URL", "Status"],
                                    datatype=["str", "str", "str", "str"],
                                    row_count=10,
                                    col_count=(4, "fixed"),
                                    height=300
                                )
                                self.refresh_api_btn = gr.Button("Refresh")
                            
                            gr.Markdown("### Request Details")
                            self.request_details = gr.JSON(label="Selected Request")
                        
                        with gr.TabItem("Performance"):
                            with gr.Row():
                                with gr.Column(scale=1):
                                    gr.Markdown("### System Metrics")
                                    self.system_metrics = gr.JSON(label="Current Metrics")
                                    self.refresh_metrics_btn = gr.Button("Refresh Metrics")
                                
                                with gr.Column(scale=2):
                                    gr.Markdown("### Performance Chart")
                                    self.performance_chart = gr.Plot(label="Resource Usage")
                        
                        with gr.TabItem("Logs"):
                            with gr.Row():
                                with gr.Column(scale=3):
                                    self.log_entries = gr.Dataframe(
                                        headers=["Time", "Level", "Source", "Message"],
                                        datatype=["str", "str", "str", "str"],
                                        row_count=15,
                                        col_count=(4, "fixed"),
                                        height=400
                                    )
                                
                                with gr.Column(scale=1):
                                    self.log_level_filter = gr.Dropdown(
                                        label="Log Level",
                                        choices=["All", "Debug", "Info", "Warning", "Error", "Critical"],
                                        value="All"
                                    )
                                    self.log_source_filter = gr.Textbox(
                                        label="Source Filter",
                                        placeholder="Filter by source"
                                    )
                                    self.apply_log_filter_btn = gr.Button("Apply Filter")
                            
                            gr.Markdown("### Log Details")
                            self.log_details = gr.JSON(label="Selected Log Entry")
            
            # Set up event handlers
            self.set_api_key_btn.click(self.set_api_key, inputs=[self.api_key_input], outputs=[self.api_key_input])
            self.create_session_btn.click(self.create_session, inputs=[self.session_name_input], outputs=[self.sessions_dropdown, self.session_info])
            self.load_session_btn.click(self.load_session, inputs=[self.sessions_dropdown], outputs=[self.session_info, self.chat_history, self.agent_state])
            self.refresh_sessions_btn.click(self.refresh_sessions, outputs=[self.sessions_dropdown])
            self.send_message_btn.click(self.send_message, inputs=[self.message_input, self.file_upload], outputs=[self.chat_history, self.agent_actions, self.agent_state, self.message_input])
            self.refresh_tools_btn.click(self.refresh_tools, outputs=[self.tools_list])
            self.tools_list.select(self.select_tool, outputs=[self.tool_details, self.tool_name_input])
            self.execute_tool_btn.click(self.execute_tool, inputs=[self.tool_name_input, self.tool_params_input], outputs=[self.tool_result])
            self.refresh_api_btn.click(self.refresh_api_monitoring, outputs=[self.api_requests])
            self.api_requests.select(self.select_api_request, outputs=[self.request_details])
            self.refresh_metrics_btn.click(self.refresh_metrics, outputs=[self.system_metrics, self.performance_chart])
            self.apply_log_filter_btn.click(self.apply_log_filter, inputs=[self.log_level_filter, self.log_source_filter], outputs=[self.log_entries])
            self.log_entries.select(self.select_log_entry, outputs=[self.log_details])

    def select_log_entry(self, evt: gr.SelectData):
        """
        Handle log entry selection.
        
        Args:
            evt: Selection event
            
        Returns:
            Log entry details
        """
        try:
            # Get the selected log entry
            row_index = evt.index[0]
            logs = self.apply_log_filter("All", "")
            if row_index < len(logs):
                log = logs[row_index]
                
                # Generate mock log details
                log_details = {
                    "id": f"log_{int(time.time())}_{uuid.uuid4().hex[:8]}",
                    "timestamp": datetime.now().timestamp(),
                    "level": log["Level"],
                    "source": log["Source"],
                    "message": log["Message"],
                    "data": {"context": "UI interaction"},
                    "tags": ["ui", "log", log["Level"].lower()]
                }
                
                # Log the event
                self.event_logger.info(f"Selected log entry: {log['Message']}", "ui")
                
                return log_details
            
            return {}
        except Exception as e:
            self.event_logger.error(f"Error selecting log entry: {str(e)}", "ui")
            return {}

def launch_ui(api_key=None, port=7860, host="0.0.0.0", share=False, debug=False):
    """
    Launch the Enhanced Devin UI.
    
    Args:
        api_key: API key for Devin API
        port: Port to run the UI on
        host: Host to run the UI on
        share: Whether to create a public URL
        debug: Whether to enable debug mode
    
    Returns:
        The Gradio interface
    """
    ui = EnhancedDevinUI(api_key=api_key)
    ui.interface.launch(
        server_name=host,
        server_port=port,
        share=share,
        debug=debug
    )
    return ui.interface

if __name__ == "__main__":
    import argparse
    
    # Parse arguments
    parser = argparse.ArgumentParser(description="Enhanced Devin UI")
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
