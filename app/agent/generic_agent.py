"""
GenericAgent implementation using the Working Backwards methodology.
This implementation uses the new OpenAI API format.
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Union

from openai import OpenAI
from pydantic import BaseModel, Field

from app.schema.message import Message
from app.tool.collection import ToolCollection

# Configure logging
logger = logging.getLogger(__name__)


class GenericAgent(BaseModel):
    """
    A generic agent that uses the Working Backwards methodology to solve problems.
    This implementation uses the new OpenAI API format.
    """
    
    name: str = Field(description="Name of the agent")
    description: str = Field(description="Description of the agent's purpose")
    available_tools: Optional[ToolCollection] = Field(
        default=None, 
        description="Collection of tools available to the agent"
    )
    max_steps: int = Field(
        default=15, 
        description="Maximum number of steps the agent can take"
    )
    goal: Optional[str] = Field(
        default=None,
        description="The goal that the agent is trying to achieve"
    )
    
    # Internal state tracking
    memory: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Memory of the agent's conversation"
    )
    backwards_steps: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Steps identified during backwards planning"
    )
    forward_plan: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Steps for forward execution"
    )
    completed_steps: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Steps that have been completed"
    )
    current_step_index: int = Field(
        default=0,
        description="Index of the current step in the forward plan"
    )
    plan_ready: bool = Field(
        default=False,
        description="Whether the plan is ready for execution"
    )
    
    # OpenAI client
    _client: Optional[OpenAI] = None
    
    class Config:
        arbitrary_types_allowed = True
    
    def __init__(self, **data):
        super().__init__(**data)
        self._client = OpenAI()
    
    async def set_goal(self, goal: str) -> None:
        """
        Set the goal for the agent to achieve.
        
        Args:
            goal: The goal to achieve
        """
        self.goal = goal
        self.update_memory("system", f"Your goal is to: {goal}")
    
    def update_memory(self, role: str, content: str) -> None:
        """
        Update the agent's memory with a new message.
        
        Args:
            role: The role of the message sender (system, user, assistant)
            content: The content of the message
        """
        self.memory.append({"role": role, "content": content})
        
    def _extract_text_from_response(self, response) -> str:
        """
        Extract text from an OpenAI API response.
        
        Args:
            response: The OpenAI API response
            
        Returns:
            The extracted text as a string
        """
        text = ""
        if response.output and len(response.output) > 0:
            for output_item in response.output:
                if hasattr(output_item, 'content') and output_item.content:
                    for content_item in output_item.content:
                        if hasattr(content_item, 'text') and content_item.text:
                            text += content_item.text
        return text
    
    async def run(self, goal: Optional[str] = None) -> str:
        """
        Run the agent to achieve the specified goal.
        
        Args:
            goal: The goal to achieve, if not already set
            
        Returns:
            A summary of the execution
        """
        if goal:
            await self.set_goal(goal)
        
        if not self.goal:
            raise ValueError("Goal must be set before running the agent")
        
        # First, plan by working backwards from the goal
        await self._plan_backwards()
        
        # Then, execute the plan forwards
        result = await self._execute_plan()
        
        return result
    
    async def _plan_backwards(self) -> None:
        """
        Plan by working backwards from the goal to the initial state.
        This uses the Working Backwards methodology.
        """
        # Start with the goal
        self.update_memory("system", "Plan by working backwards from the goal. What is the final step needed to achieve the goal?")
        
        # Use the new OpenAI API format for planning
        response = self._client.responses.create(
            model="gpt-4o",
            input=[
                {
                    "role": "system",
                    "content": f"You are a planning agent that uses the Working Backwards methodology. Your goal is: {self.goal}"
                },
                {
                    "role": "user",
                    "content": "What is the final step needed to achieve the goal?"
                }
            ],
            text={
                "format": {
                    "type": "text"
                }
            },
            reasoning={},
            tools=[],
            temperature=0.7,
            max_output_tokens=2048,
            top_p=1,
            store=True
        )
        
        # Extract the response text using helper method
        final_step_description = self._extract_text_from_response(response)
        
        # Add the final step to the backwards steps
        final_step = {
            "description": final_step_description,
            "prerequisites": [],
            "tools_needed": []
        }
        self.backwards_steps.append(final_step)
        
        # Continue working backwards until we reach the initial state
        current_step = final_step
        max_backwards_steps = 10  # Limit to prevent infinite loops
        
        for i in range(max_backwards_steps):
            # Ask what needs to be done before the current step
            step_query = f"What needs to be done before this step: '{current_step['description']}'?"
            self.update_memory("system", step_query)
            
            # Use the new OpenAI API format for step-back questioning
            response = self._client.responses.create(
                model="gpt-4o",
                input=[
                    {
                        "role": "system",
                        "content": f"You are a planning agent that uses the Working Backwards methodology. Your goal is: {self.goal}"
                    },
                    {
                        "role": "user",
                        "content": step_query
                    }
                ],
                text={
                    "format": {
                        "type": "text"
                    }
                },
                reasoning={},
                tools=[],
                temperature=0.7,
                max_output_tokens=2048,
                top_p=1,
                store=True
            )
            
            # Extract the response text using helper method
            previous_step_description = self._extract_text_from_response(response)
            
            # Check if we've reached the initial state
            if "initial state" in previous_step_description.lower() or "already at initial state" in previous_step_description.lower():
                break
            
            # Add the previous step to the backwards steps
            previous_step = {
                "description": previous_step_description,
                "prerequisites": [],
                "tools_needed": []
            }
            self.backwards_steps.append(previous_step)
            
            # Update the current step
            current_step = previous_step
        
        # Create the forward plan by reversing the backwards steps
        self.forward_plan = list(reversed(self.backwards_steps))
        self.plan_ready = True
    
    async def _execute_plan(self) -> str:
        """
        Execute the plan by following the steps in order.
        
        Returns:
            A summary of the execution
        """
        if not self.plan_ready:
            raise ValueError("Plan must be ready before execution")
        
        # Execute each step in the forward plan
        for i, step in enumerate(self.forward_plan):
            self.current_step_index = i
            
            # Execute the current step
            step_result = await self._execute_step(step)
            
            # Add the result to the step
            step["result"] = step_result
            
            # Add the completed step to the list
            self.completed_steps.append(step)
        
        # Generate a summary of the execution
        summary = await self._generate_summary()
        
        return summary
    
    async def _execute_step(self, step: Dict[str, Any]) -> str:
        """
        Execute a single step in the plan.
        
        Args:
            step: The step to execute
            
        Returns:
            The result of executing the step
        """
        # Determine which tools to use for this step
        tools_to_use = []
        if self.available_tools:
            tools_to_use = [tool.name for tool in self.available_tools.tools]
        
        # Use the new OpenAI API format for step execution
        response = self._client.responses.create(
            model="gpt-4o",
            input=[
                {
                    "role": "system",
                    "content": f"You are an execution agent that executes steps to achieve a goal. Your goal is: {self.goal}"
                },
                {
                    "role": "user",
                    "content": f"Execute this step: {step['description']}. Available tools: {', '.join(tools_to_use)}"
                }
            ],
            text={
                "format": {
                    "type": "text"
                }
            },
            reasoning={},
            tools=[],
            temperature=0.7,
            max_output_tokens=2048,
            top_p=1,
            store=True
        )
        
        # Extract the response text using helper method
        execution_plan = self._extract_text_from_response(response)
        
        # Determine if we need to use a tool
        tool_to_use = None
        tool_args = {}
        
        # Parse the execution plan to identify tool usage
        if "use tool:" in execution_plan.lower():
            # Extract tool name and arguments
            tool_lines = [line for line in execution_plan.split('\n') if "use tool:" in line.lower()]
            if tool_lines:
                tool_line = tool_lines[0]
                tool_parts = tool_line.split("use tool:", 1)[1].strip().split(" ", 1)
                tool_name = tool_parts[0].strip()
                
                # Find the tool in the available tools
                if self.available_tools:
                    for tool in self.available_tools.tools:
                        if tool.name.lower() == tool_name.lower():
                            tool_to_use = tool
                            
                            # Extract arguments if provided
                            if len(tool_parts) > 1:
                                try:
                                    # Try to parse as JSON
                                    tool_args = json.loads(tool_parts[1])
                                except json.JSONDecodeError:
                                    # If not JSON, use as a single argument
                                    tool_args = {"input": tool_parts[1].strip()}
                            break
        
        # Execute the tool if needed
        if tool_to_use:
            try:
                # Execute the tool with the provided arguments
                tool_result = await tool_to_use.run(**tool_args)
                
                # Update the step with the tool used and result
                step["tool_used"] = tool_to_use.name
                step["tool_args"] = tool_args
                
                return f"Used tool '{tool_to_use.name}' with result: {tool_result}"
            except Exception as e:
                error_message = f"Error executing tool '{tool_to_use.name}': {str(e)}"
                logger.error(error_message)
                return error_message
        
        # If no tool was used, return the execution plan
        return execution_plan
    
    async def _generate_summary(self) -> str:
        """
        Generate a summary of the execution.
        
        Returns:
            A summary of the execution
        """
        # Use the new OpenAI API format for summary generation
        response = self._client.responses.create(
            model="gpt-4o",
            input=[
                {
                    "role": "system",
                    "content": f"You are a summary agent that summarizes the execution of a plan. The goal was: {self.goal}"
                },
                {
                    "role": "user",
                    "content": f"Summarize the execution of the plan. {len(self.completed_steps)} steps were completed out of {len(self.forward_plan)} total steps."
                }
            ],
            text={
                "format": {
                    "type": "text"
                }
            },
            reasoning={},
            tools=[],
            temperature=0.7,
            max_output_tokens=2048,
            top_p=1,
            store=True
        )
        
        # Extract the response text using helper method
        summary = self._extract_text_from_response(response)
        
        return summary
    
    async def get_execution_status(self) -> str:
        """
        Get the current execution status.
        
        Returns:
            A formatted string showing the current execution status
        """
        status = f"Goal: {self.goal}\n\n"
        
        if not self.plan_ready:
            status += "Planning in progress...\n"
        else:
            status += f"Plan: {len(self.forward_plan)} steps\n"
            status += f"Completed: {len(self.completed_steps)} steps\n\n"
            
            for i, step in enumerate(self.forward_plan):
                if i < self.current_step_index:
                    status += f"✅ Step {i+1}: {step['description']}\n"
                    if "result" in step:
                        status += f"   Result: {step['result'][:100]}...\n" if len(step['result']) > 100 else f"   Result: {step['result']}\n"
                elif i == self.current_step_index:
                    status += f"🔄 Step {i+1}: {step['description']} (in progress)\n"
                else:
                    status += f"⏳ Step {i+1}: {step['description']}\n"
        
        return status
