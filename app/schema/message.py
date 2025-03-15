"""
Message schema for agent communication.
"""

from typing import Optional
from pydantic import BaseModel, Field


class Message(BaseModel):
    """
    A message in a conversation between a user and an agent.
    """
    
    role: str = Field(
        description="The role of the message sender (system, user, assistant)"
    )
    content: str = Field(
        description="The content of the message"
    )
    name: Optional[str] = Field(
        default=None,
        description="The name of the message sender"
    )
