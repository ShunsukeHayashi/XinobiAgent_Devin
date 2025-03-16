"""
Example usage of the GenericAgent for Kindle Unlimited affiliate marketing.

This example demonstrates how to use the GenericAgent with the Working Backwards
methodology to implement a Kindle Unlimited affiliate marketing strategy.
"""

import asyncio
from typing import List

from app.agent.generic_agent import GenericAgent
from app.tool.collection import ToolCollection
from app.tool.base import BaseTool
from pydantic import Field


class BlogPostTool(BaseTool):
    """Tool for creating blog posts about Kindle Unlimited books."""
    
    name: str = "blog_post_tool"
    description: str = "Creates blog posts about Kindle Unlimited books"
    
    async def run(self, topic: str = "", persona: str = "", **kwargs) -> str:
        """
        Create a blog post about Kindle Unlimited books.
        
        Args:
            topic: The topic of the blog post
            persona: The target reader persona
            
        Returns:
            A confirmation message
        """
        return f"Created blog post about '{topic}' for {persona} persona"


class SocialMediaTool(BaseTool):
    """Tool for creating social media posts about Kindle Unlimited books."""
    
    name: str = "social_media_tool"
    description: str = "Creates social media posts about Kindle Unlimited books"
    
    async def run(self, platform: str = "", content: str = "", **kwargs) -> str:
        """
        Create a social media post about Kindle Unlimited books.
        
        Args:
            platform: The social media platform
            content: The content of the post
            
        Returns:
            A confirmation message
        """
        return f"Created {platform} post with content: {content[:50]}..."


class EmailCampaignTool(BaseTool):
    """Tool for creating email campaigns about Kindle Unlimited books."""
    
    name: str = "email_campaign_tool"
    description: str = "Creates email campaigns about Kindle Unlimited books"
    
    async def run(self, subject: str = "", segment: str = "", content: str = "", **kwargs) -> str:
        """
        Create an email campaign about Kindle Unlimited books.
        
        Args:
            subject: The subject of the email
            segment: The target segment
            content: The content of the email
            
        Returns:
            A confirmation message
        """
        return f"Created email campaign with subject '{subject}' for {segment} segment"


class AnalyticsTool(BaseTool):
    """Tool for analyzing campaign performance."""
    
    name: str = "analytics_tool"
    description: str = "Analyzes campaign performance"
    
    async def run(self, campaign_type: str = "", metric: str = "", **kwargs) -> str:
        """
        Analyze campaign performance.
        
        Args:
            campaign_type: The type of campaign to analyze
            metric: The metric to analyze
            
        Returns:
            Analysis results
        """
        # Simulate different metrics for different campaign types
        if campaign_type == "blog":
            if metric == "traffic":
                return "Blog traffic: 1,200 page views"
            elif metric == "conversion":
                return "Blog conversion rate: 12%"
        elif campaign_type == "social":
            if metric == "engagement":
                return "Social engagement: 350 likes, 45 shares"
            elif metric == "clicks":
                return "Social clicks: 280 clicks"
        elif campaign_type == "email":
            if metric == "open_rate":
                return "Email open rate: 32%"
            elif metric == "click_rate":
                return "Email click rate: 8%"
        
        return f"Analyzed {metric} for {campaign_type} campaign"


async def run_kindle_unlimited_agent() -> None:
    """
    Run the GenericAgent for Kindle Unlimited affiliate marketing.
    """
    # Create custom tools for Kindle Unlimited affiliate marketing
    tools = ToolCollection([
        BlogPostTool(),
        SocialMediaTool(),
        EmailCampaignTool(),
        AnalyticsTool()
    ])
    
    # Create the generic agent
    agent = GenericAgent(
        name="kindle_unlimited_agent",
        description="Agent for Kindle Unlimited affiliate marketing",
        available_tools=tools,
        max_steps=20
    )
    
    # Define the goal for the Kindle Unlimited affiliate marketing campaign
    goal = """
    Implement a Kindle Unlimited affiliate marketing campaign from March 18 to April 18, 2025
    targeting commuters, manga fans, and self-improvement enthusiasts through blog posts,
    social media, and email marketing to achieve 1,000+ blog post page views, 30%+ email open rate,
    and 10%+ registration conversion rate while complying with Amazon Associate Program rules.
    """
    
    # Run the agent with the goal
    result = await agent.run(goal)
    
    # Print the result
    print("\n=== EXECUTION RESULT ===")
    print(result)
    
    # Print the execution status
    status = await agent.get_execution_status()
    print("\n=== EXECUTION STATUS ===")
    print(status)


async def main() -> None:
    """Run the Kindle Unlimited affiliate marketing example."""
    print("Running Kindle Unlimited Affiliate Marketing Agent...")
    await run_kindle_unlimited_agent()


if __name__ == "__main__":
    asyncio.run(main())
