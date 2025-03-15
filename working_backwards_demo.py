"""
Working Backwards Methodology Demo
This script demonstrates the GenericAgent using the Working Backwards methodology
with a simple example that creates a Fibonacci sequence.
"""

import asyncio
import logging
import os
import time
from typing import List, Dict, Any

from app.agent.generic_agent import GenericAgent
from app.tool import ToolCollection, Terminate, PythonExecute, Bash
from app.schema import Message

# Configure logging to show detailed information
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')

# Create a simple logger for the demo
demo_logger = logging.getLogger("demo")

class DemoRunner:
    """Helper class to run and visualize the Working Backwards demo."""
    
    def __init__(self):
        """Initialize the demo runner."""
        self.agent = None
        self.goal = "Calculate the first 10 Fibonacci numbers and save them to a file"
        self.steps_taken = []
        
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
            name="fibonacci_calculator",
            description="Calculates Fibonacci numbers using Working Backwards methodology",
            available_tools=tools,
            max_steps=10  # Limit steps for demo
        )
        
        # Set the goal
        await self.agent.set_goal(self.goal)
        
    async def run_demo(self):
        """Run the demo with visualization."""
        print("\n" + "◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
        print(f"Working Backwards Methodology Demo")
        print(f"Goal: {self.goal}")
        print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
        
        # Set up the agent
        await self.setup_agent()
        
        # Add a hook to capture messages
        original_update_memory = self.agent.update_memory
        
        def memory_hook(role, content):
            if role == "assistant" and "step" in content.lower():
                step_info = {
                    "timestamp": time.time(),
                    "content": content
                }
                self.steps_taken.append(step_info)
                print(f"\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
                print(f"Agent Thinking: Step {len(self.steps_taken)}")
                print(content[:500] + "..." if len(content) > 500 else content)
                print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
            return original_update_memory(role, content)
        
        self.agent.update_memory = memory_hook
        
        # Run the agent
        print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
        print("Starting Agent Execution")
        print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
        
        result = await self.agent.run()
        
        # Print the execution summary
        print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
        print("Execution Summary")
        print(result)
        print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
        
        # Check for Fibonacci files
        print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
        print("Checking Results")
        
        # Use a direct shell command to find and display Fibonacci files
        import subprocess
        try:
            result = subprocess.run(
                "find /home/ubuntu -name 'fibonacci*' -type f | xargs cat 2>/dev/null || echo 'No Fibonacci files found'",
                shell=True,
                capture_output=True,
                text=True
            )
            print(f"Fibonacci file contents:\n{result.stdout}")
        except Exception as e:
            print(f"Error checking results: {e}")
        
        print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
        
        # Show the Working Backwards analysis
        print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
        print("Working Backwards Analysis")
        
        if hasattr(self.agent, 'backwards_steps') and self.agent.backwards_steps:
            for i, step in enumerate(reversed(self.agent.backwards_steps)):
                print(f"Step {i+1}: {step.get('description', 'Unknown step')}")
                if 'prerequisites' in step and step['prerequisites']:
                    print(f"  Prerequisites: {', '.join(step['prerequisites'])}")
                if 'tools_needed' in step and step['tools_needed']:
                    print(f"  Tools needed: {', '.join(step['tools_needed'])}")
                print()
        else:
            print("No backwards analysis steps recorded.")
        
        print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
        
        # Show the forward execution plan
        print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
        print("Forward Execution Plan")
        
        if hasattr(self.agent, 'forward_plan') and self.agent.forward_plan:
            for i, step in enumerate(self.agent.forward_plan):
                print(f"Step {i+1}: {step.get('description', 'Unknown step')}")
                if 'tools_needed' in step and step['tools_needed']:
                    print(f"  Tools used: {', '.join(step['tools_needed'])}")
                print()
        else:
            print("No forward execution plan recorded.")
        
        print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
        
        return result


async def main():
    """Run the Working Backwards methodology demo."""
    runner = DemoRunner()
    await runner.run_demo()


if __name__ == "__main__":
    asyncio.run(main())
