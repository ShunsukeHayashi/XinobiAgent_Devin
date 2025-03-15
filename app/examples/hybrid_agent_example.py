"""
Example usage of the Hybrid Agent combining OpenAI API and LangChain.

This example demonstrates how to create and use a Hybrid Agent that combines
the Working Backwards methodology from GenericAgent with the multi-agent
conversation capabilities of LangChain.
"""

import asyncio
from typing import Dict, List, Optional, Any

from app.agent.hybrid_agent import HybridAgent, AgentRole
from app.tool import ToolCollection, Bash, GoogleSearch, PythonExecute, Terminate


async def run_hybrid_agent_example() -> None:
    """
    Run an example of the Hybrid Agent.
    """
    print("\n" + "="*80)
    print("DEMO: Hybrid Agent (OpenAI API + LangChain)")
    print("="*80 + "\n")
    
    # Create a tool collection
    tools = ToolCollection([
        Bash(),
        GoogleSearch(),
        PythonExecute(),
        Terminate()
    ])
    
    # Create agent roles
    roles = [
        AgentRole(
            name="戦略家",  # Strategist
            description="ビジネス戦略アドバイザー",  # Business Strategy Advisor
            expertise=["市場分析", "競合分析", "ビジネスモデル設計"],  # Market analysis, Competitor analysis, Business model design
            system_prompt="""あなたは「戦略家」として、ビジネス戦略の専門知識を持っています。
            市場分析、競合分析、ビジネスモデル設計に関する深い知見があります。
            会話では、ビジネス目標の達成方法、市場機会の特定、競争上の優位性の構築に焦点を当ててください。
            常に長期的な視点と戦略的思考を提供してください。"""
        ),
        AgentRole(
            name="エンジニア",  # Engineer
            description="AIシステム開発者",  # AI System Developer
            expertise=["機械学習", "システムアーキテクチャ", "APIデザイン"],  # Machine learning, System architecture, API design
            system_prompt="""あなたは「エンジニア」として、AIシステム開発の専門知識を持っています。
            機械学習、システムアーキテクチャ、APIデザインに関する深い知見があります。
            会話では、技術的な実装の詳細、システム設計の選択肢、開発上の課題に焦点を当ててください。
            常に実用的で効率的な技術ソリューションを提案してください。"""
        ),
        AgentRole(
            name="ユーザー代弁者",  # User Advocate
            description="ユーザーエクスペリエンスの専門家",  # User Experience Specialist
            expertise=["ユーザー調査", "UXデザイン", "アクセシビリティ"],  # User research, UX design, Accessibility
            system_prompt="""あなたは「ユーザー代弁者」として、ユーザーエクスペリエンスの専門知識を持っています。
            ユーザー調査、UXデザイン、アクセシビリティに関する深い知見があります。
            会話では、エンドユーザーのニーズ、使いやすさの課題、ユーザー中心の設計原則に焦点を当ててください。
            常にユーザーの視点からフィードバックを提供し、より良いユーザーエクスペリエンスを提唱してください。"""
        )
    ]
    
    # Create the hybrid agent
    agent = HybridAgent(
        name="hybrid_agent",
        description="A hybrid agent that combines OpenAI API and LangChain",
        available_tools=tools,
        max_steps=9,  # 3 turns per agent
        roles=roles
    )
    
    # Set the goal
    goal = """
    OpenAI APIを使用して、顧客の問い合わせに自動的に応答し、適切な部門に振り分けるシステムを開発したいと考えています。
    このシステムは、メール、チャット、SNSなど複数のチャネルからの問い合わせを処理できる必要があります。
    また、顧客の感情を分析し、緊急性の高い問い合わせを優先的に処理する機能も必要です。
    このプロジェクトをどのように進めるべきでしょうか？
    """
    
    print(f"Goal:\n{goal}\n")
    print("=" * 80)
    
    # Run the agent
    print("\nRunning the hybrid agent...\n")
    result = await agent.run(goal)
    
    # Print the result
    print("\n" + "="*80)
    print("RESULT:")
    print("="*80 + "\n")
    print(result)
    
    # Print the thinking processes
    print("\n" + "="*80)
    print("THINKING PROCESSES:")
    print("="*80 + "\n")
    
    thinking_processes = await agent.get_thinking_processes()
    for agent_name, thinking in thinking_processes.items():
        print(f"\n{agent_name.upper()}'S THINKING PROCESS:")
        print("-" * 60)
        print(thinking)
        print("=" * 80)


async def main():
    """Run the example."""
    await run_hybrid_agent_example()


if __name__ == "__main__":
    asyncio.run(main())
