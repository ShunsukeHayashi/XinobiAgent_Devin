"""
Base tool for agent use.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class BaseTool(BaseModel):
    """
    Base class for tools that can be used by an agent.
    """
    
    name: str = Field(
        description="Name of the tool"
    )
    description: str = Field(
        description="Description of what the tool does"
    )
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Parameters that the tool accepts"
    )
    
    async def run(self, **kwargs) -> str:
        """
        Run the tool with the provided arguments.
        
        Args:
            **kwargs: Arguments to pass to the tool
            
        Returns:
            The result of running the tool
        """
        raise NotImplementedError("Subclasses must implement this method")
