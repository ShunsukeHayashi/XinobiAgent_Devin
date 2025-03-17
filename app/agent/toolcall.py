"""
ToolCallAgent implementation for the XinobiAgent framework.

This module defines the ToolCallAgent class that provides a foundation for
agents that need to use tools to accomplish tasks.
"""

from typing import Dict, List, Optional, Any
from abc import abstractmethod

from pydantic import BaseModel, Field

from app.agent.base import BaseAgent
from app.logger import logger
from app.schema.message import Message
from app.tool.collection import ToolCollection


class ToolCall(BaseModel):
    """
    A tool call made by an agent.
    """
    
    tool_name: str = Field(description="Name of the tool to call")
    tool_args: Dict[str, Any] = Field(default_factory=dict, description="Arguments for the tool call")


class AgentState(BaseModel):
    """
    State of an agent during execution.
    """
    
    messages: List[Message] = Field(default_factory=list, description="Message history")
    tool_calls: List[ToolCall] = Field(default_factory=list, description="Pending tool calls")
    thinking: str = Field(default="", description="Current thinking process")
    memory: Dict[str, Any] = Field(default_factory=dict, description="Agent memory")


class ToolCallAgent(BaseAgent):
    """
    An agent that can use tools to accomplish tasks.
    
    This class provides the foundation for agents that need to use tools,
    including methods for thinking, acting, and managing tool calls.
    """
    
    name: str = Field(description="Name of the agent")
    description: str = Field(description="Description of the agent's purpose")
    
    # Tool management
    available_tools: ToolCollection = Field(
        default_factory=ToolCollection,
        description="Collection of tools available to the agent"
    )
    special_tool_names: List[str] = Field(
        default=["terminate"],
        description="Names of special tools that have specific handling"
    )
    
    # State management
    messages: List[Message] = Field(
        default_factory=list,
        description="Message history"
    )
    memory: Dict[str, Any] = Field(
        default_factory=dict,
        description="Agent memory"
    )
    tool_calls: List[ToolCall] = Field(
        default_factory=list,
        description="Pending tool calls"
    )
    
    # Configuration
    max_steps: int = Field(
        default=10,
        description="Maximum number of steps the agent can take"
    )
    
    def update_memory(self, role: str, content: str) -> None:
        """
        Update the agent's memory with a new message.
        
        Args:
            role: The role of the message sender (system, user, assistant)
            content: The content of the message
        """
        self.messages.append(Message(role=role, content=content))
    
    @abstractmethod
    async def think(self) -> bool:
        """
        Process the current state and decide the next action.
        
        Returns:
            bool: True if there are actions to take, False otherwise.
        """
        # This method should be implemented by subclasses
        pass
    
    async def act(self) -> str:
        """
        Execute the next action based on the current tool calls.
        
        Returns:
            str: Result of the action.
        """
        if not self.tool_calls:
            return "No actions to take."
        
        # Get the next tool call
        tool_call = self.tool_calls.pop(0)
        
        # Check if it's a special tool
        if tool_call.tool_name in self.special_tool_names:
            # Handle termination
            if tool_call.tool_name == "terminate":
                reason = tool_call.tool_args.get("reason", "Task completed")
                return f"Agent execution terminated: {reason}"
        
        # Find the tool
        tool = self.available_tools.get_tool(tool_call.tool_name)
        if not tool:
            return f"Error: Tool '{tool_call.tool_name}' not found."
        
        try:
            # Execute the tool
            result = await tool.run(**tool_call.tool_args)
            return result
        except Exception as e:
            error_message = f"Error executing tool '{tool_call.tool_name}': {str(e)}"
            logger.error(error_message)
            return error_message
    
    async def run(self, request: Optional[str] = None) -> str:
        """
        Run the agent's main workflow.
        
        Args:
            request: Initial request for the agent.
            
        Returns:
            str: The agent's response.
        """
        if request:
            self.update_memory("user", request)
        
        steps_taken = 0
        result = ""
        
        while steps_taken < self.max_steps:
            # Think about what to do next
            has_actions = await self.think()
            
            if not has_actions:
                break
            
            # Execute the action
            result = await self.act()
            
            # Update the memory with the result
            self.update_memory("system", f"Action result: {result}")
            
            # Check for termination
            if "Agent execution terminated" in result:
                break
            
            steps_taken += 1
        
        if steps_taken >= self.max_steps:
            logger.warning(f"Agent reached maximum steps ({self.max_steps})")
            result = f"Reached maximum steps ({self.max_steps}). Last result: {result}"
        
        return result
    
    def get_state(self) -> AgentState:
        """
        Get the current state of the agent.
        
        Returns:
            AgentState: The current state.
        """
        return AgentState(
            messages=self.messages,
            tool_calls=self.tool_calls,
            memory=self.memory
        )
    
    def set_state(self, state: AgentState) -> None:
        """
        Set the state of the agent.
        
        Args:
            state: The state to set.
        """
        self.messages = state.messages
        self.tool_calls = state.tool_calls
        self.memory = state.memory
