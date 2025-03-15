"""
Demo script for using the GenericAgent with the new OpenAI API format.
"""

import asyncio
import json
from typing import Dict, Any

from openai import OpenAI

from app.agent.generic_agent import GenericAgent
from app.tool import ToolCollection, Bash, PythonExecute, Terminate


async def run_openai_api_demo():
    """Run a demonstration of the GenericAgent with the new OpenAI API format."""
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("OpenAI API Demo: Working Backwards Methodology")
    print("Goal: Find the current date and time and save it to a file")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢\n")
    
    # Create tools collection
    tools = ToolCollection([
        PythonExecute(),
        Bash(),
        Terminate()
    ])
    
    # Create the agent
    agent = GenericAgent(
        name="datetime_agent",
        description="Finds the current date and time using Working Backwards methodology",
        available_tools=tools,
        max_steps=5  # Simple task needs fewer steps
    )
    
    # Set the goal
    goal = "Find the current date and time and save it to a file"
    await agent.set_goal(goal)
    
    # Run the agent
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("Starting Agent Execution")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢\n")
    
    result = await agent.run()
    
    # Get the execution status
    status = await agent.get_execution_status()
    
    # Print the execution summary
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("Execution Summary")
    print(result)
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢\n")
    
    # Format the results using the new OpenAI API format
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("Converting to OpenAI API Format")
    
    # Create a simple example of using the OpenAI API directly
    client = OpenAI()
    
    # Create a simple example of using the OpenAI API directly
    example_response = client.responses.create(
        model="gpt-4o",
        input=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": f"Task completed: {goal}\n\nResult: {result}\n\nStatus: {status}"
            }
        ],
        text={
            "format": {
                "type": "text"
            }
        },
        reasoning={},
        tools=[],
        temperature=1,
        max_output_tokens=2048,
        top_p=1,
        store=True
    )
    
    # Print the formatted response
    response_text = ""
    if example_response.output and len(example_response.output) > 0:
        for output_item in example_response.output:
            if hasattr(output_item, 'content') and output_item.content:
                for content_item in output_item.content:
                    if hasattr(content_item, 'text') and content_item.text:
                        response_text += content_item.text
    
    print(f"OpenAI API Response: {response_text[:200]}...")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢\n")
    
    # Check for datetime files
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("Checking Results")
    
    import subprocess
    try:
        # Use subprocess directly to find and display datetime files
        result = subprocess.run(
            "find /home/ubuntu -name 'date*' -type f -mmin -5 -print | xargs cat 2>/dev/null || echo 'No recent datetime files found'",
            shell=True,
            capture_output=True,
            text=True
        )
        print(f"Datetime file contents:\n{result.stdout}")
    except Exception as e:
        print(f"Error checking results: {e}")
    
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢\n")
    
    return "Demo completed successfully"


if __name__ == "__main__":
    asyncio.run(run_openai_api_demo())
