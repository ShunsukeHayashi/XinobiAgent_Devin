"""
Demo script for the LangChain-based multi-agent conversation system.

This script demonstrates how multiple agents with different roles and expertise
can engage in a conversation rally to solve a problem together, with each agent
contributing based on their unique perspective and knowledge.
"""

import asyncio
import logging
from typing import Dict, List, Tuple

from app.agent.langchain_agent import LangChainAgent, AgentProfile, MultiAgentConversation


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def run_langchain_multi_agent_demo() -> None:
    """
    Run a demonstration of the LangChain multi-agent conversation system.
    """
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("LangChain Multi-Agent Conversation System Demo")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢\n")
    
    # Create agent profiles with Japanese expertise
    strategist_profile = AgentProfile(
        name="戦略家",  # Strategist
        role="ビジネス戦略アドバイザー",  # Business Strategy Advisor
        expertise=["市場分析", "競合分析", "ビジネスモデル設計"],  # Market analysis, Competitor analysis, Business model design
        system_prompt="""あなたは「戦略家」として、ビジネス戦略の専門知識を持っています。
        市場分析、競合分析、ビジネスモデル設計に関する深い知見があります。
        会話では、ビジネス目標の達成方法、市場機会の特定、競争上の優位性の構築に焦点を当ててください。
        常に長期的な視点と戦略的思考を提供してください。"""
    )
    
    engineer_profile = AgentProfile(
        name="エンジニア",  # Engineer
        role="AIシステム開発者",  # AI System Developer
        expertise=["機械学習", "システムアーキテクチャ", "APIデザイン"],  # Machine learning, System architecture, API design
        system_prompt="""あなたは「エンジニア」として、AIシステム開発の専門知識を持っています。
        機械学習、システムアーキテクチャ、APIデザインに関する深い知見があります。
        会話では、技術的な実装の詳細、システム設計の選択肢、開発上の課題に焦点を当ててください。
        常に実用的で効率的な技術ソリューションを提案してください。"""
    )
    
    user_advocate_profile = AgentProfile(
        name="ユーザー代弁者",  # User Advocate
        role="ユーザーエクスペリエンスの専門家",  # User Experience Specialist
        expertise=["ユーザー調査", "UXデザイン", "アクセシビリティ"],  # User research, UX design, Accessibility
        system_prompt="""あなたは「ユーザー代弁者」として、ユーザーエクスペリエンスの専門知識を持っています。
        ユーザー調査、UXデザイン、アクセシビリティに関する深い知見があります。
        会話では、エンドユーザーのニーズ、使いやすさの課題、ユーザー中心の設計原則に焦点を当ててください。
        常にユーザーの視点からフィードバックを提供し、より良いユーザーエクスペリエンスを提唱してください。"""
    )
    
    # Create agents
    strategist = LangChainAgent(profile=strategist_profile)
    engineer = LangChainAgent(profile=engineer_profile)
    user_advocate = LangChainAgent(profile=user_advocate_profile)
    
    # Create multi-agent conversation
    conversation = MultiAgentConversation(max_turns=9)  # 3 turns per agent
    
    # Add agents to the conversation
    conversation.add_agent(strategist)
    conversation.add_agent(engineer)
    conversation.add_agent(user_advocate)
    
    # Start the conversation with a prompt in Japanese
    initial_message = """
    OpenAI APIを使用して、顧客の問い合わせに自動的に応答し、適切な部門に振り分けるシステムを開発したいと考えています。
    このシステムは、メール、チャット、SNSなど複数のチャネルからの問い合わせを処理できる必要があります。
    また、顧客の感情を分析し、緊急性の高い問い合わせを優先的に処理する機能も必要です。
    このプロジェクトをどのように進めるべきでしょうか？
    """
    
    print(f"初期メッセージ:\n'{initial_message}'\n")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    
    # Run the conversation
    print("\n会話を開始します...\n")
    conversation_log = await conversation.start_conversation(initial_message)
    
    # Print the conversation
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("会話ログ:")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢\n")
    
    for speaker, message in conversation_log:
        print(f"\n【{speaker}】")
        print(f"{message}\n")
        print("-" * 80)
    
    # Print the thinking processes
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("思考プロセス:")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢\n")
    
    thinking_processes = await conversation.get_thinking_processes()
    for agent_name, thinking in thinking_processes.items():
        print(f"\n【{agent_name}の思考プロセス】")
        print("-" * 60)
        print(thinking)
        print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    
    # Summary
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("デモ完了")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢\n")
    
    return "デモが正常に完了しました。"


if __name__ == "__main__":
    asyncio.run(run_langchain_multi_agent_demo())
