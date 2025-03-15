"""
LangChain-based multi-agent conversation system.

This module implements a multi-agent conversation system using LangChain's
LMChain and prompt templates to enable agents to engage in a conversation
rally and advance their thinking process together.
"""

import asyncio
from typing import Dict, List, Optional, Any, Tuple

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel, Field

from app.agent.base import BaseAgent
from app.logger import logger
from app.schema.message import Message


class AgentProfile(BaseModel):
    """Profile for an agent in the multi-agent conversation system."""
    
    name: str = Field(description="Name of the agent")
    role: str = Field(description="Role of the agent in the conversation")
    expertise: List[str] = Field(default_factory=list, description="Areas of expertise")
    system_prompt: str = Field(description="System prompt that defines the agent's behavior")
    
    def get_system_message(self) -> SystemMessage:
        """Get the system message for this agent."""
        return SystemMessage(content=self.system_prompt)


class ConversationState(BaseModel):
    """State of a multi-agent conversation."""
    
    history: List[BaseMessage] = Field(default_factory=list)
    current_speaker: str = Field(default="")
    thinking_process: Dict[str, List[str]] = Field(default_factory=dict)
    
    def add_message(self, message: BaseMessage) -> None:
        """Add a message to the conversation history."""
        self.history.append(message)
    
    def add_thinking(self, agent_name: str, thought: str) -> None:
        """Add a thought to an agent's thinking process."""
        if agent_name not in self.thinking_process:
            self.thinking_process[agent_name] = []
        self.thinking_process[agent_name].append(thought)
    
    def get_formatted_history(self, include_system: bool = False) -> str:
        """Get the formatted conversation history."""
        formatted = []
        for msg in self.history:
            if isinstance(msg, SystemMessage) and not include_system:
                continue
            
            role = "System" if isinstance(msg, SystemMessage) else (
                "Human" if isinstance(msg, HumanMessage) else "AI"
            )
            formatted.append(f"{role}: {msg.content}")
        
        return "\n".join(formatted)
    
    def get_thinking_process(self, agent_name: str) -> str:
        """Get the thinking process for a specific agent."""
        if agent_name not in self.thinking_process:
            return "No thoughts recorded yet."
        
        return "\n".join([
            f"Thought {i+1}: {thought}" 
            for i, thought in enumerate(self.thinking_process[agent_name])
        ])


class LangChainAgent(BaseAgent):
    """
    An agent that uses LangChain's LMChain and prompt templates to participate
    in multi-agent conversations.
    """
    
    name: str = "langchain_agent"
    description: str = "An agent that uses LangChain for multi-agent conversations"
    
    # Agent profile
    profile: AgentProfile = Field(...)
    
    # LangChain components
    llm_chain: Optional[LLMChain] = None
    thinking_chain: Optional[LLMChain] = None
    
    # Conversation state
    conversation: ConversationState = Field(default_factory=ConversationState)
    
    # Templates
    response_template: str = """
    You are {agent_name}, a {agent_role} with expertise in {agent_expertise}.
    
    Conversation history:
    {conversation_history}
    
    Your task is to respond to the conversation, advancing the discussion and sharing your expertise.
    Think about what would be most helpful to contribute based on your role and expertise.
    
    Your response:
    """
    
    thinking_template: str = """
    You are {agent_name}, a {agent_role} with expertise in {agent_expertise}.
    
    Conversation history:
    {conversation_history}
    
    Before responding, think step by step about:
    1. What is being discussed?
    2. What insights can you provide based on your expertise?
    3. How can you advance the conversation?
    4. What questions might help clarify or deepen the discussion?
    
    Your thinking process (not shared with others):
    """
    
    def __init__(self, **data):
        """Initialize the LangChain agent."""
        super().__init__(**data)
        
        # Initialize LangChain components
        self._initialize_chains()
    
    def _initialize_chains(self) -> None:
        """Initialize the LangChain chains for thinking and responding."""
        # Create the LLM
        llm = ChatOpenAI(temperature=0.7)
        
        # Create the response chain
        response_prompt = PromptTemplate(
            input_variables=["agent_name", "agent_role", "agent_expertise", "conversation_history"],
            template=self.response_template
        )
        self.llm_chain = LLMChain(llm=llm, prompt=response_prompt)
        
        # Create the thinking chain
        thinking_prompt = PromptTemplate(
            input_variables=["agent_name", "agent_role", "agent_expertise", "conversation_history"],
            template=self.thinking_template
        )
        self.thinking_chain = LLMChain(llm=llm, prompt=thinking_prompt)
    
    async def think(self) -> bool:
        """
        Process the current conversation state and think about a response.
        
        Returns:
            bool: True if thinking was successful, False otherwise.
        """
        if not self.thinking_chain:
            logger.error("Thinking chain not initialized")
            return False
        
        # Get the conversation history
        conversation_history = self.conversation.get_formatted_history()
        
        # Run the thinking chain
        thinking_result = await asyncio.to_thread(
            self.thinking_chain.run,
            agent_name=self.profile.name,
            agent_role=self.profile.role,
            agent_expertise=", ".join(self.profile.expertise),
            conversation_history=conversation_history
        )
        
        # Record the thinking process
        self.conversation.add_thinking(self.profile.name, thinking_result)
        
        # Log the thinking process
        logger.info(f"{self.profile.name}'s thinking: {thinking_result[:100]}...")
        
        return True
    
    async def respond(self) -> str:
        """
        Generate a response based on the current conversation state.
        
        Returns:
            str: The agent's response.
        """
        if not self.llm_chain:
            logger.error("LLM chain not initialized")
            return "Error: LLM chain not initialized"
        
        # Get the conversation history
        conversation_history = self.conversation.get_formatted_history()
        
        # Run the response chain
        response = await asyncio.to_thread(
            self.llm_chain.run,
            agent_name=self.profile.name,
            agent_role=self.profile.role,
            agent_expertise=", ".join(self.profile.expertise),
            conversation_history=conversation_history
        )
        
        # Add the response to the conversation
        self.conversation.add_message(AIMessage(content=response))
        
        # Set this agent as the current speaker
        self.conversation.current_speaker = self.profile.name
        
        return response
    
    async def receive_message(self, message: str, sender: str) -> None:
        """
        Receive a message from another agent or a human.
        
        Args:
            message: The message content
            sender: The name of the sender
        """
        if sender == "human":
            self.conversation.add_message(HumanMessage(content=message))
        else:
            self.conversation.add_message(AIMessage(content=message))
        
        # Update the current speaker
        self.conversation.current_speaker = sender
    
    async def get_thinking_process(self) -> str:
        """
        Get this agent's thinking process.
        
        Returns:
            str: The agent's thinking process.
        """
        return self.conversation.get_thinking_process(self.profile.name)
    
    async def run(self, request: Optional[str] = None) -> str:
        """
        Run the agent's main workflow.
        
        Args:
            request: Initial request for the agent.
            
        Returns:
            str: The agent's response.
        """
        if request:
            await self.receive_message(request, "human")
        
        # Think about the conversation
        await self.think()
        
        # Generate a response
        return await self.respond()


class MultiAgentConversation(BaseModel):
    """
    A system for managing conversations between multiple LangChain agents.
    """
    
    agents: Dict[str, LangChainAgent] = Field(default_factory=dict)
    conversation: ConversationState = Field(default_factory=ConversationState)
    max_turns: int = Field(default=10)
    
    def add_agent(self, agent: LangChainAgent) -> None:
        """
        Add an agent to the conversation.
        
        Args:
            agent: The agent to add
        """
        self.agents[agent.profile.name] = agent
        
        # Share the conversation state with the agent
        agent.conversation = self.conversation
    
    async def start_conversation(self, initial_message: str) -> List[Tuple[str, str]]:
        """
        Start a conversation with an initial message.
        
        Args:
            initial_message: The initial message to start the conversation
            
        Returns:
            List of (agent_name, message) tuples representing the conversation
        """
        # Add the initial message to the conversation
        self.conversation.add_message(HumanMessage(content=initial_message))
        
        # Initialize the conversation log
        conversation_log = [("human", initial_message)]
        
        # Determine the first agent to respond (can be random or fixed)
        current_agent_name = next(iter(self.agents.keys()))
        
        # Run the conversation for max_turns
        for _ in range(self.max_turns):
            # Get the current agent
            current_agent = self.agents[current_agent_name]
            
            # Have the agent think and respond
            await current_agent.think()
            response = await current_agent.respond()
            
            # Add to the conversation log
            conversation_log.append((current_agent_name, response))
            
            # Notify other agents of the message
            for agent_name, agent in self.agents.items():
                if agent_name != current_agent_name:
                    await agent.receive_message(response, current_agent_name)
            
            # Select the next agent (simple round-robin for now)
            agent_names = list(self.agents.keys())
            current_idx = agent_names.index(current_agent_name)
            next_idx = (current_idx + 1) % len(agent_names)
            current_agent_name = agent_names[next_idx]
        
        return conversation_log
    
    async def get_thinking_processes(self) -> Dict[str, str]:
        """
        Get the thinking processes for all agents.
        
        Returns:
            Dict mapping agent names to their thinking processes
        """
        thinking_processes = {}
        for agent_name, agent in self.agents.items():
            thinking_processes[agent_name] = await agent.get_thinking_process()
        
        return thinking_processes
