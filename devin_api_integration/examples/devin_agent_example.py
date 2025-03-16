"""
Example usage of the DevinAgent with the Devin API.
"""

import os
import asyncio
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the DevinAgent
from devin_api_integration.src.devin_agent import DevinAgent

async def run_simple_task_example():
    """
    Run a simple task using the DevinAgent.
    """
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("Devin API Example: Simple Task")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢\n")
    
    # Create the agent
    agent = DevinAgent(
        name="example_agent",
        description="Example agent for demonstrating Devin API integration",
        api_key=os.environ.get("DEVIN_API_KEY")
    )
    
    # Create a task
    prompt = "Create a simple Python function that calculates the Fibonacci sequence"
    
    try:
        # Create the task
        session_id = await agent.create_task(prompt)
        
        print(f"Created task with session ID: {session_id}")
        
        # Get the status
        status = await agent.get_status()
        
        print(f"Session status: {status}")
        
        # Send a follow-up message
        await agent.send_follow_up("Please optimize the function for performance")
        
        print("Sent follow-up message")
        
        # Get the updated status
        status = await agent.get_status()
        
        print(f"Updated session status: {status}")
        
    except Exception as e:
        logger.error(f"Error running task: {str(e)}")
        print(f"Error: {str(e)}")

async def run_xinobi_template_example():
    """
    Run a task using a XinobiAgent template.
    """
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("Devin API Example: XinobiAgent Template")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢\n")
    
    # Create the agent
    agent = DevinAgent(
        name="xinobi_agent",
        description="Agent for demonstrating XinobiAgent template integration",
        api_key=os.environ.get("DEVIN_API_KEY")
    )
    
    # Create a template
    template_data = {
        "user_input": "I need a Python script that can download stock price data and create a chart",
        "fixed_goals": [
            "Create a Python script for downloading stock price data",
            "Generate a chart visualization of the data"
        ],
        "tasks": [
            "Set up the environment and required libraries",
            "Implement data download functionality",
            "Create chart visualization",
            "Add error handling and documentation"
        ]
    }
    
    try:
        # Format the prompt
        prompt = await agent.format_prompt_from_xinobi_template(template_data)
        
        print(f"Formatted prompt:\n{prompt}\n")
        
        # Create the task
        session_id = await agent.run_task_from_xinobi_template(template_data)
        
        print(f"Created task with session ID: {session_id}")
        
        # Get the status
        status = await agent.get_status()
        
        print(f"Session status: {status}")
        
    except Exception as e:
        logger.error(f"Error running task: {str(e)}")
        print(f"Error: {str(e)}")

async def run_file_upload_example():
    """
    Run an example that uploads a file to provide context.
    """
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("Devin API Example: File Upload")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢\n")
    
    # Create the agent
    agent = DevinAgent(
        name="file_upload_agent",
        description="Agent for demonstrating file upload",
        api_key=os.environ.get("DEVIN_API_KEY")
    )
    
    # Create a temporary file
    import tempfile
    
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp:
        temp.write(b"""
# Example Python file
def hello_world():
    print("Hello, world!")

if __name__ == "__main__":
    hello_world()
""")
        temp_file_path = temp.name
    
    try:
        # Upload the file
        attachment_id = await agent.upload_context_file(temp_file_path)
        
        print(f"Uploaded file with attachment ID: {attachment_id}")
        
        # Create a task that references the file
        prompt = f"Analyze the Python file I uploaded and suggest improvements"
        
        session_id = await agent.create_task(prompt)
        
        print(f"Created task with session ID: {session_id}")
        
        # Get the status
        status = await agent.get_status()
        
        print(f"Session status: {status}")
        
    except Exception as e:
        logger.error(f"Error running task: {str(e)}")
        print(f"Error: {str(e)}")
    finally:
        # Clean up the temporary file
        os.unlink(temp_file_path)

async def main():
    """
    Run all examples.
    """
    # Check if API key is set
    if not os.environ.get("DEVIN_API_KEY"):
        print("Error: DEVIN_API_KEY environment variable not set")
        print("Please set the DEVIN_API_KEY environment variable to your Devin API key")
        return
    
    # Run the examples
    await run_simple_task_example()
    await run_xinobi_template_example()
    await run_file_upload_example()

if __name__ == "__main__":
    asyncio.run(main())
