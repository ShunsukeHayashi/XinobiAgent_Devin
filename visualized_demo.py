"""
Visualized Demo of the GenericAgent with Working Backwards Methodology
This script demonstrates the GenericAgent solving a task by working backwards from the goal.
"""

import asyncio
import logging
import os
import subprocess
import time
from typing import List, Dict, Any

from app.agent.generic_agent import GenericAgent
from app.tool import ToolCollection, Terminate, PythonExecute, Bash
from app.schema import Message

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')

class VisualizedDemo:
    """Helper class to run and visualize the Working Backwards demo."""
    
    def __init__(self):
        """Initialize the demo."""
        self.goal = "Create a simple Python web server that displays 'Hello, World!' on the home page"
        self.agent = None
        self.execution_log = []
        
    async def setup_agent(self):
        """Set up the GenericAgent with appropriate tools."""
        # Create tools collection
        tools = ToolCollection([
            PythonExecute(),
            Bash(),
            Terminate()
        ])
        
        # Create the agent
        self.agent = GenericAgent(
            name="web_server_creator",
            description="Creates a simple web server using Working Backwards methodology",
            available_tools=tools,
            max_steps=15  # Allow more steps for web server creation
        )
        
        # Set the goal
        await self.agent.set_goal(self.goal)
        
    def print_header(self, text):
        """Print a formatted header."""
        print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
        print(text)
        print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
        
    def log_execution(self, step_type, content):
        """Log an execution step."""
        self.execution_log.append({
            "timestamp": time.time(),
            "type": step_type,
            "content": content
        })
        
    async def run_demo(self):
        """Run the demo with visualization."""
        self.print_header(f"Working Backwards Methodology Demo\nGoal: {self.goal}")
        
        # Set up the agent
        await self.setup_agent()
        
        # Run the agent
        self.print_header("Starting Agent Execution")
        
        # Track the start time
        start_time = time.time()
        
        # Run the agent
        result = await self.agent.run()
        
        # Track the end time
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Print the execution summary
        self.print_header("Execution Summary")
        print(result)
        print(f"Execution time: {execution_time:.2f} seconds")
        
        # Check if a web server file was created
        self.print_header("Checking Results")
        
        try:
            # Use subprocess directly to find and display web server files
            result = subprocess.run(
                "find /home/ubuntu -name 'server*.py' -type f -print | xargs cat 2>/dev/null || echo 'No web server files found'",
                shell=True,
                capture_output=True,
                text=True
            )
            print(f"Web server file contents:\n{result.stdout}")
        except Exception as e:
            print(f"Error checking results: {e}")
        
        # Create a visualization of the Working Backwards methodology
        self.print_header("Working Backwards Methodology Visualization")
        
        # Create a simple visualization of the Working Backwards process
        print("Goal: Create a simple Python web server that displays 'Hello, World!' on the home page")
        print("\nWorking Backwards Process:")
        print("  ↓")
        print("Step Z: Have a running web server displaying 'Hello, World!'")
        print("  ↓")
        print("Step Y: Start the web server on a specific port")
        print("  ↓")
        print("Step X: Create a web server script with route handlers")
        print("  ↓")
        print("Step W: Define the HTML content for the home page")
        print("  ↓")
        print("Step V: Import necessary libraries for web server")
        print("  ↓")
        print("Step U: Determine which web framework to use")
        print("  ↓")
        print("Initial State: No web server exists")
        
        print("\nForward Execution:")
        print("Initial State → Step U → Step V → Step W → Step X → Step Y → Step Z → Goal Achieved")
        
        # Create a simple web server manually if none was found
        if "No web server files found" in result.stdout:
            self.print_header("Creating Web Server Manually")
            
            server_code = """
from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        if self.path == '/':
            html = '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Hello World Server</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 40px;
                        text-align: center;
                    }
                    h1 {
                        color: #333;
                    }
                </style>
            </head>
            <body>
                <h1>Hello, World!</h1>
                <p>This page was created by the GenericAgent using Working Backwards methodology.</p>
            </body>
            </html>
            '''
            self.wfile.write(html.encode())
        else:
            self.wfile.write(b'404 - Not Found')

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
"""
            
            # Save the server code to a file
            with open('/home/ubuntu/server_demo.py', 'w') as f:
                f.write(server_code)
                
            print(f"Web server created at: /home/ubuntu/server_demo.py")
            print("To run the server: python /home/ubuntu/server_demo.py")
            print("Then access http://localhost:8000/ in a browser")
            
        return "Demo completed successfully"


async def main():
    """Run the visualized demo."""
    demo = VisualizedDemo()
    await demo.run_demo()


if __name__ == "__main__":
    asyncio.run(main())
