"""
Gradio demo for Devin API integration.
"""

import os
import sys
import asyncio
import gradio as gr
from typing import Dict, Any, Optional, List, Tuple

# Add parent directory to path to import DevinAPIClient and DevinAgent
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from devin_api_integration.src.devin_api_client import DevinAPIClient
from devin_api_integration.src.devin_agent import DevinAgent

# Configure CSS
css = """
.container {
    max-width: 900px;
    margin: auto;
    padding-top: 1.5rem;
}
.title {
    text-align: center;
    margin-bottom: 1rem;
}
.subtitle {
    text-align: center;
    margin-bottom: 2rem;
    color: #666;
}
.api-key-input {
    margin-bottom: 1rem;
}
.session-info {
    margin-top: 1rem;
    padding: 1rem;
    border-radius: 0.5rem;
    background-color: #f8f9fa;
}
.status-success {
    color: green;
    font-weight: bold;
}
.status-error {
    color: red;
    font-weight: bold;
}
.status-info {
    color: blue;
    font-weight: bold;
}
"""

# Initialize session state
session_id = None
agent = None

async def create_agent(api_key: str, agent_name: str, agent_description: str) -> Tuple[str, str]:
    """
    Create a DevinAgent instance.
    
    Args:
        api_key: API key for authentication.
        agent_name: Name of the agent.
        agent_description: Description of the agent.
        
    Returns:
        Status message and status type.
    """
    global agent
    
    try:
        # Create the agent
        agent = DevinAgent(
            name=agent_name,
            description=agent_description,
            api_key=api_key
        )
        
        return "エージェントが正常に作成されました ✅", "success"
    except Exception as e:
        return f"エージェント作成エラー: {str(e)} ❌", "error"

async def create_task(prompt: str, playbook_id: Optional[str] = None) -> Tuple[str, str, str]:
    """
    Create a new task for Devin.
    
    Args:
        prompt: The task description for Devin.
        playbook_id: Optional playbook ID to guide execution.
        
    Returns:
        Status message, status type, and session ID.
    """
    global agent, session_id
    
    if not agent:
        return "APIキーを設定してエージェントを作成してください ⚠️", "error", ""
    
    try:
        # Create a new task
        session_id = await agent.create_task(prompt, playbook_id)
        
        return f"タスクが正常に作成されました (セッションID: {session_id}) ✅", "success", session_id
    except Exception as e:
        return f"タスク作成エラー: {str(e)} ❌", "error", ""

async def send_follow_up(message: str) -> Tuple[str, str]:
    """
    Send a follow-up message to Devin.
    
    Args:
        message: Message to send.
        
    Returns:
        Status message and status type.
    """
    global agent, session_id
    
    if not agent:
        return "APIキーを設定してエージェントを作成してください ⚠️", "error"
    
    if not session_id:
        return "タスクを作成してください ⚠️", "error"
    
    try:
        # Send the follow-up message
        await agent.send_follow_up(message)
        
        return f"メッセージが正常に送信されました ✅", "success"
    except Exception as e:
        return f"メッセージ送信エラー: {str(e)} ❌", "error"

async def get_session_status() -> Tuple[str, Dict[str, Any]]:
    """
    Get the status of the current session.
    
    Returns:
        Status message and session details.
    """
    global agent, session_id
    
    if not agent:
        return "APIキーを設定してエージェントを作成してください ⚠️", {}
    
    if not session_id:
        return "タスクを作成してください ⚠️", {}
    
    try:
        # Get session details
        status = await agent.get_status()
        
        return "セッションステータスを取得しました ✅", status
    except Exception as e:
        return f"ステータス取得エラー: {str(e)} ❌", {}

async def upload_file(file_path: str) -> Tuple[str, str]:
    """
    Upload a file to provide context for the task.
    
    Args:
        file_path: Path to the file to upload.
        
    Returns:
        Status message and status type.
    """
    global agent
    
    if not agent:
        return "APIキーを設定してエージェントを作成してください ⚠️", "error"
    
    try:
        # Upload the file
        attachment_id = await agent.upload_context_file(file_path)
        
        return f"ファイルが正常にアップロードされました (添付ファイルID: {attachment_id}) ✅", "success"
    except Exception as e:
        return f"ファイルアップロードエラー: {str(e)} ❌", "error"

def format_session_details(details: Dict[str, Any]) -> str:
    """
    Format session details for display.
    
    Args:
        details: Session details.
        
    Returns:
        Formatted session details.
    """
    if not details:
        return ""
    
    formatted = "## セッション詳細\n\n"
    
    # Add session ID
    session_id = details.get("session_id", "不明")
    formatted += f"**セッションID:** {session_id}\n\n"
    
    # Add status
    status = details.get("status", "不明")
    formatted += f"**ステータス:** {status}\n\n"
    
    # Add created at
    created_at = details.get("created_at", "不明")
    formatted += f"**作成日時:** {created_at}\n\n"
    
    # Add prompt
    prompt = details.get("prompt", "不明")
    formatted += f"**プロンプト:** {prompt}\n\n"
    
    # Add messages
    messages = details.get("messages", [])
    if messages:
        formatted += "### メッセージ\n\n"
        for message in messages:
            role = message.get("role", "不明")
            content = message.get("content", "不明")
            formatted += f"**{role}:** {content}\n\n"
    
    return formatted

def create_ui():
    """
    Create the Gradio UI.
    
    Returns:
        Gradio interface.
    """
    with gr.Blocks(css=css) as demo:
        gr.HTML("<h1 class='title'>Devin API デモ</h1>")
        gr.HTML("<p class='subtitle'>XinobiAgent フレームワークを使用した Devin API 統合のデモ</p>")
        
        with gr.Tab("エージェント設定"):
            with gr.Row():
                with gr.Column():
                    api_key_input = gr.Textbox(
                        label="Devin API キー",
                        placeholder="sk-...",
                        type="password",
                        scale=3
                    )
                    agent_name = gr.Textbox(
                        label="エージェント名",
                        value="demo_agent",
                        scale=1
                    )
                    agent_description = gr.Textbox(
                        label="エージェントの説明",
                        value="Devin API デモ用エージェント",
                        scale=2
                    )
                    create_agent_btn = gr.Button("エージェントを作成", variant="primary")
                    agent_status = gr.Markdown()
        
        with gr.Tab("タスク作成"):
            with gr.Row():
                with gr.Column():
                    prompt_input = gr.Textbox(
                        label="タスクの説明",
                        placeholder="Pythonでシンプルなウェブサーバーを作成してください",
                        lines=5
                    )
                    playbook_id = gr.Textbox(
                        label="プレイブックID (オプション)",
                        placeholder="playbook-..."
                    )
                    create_task_btn = gr.Button("タスクを作成", variant="primary")
                    task_status = gr.Markdown()
                    session_id_display = gr.Textbox(label="セッションID", interactive=False)
        
        with gr.Tab("フォローアップ"):
            with gr.Row():
                with gr.Column():
                    follow_up_input = gr.Textbox(
                        label="フォローアップメッセージ",
                        placeholder="ウェブサーバーにルートを追加してください",
                        lines=3
                    )
                    send_follow_up_btn = gr.Button("メッセージを送信", variant="primary")
                    follow_up_status = gr.Markdown()
        
        with gr.Tab("セッションステータス"):
            with gr.Row():
                with gr.Column():
                    get_status_btn = gr.Button("ステータスを取得", variant="primary")
                    status_display = gr.Markdown()
                    session_details = gr.Markdown(label="セッション詳細")
        
        with gr.Tab("ファイルアップロード"):
            with gr.Row():
                with gr.Column():
                    file_upload = gr.File(label="ファイルをアップロード")
                    upload_file_btn = gr.Button("ファイルをアップロード", variant="primary")
                    upload_status = gr.Markdown()
        
        # Event handlers
        create_agent_btn.click(
            fn=lambda api_key, name, desc: asyncio.run(create_agent(api_key, name, desc)),
            inputs=[api_key_input, agent_name, agent_description],
            outputs=[agent_status]
        )
        
        create_task_btn.click(
            fn=lambda prompt, playbook_id: asyncio.run(create_task(prompt, playbook_id)),
            inputs=[prompt_input, playbook_id],
            outputs=[task_status, session_id_display]
        )
        
        send_follow_up_btn.click(
            fn=lambda message: asyncio.run(send_follow_up(message)),
            inputs=[follow_up_input],
            outputs=[follow_up_status]
        )
        
        get_status_btn.click(
            fn=lambda: asyncio.run(get_session_status()),
            inputs=[],
            outputs=[status_display, session_details]
        )
        
        upload_file_btn.click(
            fn=lambda file: asyncio.run(upload_file(file.name)) if file else ("ファイルを選択してください ⚠️", "error"),
            inputs=[file_upload],
            outputs=[upload_status]
        )
        
        # Update status display format
        agent_status.change(
            fn=lambda status: f"<div class='status-{status[1]}'>{status[0]}</div>" if isinstance(status, tuple) else status,
            inputs=[agent_status],
            outputs=[agent_status]
        )
        
        task_status.change(
            fn=lambda status: f"<div class='status-{status[1]}'>{status[0]}</div>" if isinstance(status, tuple) else status,
            inputs=[task_status],
            outputs=[task_status]
        )
        
        follow_up_status.change(
            fn=lambda status: f"<div class='status-{status[1]}'>{status[0]}</div>" if isinstance(status, tuple) else status,
            inputs=[follow_up_status],
            outputs=[follow_up_status]
        )
        
        status_display.change(
            fn=lambda status: f"<div class='status-info'>{status[0]}</div>" if isinstance(status, tuple) else status,
            inputs=[status_display],
            outputs=[status_display]
        )
        
        session_details.change(
            fn=lambda details: format_session_details(details[1]) if isinstance(details, tuple) else details,
            inputs=[session_details],
            outputs=[session_details]
        )
        
        upload_status.change(
            fn=lambda status: f"<div class='status-{status[1]}'>{status[0]}</div>" if isinstance(status, tuple) else status,
            inputs=[upload_status],
            outputs=[upload_status]
        )
    
    return demo

if __name__ == "__main__":
    demo = create_ui()
    demo.launch()
