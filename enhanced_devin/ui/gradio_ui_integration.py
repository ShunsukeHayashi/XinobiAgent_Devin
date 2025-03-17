"""
Gradio UI integration for Enhanced Devin.

This module integrates the Enhanced Devin system with the Gradio UI.
"""

import os
import sys
import time
import json
import asyncio
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import uuid
import gradio as gr

# Import Enhanced Devin components
from enhanced_devin.api.enhanced_api_client import EnhancedDevinAPIClient
from enhanced_devin.monitoring.api_monitor import APIMonitor
from enhanced_devin.monitoring.event_logger import EventLogger
from enhanced_devin.tools.tool_registry import ToolRegistry
from enhanced_devin.ui.method_implementations import GradioMethodImplementations

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedDevinGradioIntegration:
    """
    Gradio UI integration for Enhanced Devin.
    
    This class integrates the Enhanced Devin system with the Gradio UI.
    """
    
    def __init__(self, api_client: EnhancedDevinAPIClient, api_monitor: APIMonitor, 
                event_logger: EventLogger, tool_registry: ToolRegistry):
        """
        Initialize the Gradio UI integration.
        
        Args:
            api_client: Enhanced Devin API client
            api_monitor: API monitor
            event_logger: Event logger
            tool_registry: Tool registry
        """
        self.api_client = api_client
        self.api_monitor = api_monitor
        self.event_logger = event_logger
        self.tool_registry = tool_registry
        
        # Create the UI instance
        self.ui = self._create_ui_instance()
        
        # Create method implementations
        self.methods = GradioMethodImplementations(self.ui)
        
        # Connect methods to UI
        self._connect_methods()
    
    def _create_ui_instance(self):
        """
        Create the UI instance.
        
        Returns:
            The UI instance
        """
        # Create a mock UI instance
        ui = type('UI', (), {})()
        
        # Set attributes
        ui.api_client = self.api_client
        ui.api_monitor = self.api_monitor
        ui.event_logger = self.event_logger
        ui.tool_registry = self.tool_registry
        ui.sessions = {}
        ui.current_session_id = None
        
        return ui
    
    def _connect_methods(self):
        """Connect methods to UI."""
        # Connect methods to UI
        self.ui.set_api_key = self.methods.set_api_key
        self.ui.create_session = self.methods.create_session
        self.ui.load_session = self.methods.load_session
        self.ui.refresh_sessions = self.methods.refresh_sessions
        self.ui.send_message = self.methods.send_message
        self.ui.refresh_tools = self.methods.refresh_tools
        self.ui.select_tool = self.methods.select_tool
        self.ui.execute_tool = self.methods.execute_tool
        self.ui.refresh_api_monitoring = self.methods.refresh_api_monitoring
        self.ui.select_api_request = self.methods.select_api_request
        self.ui.refresh_metrics = self.methods.refresh_metrics
        self.ui.apply_log_filter = self.methods.apply_log_filter
        self.ui.select_log_entry = self.methods.select_log_entry
    
    def create_interface(self):
        """
        Create the Gradio interface.
        
        Returns:
            The Gradio interface
        """
        with gr.Blocks(title="Enhanced Devin", theme=gr.themes.Soft()) as interface:
            # Header
            gr.Markdown("# Enhanced Devin")
            gr.Markdown("A superior version of Devin with enhanced capabilities")
            
            # API Key input
            with gr.Row():
                api_key_input = gr.Textbox(
                    label="API Key",
                    placeholder="Enter your Devin API key",
                    type="password"
                )
                set_api_key_btn = gr.Button("Set API Key")
            
            # Tabs for different sections
            with gr.Tabs():
                # Session tab
                with gr.TabItem("Sessions"):
                    with gr.Row():
                        with gr.Column(scale=2):
                            session_name_input = gr.Textbox(
                                label="Session Name",
                                placeholder="Enter a name for the new session"
                            )
                            create_session_btn = gr.Button("Create Session")
                        
                        with gr.Column(scale=3):
                            sessions_dropdown = gr.Dropdown(
                                label="Active Sessions",
                                choices=[],
                                interactive=True
                            )
                            with gr.Row():
                                load_session_btn = gr.Button("Load Session")
                                refresh_sessions_btn = gr.Button("Refresh")
                    
                    # Session info
                    with gr.Box():
                        gr.Markdown("### Session Information")
                        session_info = gr.JSON(label="Session Details")
                
                # Chat tab
                with gr.TabItem("Chat"):
                    # Chat interface
                    with gr.Row():
                        with gr.Column(scale=3):
                            chat_history = gr.Chatbot(
                                label="Chat History",
                                height=500
                            )
                            with gr.Row():
                                message_input = gr.Textbox(
                                    label="Message",
                                    placeholder="Type your message here",
                                    lines=3
                                )
                                file_upload = gr.File(
                                    label="Upload File",
                                    file_count="multiple"
                                )
                            send_message_btn = gr.Button("Send Message")
                        
                        with gr.Column(scale=2):
                            gr.Markdown("### Agent Actions")
                            agent_actions = gr.Dataframe(
                                headers=["Time", "Action", "Status"],
                                datatype=["str", "str", "str"],
                                row_count=10,
                                col_count=(3, "fixed"),
                                height=300
                            )
                            gr.Markdown("### Agent State")
                            agent_state = gr.JSON(label="Current State")
                
                # Tools tab
                with gr.TabItem("Tools"):
                    with gr.Row():
                        with gr.Column(scale=1):
                            gr.Markdown("### Available Tools")
                            tools_list = gr.Dataframe(
                                headers=["Name", "Version", "Author"],
                                datatype=["str", "str", "str"],
                                row_count=10,
                                col_count=(3, "fixed"),
                                height=300
                            )
                            refresh_tools_btn = gr.Button("Refresh Tools")
                        
                        with gr.Column(scale=2):
                            gr.Markdown("### Tool Details")
                            tool_details = gr.JSON(label="Selected Tool")
                            gr.Markdown("### Tool Execution")
                            with gr.Row():
                                tool_name_input = gr.Textbox(
                                    label="Tool Name",
                                    placeholder="Enter tool name"
                                )
                                tool_params_input = gr.Textbox(
                                    label="Parameters (JSON)",
                                    placeholder='{"param1": "value1", "param2": "value2"}',
                                    lines=3
                                )
                            execute_tool_btn = gr.Button("Execute Tool")
                            tool_result = gr.JSON(label="Execution Result")
                
                # Monitoring tab
                with gr.TabItem("Monitoring"):
                    with gr.Tabs():
                        with gr.TabItem("API Monitoring"):
                            with gr.Row():
                                api_requests = gr.Dataframe(
                                    headers=["Time", "Method", "URL", "Status"],
                                    datatype=["str", "str", "str", "str"],
                                    row_count=10,
                                    col_count=(4, "fixed"),
                                    height=300
                                )
                                refresh_api_btn = gr.Button("Refresh")
                            
                            gr.Markdown("### Request Details")
                            request_details = gr.JSON(label="Selected Request")
                        
                        with gr.TabItem("Performance"):
                            with gr.Row():
                                with gr.Column(scale=1):
                                    gr.Markdown("### System Metrics")
                                    system_metrics = gr.JSON(label="Current Metrics")
                                    refresh_metrics_btn = gr.Button("Refresh Metrics")
                                
                                with gr.Column(scale=2):
                                    gr.Markdown("### Performance Chart")
                                    performance_chart = gr.Plot(label="Resource Usage")
                        
                        with gr.TabItem("Logs"):
                            with gr.Row():
                                with gr.Column(scale=3):
                                    log_entries = gr.Dataframe(
                                        headers=["Time", "Level", "Source", "Message"],
                                        datatype=["str", "str", "str", "str"],
                                        row_count=15,
                                        col_count=(4, "fixed"),
                                        height=400
                                    )
                                
                                with gr.Column(scale=1):
                                    log_level_filter = gr.Dropdown(
                                        label="Log Level",
                                        choices=["All", "Debug", "Info", "Warning", "Error", "Critical"],
                                        value="All"
                                    )
                                    log_source_filter = gr.Textbox(
                                        label="Source Filter",
                                        placeholder="Filter by source"
                                    )
                                    apply_log_filter_btn = gr.Button("Apply Filter")
                            
                            gr.Markdown("### Log Details")
                            log_details = gr.JSON(label="Selected Log Entry")
            
            # Set up event handlers
            set_api_key_btn.click(self.ui.set_api_key, inputs=[api_key_input], outputs=[api_key_input])
            create_session_btn.click(self.ui.create_session, inputs=[session_name_input], outputs=[sessions_dropdown, session_info])
            load_session_btn.click(self.ui.load_session, inputs=[sessions_dropdown], outputs=[session_info, chat_history, agent_state])
            refresh_sessions_btn.click(self.ui.refresh_sessions, outputs=[sessions_dropdown])
            send_message_btn.click(self.ui.send_message, inputs=[message_input, file_upload], outputs=[chat_history, agent_actions, agent_state, message_input])
            refresh_tools_btn.click(self.ui.refresh_tools, outputs=[tools_list])
            tools_list.select(self.ui.select_tool, outputs=[tool_details, tool_name_input])
            execute_tool_btn.click(self.ui.execute_tool, inputs=[tool_name_input, tool_params_input], outputs=[tool_result])
            refresh_api_btn.click(self.ui.refresh_api_monitoring, outputs=[api_requests])
            api_requests.select(self.ui.select_api_request, outputs=[request_details])
            refresh_metrics_btn.click(self.ui.refresh_metrics, outputs=[system_metrics, performance_chart])
            apply_log_filter_btn.click(self.ui.apply_log_filter, inputs=[log_level_filter, log_source_filter], outputs=[log_entries])
            log_entries.select(self.ui.select_log_entry, outputs=[log_details])
        
        return interface
    
    def launch(self, server_name="0.0.0.0", server_port=7860, share=False, debug=False):
        """
        Launch the Gradio interface.
        
        Args:
            server_name: Host to run the UI on
            server_port: Port to run the UI on
            share: Whether to create a public URL
            debug: Whether to enable debug mode
        
        Returns:
            The Gradio interface
        """
        interface = self.create_interface()
        interface.launch(
            server_name=server_name,
            server_port=server_port,
            share=share,
            debug=debug
        )
        return interface

def create_integration(api_key=None):
    """
    Create an Enhanced Devin Gradio integration.
    
    Args:
        api_key: API key for Devin API
    
    Returns:
        The integration instance
    """
    # Create components
    api_client = EnhancedDevinAPIClient(api_key=api_key)
    api_monitor = APIMonitor()
    event_logger = EventLogger(log_file="enhanced_devin_ui.log")
    tool_registry = ToolRegistry()
    
    # Create integration
    integration = EnhancedDevinGradioIntegration(
        api_client=api_client,
        api_monitor=api_monitor,
        event_logger=event_logger,
        tool_registry=tool_registry
    )
    
    return integration

def launch_integration(api_key=None, port=7860, host="0.0.0.0", share=False, debug=False):
    """
    Launch the Enhanced Devin Gradio integration.
    
    Args:
        api_key: API key for Devin API
        port: Port to run the UI on
        host: Host to run the UI on
        share: Whether to create a public URL
        debug: Whether to enable debug mode
    
    Returns:
        The Gradio interface
    """
    # Create integration
    integration = create_integration(api_key=api_key)
    
    # Launch interface
    return integration.launch(
        server_name=host,
        server_port=port,
        share=share,
        debug=debug
    )

if __name__ == "__main__":
    import argparse
    
    # Parse arguments
    parser = argparse.ArgumentParser(description="Enhanced Devin Gradio Integration")
    parser.add_argument("--api-key", help="API key for Devin API")
    parser.add_argument("--port", type=int, default=7860, help="Port to run the UI on")
    parser.add_argument("--host", default="0.0.0.0", help="Host to run the UI on")
    parser.add_argument("--share", action="store_true", help="Create a public URL")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    
    # Launch integration
    launch_integration(
        api_key=args.api_key,
        port=args.port,
        host=args.host,
        share=args.share,
        debug=args.debug
    )
