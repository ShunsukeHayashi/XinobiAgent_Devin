"""
Python Execute Tool for Enhanced Devin.

This module provides a tool for executing Python code.
"""

import asyncio
import sys
from io import StringIO
from typing import Dict, Any, Optional
import traceback

from enhanced_devin.tools.base_tool import BaseTool


class PythonExecuteTool(BaseTool):
    """
    Tool for executing Python code.
    
    This tool provides a way to execute Python code and capture its output.
    It includes options for handling errors, timeouts, and environment setup.
    """
    
    name: str = "python_execute"
    description: str = "Execute Python code and capture its output"
    version: str = "0.2.0"
    author: str = "Enhanced Devin Team"
    parameters: Dict[str, Any] = {
        "code": {
            "type": "string",
            "description": "The Python code to execute"
        },
        "timeout": {
            "type": "integer",
            "description": "Timeout in seconds (default: 30)",
            "default": 30
        },
        "globals": {
            "type": "object",
            "description": "Global variables for the execution context",
            "default": None
        },
        "locals": {
            "type": "object",
            "description": "Local variables for the execution context",
            "default": None
        }
    }
    
    async def _execute(self, code: str, timeout: int = 30, 
                      globals: Optional[Dict[str, Any]] = None, 
                      locals: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute Python code.
        
        Args:
            code: The Python code to execute
            timeout: Timeout in seconds (default: 30)
            globals: Global variables for the execution context
            locals: Local variables for the execution context
            
        Returns:
            Dict containing the execution result, stdout, stderr, and local variables
            
        Raises:
            asyncio.TimeoutError: If the code execution times out
            Exception: If the code execution fails
        """
        # Create string buffers for stdout and stderr
        stdout_buffer = StringIO()
        stderr_buffer = StringIO()
        
        # Save the original stdout and stderr
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        
        # Initialize the execution context
        if globals is None:
            globals = {}
        if locals is None:
            locals = {}
        
        # Add the asyncio module to the globals
        globals["asyncio"] = asyncio
        
        # Create a future for the result
        result_future = asyncio.Future()
        
        async def execute_with_timeout():
            try:
                # Redirect stdout and stderr to the buffers
                sys.stdout = stdout_buffer
                sys.stderr = stderr_buffer
                
                # Execute the code
                exec(code, globals, locals)
                
                # Get the output
                stdout_output = stdout_buffer.getvalue()
                stderr_output = stderr_buffer.getvalue()
                
                # Set the result
                result_future.set_result({
                    "success": True,
                    "stdout": stdout_output,
                    "stderr": stderr_output,
                    "locals": {k: v for k, v in locals.items() if not k.startswith("_")}
                })
            except Exception as e:
                # Get the traceback
                tb = traceback.format_exc()
                
                # Get the output
                stdout_output = stdout_buffer.getvalue()
                stderr_output = stderr_buffer.getvalue()
                
                # Set the result
                result_future.set_result({
                    "success": False,
                    "error": str(e),
                    "traceback": tb,
                    "stdout": stdout_output,
                    "stderr": stderr_output,
                    "locals": {k: v for k, v in locals.items() if not k.startswith("_")}
                })
            finally:
                # Restore the original stdout and stderr
                sys.stdout = original_stdout
                sys.stderr = original_stderr
        
        try:
            # Start the execution task
            execution_task = asyncio.create_task(execute_with_timeout())
            
            # Wait for the result with timeout
            await asyncio.wait_for(result_future, timeout=timeout)
            
            # Return the result
            return result_future.result()
        except asyncio.TimeoutError:
            # Cancel the execution task
            execution_task.cancel()
            
            # Restore the original stdout and stderr
            sys.stdout = original_stdout
            sys.stderr = original_stderr
            
            # Get the output
            stdout_output = stdout_buffer.getvalue()
            stderr_output = stderr_buffer.getvalue()
            
            # Return the timeout error
            return {
                "success": False,
                "error": f"Code execution timed out after {timeout} seconds",
                "stdout": stdout_output,
                "stderr": stderr_output,
                "locals": {k: v for k, v in locals.items() if not k.startswith("_")}
            }
