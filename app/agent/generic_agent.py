"""
Generic Agent implementation that uses a Working Backwards methodology.
This agent starts from the goal state and works backwards to create a plan,
then executes the plan step by step using available tools.
"""

from typing import Dict, List, Optional, Any, Literal

from pydantic import Field, model_validator

from app.agent.toolcall import ToolCallAgent
from app.logger import logger
from app.prompt.generic_agent import (
    SYSTEM_PROMPT,
    NEXT_STEP_PROMPT,
    PLANNING_TEMPLATE,
    EXECUTION_STATUS_TEMPLATE
)
from app.schema import Message, ToolCall, AgentState
from app.tool import ToolCollection, Terminate


class GenericAgent(ToolCallAgent):
    """
    An agent that implements the Working Backwards methodology to solve problems.

    This agent first clarifies the goal, then uses step-back questioning to identify
    prerequisites for each step, working backwards until reaching actions that can be
    taken from the current state. It then reorders these steps and executes them.
    """

    name: str = "generic_agent"
    description: str = "A general-purpose agent that uses Working Backwards methodology to solve tasks"

    system_prompt: str = SYSTEM_PROMPT
    next_step_prompt: str = NEXT_STEP_PROMPT

    # Tracking goal and plan
    goal_state: str = Field(default="")
    current_state: str = Field(default="")
    current_progress: str = Field(default="No progress yet. Planning phase.")

    # Working backwards tracking
    backwards_steps: List[Dict[str, Any]] = Field(default_factory=list)
    forward_plan: List[Dict[str, Any]] = Field(default_factory=list)

    # Execution tracking
    plan_ready: bool = Field(default=False)
    current_step_index: int = Field(default=0)
    completed_steps: List[Dict[str, Any]] = Field(default_factory=list)
    pending_steps: List[Dict[str, Any]] = Field(default_factory=list)

    # Additional state for flexibility
    state_variables: Dict[str, Any] = Field(default_factory=dict)

    max_steps: int = 30

    def __init__(self, **data):
        """Initialize the GenericAgent with custom tools if provided."""
        # If no tools are provided, add a basic set
        if "available_tools" not in data:
            data["available_tools"] = ToolCollection([Terminate()])
        
        # Ensure Terminate tool is always available
        terminate_tool_exists = False
        if "available_tools" in data:
            tools_collection = data["available_tools"]
            for tool in tools_collection.tools:
                if isinstance(tool, Terminate) or (hasattr(tool, "name") and tool.name == "terminate"):
                    terminate_tool_exists = True
                    break
                
            if not terminate_tool_exists:
                tools_collection.add_tool(Terminate())
            
        super().__init__(**data)

    @model_validator(mode="after")
    def validate_agent_state(self) -> "GenericAgent":
        """Validate the agent's state and ensure all required fields are initialized."""
        if not self.goal_state:
            self.goal_state = "Not yet specified"
            
        if not self.current_state:
            self.current_state = "Initial state"
            
        # Ensure special tools are properly tracked
        terminate_names = ["terminate", "finish", "complete"]
        self.special_tool_names = list(set(self.special_tool_names + [
            tool for tool in terminate_names if tool in [t.name for t in self.available_tools.tools]
        ]))
            
        return self
        
    async def set_goal(self, goal: str) -> str:
        """
        Set the agent's goal state.
        
        Args:
            goal: The goal state the agent should work towards.
            
        Returns:
            A confirmation message.
        """
        self.goal_state = goal
        logger.info(f"Goal set: {goal}")
        
        # Clear previous plan if it exists
        self.backwards_steps = []
        self.forward_plan = []
        self.plan_ready = False
        self.current_step_index = 0
        self.completed_steps = []
        self.pending_steps = []
        
        # Add goal setting message to memory
        self.update_memory("system", f"Goal set: {goal}")
        
        # Generate initial clarification of the goal
        goal_clarification_msg = Message.user_message(
            f"My goal is: {goal}\n\nPlease clarify this goal in concrete, specific terms "
            f"and begin the Working Backwards analysis to determine how to achieve it."
        )
        self.memory.append(goal_clarification_msg)
        
        return f"Goal set to: {goal}. I will now analyze this goal and work backwards to create a plan."

    async def think(self) -> bool:
        """
        Process the current state and decide the next action using Working Backwards methodology.
        
        Returns:
            bool: True if there are actions to take, False otherwise.
        """
        formatted_prompt = NEXT_STEP_PROMPT.format(
            goal_state=self.goal_state,
            current_progress=self.current_progress,
            current_state=self.current_state
        )
        
        # Add next step prompt to memory
        self.messages.append(Message.user_message(formatted_prompt))
        
        # Get response with tool options
        result = await super().think()
        
        # If we're done planning but haven't started executing, organize the plan
        if not self.plan_ready and self.backwards_steps and not self.tool_calls:
            await self._organize_plan()
            
        return result

    async def act(self) -> str:
        """
        Execute decided actions and update plan progress.
        
        Returns:
            str: Result of the action.
        """
        # Execute the action
        result = await super().act()
        
        # Update plan status if we have a plan
        if self.plan_ready and self.forward_plan:
            # Find the current step and mark it as completed
            if self.current_step_index < len(self.forward_plan):
                completed_step = self.forward_plan[self.current_step_index].copy()
                completed_step["result"] = result
                self.completed_steps.append(completed_step)
                
                # Update progress tracking
                self.current_progress = (
                    f"Completed {len(self.completed_steps)}/{len(self.forward_plan)} steps. "
                    f"Last completed: {completed_step.get('description', 'Step')}"
                )
                
                # Move to next step
                self.current_step_index += 1
                
                # Update pending steps
                self.pending_steps = self.forward_plan[self.current_step_index:] if self.current_step_index < len(self.forward_plan) else []
                
                logger.info(f"Completed step {self.current_step_index}/{len(self.forward_plan)}: {result[:100]}...")
        
        return result

    async def run(self, request: Optional[str] = None) -> str:
        """
        Execute the agent's main workflow.
        
        Args:
            request: Initial request or goal for the agent.
            
        Returns:
            str: Summary of execution results.
        """
        if request:
            await self.set_goal(request)
            
        return await super().run()

    async def _organize_plan(self) -> None:
        """
        Organize the backwards steps into a forward execution plan.
        This reverses the order of steps and prepares them for execution.
        """
        if not self.backwards_steps:
            return
            
        # Prepare to create the forward plan using LLM
        planning_prompt = PLANNING_TEMPLATE.format(
            goal=self.goal_state,
            current_state=self.current_state,
            backwards_analysis="\n".join([f"{i+1}. {step.get('description', 'Step')}" for i, step in enumerate(self.backwards_steps)]),
            forward_plan="To be determined",
            tools_required=", ".join([tool.name for tool in self.available_tools.tools]),
            success_criteria="To be determined",
            potential_challenges="To be determined",
            monitoring_approach="To be determined"
        )
        
        # Ask LLM to create the forward plan
        messages = self.messages + [Message.user_message(planning_prompt)]
        response = await self.llm.ask(messages=messages)
        
        # Parse the response to extract the forward plan
        # This is simplified and might need more robust parsing in a real implementation
        self.update_memory("assistant", response)
        
        # Create simple forward plan by reversing backwards steps
        self.forward_plan = list(reversed(self.backwards_steps))
        
        # Mark the plan as ready
        self.plan_ready = True
        self.pending_steps = self.forward_plan.copy()
        
        # Log the plan creation
        plan_summary = "\n".join([f"{i+1}. {step.get('description', 'Step')}" for i, step in enumerate(self.forward_plan)])
        logger.info(f"Forward execution plan created with {len(self.forward_plan)} steps:\n{plan_summary}")
        
        # Add the plan to memory
        self.update_memory("system", f"Forward execution plan created with {len(self.forward_plan)} steps:\n{plan_summary}")

    def _update_execution_status(self) -> str:
        """
        Create a formatted status of the execution plan.
        
        Returns:
            str: Formatted execution status.
        """
        if not self.plan_ready:
            return "Plan is still being formulated."
            
        plan_steps = "\n".join([f"{i+1}. {step.get('description', 'Step')}" for i, step in enumerate(self.forward_plan)])
        completed_steps = "\n".join([f"✓ {i+1}. {step.get('description', 'Step')}" for i, step in enumerate(self.completed_steps)])
        pending_steps = "\n".join([f"○ {self.current_step_index+i+1}. {step.get('description', 'Step')}" for i, step in enumerate(self.pending_steps)])
        
        current_step = (
            f"Currently executing step {self.current_step_index+1}/{len(self.forward_plan)}: "
            f"{self.forward_plan[self.current_step_index].get('description', 'Step')}"
            if self.current_step_index < len(self.forward_plan) else "All steps completed."
        )
        
        return EXECUTION_STATUS_TEMPLATE.format(
            goal=self.goal_state,
            plan_steps=plan_steps,
            current_step=current_step,
            completed_steps=completed_steps if self.completed_steps else "None yet.",
            pending_steps=pending_steps if self.pending_steps else "None remaining.",
            observations=self.current_progress,
            adjustments="None required at this time."
        )

    def add_backward_step(self, description: str, tools_needed: List[str], prerequisites: List[str]) -> None:
        """
        Add a step to the backwards planning process.
        
        Args:
            description: Description of this step
            tools_needed: Tools required for this step
            prerequisites: What must be true before this step
        """
        self.backwards_steps.append({
            "description": description,
            "tools_needed": tools_needed,
            "prerequisites": prerequisites
        })
        
    async def get_execution_status(self) -> str:
        """
        Get the current execution status.
        
        Returns:
            str: Formatted execution status.
        """
        return self._update_execution_status()
