"""
Base agent class for the XinobiAgent framework.

This module defines the BaseAgent abstract class that all agent implementations
should inherit from to ensure a consistent interface.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any

from pydantic import BaseModel, Field


class BaseAgent(ABC, BaseModel):
    """
    Abstract base class for all agents in the XinobiAgent framework.
    """
    
    name: str = Field(description="Name of the agent")
    description: str = Field(description="Description of the agent's purpose")
    
    @abstractmethod
    async def run(self, request: Optional[str] = None) -> str:
        """
        Run the agent's main workflow.
        
        Args:
            request: Initial request for the agent.
            
        Returns:
            str: The agent's response.
        """
        pass
