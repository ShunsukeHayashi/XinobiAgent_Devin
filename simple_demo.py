"""
Simple demo script for the GenericAgent implementation.
This script demonstrates the Working Backwards methodology with a simple goal.
"""

import asyncio
import logging
from typing import List

from app.agent.generic_agent import GenericAgent
from app.tool import Bash, PythonExecute, ToolCollection, Terminate


# Configure logging to show more details
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


async def run_simple_demo() -> None:
    """Run a simple demonstration of the GenericAgent."""
    print("\n" + "="*80)
    print(f"DEMO: GenericAgent with Working Backwards Methodology")
    print(f"GOAL: Calculate the first 10 Fibonacci numbers and save them to a file")
    print("="*80 + "\n")
    
    # Create a tool collection with useful tools
    tools = ToolCollection([
        Bash(),
        PythonExecute(),
        Terminate()
    ])

    # Create the generic agent
    agent = GenericAgent(
        name="fibonacci_calculator",
        description="Calculates Fibonacci numbers using Working Backwards methodology",
        available_tools=tools,
        max_steps=10  # Limit steps for demo purposes
    )
    
    # Set the goal
    await agent.set_goal("Calculate the first 10 Fibonacci numbers and save them to a file")
    
    # Run the agent
    print("\n🚀 STARTING AGENT EXECUTION\n")
    result = await agent.run()
    
    # Print the execution summary
    print("\n" + "="*80)
    print("EXECUTION SUMMARY")
    print("="*80)
    print(result)
    
    # Print the final plan status
    status = await agent.get_execution_status()
    print("\n" + "="*80)
    print("FINAL PLAN STATUS")
    print("="*80)
    print(status)
    
    # Check if a Fibonacci file was created
    print("\n" + "="*80)
    print("CHECKING RESULTS")
    print("="*80)
    
    bash_tool = Bash()
    result = await bash_tool.run("find ~ -name 'fibonacci*' -type f | xargs cat")
    print(f"Fibonacci file contents:\n{result}")


if __name__ == "__main__":
    asyncio.run(run_simple_demo())
