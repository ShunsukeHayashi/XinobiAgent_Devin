"""
Example usage of the LangChain-based multi-agent conversation system.

This example demonstrates how to create and use multiple LangChain agents
to engage in a conversation rally and advance their thinking process together.
"""

import asyncio
from typing import Dict, List, Tuple

from app.agent.langchain_agent import LangChainAgent, AgentProfile, MultiAgentConversation


async def run_multi_agent_example() -> None:
    """
    Run an example of the multi-agent conversation system.
    """
    print("\n" + "="*80)
    print("DEMO: LangChain Multi-Agent Conversation System")
    print("="*80 + "\n")
    
    # Create agent profiles
    planner_profile = AgentProfile(
        name="Planner",
        role="Strategic Planner",
        expertise=["project management", "task decomposition", "risk assessment"],
        system_prompt="""You are a Strategic Planner who excels at breaking down complex problems into manageable steps.
        Your expertise is in project management, task decomposition, and risk assessment.
        In conversations, focus on creating structured plans, identifying dependencies between tasks,
        and ensuring all aspects of a problem are addressed systematically."""
    )
    
    developer_profile = AgentProfile(
        name="Developer",
        role="Software Developer",
        expertise=["coding", "software architecture", "debugging"],
        system_prompt="""You are a Software Developer with deep expertise in coding, software architecture, and debugging.
        In conversations, focus on implementation details, code structure, and technical feasibility.
        Provide concrete examples and suggest practical solutions to technical challenges."""
    )
    
    critic_profile = AgentProfile(
        name="Critic",
        role="Quality Assurance Specialist",
        expertise=["testing", "edge cases", "user experience"],
        system_prompt="""You are a Quality Assurance Specialist who excels at identifying potential issues and edge cases.
        Your expertise is in testing, finding edge cases, and evaluating user experience.
        In conversations, focus on what might go wrong, how to test solutions thoroughly,
        and how to ensure a good user experience."""
    )
    
    # Create agents
    planner = LangChainAgent(profile=planner_profile)
    developer = LangChainAgent(profile=developer_profile)
    critic = LangChainAgent(profile=critic_profile)
    
    # Create multi-agent conversation
    conversation = MultiAgentConversation(max_turns=6)  # 2 turns per agent
    
    # Add agents to the conversation
    conversation.add_agent(planner)
    conversation.add_agent(developer)
    conversation.add_agent(critic)
    
    # Start the conversation
    initial_message = "We need to build a system that can process customer feedback from multiple sources and generate actionable insights."
    
    print(f"Starting conversation with initial message:\n'{initial_message}'\n")
    print("=" * 80)
    
    # Run the conversation
    conversation_log = await conversation.start_conversation(initial_message)
    
    # Print the conversation
    print("\nCONVERSATION LOG:")
    print("-" * 80)
    for speaker, message in conversation_log:
        print(f"\n{speaker.upper()}:")
        print(f"{message}\n")
        print("-" * 80)
    
    # Print the thinking processes
    print("\nTHINKING PROCESSES:")
    print("=" * 80)
    thinking_processes = await conversation.get_thinking_processes()
    for agent_name, thinking in thinking_processes.items():
        print(f"\n{agent_name.upper()}'S THINKING PROCESS:")
        print("-" * 60)
        print(thinking)
        print("=" * 80)


async def main():
    """Run the example."""
    await run_multi_agent_example()


if __name__ == "__main__":
    asyncio.run(main())
