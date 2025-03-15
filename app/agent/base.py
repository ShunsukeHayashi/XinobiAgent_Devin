"""
Base agent implementation.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from app.schema import Message
from app.logger import logger


class BaseAgent(BaseModel):
    """
    Base class for all agents in the system.
    
    This provides common functionality for agents, such as memory
    management and message handling.
    """
    
    name: str = Field(
        description="The name of the agent"
    )
    description: str = Field(
        description="A description of what the agent does"
    )
    system_prompt: str = Field(
        default="You are a helpful AI assistant.",
        description="The system prompt for the agent"
    )
    memory: List[Message] = Field(
        default_factory=list,
        description="The agent's memory (list of messages)"
    )
    
    async def think(self) -> bool:
        """
        Process the current state and decide the next action.
        
        Returns:
            True if there are actions to take, False otherwise
        """
        raise NotImplementedError("Agent thinking not implemented")
    
    async def act(self) -> str:
        """
        Execute the decided action.
        
        Returns:
            The result of the action
        """
        raise NotImplementedError("Agent action not implemented")
    
    async def run(self, request: Optional[str] = None) -> str:
        """
        Execute the agent's main workflow.
        
        Args:
            request: Initial request for the agent
            
        Returns:
            The final result
        """
        # Add the request to memory if provided
        if request:
            self.memory.append(Message.user_message(request))
            
        # Add the system prompt to memory if not already present
        if not any(msg.role == "system" for msg in self.memory):
            self.memory.insert(0, Message.system_message(self.system_prompt))
            
        # Run the agent's workflow
        while True:
            # Think about what to do next
            has_actions = await self.think()
            
            # If there are no more actions, we're done
            if not has_actions:
                break
                
            # Execute the action
            result = await self.act()
            
            # If the result indicates termination, we're done
            if result.startswith("TERMINATING:"):
                return result[len("TERMINATING:"):].strip()
                
        # Return a summary of what was done
        return "Task completed successfully"
    
    def update_memory(self, role: str, content: str) -> None:
        """
        Add a message to the agent's memory.
        
        Args:
            role: The role of the message sender
            content: The content of the message
        """
        if role == "user":
            self.memory.append(Message.user_message(content))
        elif role == "assistant":
            self.memory.append(Message.assistant_message(content))
        elif role == "system":
            self.memory.append(Message.system_message(content))
        else:
            raise ValueError(f"Invalid role: {role}")
