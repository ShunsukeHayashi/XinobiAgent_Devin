"""
Tool-calling agent implementation.
"""

from typing import List, Dict, Any, Optional
import json
from pydantic import Field

from app.agent.base import BaseAgent
from app.schema import Message, ToolCall
from app.tool import ToolCollection
from app.logger import logger


class ToolCallAgent(BaseAgent):
    """
    An agent that can use tools to accomplish tasks.
    
    This agent can decide which tools to use and how to use them
    based on the current state and goal.
    """
    
    available_tools: ToolCollection = Field(
        default_factory=ToolCollection,
        description="The tools available to this agent"
    )
    messages: List[Message] = Field(
        default_factory=list,
        description="The agent's message history"
    )
    tool_calls: List[ToolCall] = Field(
        default_factory=list,
        description="The agent's pending tool calls"
    )
    special_tool_names: List[str] = Field(
        default=["terminate"],
        description="Names of special tools with specific handling"
    )
    
    class Config:
        arbitrary_types_allowed = True
    
    async def think(self) -> bool:
        """
        Process the current state and decide which tools to use.
        
        Returns:
            True if there are tool calls to make, False otherwise
        """
        # If there are pending tool calls, we don't need to think again
        if self.tool_calls:
            return True
            
        # Prepare the messages for the LLM
        messages = self.messages.copy()
        
        # Add the system prompt if not already present
        if not any(msg.role == "system" for msg in messages):
            messages.insert(0, Message.system_message(self.system_prompt))
            
        # Get tool schemas
        tool_schemas = self.available_tools.get_schemas()
        
        # Ask the LLM what to do next
        # This is a placeholder - in a real implementation, you would call an LLM API
        response = "I need to use the terminate tool to complete the task."
        
        # Parse the response to extract tool calls
        # This is a simplified implementation - in reality, you would parse the LLM's response
        # to extract structured tool calls
        
        # For this example, we'll just create a terminate tool call
        self.tool_calls = [
            ToolCall(
                tool_name="terminate",
                tool_args={"message": "Task completed successfully"}
            )
        ]
        
        # Add the assistant's response to the message history
        self.messages.append(Message.assistant_message(response))
        
        # Return True if there are tool calls to make
        return bool(self.tool_calls)
    
    async def act(self) -> str:
        """
        Execute the next tool call.
        
        Returns:
            The result of the tool call
        """
        # If there are no tool calls, return an error
        if not self.tool_calls:
            return "No tool calls to execute"
            
        # Get the next tool call
        tool_call = self.tool_calls.pop(0)
        
        # Get the tool
        tool = self.available_tools.get_tool(tool_call.tool_name)
        
        # If the tool doesn't exist, return an error
        if not tool:
            return f"Tool not found: {tool_call.tool_name}"
            
        # Execute the tool
        try:
            result = await tool.execute(**tool_call.tool_args)
        except Exception as e:
            result = f"Error executing tool: {str(e)}"
            
        # Update the tool call with the result
        tool_call.tool_result = result
        
        # Add the tool call result to the message history
        self.messages.append(
            Message.user_message(f"Tool result: {result}")
        )
        
        # If this is a special tool, handle it specially
        if tool_call.tool_name in self.special_tool_names:
            # For terminate, return a termination message
            if tool_call.tool_name == "terminate":
                return f"TERMINATING: {result}"
                
        # Return the result
        return result
