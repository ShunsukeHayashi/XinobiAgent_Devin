"""
Example usage of the Devin Chat Tool in a chat thread.

This example demonstrates how to use the DevinChatTool with the GenericAgent
and ToolCollection classes from the XinobiAgent framework.
"""

import asyncio
import os
import json
from typing import Dict, Any, List

from app.agent.generic_agent import GenericAgent
from app.tool.collection import ToolCollection
from app.tool.bash import Bash
from app.tool.google_search import GoogleSearch

from devin_api_integration.chat_tool.devin_chat_tool import DevinChatTool


async def run_example():
    """
    Run an example of using the Devin Chat Tool in a chat thread.
    """
    # Create a tool collection with the Devin Chat Tool and other tools
    tools = ToolCollection([
        Bash(),
        GoogleSearch(),
        DevinChatTool(api_key=os.environ.get("DEVIN_API_KEY"))
    ])
    
    # Create a generic agent with the tool collection
    agent = GenericAgent(
        name="devin_chat_agent",
        description="An agent that can use Devin AI to solve programming tasks",
        available_tools=tools
    )
    
    # Set the goal for the agent
    goal = "Create a simple Python web server using Devin AI"
    await agent.set_goal(goal)
    
    # Run the agent
    result = await agent.run()
    
    # Print the result
    print("\n=== EXECUTION RESULT ===")
    print(result)
    
    # Print the execution status
    status = await agent.get_execution_status()
    print("\n=== EXECUTION STATUS ===")
    print(status)


async def run_direct_example():
    """
    Run an example of using the Devin Chat Tool directly.
    """
    # Create the Devin Chat Tool
    devin_tool = DevinChatTool(api_key=os.environ.get("DEVIN_API_KEY"))
    
    # Create a session
    create_result = await devin_tool.run(
        command="create_session",
        arguments={
            "prompt": "Create a simple Python web server"
        }
    )
    print("\n=== CREATE SESSION RESULT ===")
    print(create_result)
    
    # Parse the result to get the session ID
    create_data = json.loads(create_result)
    session_id = create_data.get("session_id")
    
    if session_id:
        # Send a follow-up message
        message_result = await devin_tool.run(
            command="send_message",
            arguments={
                "message": "Make it serve static files from a directory",
                "session_id": session_id
            }
        )
        print("\n=== SEND MESSAGE RESULT ===")
        print(message_result)
        
        # Get the session status
        status_result = await devin_tool.run(
            command="get_session_status",
            arguments={
                "session_id": session_id
            }
        )
        print("\n=== SESSION STATUS RESULT ===")
        print(status_result)


async def run_chat_thread_example():
    """
    Run an example of using the Devin Chat Tool in a simulated chat thread.
    """
    # Create the Devin Chat Tool
    devin_tool = DevinChatTool(api_key=os.environ.get("DEVIN_API_KEY"))
    
    # Simulate a chat thread
    chat_thread = [
        {"role": "user", "content": "I need to create a simple Python web server."},
        {"role": "assistant", "content": "I can help you with that. Let me use Devin AI to create a Python web server for you."},
        {"role": "tool", "name": "devin", "content": json.dumps({
            "command": "create_session",
            "arguments": {
                "prompt": "Create a simple Python web server that serves static files from a directory"
            }
        })}
    ]
    
    # Process the tool call
    if chat_thread[-1]["role"] == "tool" and chat_thread[-1]["name"] == "devin":
        tool_call = json.loads(chat_thread[-1]["content"])
        tool_result = await devin_tool.run(
            command=tool_call["command"],
            arguments=tool_call["arguments"]
        )
        
        # Add the tool result to the chat thread
        chat_thread.append({
            "role": "tool_result",
            "name": "devin",
            "content": tool_result
        })
        
        # Parse the result to get the session ID
        result_data = json.loads(tool_result)
        session_id = result_data.get("session_id")
        
        if session_id:
            # Add a follow-up message from the user
            chat_thread.append({
                "role": "user",
                "content": "Can you make it support HTTPS as well?"
            })
            
            # Add a tool call for the follow-up message
            chat_thread.append({
                "role": "tool",
                "name": "devin",
                "content": json.dumps({
                    "command": "send_message",
                    "arguments": {
                        "message": "Add HTTPS support to the web server",
                        "session_id": session_id
                    }
                })
            })
            
            # Process the follow-up tool call
            if chat_thread[-1]["role"] == "tool" and chat_thread[-1]["name"] == "devin":
                tool_call = json.loads(chat_thread[-1]["content"])
                tool_result = await devin_tool.run(
                    command=tool_call["command"],
                    arguments=tool_call["arguments"]
                )
                
                # Add the tool result to the chat thread
                chat_thread.append({
                    "role": "tool_result",
                    "name": "devin",
                    "content": tool_result
                })
    
    # Print the chat thread
    print("\n=== CHAT THREAD ===")
    for message in chat_thread:
        role = message["role"]
        if role == "tool":
            print(f"{role} ({message['name']}): {message['content']}")
        elif role == "tool_result":
            print(f"{role} ({message['name']}): {message['content']}")
        else:
            print(f"{role}: {message['content']}")


if __name__ == "__main__":
    # Run the examples
    asyncio.run(run_example())
    asyncio.run(run_direct_example())
    asyncio.run(run_chat_thread_example())
