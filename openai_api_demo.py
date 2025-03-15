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
    
    # Prepare the reasoning section
    reasoning = {
        "working_backwards_analysis": [],
        "forward_execution_plan": []
    }
    
    # Add backwards steps if available
    if hasattr(agent, 'backwards_steps') and agent.backwards_steps:
        for i, step in enumerate(agent.backwards_steps):
            reasoning["working_backwards_analysis"].append({
                "step_number": len(agent.backwards_steps) - i,
                "description": step.get('description', 'Unknown step'),
                "prerequisites": step.get('prerequisites', []),
                "tools_needed": step.get('tools_needed', [])
            })
    
    # Add forward plan if available
    if hasattr(agent, 'forward_plan') and agent.forward_plan:
        for i, step in enumerate(agent.forward_plan):
            reasoning["forward_execution_plan"].append({
                "step_number": i + 1,
                "description": step.get('description', 'Unknown step'),
                "tools_needed": step.get('tools_needed', []),
                "completed": i < agent.current_step_index
            })
    
    # Create a mock OpenAI API response (without actually calling the API)
    openai_response = {
        "model": "gpt-4o",
        "text": {
            "format": {
                "type": "text"
            },
            "value": f"Task completed: {goal}\n\nResult: {result}\n\nStatus: {status}"
        },
        "reasoning": reasoning,
        "tools": [],
        "temperature": 1,
        "max_output_tokens": 2048,
        "top_p": 1
    }
    
    # Print the formatted response
    print(json.dumps(openai_response, indent=2))
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
