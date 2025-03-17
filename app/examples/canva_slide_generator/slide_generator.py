"""
Canva Slide Generator Example

This example demonstrates how to use the XinobiAgent framework with the Working Backwards
methodology to create a presentation slide generator using the Canva API.

The slide generator takes a text prompt and generates a complete presentation with
appropriate slides, text, and images.
"""

import asyncio
import json
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

async def create_slide_generator_agent(api_key: Optional[str] = None) -> GenericAgent:
    """
    Create a GenericAgent configured for slide generation using the Canva API.
    
    Args:
        api_key: Optional Canva API key (if not provided, will look for CANVA_API_KEY env var)
        
    Returns:
        Configured GenericAgent
    """
    # Create the Canva API tool
    canva_tool = CanvaAPITool(api_key=api_key)
    
    # Create a tool collection with the Canva API tool and other useful tools
    tools = ToolCollection([
        canva_tool,
        Bash(),
        Terminate(),
    ])
    
    # Create the agent
    agent = GenericAgent(
        name="canva_slide_generator",
        description="Creates presentation slides from text prompts using the Canva API",
        available_tools=tools,
        max_steps=20,  # Allow more steps for complex presentations
    )
    
    return agent

async def generate_slides_from_prompt(
    prompt: str,
    num_slides: int = 5,
    title: Optional[str] = None,
    api_key: Optional[str] = None,
    template_type: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate a presentation from a text prompt using the Canva API.
    
    Args:
        prompt: Text prompt describing the desired presentation
        num_slides: Number of slides to generate
        title: Optional title for the presentation
        api_key: Optional Canva API key
        template_type: Optional template type to apply
        
    Returns:
        Dictionary containing the generated presentation details
    """
    # Create the agent
    agent = await create_slide_generator_agent(api_key)
    
    # Define the goal for the agent
    goal = f"""
    Create a presentation with {num_slides} slides based on the following prompt:
    
    {prompt}
    
    The presentation should have a coherent structure with appropriate text and images.
    Use appropriate templates for different types of content:
    - タイムライン (Timeline) for chronological information
    - フロー図 (Arrows) for process flows
    - サイクル (Cycle) for cyclical processes
    - アイコン (Icons) for feature highlights
    - ボックス (Boxes) for grouped information
    - 箇条書き (Bullets) for simple lists
    """
    
    if title:
        goal += f"\nThe presentation should be titled: {title}"
    
    if template_type:
        goal += f"\nUse the {template_type} template for all slides."
    
    # Run the agent with the goal
    result = await agent.run(goal)
    
    # Extract the presentation details from the result
    # In a real implementation, this would parse the agent's output to get the presentation ID
    # For now, we'll return the raw result
    return {
        "result": result,
        "prompt": prompt,
        "num_slides": num_slides,
        "title": title,
        "template_type": template_type,
    }

async def main():
    """
    Run the slide generator example.
    """
    # Example prompts
    prompts = [
        "Create a business presentation about artificial intelligence trends in 2025",
        "Design an educational presentation about climate change for high school students",
        "Make a marketing presentation for a new smartphone product launch",
    ]
    
    # Select a prompt
    selected_prompt = prompts[0]  # Change index to try different prompts
    
    # Get API key from environment variable
    api_key = os.environ.get("CANVA_API_KEY")
    
    if not api_key:
        logger.warning("No Canva API key found in environment variables. Using mock API responses.")
    
    # Generate slides
    logger.info(f"Generating slides for prompt: {selected_prompt}")
    result = await generate_slides_from_prompt(
        prompt=selected_prompt,
        num_slides=5,
        title="AI Trends 2025",
        api_key=api_key,
    )
    
    # Print the result
    logger.info("Slide generation complete!")
    logger.info(f"Result: {json.dumps(result, indent=2)}")

if __name__ == "__main__":
    asyncio.run(main())
