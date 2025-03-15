"""
Hybrid agent implementation combining OpenAI API and LangChain.

This module implements a hybrid agent that combines the Working Backwards methodology
from the GenericAgent with the multi-agent conversation capabilities of LangChain.
"""

import asyncio
import json
from typing import Dict, List, Optional, Any, Tuple, Union

from openai import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel, Field

from app.agent.base import BaseAgent
from app.agent.generic_agent import GenericAgent
from app.agent.langchain_agent import LangChainAgent, AgentProfile, ConversationState
from app.logger import logger
from app.schema.message import Message
from app.tool.collection import ToolCollection


class AgentRole(BaseModel):
    """Role definition for an agent in the hybrid system."""
    
    name: str = Field(description="Name of the role")
    description: str = Field(description="Description of the role")
    expertise: List[str] = Field(default_factory=list, description="Areas of expertise")
    system_prompt: str = Field(description="System prompt that defines the role's behavior")
    
    def to_agent_profile(self) -> AgentProfile:
        """Convert to an AgentProfile for LangChainAgent."""
        return AgentProfile(
            name=self.name,
            role=self.description,
            expertise=self.expertise,
            system_prompt=self.system_prompt
        )


class HybridAgent(BaseAgent):
    """
    A hybrid agent that combines the Working Backwards methodology from GenericAgent
    with the multi-agent conversation capabilities of LangChain.
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
    
    # Agent roles for the multi-agent conversation
    roles: List[AgentRole] = Field(
        default_factory=list,
        description="Roles for the multi-agent conversation"
    )
    
    # Internal agents
    planning_agent: Optional[GenericAgent] = None
    execution_agents: Dict[str, LangChainAgent] = Field(
        default_factory=dict,
        description="Execution agents for different roles"
    )
    
    # Conversation state
    conversation: ConversationState = Field(
        default_factory=ConversationState,
        description="State of the multi-agent conversation"
    )
    
    # OpenAI client
    _client: Optional[OpenAI] = None
    
    class Config:
        arbitrary_types_allowed = True
    
    def __init__(self, **data):
        """Initialize the hybrid agent."""
        super().__init__(**data)
        self._client = OpenAI()
        
        # Initialize the planning agent
        self._initialize_planning_agent()
        
        # Initialize the execution agents
        self._initialize_execution_agents()
    
    def _initialize_planning_agent(self) -> None:
        """Initialize the planning agent using GenericAgent."""
        self.planning_agent = GenericAgent(
            name=f"{self.name}_planner",
            description=f"Planning agent for {self.name}",
            available_tools=self.available_tools,
            max_steps=self.max_steps
        )
    
    def _initialize_execution_agents(self) -> None:
        """Initialize the execution agents using LangChainAgent."""
        # Create default roles if none are provided
        if not self.roles:
            self.roles = [
                AgentRole(
                    name="Planner",
                    description="Strategic Planner",
                    expertise=["project management", "task decomposition", "risk assessment"],
                    system_prompt="""You are a Strategic Planner who excels at breaking down complex problems into manageable steps.
                    Your expertise is in project management, task decomposition, and risk assessment.
                    In conversations, focus on creating structured plans, identifying dependencies between tasks,
                    and ensuring all aspects of a problem are addressed systematically."""
                ),
                AgentRole(
                    name="Developer",
                    description="Software Developer",
                    expertise=["coding", "software architecture", "debugging"],
                    system_prompt="""You are a Software Developer with deep expertise in coding, software architecture, and debugging.
                    In conversations, focus on implementation details, code structure, and technical feasibility.
                    Provide concrete examples and suggest practical solutions to technical challenges."""
                ),
                AgentRole(
                    name="Critic",
                    description="Quality Assurance Specialist",
                    expertise=["testing", "edge cases", "user experience"],
                    system_prompt="""You are a Quality Assurance Specialist who excels at identifying potential issues and edge cases.
                    Your expertise is in testing, finding edge cases, and evaluating user experience.
                    In conversations, focus on what might go wrong, how to test solutions thoroughly,
                    and how to ensure a good user experience."""
                )
            ]
        
        # Create an execution agent for each role
        for role in self.roles:
            agent_profile = role.to_agent_profile()
            self.execution_agents[role.name] = LangChainAgent(profile=agent_profile)
            
            # Share the conversation state with the agent
            self.execution_agents[role.name].conversation = self.conversation
    
    async def set_goal(self, goal: str) -> None:
        """
        Set the goal for the agent to achieve.
        
        Args:
            goal: The goal to achieve
        """
        self.goal = goal
        
        # Set the goal for the planning agent
        if self.planning_agent:
            await self.planning_agent.set_goal(goal)
        
        # Add the goal to the conversation
        self.conversation.add_message(SystemMessage(content=f"Goal: {goal}"))
    
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
        
        # First, use the planning agent to create a plan
        logger.info(f"Creating plan for goal: {self.goal}")
        plan_result = await self.planning_agent.run()
        
        # Add the plan to the conversation
        self.conversation.add_message(SystemMessage(content=f"Plan: {plan_result}"))
        
        # Get the execution status from the planning agent
        plan_status = await self.planning_agent.get_execution_status()
        
        # Extract the steps from the plan status
        steps = []
        for line in plan_status.split("\n"):
            if line.startswith("✅ Step ") or line.startswith("🔄 Step ") or line.startswith("⏳ Step "):
                step_description = line.split(":", 1)[1].strip()
                steps.append(step_description)
        
        # Start the multi-agent conversation to execute the plan
        logger.info("Starting multi-agent conversation to execute the plan")
        
        # Create the initial message for the conversation
        initial_message = f"""
        Goal: {self.goal}
        
        Plan:
        {plan_result}
        
        Steps:
        {chr(10).join([f"{i+1}. {step}" for i, step in enumerate(steps)])}
        
        Let's work together to execute this plan. Each agent should contribute based on their expertise.
        """
        
        # Add the initial message to the conversation
        self.conversation.add_message(HumanMessage(content=initial_message))
        
        # Initialize the conversation log
        conversation_log = [("system", initial_message)]
        
        # Determine the first agent to respond (start with the Planner)
        current_agent_name = "Planner" if "Planner" in self.execution_agents else next(iter(self.execution_agents.keys()))
        
        # Run the conversation for max_steps
        for _ in range(self.max_steps):
            # Get the current agent
            current_agent = self.execution_agents[current_agent_name]
            
            # Have the agent think and respond
            await current_agent.think()
            response = await current_agent.respond()
            
            # Add to the conversation log
            conversation_log.append((current_agent_name, response))
            
            # Notify other agents of the message
            for agent_name, agent in self.execution_agents.items():
                if agent_name != current_agent_name:
                    await agent.receive_message(response, current_agent_name)
            
            # Select the next agent (simple round-robin for now)
            agent_names = list(self.execution_agents.keys())
            current_idx = agent_names.index(current_agent_name)
            next_idx = (current_idx + 1) % len(agent_names)
            current_agent_name = agent_names[next_idx]
        
        # Generate a summary of the execution
        summary = await self._generate_summary(conversation_log)
        
        return summary
    
    async def _generate_summary(self, conversation_log: List[Tuple[str, str]]) -> str:
        """
        Generate a summary of the execution.
        
        Args:
            conversation_log: The conversation log
            
        Returns:
            A summary of the execution
        """
        # Format the conversation log
        formatted_log = "\n\n".join([f"{speaker}: {message}" for speaker, message in conversation_log])
        
        # Use the OpenAI API to generate a summary
        response = self._client.responses.create(
            model="gpt-4o",
            input=[
                {
                    "role": "system",
                    "content": f"You are a summary agent that summarizes the execution of a plan. The goal was: {self.goal}"
                },
                {
                    "role": "user",
                    "content": f"Summarize the execution of the plan based on the following conversation:\n\n{formatted_log}"
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
        
        # Extract the response text
        summary = self._extract_text_from_response(response)
        
        return summary
    
    async def get_thinking_processes(self) -> Dict[str, str]:
        """
        Get the thinking processes for all execution agents.
        
        Returns:
            Dict mapping agent names to their thinking processes
        """
        thinking_processes = {}
        for agent_name, agent in self.execution_agents.items():
            thinking_processes[agent_name] = await agent.get_thinking_process()
        
        return thinking_processes
    
    async def get_execution_status(self) -> str:
        """
        Get the current execution status.
        
        Returns:
            A formatted string showing the current execution status
        """
        if self.planning_agent:
            return await self.planning_agent.get_execution_status()
        else:
            return f"Goal: {self.goal}\n\nNo planning agent initialized."
