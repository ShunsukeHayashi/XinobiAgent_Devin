"""
Demo script for the Hybrid Agent combining OpenAI API and LangChain.

This script demonstrates how to use a Hybrid Agent that combines the Working
Backwards methodology from GenericAgent with the multi-agent conversation
capabilities of LangChain to solve a complex problem.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any

from app.agent.hybrid_agent import HybridAgent, AgentRole
from app.tool import ToolCollection, Bash, PythonExecute, Terminate


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def run_hybrid_agent_demo() -> None:
    """
    Run a demonstration of the Hybrid Agent.
    """
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("ハイブリッドエージェントデモ (OpenAI API + LangChain)")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢\n")
    
    # Create a tool collection
    tools = ToolCollection([
        PythonExecute(),
        Bash(),
        Terminate()
    ])
    
    # Create agent roles
    roles = [
        AgentRole(
            name="プランナー",  # Planner
            description="戦略的計画立案者",  # Strategic Planner
            expertise=["プロジェクト管理", "タスク分解", "リスク評価"],  # Project management, Task decomposition, Risk assessment
            system_prompt="""あなたは「プランナー」として、複雑な問題を管理可能なステップに分解する能力に優れています。
            プロジェクト管理、タスク分解、リスク評価に関する専門知識があります。
            会話では、構造化された計画の作成、タスク間の依存関係の特定、
            問題のすべての側面が体系的に対処されるようにすることに焦点を当ててください。"""
        ),
        AgentRole(
            name="開発者",  # Developer
            description="ソフトウェア開発者",  # Software Developer
            expertise=["コーディング", "ソフトウェアアーキテクチャ", "デバッグ"],  # Coding, Software architecture, Debugging
            system_prompt="""あなたは「開発者」として、コーディング、ソフトウェアアーキテクチャ、デバッグに関する深い専門知識を持っています。
            会話では、実装の詳細、コード構造、技術的な実現可能性に焦点を当ててください。
            具体的な例を提供し、技術的な課題に対する実用的なソリューションを提案してください。"""
        ),
        AgentRole(
            name="評価者",  # Critic
            description="品質保証スペシャリスト",  # Quality Assurance Specialist
            expertise=["テスト", "エッジケース", "ユーザーエクスペリエンス"],  # Testing, Edge cases, User experience
            system_prompt="""あなたは「評価者」として、潜在的な問題やエッジケースを特定することに優れた品質保証スペシャリストです。
            テスト、エッジケースの発見、ユーザーエクスペリエンスの評価に関する専門知識があります。
            会話では、何が間違う可能性があるか、ソリューションを徹底的にテストする方法、
            良好なユーザーエクスペリエンスを確保する方法に焦点を当ててください。"""
        )
    ]
    
    # Create the hybrid agent
    agent = HybridAgent(
        name="hybrid_agent",
        description="OpenAI APIとLangChainを組み合わせたハイブリッドエージェント",
        available_tools=tools,
        max_steps=9,  # 3 turns per agent
        roles=roles
    )
    
    # Set the goal
    goal = """
    現在の日付と時刻を取得し、それをファイルに保存するPythonスクリプトを作成してください。
    スクリプトは以下の要件を満たす必要があります：
    1. 現在の日付と時刻を日本のフォーマット（YYYY年MM月DD日 HH時MM分SS秒）で表示する
    2. 結果を「current_datetime.txt」というファイルに保存する
    3. ファイルが正常に作成されたことを確認するメッセージを表示する
    """
    
    print(f"目標:\n{goal}\n")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    
    # Run the agent
    print("\nハイブリッドエージェントを実行中...\n")
    result = await agent.run(goal)
    
    # Print the result
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("結果:")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢\n")
    print(result)
    
    # Print the thinking processes
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("思考プロセス:")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢\n")
    
    thinking_processes = await agent.get_thinking_processes()
    for agent_name, thinking in thinking_processes.items():
        print(f"\n【{agent_name}の思考プロセス】")
        print("-" * 60)
        print(thinking)
        print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    
    # Check if the file was created
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("ファイルの確認:")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢\n")
    
    import subprocess
    try:
        # Check if the file exists
        result = subprocess.run(
            "ls -l current_datetime.txt 2>/dev/null || echo 'ファイルが見つかりません'",
            shell=True,
            capture_output=True,
            text=True
        )
        print(f"ファイル情報:\n{result.stdout}")
        
        # Display the file contents if it exists
        if "ファイルが見つかりません" not in result.stdout:
            result = subprocess.run(
                "cat current_datetime.txt",
                shell=True,
                capture_output=True,
                text=True
            )
            print(f"\nファイルの内容:\n{result.stdout}")
    except Exception as e:
        print(f"ファイルの確認中にエラーが発生しました: {e}")
    
    print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢")
    print("デモ完了")
    print("◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢\n")
    
    return "デモが正常に完了しました。"


if __name__ == "__main__":
    asyncio.run(run_hybrid_agent_demo())
