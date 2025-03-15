"""
Demo script for the GenericAgent implementation with detailed output.
This script demonstrates the Working Backwards methodology in action.
"""

import asyncio
import logging
from typing import List

from app.agent.generic_agent import GenericAgent
from app.tool import Bash, GoogleSearch, ToolCollection, Terminate, PythonExecute


# Configure logging to show more details
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


async def run_demo(goal: str) -> None:
    """
    Run a demonstration of the GenericAgent with detailed output.

    Args:
        goal: The goal to achieve
    """
    print("\n" + "="*80)
    print(f"DEMO: GenericAgent with Working Backwards Methodology")
    print(f"GOAL: {goal}")
    print("="*80 + "\n")
    
    # Create a tool collection with useful tools
    tools = ToolCollection([
        Bash(),
        GoogleSearch(),
        PythonExecute(),
        Terminate()
    ])

    # Create the generic agent with visualization
    agent = GenericAgent(
        name="task_solver",
        description="Solves tasks using Working Backwards methodology",
        available_tools=tools,
        max_steps=10  # Limit steps for demo purposes
    )
    
    # Set up visualization hooks
    original_think = agent.think
    original_act = agent.act
    
    async def visualized_think():
        print("\n🤔 THINKING: Working backwards from goal...")
        result = await original_think()
        if agent.backwards_steps and not agent.plan_ready:
            print("\n📋 BACKWARDS ANALYSIS:")
            for i, step in enumerate(agent.backwards_steps):
                print(f"  Step {len(agent.backwards_steps)-i}: {step.get('description', 'Unknown step')}")
        return result
    
    async def visualized_act():
        if agent.plan_ready and agent.current_step_index < len(agent.forward_plan):
            current_step = agent.forward_plan[agent.current_step_index]
            print(f"\n🔄 EXECUTING: Step {agent.current_step_index+1}/{len(agent.forward_plan)}")
            print(f"  {current_step.get('description', 'Unknown step')}")
        
        result = await original_act()
        
        if agent.plan_ready and agent.completed_steps:
            latest_step = agent.completed_steps[-1]
            print(f"\n✅ COMPLETED: {latest_step.get('description', 'Unknown step')}")
            print(f"  Result: {latest_step.get('result', 'No result')[:100]}...")
        
        return result
    
    # Replace methods with visualized versions
    agent.think = visualized_think
    agent.act = visualized_act
    
    # Run the agent with the provided goal
    print("\n🚀 STARTING AGENT EXECUTION\n")
    result = await agent.run(goal)
    
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


async def main():
    """Run the demo with a selected goal."""
    GOALS: List[str] = [
        "Create a simple Python web server that displays 'Hello, World!' on the home page",
        "Calculate the first 10 Fibonacci numbers and save them to a file",
        "Find the current weather in Tokyo and create a summary report"
    ]

    # Choose a goal to execute
    selected_goal = GOALS[1]  # Using the Fibonacci example for demonstration
    
    await run_demo(selected_goal)


if __name__ == "__main__":
    asyncio.run(main())
