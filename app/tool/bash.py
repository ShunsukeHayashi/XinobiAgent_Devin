"""
Bash tool for agent use.
"""

import asyncio
import subprocess
from typing import Optional

from app.tool.base import BaseTool


class Bash(BaseTool):
    """
    Tool for executing bash commands.
    """
    
    name: str = "bash"
    description: str = "Execute bash commands in the shell"
    
    async def run(self, command: str) -> str:
        """
        Run a bash command.
        
        Args:
            command: The command to run
            
        Returns:
            The output of the command
        """
        try:
            # Run the command in a subprocess
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Get the output
            stdout, stderr = await process.communicate()
            
            # Decode the output
            stdout_str = stdout.decode("utf-8")
            stderr_str = stderr.decode("utf-8")
            
            # Return the output
            if process.returncode == 0:
                return stdout_str
            else:
                return f"Error: {stderr_str}"
        except Exception as e:
            return f"Error executing bash command: {str(e)}"
