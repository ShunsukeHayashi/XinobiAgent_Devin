"""
Example usage of the GenericAgent with the Working Backwards methodology.

This example demonstrates how to create and use a GenericAgent to solve
a task by working backwards from the goal.
"""

import asyncio
from typing import List


from app.agent.generic_agent import GenericAgent
from app.tool import Bash, GoogleSearch, ToolCollection, Terminate, PythonExecute


async def run_generic_agent_example(goal: str) -> None:
    """
    Run an example of the GenericAgent with a specific goal.

    Args:
        goal: The goal to achieve
    """
    # Create a tool collection with useful tools
    tools = ToolCollection([
        Bash(),
        GoogleSearch(),
        PythonExecute(),
        Terminate()
    ])

    # Create the generic agent
    agent = GenericAgent(
        name="task_solver",
        description="Solves tasks using Working Backwards methodology",
        available_tools=tools,
        max_steps=15  # Limit steps to prevent excessive execution
    )

    # Run the agent with the provided goal
    result = await agent.run(goal)

    # Print the execution summary
    print("\n=== EXECUTION SUMMARY ===")
    print(result)

    # Print the final plan status
    status = await agent.get_execution_status()
    print("\n=== FINAL PLAN STATUS ===")
    print(status)

async def main():
    """Run the example."""
    GOALS: List[str] = [
        "Create a simple Python web server that displays 'Hello, World!' on the home page",
        "Calculate the first 10 Fibonacci numbers and save them to a file",
        "Find the current weather in Tokyo and create a summary report"
    ]

    # Choose a goal to execute
    selected_goal = GOALS[0]  # Change index to try different goals

    print(f"Running GenericAgent with goal: {selected_goal}")
    await run_generic_agent_example(selected_goal)

if __name__ == "__main__":
    asyncio.run(main())
