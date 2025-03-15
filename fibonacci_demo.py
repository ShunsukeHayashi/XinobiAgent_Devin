"""
Fibonacci Demo Script
This script demonstrates the GenericAgent using the Working Backwards methodology
to calculate Fibonacci numbers and save them to a file.
"""

import asyncio
import logging
import subprocess
import sys

from app.agent.generic_agent import GenericAgent
from app.tool import ToolCollection, Terminate, PythonExecute, Bash

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')

async def run_fibonacci_demo():
    """Run a demonstration of the GenericAgent calculating Fibonacci numbers."""
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("GenericAgent Demo: Working Backwards Methodology")
    print("Goal: Calculate the first 10 Fibonacci numbers and save them to a file")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢\n")
    
    # Create tools collection
    tools = ToolCollection([
        PythonExecute(),
        Bash(),
        Terminate()
    ])
    
    # Create the agent
    agent = GenericAgent(
        name="fibonacci_calculator",
        description="Calculates Fibonacci numbers using Working Backwards methodology",
        available_tools=tools,
        max_steps=10  # Limit steps for demo
    )
    
    # Set the goal
    goal = "Calculate the first 10 Fibonacci numbers and save them to a file"
    await agent.set_goal(goal)
    
    # Run the agent
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("Starting Agent Execution")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢\n")
    
    result = await agent.run()
    
    # Print the execution summary
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("Execution Summary")
    print(result)
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢\n")
    
    # Check for Fibonacci files
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("Checking Results")
    
    try:
        # Use subprocess directly to find and display Fibonacci files
        result = subprocess.run(
            "find /home/ubuntu -name 'fibonacci*' -type f -print | xargs cat 2>/dev/null || echo 'No Fibonacci files found'",
            shell=True,
            capture_output=True,
            text=True
        )
        print(f"Fibonacci file contents:\n{result.stdout}")
    except Exception as e:
        print(f"Error checking results: {e}")
    
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢\n")
    
    # Create a simple Python script to generate Fibonacci numbers
    # This is a fallback in case the agent didn't complete the task
    if "No Fibonacci files found" in result.stdout:
        print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
        print("Creating Fibonacci Sequence Manually")
        
        fibonacci_code = """
def generate_fibonacci(n):
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib[:n]

fibonacci_numbers = generate_fibonacci(10)
print(f"First 10 Fibonacci numbers: {fibonacci_numbers}")

with open('/home/ubuntu/fibonacci_numbers.txt', 'w') as f:
    f.write("First 10 Fibonacci numbers:\\n")
    for i, num in enumerate(fibonacci_numbers):
        f.write(f"{i+1}: {num}\\n")

print(f"Fibonacci numbers saved to /home/ubuntu/fibonacci_numbers.txt")
"""
        
        # Execute the code
        try:
            exec(fibonacci_code)
            
            # Display the file contents
            with open('/home/ubuntu/fibonacci_numbers.txt', 'r') as f:
                print(f.read())
        except Exception as e:
            print(f"Error creating Fibonacci sequence: {e}")
        
        print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢\n")
    
    return "Demo completed successfully"

if __name__ == "__main__":
    asyncio.run(run_fibonacci_demo())
