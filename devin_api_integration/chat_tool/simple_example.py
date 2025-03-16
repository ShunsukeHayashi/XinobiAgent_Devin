"""
Simple example of using the Devin API as a tool call within a chat thread.
"""

import os
import json
import asyncio
from typing import Dict, Any, List

from devin_api_integration.chat_tool.devin_chat_tool import DevinChatTool


async def simulate_chat_thread():
    """
    Simulate a chat thread with Devin API tool calls.
    """
    # Initialize the Devin Chat Tool
    api_key = os.environ.get("DEVIN_API_KEY", "your_api_key")
    devin_tool = DevinChatTool(api_key=api_key)
    
    # Simulate a chat thread
    chat_thread = [
        {"role": "user", "content": "Pythonでシンプルなウェブサーバーを作成してください。"},
        {"role": "assistant", "content": "Pythonでウェブサーバーを作成するお手伝いをします。Devin AIを使って作成しましょう。"}
    ]
    
    # Print the chat thread so far
    print("\n=== チャットスレッド ===")
    for message in chat_thread:
        print(f"{message['role']}: {message['content']}")
    
    # Add a tool call to the chat thread
    tool_call = {
        "role": "tool",
        "name": "devin",
        "content": json.dumps({
            "command": "create_session",
            "arguments": {
                "prompt": "Create a simple Python web server that serves static files from a directory"
            }
        })
    }
    
    # Print the tool call
    print(f"\n{tool_call['role']} ({tool_call['name']}): {tool_call['content']}")
    
    # Process the tool call
    if tool_call["name"] == "devin":
        tool_args = json.loads(tool_call["content"])
        tool_result = await devin_tool.run(
            command=tool_args["command"],
            arguments=tool_args["arguments"]
        )
        
        # Add the tool result to the chat thread
        result_message = {
            "role": "tool_result",
            "name": "devin",
            "content": tool_result
        }
        chat_thread.append(result_message)
        
        # Print the tool result
        print(f"{result_message['role']} ({result_message['name']}): {result_message['content']}")
        
        # Parse the result to get the session ID
        result_data = json.loads(tool_result)
        if result_data.get("status") == "success" and "session_id" in result_data:
            session_id = result_data["session_id"]
            
            # Add a response from the assistant
            assistant_response = {
                "role": "assistant",
                "content": f"Devin AIセッションを作成しました。セッションID: {session_id}\n\nDevinはあなたのリクエストに取り組んでいます。このウェブサーバーに特定の機能を追加しますか？"
            }
            chat_thread.append(assistant_response)
            
            # Print the assistant response
            print(f"{assistant_response['role']}: {assistant_response['content']}")
            
            # Add a follow-up message from the user
            user_followup = {
                "role": "user",
                "content": "HTTPSもサポートしてください。"
            }
            chat_thread.append(user_followup)
            
            # Print the user follow-up
            print(f"{user_followup['role']}: {user_followup['content']}")
            
            # Add another tool call for the follow-up
            followup_tool_call = {
                "role": "tool",
                "name": "devin",
                "content": json.dumps({
                    "command": "send_message",
                    "arguments": {
                        "message": "Add HTTPS support to the web server",
                        "session_id": session_id
                    }
                })
            }
            
            # Print the follow-up tool call
            print(f"{followup_tool_call['role']} ({followup_tool_call['name']}): {followup_tool_call['content']}")
            
            # Process the follow-up tool call
            if followup_tool_call["name"] == "devin":
                followup_args = json.loads(followup_tool_call["content"])
                followup_result = await devin_tool.run(
                    command=followup_args["command"],
                    arguments=followup_args["arguments"]
                )
                
                # Add the follow-up tool result to the chat thread
                followup_result_message = {
                    "role": "tool_result",
                    "name": "devin",
                    "content": followup_result
                }
                chat_thread.append(followup_result_message)
                
                # Print the follow-up tool result
                print(f"{followup_result_message['role']} ({followup_result_message['name']}): {followup_result_message['content']}")
                
                # Add a final response from the assistant
                final_response = {
                    "role": "assistant",
                    "content": "HTTPSサポートの追加をDevin AIに依頼しました。Devinはあなたのリクエストに取り組んでいます。他に必要な機能はありますか？"
                }
                chat_thread.append(final_response)
                
                # Print the final response
                print(f"{final_response['role']}: {final_response['content']}")
    
    # Return the chat thread
    return chat_thread


if __name__ == "__main__":
    # Run the example
    asyncio.run(simulate_chat_thread())
