"""
Message schema for agent communication.
"""

from typing import Dict, List, Optional, Any, Literal
from pydantic import BaseModel, Field


class Message(BaseModel):
    """
    A message in the agent system.
    
    This can be a user message, assistant message, or system message.
    """
    
    role: Literal["user", "assistant", "system"] = Field(
        description="The role of the message sender"
    )
    content: str = Field(
        description="The content of the message"
    )
    
    @classmethod
    def user_message(cls, content: str) -> "Message":
        """Create a user message."""
        return cls(role="user", content=content)
    
    @classmethod
    def assistant_message(cls, content: str) -> "Message":
        """Create an assistant message."""
        return cls(role="assistant", content=content)
    
    @classmethod
    def system_message(cls, content: str) -> "Message":
        """Create a system message."""
        return cls(role="system", content=content)
