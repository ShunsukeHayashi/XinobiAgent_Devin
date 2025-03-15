"""
Python Execute tool for running Python code.
"""

from typing import Dict, Any
import asyncio
import sys
import io
from contextlib import redirect_stdout, redirect_stderr
from app.tool.base import BaseTool


class PythonExecute(BaseTool):
    """
    A tool that allows an agent to execute Python code.
    
    This provides a way for agents to run Python code and get the results.
    """
    
    name: str = "python_execute"
    description: str = "Execute Python code and return the output"
    
    async def execute(self, code: str) -> str:
        """
        Execute Python code.
        
        Args:
            code: The Python code to execute
            
        Returns:
            The code output (stdout and stderr)
        """
        # Capture stdout and stderr
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        
        # Execute the code
        try:
            with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
                # Use exec to run the code
                exec(code, {})
                
            # Get the output
            stdout_str = stdout_buffer.getvalue()
            stderr_str = stderr_buffer.getvalue()
            
            # Combine stdout and stderr
            result = stdout_str
            if stderr_str:
                result += f"\nERROR: {stderr_str}"
                
            return result
        except Exception as e:
            return f"Error executing Python code: {str(e)}"
    
    def get_schema(self) -> Dict[str, Any]:
        """
        Get the schema for this tool.
        
        Returns:
            A dictionary describing the tool's parameters
        """
        return {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The Python code to execute"
                }
            },
            "required": ["code"]
        }
