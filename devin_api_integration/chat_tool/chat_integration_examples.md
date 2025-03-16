# Devin API Chat Integration Examples

This document provides examples of how to integrate the Devin API as a tool call within different chat frameworks.

## OpenAI Chat Completion API

### Tool Definition

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "devin",
            "description": "Interact with Devin AI to solve programming tasks",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "enum": ["create_session", "send_message", "get_session_status", "list_sessions", "upload_file"],
                        "description": "The command to execute"
                    },
                    "arguments": {
                        "type": "object",
                        "description": "Arguments for the command"
                    }
                },
                "required": ["command", "arguments"]
            }
        }
    }
]
```

### Example Usage

```python
import json
import openai
from devin_api_integration.chat_tool.devin_chat_tool import DevinChatTool

# Initialize the Devin Chat Tool
devin_tool = DevinChatTool(api_key="your_api_key")

# Define the chat messages
messages = [
    {"role": "system", "content": "You are a helpful assistant that can use Devin AI to solve programming tasks."},
    {"role": "user", "content": "I need to create a simple Python web server."}
]

# Create a chat completion with tool calling
response = openai.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

# Process the response
message = response.choices[0].message
messages.append(message)

# Check if there's a tool call
if message.tool_calls:
    for tool_call in message.tool_calls:
        if tool_call.function.name == "devin":
            # Parse the tool call arguments
            function_args = json.loads(tool_call.function.arguments)
            
            # Execute the tool call
            tool_result = await devin_tool.run(
                command=function_args["command"],
                arguments=function_args["arguments"]
            )
            
            # Add the tool result to the messages
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": "devin",
                "content": tool_result
            })
    
    # Get the assistant's response to the tool result
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    
    # Add the assistant's response to the messages
    messages.append(response.choices[0].message)
```

## Anthropic Claude API

### Example Usage

```python
import json
import anthropic
from devin_api_integration.chat_tool.devin_chat_tool import DevinChatTool

# Initialize the Devin Chat Tool
devin_tool = DevinChatTool(api_key="your_api_key")

# Initialize the Anthropic client
client = anthropic.Anthropic(api_key="your_anthropic_api_key")

# Define the tools
tools = [
    {
        "name": "devin",
        "description": "Interact with Devin AI to solve programming tasks",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "enum": ["create_session", "send_message", "get_session_status", "list_sessions", "upload_file"],
                    "description": "The command to execute"
                },
                "arguments": {
                    "type": "object",
                    "description": "Arguments for the command"
                }
            },
            "required": ["command", "arguments"]
        }
    }
]

# Define the chat messages
messages = [
    {"role": "user", "content": "I need to create a simple Python web server."}
]

# Create a message with tool calling
response = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1000,
    messages=messages,
    tools=tools
)

# Process the response
message = response.content[0].text
tool_calls = response.tool_calls

# Check if there are tool calls
if tool_calls:
    for tool_call in tool_calls:
        if tool_call.name == "devin":
            # Parse the tool call input
            function_args = json.loads(tool_call.input)
            
            # Execute the tool call
            tool_result = await devin_tool.run(
                command=function_args["command"],
                arguments=function_args["arguments"]
            )
            
            # Add the tool result to the messages
            messages.append({
                "role": "assistant",
                "content": message
            })
            messages.append({
                "role": "tool",
                "name": "devin",
                "content": tool_result
            })
    
    # Get the assistant's response to the tool result
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        messages=messages
    )
    
    # Add the assistant's response to the messages
    messages.append({
        "role": "assistant",
        "content": response.content[0].text
    })
```

## Custom Chat Framework

### Example Usage

```python
import json
from devin_api_integration.chat_tool.devin_chat_tool import DevinChatTool

class ChatFramework:
    def __init__(self):
        self.messages = []
        self.tools = {
            "devin": DevinChatTool(api_key="your_api_key")
        }
    
    async def process_message(self, message):
        # Add the message to the chat history
        self.messages.append(message)
        
        # If the message is from the user, generate a response
        if message["role"] == "user":
            # Generate a response (this would typically use an LLM)
            response = self._generate_response(message["content"])
            
            # Check if the response includes a tool call
            if "use_tool" in response:
                tool_call = self._parse_tool_call(response)
                
                if tool_call["name"] in self.tools:
                    # Execute the tool call
                    tool = self.tools[tool_call["name"]]
                    tool_result = await tool.run(
                        command=tool_call["command"],
                        arguments=tool_call["arguments"]
                    )
                    
                    # Add the tool result to the chat history
                    self.messages.append({
                        "role": "tool_result",
                        "name": tool_call["name"],
                        "content": tool_result
                    })
                    
                    # Generate a response to the tool result
                    final_response = self._generate_response_to_tool_result(tool_result)
                    
                    # Add the final response to the chat history
                    self.messages.append({
                        "role": "assistant",
                        "content": final_response
                    })
                    
                    return final_response
            
            # If no tool call, just return the response
            self.messages.append({
                "role": "assistant",
                "content": response
            })
            
            return response
    
    def _generate_response(self, user_message):
        # This would typically use an LLM
        if "web server" in user_message.lower():
            return "I can help you create a Python web server. Let me use Devin AI for this. use_tool: devin create_session 'Create a simple Python web server that serves static files from a directory'"
        return "I'm not sure how to help with that."
    
    def _parse_tool_call(self, response):
        # Parse a tool call from the response
        if "use_tool:" in response:
            tool_parts = response.split("use_tool:", 1)[1].strip().split(" ", 2)
            tool_name = tool_parts[0].strip()
            command = tool_parts[1].strip()
            
            # Parse arguments
            arguments = {}
            if len(tool_parts) > 2:
                arg_str = tool_parts[2].strip()
                if arg_str.startswith("{") and arg_str.endswith("}"):
                    # Parse as JSON
                    arguments = json.loads(arg_str)
                else:
                    # Parse as a single argument based on the command
                    if command == "create_session":
                        arguments = {"prompt": arg_str.strip("'")}
                    elif command == "send_message":
                        parts = arg_str.split(" ", 1)
                        if len(parts) > 1:
                            arguments = {
                                "session_id": parts[0].strip("'"),
                                "message": parts[1].strip("'")
                            }
            
            return {
                "name": tool_name,
                "command": command,
                "arguments": arguments
            }
        
        return None
    
    def _generate_response_to_tool_result(self, tool_result):
        # This would typically use an LLM
        result_data = json.loads(tool_result)
        if result_data["status"] == "success":
            if "session_id" in result_data:
                return f"I've created a Devin AI session to help you build a Python web server. The session ID is {result_data['session_id']}. Devin is now working on your request. Would you like to add any specific features to this web server?"
            return "Devin AI has processed your request successfully."
        else:
            return f"There was an error with the Devin AI request: {result_data['message']}"
```

## LINE Messaging API

### Example Usage

```python
import json
import requests
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from devin_api_integration.chat_tool.devin_chat_tool import DevinChatTool

app = Flask(__name__)

# Initialize the LINE Bot API
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

# Initialize the Devin Chat Tool
devin_tool = DevinChatTool(api_key="your_api_key")

# Store session information
sessions = {}

@app.route("/callback", methods=['POST'])
def callback():
    # Get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # Handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    text = event.message.text
    
    # Check if the user has an active session
    if user_id not in sessions:
        sessions[user_id] = {
            "devin_session_id": None,
            "state": "initial"
        }
    
    session = sessions[user_id]
    
    # Handle different states
    if session["state"] == "initial":
        if "create web server" in text.lower():
            # Create a Devin session
            result = await devin_tool.run(
                command="create_session",
                arguments={
                    "prompt": "Create a simple Python web server that serves static files from a directory"
                }
            )
            
            result_data = json.loads(result)
            if result_data["status"] == "success":
                session["devin_session_id"] = result_data["session_id"]
                session["state"] = "session_created"
                
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=f"Devin AIセッションを作成しました。セッションID: {session['devin_session_id']}\n\nDevinはあなたのリクエストに取り組んでいます。このWebサーバーに特定の機能を追加しますか？")
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=f"Devin AIセッションの作成中にエラーが発生しました: {result_data['message']}")
                )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="こんにちは！Pythonのウェブサーバーを作成するには「create web server」と入力してください。")
            )
    
    elif session["state"] == "session_created":
        # Send a message to the Devin session
        result = await devin_tool.run(
            command="send_message",
            arguments={
                "message": text,
                "session_id": session["devin_session_id"]
            }
        )
        
        result_data = json.loads(result)
        if result_data["status"] == "success":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"メッセージをDevin AIに送信しました。Devinはあなたのリクエストに取り組んでいます。")
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"Devin AIへのメッセージ送信中にエラーが発生しました: {result_data['message']}")
            )

if __name__ == "__main__":
    app.run(debug=True)
```

## Slack Bot API

### Example Usage

```python
import os
import json
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from devin_api_integration.chat_tool.devin_chat_tool import DevinChatTool

# Initialize the Slack app
app = App(token=os.environ["SLACK_BOT_TOKEN"])

# Initialize the Devin Chat Tool
devin_tool = DevinChatTool(api_key=os.environ.get("DEVIN_API_KEY"))

# Store session information
sessions = {}

@app.message("create web server")
async def create_web_server(message, say):
    user_id = message["user"]
    
    # Create a Devin session
    result = await devin_tool.run(
        command="create_session",
        arguments={
            "prompt": "Create a simple Python web server that serves static files from a directory"
        }
    )
    
    result_data = json.loads(result)
    if result_data["status"] == "success":
        # Store the session ID
        sessions[user_id] = {
            "devin_session_id": result_data["session_id"],
            "state": "session_created"
        }
        
        await say(f"Devin AIセッションを作成しました。セッションID: {result_data['session_id']}\n\nDevinはあなたのリクエストに取り組んでいます。このWebサーバーに特定の機能を追加しますか？")
    else:
        await say(f"Devin AIセッションの作成中にエラーが発生しました: {result_data['message']}")

@app.message("status")
async def check_status(message, say):
    user_id = message["user"]
    
    if user_id in sessions and sessions[user_id]["devin_session_id"]:
        # Get the session status
        result = await devin_tool.run(
            command="get_session_status",
            arguments={
                "session_id": sessions[user_id]["devin_session_id"]
            }
        )
        
        result_data = json.loads(result)
        if result_data["status"] == "success":
            await say(f"Devin AIセッションのステータス:\n```\n{json.dumps(result_data['details'], indent=2, ensure_ascii=False)}\n```")
        else:
            await say(f"Devin AIセッションのステータス取得中にエラーが発生しました: {result_data['message']}")
    else:
        await say("アクティブなDevin AIセッションがありません。「create web server」と入力して新しいセッションを作成してください。")

@app.message()
async def handle_message(message, say):
    user_id = message["user"]
    text = message["text"]
    
    # Ignore messages that are handled by other handlers
    if text in ["create web server", "status"]:
        return
    
    if user_id in sessions and sessions[user_id]["devin_session_id"] and sessions[user_id]["state"] == "session_created":
        # Send a message to the Devin session
        result = await devin_tool.run(
            command="send_message",
            arguments={
                "message": text,
                "session_id": sessions[user_id]["devin_session_id"]
            }
        )
        
        result_data = json.loads(result)
        if result_data["status"] == "success":
            await say(f"メッセージをDevin AIに送信しました。Devinはあなたのリクエストに取り組んでいます。")
        else:
            await say(f"Devin AIへのメッセージ送信中にエラーが発生しました: {result_data['message']}")
    else:
        await say("こんにちは！Pythonのウェブサーバーを作成するには「create web server」と入力してください。")

if __name__ == "__main__":
    # Start the app
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
```

## Discord Bot API

### Example Usage

```python
import os
import json
import discord
from discord.ext import commands

from devin_api_integration.chat_tool.devin_chat_tool import DevinChatTool

# Initialize the Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Initialize the Devin Chat Tool
devin_tool = DevinChatTool(api_key=os.environ.get("DEVIN_API_KEY"))

# Store session information
sessions = {}

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.command(name="create")
async def create_web_server(ctx):
    user_id = str(ctx.author.id)
    
    # Create a Devin session
    result = await devin_tool.run(
        command="create_session",
        arguments={
            "prompt": "Create a simple Python web server that serves static files from a directory"
        }
    )
    
    result_data = json.loads(result)
    if result_data["status"] == "success":
        # Store the session ID
        sessions[user_id] = {
            "devin_session_id": result_data["session_id"],
            "state": "session_created"
        }
        
        await ctx.send(f"Devin AIセッションを作成しました。セッションID: {result_data['session_id']}\n\nDevinはあなたのリクエストに取り組んでいます。このWebサーバーに特定の機能を追加しますか？")
    else:
        await ctx.send(f"Devin AIセッションの作成中にエラーが発生しました: {result_data['message']}")

@bot.command(name="status")
async def check_status(ctx):
    user_id = str(ctx.author.id)
    
    if user_id in sessions and sessions[user_id]["devin_session_id"]:
        # Get the session status
        result = await devin_tool.run(
            command="get_session_status",
            arguments={
                "session_id": sessions[user_id]["devin_session_id"]
            }
        )
        
        result_data = json.loads(result)
        if result_data["status"] == "success":
            await ctx.send(f"Devin AIセッションのステータス:\n```\n{json.dumps(result_data['details'], indent=2, ensure_ascii=False)}\n```")
        else:
            await ctx.send(f"Devin AIセッションのステータス取得中にエラーが発生しました: {result_data['message']}")
    else:
        await ctx.send("アクティブなDevin AIセッションがありません。「!create」と入力して新しいセッションを作成してください。")

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    
    # Process commands
    await bot.process_commands(message)
    
    # If the message is not a command and starts with a mention of the bot
    if message.content.startswith(f"<@{bot.user.id}>"):
        user_id = str(message.author.id)
        text = message.content.replace(f"<@{bot.user.id}>", "").strip()
        
        if user_id in sessions and sessions[user_id]["devin_session_id"] and sessions[user_id]["state"] == "session_created":
            # Send a message to the Devin session
            result = await devin_tool.run(
                command="send_message",
                arguments={
                    "message": text,
                    "session_id": sessions[user_id]["devin_session_id"]
                }
            )
            
            result_data = json.loads(result)
            if result_data["status"] == "success":
                await message.channel.send(f"メッセージをDevin AIに送信しました。Devinはあなたのリクエストに取り組んでいます。")
            else:
                await message.channel.send(f"Devin AIへのメッセージ送信中にエラーが発生しました: {result_data['message']}")
        else:
            await message.channel.send("こんにちは！Pythonのウェブサーバーを作成するには「!create」と入力してください。")

# Run the bot
bot.run(os.environ["DISCORD_BOT_TOKEN"])
```

## Conclusion

These examples demonstrate how to integrate the Devin API as a tool call within different chat frameworks. The integration pattern is similar across all frameworks:

1. Initialize the DevinChatTool
2. Define the tool schema for the chat framework
3. Process user messages to identify when to use the Devin tool
4. Execute the appropriate Devin command
5. Process the result and send a response to the user

This approach allows for seamless integration of Devin AI capabilities within existing chat interfaces, providing users with powerful programming assistance without leaving their preferred communication platform.
