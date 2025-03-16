"""
GenericAgent implementation using the Working Backwards methodology.
This implementation inherits from BaseAgent and uses prompt templates.
"""

import asyncio
import json
import logging
import os
from typing import Dict, List, Any, Optional, Union

import openai
from pydantic import BaseModel, Field, model_validator

from app.agent.base import BaseAgent
from app.schema.message import Message
from app.tool.collection import ToolCollection
from app.prompt.generic_agent import (
    SYSTEM_PROMPT,
    NEXT_STEP_PROMPT,
    PLANNING_TEMPLATE,
    EXECUTION_STATUS_TEMPLATE,
    FEEDBACK_REQUEST_TEMPLATE,
    TOOL_ERROR_TEMPLATE
)

# Configure logging
logger = logging.getLogger(__name__)


class GenericAgent(BaseAgent):
    """
    A generic agent that uses the Working Backwards methodology to solve problems.
    This implementation inherits from BaseAgent and uses prompt templates.
    """
    
    # Basic agent properties
    available_tools: Optional[ToolCollection] = Field(
        default=None, 
        description="Collection of tools available to the agent"
    )
    max_steps: int = Field(
        default=15, 
        description="Maximum number of steps the agent can take"
    )
    
    # Goal and state tracking
    goal_state: str = Field(
        default="",
        description="The goal state that the agent is trying to achieve"
    )
    current_state: str = Field(
        default="Initial state",
        description="The current state of the execution"
    )
    current_progress: str = Field(
        default="No progress yet. Planning phase.",
        description="Description of the current progress"
    )
    
    # Memory and conversation tracking
    messages: List[Message] = Field(
        default_factory=list,
        description="Memory of the agent's conversation"
    )
    
    # Planning and execution tracking
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
    
    # Additional state variables
    state_variables: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional state variables for flexibility"
    )
    
    # OpenAI API key is set in __init__
    
    class Config:
        arbitrary_types_allowed = True
    
    def __init__(self, **data):
        """
        Initialize the GenericAgent with the provided data.
        
        Args:
            **data: Data to initialize the agent with
        """
        super().__init__(**data)
        
        # Initialize with system prompt
        self.messages.append(Message(role="system", content=SYSTEM_PROMPT))
        
        # Set API key for OpenAI
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OPENAI_API_KEY not found in environment variables. Some functionality may be limited.")
        else:
            openai.api_key = api_key
    
    @model_validator(mode="after")
    def validate_agent_state(self) -> "GenericAgent":
        """
        Validate the agent's state and ensure all required fields are initialized.
        
        Returns:
            The validated agent
        """
        # Ensure tools are properly initialized
        if self.available_tools is None:
            self.available_tools = ToolCollection()
            
        return self
    
    async def set_goal(self, goal: str) -> str:
        """
        Set the goal for the agent to achieve.
        
        Args:
            goal: The goal to achieve
            
        Returns:
            Confirmation message
        """
        self.goal_state = goal
        logger.info(f"Goal set: {goal}")
        
        # Clear previous plan if it exists
        self.backwards_steps = []
        self.forward_plan = []
        self.plan_ready = False
        self.current_step_index = 0
        self.completed_steps = []
        
        # Add goal setting message to memory
        self.update_memory("system", f"Goal set: {goal}")
        
        # Generate initial clarification of the goal
        goal_clarification_msg = Message(
            role="user",
            content=f"My goal is: {goal}\n\nPlease clarify this goal in concrete, specific terms "
            f"and begin the Working Backwards analysis to determine how to achieve it."
        )
        self.messages.append(goal_clarification_msg)
        
        return f"Goal set to: {goal}. I will now analyze this goal and work backwards to create a plan."
    
    def update_memory(self, role: str, content: str, name: Optional[str] = None) -> None:
        """
        Update the agent's memory with a new message.
        
        Args:
            role: The role of the message sender (system, user, assistant)
            content: The content of the message
            name: Optional name of the message sender
        """
        self.messages.append(Message(role=role, content=content, name=name))
        
    async def think(self) -> bool:
        """
        Process the current state and decide the next action using Working Backwards methodology.
        
        Returns:
            True if there are actions to take, False otherwise
        """
        # Format the next step prompt with current state
        formatted_prompt = NEXT_STEP_PROMPT.format(
            goal_state=self.goal_state,
            current_progress=self.current_progress,
            current_state=self.current_state
        )
        
        # Add next step prompt to memory
        self.update_memory("user", formatted_prompt)
        
        try:
            # Use the OpenAI API for thinking
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": msg.role, "content": msg.content} for msg in self.messages],
                temperature=0.7,
                max_tokens=2048,
                top_p=1
            )
        except Exception as e:
            logger.error(f"Error during thinking phase: {str(e)}")
            self.update_memory("system", f"Error during thinking: {str(e)}")
            return False
        
        # Extract the response
        thinking_result = response['choices'][0]['message']['content']
        
        # Add the thinking result to memory
        self.update_memory("assistant", thinking_result)
        
        # Check if we need to use a tool
        tool_to_use = self._extract_tool_from_response(thinking_result)
        
        if tool_to_use:
            # We have a tool to use, so we'll continue
            return True
        
        # If we're done planning but haven't started executing, organize the plan
        if not self.plan_ready and self.backwards_steps:
            await self._organize_plan()
            return True
        
        # Check if we're done
        if self.plan_ready and self.current_step_index >= len(self.forward_plan):
            return False
        
        # Continue with the next step
        return True
    
    def _extract_tool_from_response(self, response: str) -> Optional[Dict[str, Any]]:
        """
        Extract tool usage information from a response.
        
        Args:
            response: The response to extract tool information from
            
        Returns:
            Tool information if a tool should be used, None otherwise
        """
        # Check if the response mentions using a tool
        if "use tool:" in response.lower() or "tool to use:" in response.lower():
            # Extract tool name and arguments
            tool_lines = [line for line in response.split('\n') 
                         if "use tool:" in line.lower() or "tool to use:" in line.lower()]
            
            if tool_lines:
                tool_line = tool_lines[0]
                
                # Extract the tool name and arguments
                if "use tool:" in tool_line.lower():
                    tool_parts = tool_line.split("use tool:", 1)[1].strip().split(" ", 1)
                else:
                    tool_parts = tool_line.split("tool to use:", 1)[1].strip().split(" ", 1)
                    
                tool_name = tool_parts[0].strip()
                
                # Find the tool in the available tools
                if self.available_tools:
                    for tool in self.available_tools.tools:
                        if tool.name.lower() == tool_name.lower():
                            tool_args = {}
                            
                            # Extract arguments if provided
                            if len(tool_parts) > 1:
                                try:
                                    # Try to parse as JSON
                                    tool_args = json.loads(tool_parts[1])
                                except json.JSONDecodeError:
                                    # If not JSON, use as a single argument
                                    tool_args = {"input": tool_parts[1].strip()}
                            
                            return {
                                "tool": tool,
                                "args": tool_args
                            }
        
        return None
    
    async def run(self, request: Optional[str] = None) -> str:
        """
        Run the agent's main workflow.
        
        Args:
            request: Initial request or goal for the agent
            
        Returns:
            The final result of the agent's execution
        """
        if request:
            await self.set_goal(request)
        
        if not self.goal_state:
            raise ValueError("Goal must be set before running the agent")
        
        # Main execution loop
        steps_taken = 0
        
        while steps_taken < self.max_steps:
            # Think about what to do next
            should_continue = await self.think()
            
            if not should_continue:
                break
            
            # Act on the decision
            await self.act()
            
            steps_taken += 1
        
        # Generate a summary of the execution
        summary = await self._generate_summary()
        
        return summary
    
    async def act(self) -> str:
        """
        Execute the decided action.
        
        Returns:
            The result of the action
        """
        # Check if we have a tool to use from the last thinking step
        last_message = self.messages[-1] if self.messages else None
        
        if last_message and last_message.role == "assistant":
            tool_info = self._extract_tool_from_response(last_message.content)
            
            if tool_info:
                tool = tool_info["tool"]
                args = tool_info["args"]
                
                try:
                    # Execute the tool
                    logger.info(f"Executing tool: {tool.name} with args: {args}")
                    result = await tool.run(**args)
                    
                    # Update memory with the result
                    self.update_memory("system", f"Tool result: {result}")
                    
                    # Update current progress
                    self.current_progress = f"Executed tool: {tool.name}"
                    
                    # If we're executing a plan, update the step
                    if self.plan_ready and self.current_step_index < len(self.forward_plan):
                        step = self.forward_plan[self.current_step_index]
                        step["tool_used"] = tool.name
                        step["tool_args"] = args
                        step["result"] = result
                        
                        # Add to completed steps
                        self.completed_steps.append(step)
                        
                        # Move to next step
                        self.current_step_index += 1
                        
                        # Update progress
                        self.current_progress = f"Completed step {self.current_step_index}/{len(self.forward_plan)}"
                    
                    return result
                except Exception as e:
                    # Handle tool execution error
                    error_message = f"Error executing tool '{tool.name}': {str(e)}"
                    logger.error(error_message)
                    
                    # Format error message using template
                    formatted_error = TOOL_ERROR_TEMPLATE.format(
                        tool_name=tool.name,
                        operation=str(args),
                        error=str(e),
                        impact="Plan execution may be delayed or require adjustment.",
                        recovery_steps="Consider alternative approaches or tools.",
                        user_question="Would you like me to try an alternative approach?"
                    )
                    
                    # Update memory with the error
                    self.update_memory("system", formatted_error)
                    
                    return error_message
        
        # If we're executing a plan but don't have a specific tool to use
        if self.plan_ready and self.current_step_index < len(self.forward_plan):
            # Get the current step
            step = self.forward_plan[self.current_step_index]
            
            # Execute the step using the OpenAI API
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": f"Execute this step: {step['description']}. "
                                                   f"Available tools: {', '.join([tool.name for tool in self.available_tools.tools]) if self.available_tools else 'None'}"}
                    ],
                    temperature=0.7,
                    max_tokens=2048,
                    top_p=1
                )
            except Exception as e:
                logger.error(f"Error executing step: {str(e)}")
                self.update_memory("system", f"Error executing step: {str(e)}")
                return f"Error executing step: {str(e)}"
            
            # Extract the response
            execution_result = response['choices'][0]['message']['content']
            
            # Update memory with the result
            self.update_memory("assistant", execution_result)
            
            # Update the step with the result
            step["result"] = execution_result
            
            # Add to completed steps
            self.completed_steps.append(step)
            
            # Move to next step
            self.current_step_index += 1
            
            # Update progress
            self.current_progress = f"Completed step {self.current_step_index}/{len(self.forward_plan)}"
            
            return execution_result
        
        # If we don't have a specific action to take
        return "No action taken."
    
    async def _organize_plan(self) -> None:
        """
        Organize the backwards steps into a forward execution plan.
        """
        if not self.backwards_steps:
            return
        
        # Prepare to create the forward plan
        planning_prompt = PLANNING_TEMPLATE.format(
            goal=self.goal_state,
            current_state=self.current_state,
            backwards_analysis="\n".join([f"{i+1}. {step.get('description', 'Step')}" 
                                         for i, step in enumerate(self.backwards_steps)]),
            forward_plan="To be determined",
            tools_required=", ".join([tool.name for tool in self.available_tools.tools]) 
                          if self.available_tools else "None",
            success_criteria="To be determined",
            potential_challenges="To be determined",
            monitoring_approach="To be determined"
        )
        
        # Add planning prompt to memory
        self.update_memory("user", planning_prompt)
        
        # Use the OpenAI API for planning
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": msg.role, "content": msg.content} for msg in self.messages],
                temperature=0.7,
                max_tokens=2048,
                top_p=1
            )
        except Exception as e:
            logger.error(f"Error during planning: {str(e)}")
            self.update_memory("system", f"Error during planning: {str(e)}")
            return
        
        # Extract the response
        planning_result = response['choices'][0]['message']['content']
        
        # Add the planning result to memory
        self.update_memory("assistant", planning_result)
        
        # Create the forward plan by reversing the backwards steps
        self.forward_plan = list(reversed(self.backwards_steps))
        
        # Mark the plan as ready
        self.plan_ready = True
        
        # Log the plan creation
        plan_summary = "\n".join([f"{i+1}. {step.get('description', 'Step')}" 
                                 for i, step in enumerate(self.forward_plan)])
        logger.info(f"Forward execution plan created with {len(self.forward_plan)} steps:\n{plan_summary}")
        
        # Update the current progress
        self.current_progress = f"Plan created with {len(self.forward_plan)} steps."
    
    async def _generate_summary(self) -> str:
        """
        Generate a summary of the execution.
        
        Returns:
            A summary of the execution
        """
        # Use the OpenAI API for summary generation
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": f"You are a summary agent that summarizes the execution of a plan. The goal was: {self.goal_state}"},
                    {"role": "user", "content": f"Summarize the execution of the plan. {len(self.completed_steps)} steps were completed out of {len(self.forward_plan)} total steps."}
                ],
                temperature=0.7,
                max_tokens=2048,
                top_p=1
            )
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return f"Error generating summary: {str(e)}"
        
        # Extract the response
        summary = response['choices'][0]['message']['content']
        
        return summary
    
    async def get_execution_status(self) -> str:
        """
        Get the current execution status.
        
        Returns:
            A formatted string showing the current execution status
        """
        # Format the status using the execution status template
        status_content = EXECUTION_STATUS_TEMPLATE.format(
            goal=self.goal_state,
            plan_steps="\n".join([f"{i+1}. {step.get('description', 'Step')}" 
                                for i, step in enumerate(self.forward_plan)]) if self.forward_plan else "No plan yet",
            current_step=f"Step {self.current_step_index+1}/{len(self.forward_plan)}: "
                        f"{self.forward_plan[self.current_step_index].get('description', 'Step')}" 
                        if self.plan_ready and self.current_step_index < len(self.forward_plan) else "Planning phase",
            completed_steps="\n".join([f"✅ {i+1}. {step.get('description', 'Step')}: "
                                     f"{step.get('result', 'No result')[:100]}..." 
                                     if len(str(step.get('result', ''))) > 100 
                                     else f"✅ {i+1}. {step.get('description', 'Step')}: {step.get('result', 'No result')}"
                                     for i, step in enumerate(self.completed_steps)]) if self.completed_steps else "None",
            pending_steps="\n".join([f"⏳ {i+1}. {step.get('description', 'Step')}" 
                                   for i, step in enumerate(self.forward_plan[self.current_step_index:])]) 
                         if self.plan_ready and self.current_step_index < len(self.forward_plan) else "All steps completed",
            observations=self.current_progress,
            adjustments="None" if not self.state_variables.get("adjustments") else self.state_variables.get("adjustments")
        )
        
        return status_content
