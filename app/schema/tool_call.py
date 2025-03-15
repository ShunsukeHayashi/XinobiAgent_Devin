"""
Tool call schema for agent actions.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    """
    A tool call made by an agent.
    
    This represents an action that the agent wants to take using a specific tool.
    """
    
    tool_name: str = Field(
        description="The name of the tool to call"
    )
    tool_args: Dict[str, Any] = Field(
        default_factory=dict,
        description="Arguments to pass to the tool"
    )
    tool_result: Optional[str] = Field(
        default=None,
        description="The result of the tool call, if available"
    )
