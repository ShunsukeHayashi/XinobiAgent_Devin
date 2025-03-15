"""
Base tool definition for agent actions.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class BaseTool(BaseModel):
    """
    Base class for all tools that agents can use.
    
    Tools provide specific capabilities to agents, allowing them to interact
    with the environment, process data, or perform other actions.
    """
    
    name: str = Field(
        description="The name of the tool"
    )
    description: str = Field(
        description="A description of what the tool does and how to use it"
    )
    
    async def execute(self, **kwargs) -> str:
        """
        Execute the tool with the provided arguments.
        
        Args:
            **kwargs: Arguments for the tool
            
        Returns:
            The result of executing the tool
        """
        raise NotImplementedError("Tool execution not implemented")
    
    def get_schema(self) -> Dict[str, Any]:
        """
        Get the schema for this tool.
        
        Returns:
            A dictionary describing the tool's parameters
        """
        raise NotImplementedError("Tool schema not implemented")
