"""
Canva Agent Example

This example demonstrates how to use the GenericAgent with Working Backwards methodology
to create a presentation slide generator using the Canva API.
"""

import asyncio
import logging
import os
from typing import Dict, Any, List, Optional

from app.agent.generic_agent import GenericAgent
from app.tool.collection import ToolCollection
from app.tool.canva_api import CanvaAPITool
from app.tool.bash import Bash
from app.tool.terminate import Terminate

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_canva_agent_example(prompt: str) -> None:
    """
    Run an example of the GenericAgent with Canva API integration.
    
    Args:
        prompt: The prompt describing the presentation to create
    """
    # Create a tool collection with Canva API and other useful tools
    canva_api_key = os.environ.get("CANVA_API_KEY")
    
    tools = ToolCollection([
        CanvaAPITool(api_key=canva_api_key),
        Bash(),
        Terminate()
    ])
    
    # Create the generic agent
    agent = GenericAgent(
        name="canva_slide_generator",
        description="Creates presentation slides from text prompts using the Canva API",
        available_tools=tools,
        max_steps=20  # Allow more steps for complex presentations
    )
    
    # Define the goal for the agent
    goal = f"""
    Create a presentation based on the following prompt:
    
    {prompt}
    
    The presentation should have a coherent structure with appropriate text and images.
    Use the Canva API to create the presentation.
    Use appropriate templates for different types of content:
    - タイムライン (Timeline) for chronological information
    - フロー図 (Arrows) for process flows
    - サイクル (Cycle) for cyclical processes
    - アイコン (Icons) for feature highlights
    - ボックス (Boxes) for grouped information
    - 箇条書き (Bullets) for simple lists
    """
    
    # Run the agent with the goal
    logger.info(f"Running GenericAgent with goal to create presentation from prompt: {prompt}")
    result = await agent.run(goal)
    
    # Print the execution summary
    logger.info("\n=== EXECUTION SUMMARY ===")
    logger.info(result)
    
    # Print the final plan status
    status = await agent.get_execution_status()
    logger.info("\n=== FINAL PLAN STATUS ===")
    logger.info(status)

async def main():
    """Run the example."""
    PROMPTS: List[str] = [
        "AIの最新トレンドについてのビジネスプレゼンテーション",
        "気候変動に関する高校生向け教育プレゼンテーション",
        "新しいスマートフォン製品発売のためのマーケティングプレゼンテーション"
    ]
    
    # Choose a prompt to execute
    selected_prompt = PROMPTS[0]  # Change index to try different prompts
    
    logger.info(f"Running Canva Agent with prompt: {selected_prompt}")
    await run_canva_agent_example(selected_prompt)

if __name__ == "__main__":
    asyncio.run(main())
