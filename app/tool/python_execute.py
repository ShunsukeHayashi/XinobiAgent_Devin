"""
Python execute tool for agent use.
"""

import asyncio
import sys
from io import StringIO
from typing import Optional

from app.tool.base import BaseTool


class PythonExecute(BaseTool):
    """
    Tool for executing Python code.
    """
    
    name: str = "python_execute"
    description: str = "Execute Python code"
    
    async def run(self, code: str) -> str:
        """
        Run Python code.
        
        Args:
            code: The Python code to run
            
        Returns:
            The output of the code
        """
        # Save the original stdout and stderr
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        
        # Create string buffers for stdout and stderr
        stdout_buffer = StringIO()
        stderr_buffer = StringIO()
        
        try:
            # Redirect stdout and stderr to the buffers
            sys.stdout = stdout_buffer
            sys.stderr = stderr_buffer
            
            # Execute the code
            exec(code)
            
            # Get the output
            stdout_output = stdout_buffer.getvalue()
            stderr_output = stderr_buffer.getvalue()
            
            # Return the output
            if stderr_output:
                return f"Output:\n{stdout_output}\n\nErrors:\n{stderr_output}"
            else:
                return stdout_output
        except Exception as e:
            return f"Error executing Python code: {str(e)}"
        finally:
            # Restore the original stdout and stderr
            sys.stdout = original_stdout
            sys.stderr = original_stderr
