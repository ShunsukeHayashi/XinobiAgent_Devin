"""
Bash Tool for Enhanced Devin.

This module provides a tool for executing bash commands in the shell.
"""

import asyncio
import subprocess
from typing import Optional, Dict, Any

from enhanced_devin.tools.base_tool import BaseTool


class BashTool(BaseTool):
    """
    Tool for executing bash commands in the shell.
    
    This tool provides a way to execute bash commands and capture their output.
    It includes options for handling errors, timeouts, and environment variables.
    """
    
    name: str = "bash"
    description: str = "Execute bash commands in the shell"
    version: str = "0.2.0"
    author: str = "Enhanced Devin Team"
    parameters: Dict[str, Any] = {
        "command": {
            "type": "string",
            "description": "The bash command to execute"
        },
        "timeout": {
            "type": "integer",
            "description": "Timeout in seconds (default: 60)",
            "default": 60
        },
        "cwd": {
            "type": "string",
            "description": "Working directory for the command",
            "default": None
        },
        "env": {
            "type": "object",
            "description": "Environment variables for the command",
            "default": None
        }
    }
    
    async def _execute(self, command: str, timeout: int = 60, cwd: Optional[str] = None, 
                      env: Optional[Dict[str, str]] = None) -> str:
        """
        Execute a bash command.
        
        Args:
            command: The bash command to execute
            timeout: Timeout in seconds (default: 60)
            cwd: Working directory for the command
            env: Environment variables for the command
            
        Returns:
            The output of the command
            
        Raises:
            asyncio.TimeoutError: If the command times out
            subprocess.SubprocessError: If the command fails
        """
        try:
            # Create the process
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=cwd,
                env=env
            )
            
            # Wait for the process to complete with timeout
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
            except asyncio.TimeoutError:
                # Kill the process if it times out
                process.kill()
                raise asyncio.TimeoutError(f"Command timed out after {timeout} seconds: {command}")
            
            # Decode the output
            stdout_str = stdout.decode("utf-8")
            stderr_str = stderr.decode("utf-8")
            
            # Check the return code
            if process.returncode != 0:
                raise subprocess.SubprocessError(f"Command failed with return code {process.returncode}: {stderr_str}")
            
            # Return the output
            return stdout_str if stdout_str else stderr_str
        except asyncio.TimeoutError:
            raise
        except subprocess.SubprocessError:
            raise
        except Exception as e:
            raise RuntimeError(f"Error executing bash command: {str(e)}")
