"""
Bash tool for executing shell commands.
"""

from typing import Dict, Any
import asyncio
import subprocess
from app.tool.base import BaseTool


class Bash(BaseTool):
    """
    A tool that allows an agent to execute bash commands.
    
    This provides a way for agents to interact with the system shell.
    """
    
    name: str = "bash"
    description: str = "Execute a bash command and return the output"
    
    async def execute(self, command: str) -> str:
        """
        Execute a bash command.
        
        Args:
            command: The command to execute
            
        Returns:
            The command output (stdout and stderr)
        """
        # Use asyncio to run the command asynchronously
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Wait for the command to complete and get output
        stdout, stderr = await process.communicate()
        
        # Decode the output
        stdout_str = stdout.decode("utf-8", errors="replace")
        stderr_str = stderr.decode("utf-8", errors="replace")
        
        # Combine stdout and stderr
        result = stdout_str
        if stderr_str:
            result += f"\nERROR: {stderr_str}"
        
        return result
    
    def get_schema(self) -> Dict[str, Any]:
        """
        Get the schema for this tool.
        
        Returns:
            A dictionary describing the tool's parameters
        """
        return {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The bash command to execute"
                }
            },
            "required": ["command"]
        }
