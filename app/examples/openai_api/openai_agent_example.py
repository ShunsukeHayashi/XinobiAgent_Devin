"""
Example of using the GenericAgent with the new OpenAI API format.
This demonstrates how to integrate the Working Backwards methodology
with the latest OpenAI API.
"""

import asyncio
import json
from typing import List, Dict, Any, Optional

from openai import OpenAI

from app.agent.generic_agent import GenericAgent
from app.tool import ToolCollection, Bash, PythonExecute, Terminate


async def run_with_openai_api(goal: str) -> Dict[str, Any]:
    """
    Run a task using the GenericAgent and then format the results
    using the new OpenAI API format.
    
    Args:
        goal: The goal to achieve
        
    Returns:
        Dict containing the formatted response
    """
    # First, run the GenericAgent to solve the task
    tools = ToolCollection([
        Bash(),
        PythonExecute(),
        Terminate()
    ])
    
    agent = GenericAgent(
        name="openai_agent",
        description="Solves tasks using Working Backwards methodology",
        available_tools=tools,
        max_steps=10
    )
    
    # Run the agent with the provided goal
    result = await agent.run(goal)
    
    # Get the execution status
    status = await agent.get_execution_status()
    
    # Format the results using the new OpenAI API format
    client = OpenAI()
    
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
    
    # Create the OpenAI API response
    response = client.responses.create(
        model="gpt-4o",
        input=[],
        text={
            "format": {
                "type": "text"
            },
            "value": f"Task completed: {goal}\n\nResult: {result}\n\nStatus: {status}"
        },
        reasoning=reasoning,
        tools=[],
        temperature=1,
        max_output_tokens=2048,
        top_p=1,
        store=True
    )
    
    return {
        "response": response,
        "agent_result": result,
        "agent_status": status
    }


async def main():
    """Run an example with the new OpenAI API format."""
    GOALS: List[str] = [
        "Calculate the first 10 Fibonacci numbers and save them to a file",
        "Create a simple Python web server that displays 'Hello, World!' on the home page",
        "Find the current date and time and save it to a file"
    ]
    
    # Choose a goal to execute
    selected_goal = GOALS[2]  # Using a simple date/time example
    
    print(f"Running OpenAI API example with goal: {selected_goal}")
    result = await run_with_openai_api(selected_goal)
    
    # Print the formatted response
    print("\n=== OPENAI API RESPONSE ===")
    print(json.dumps(result["response"], indent=2))
    
    print("\n=== AGENT RESULT ===")
    print(result["agent_result"])
    
    print("\n=== AGENT STATUS ===")
    print(result["agent_status"])


if __name__ == "__main__":
    asyncio.run(main())
