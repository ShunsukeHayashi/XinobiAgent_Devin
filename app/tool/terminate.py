"""
Terminate tool for ending agent execution.
"""

from typing import Dict, Any
from app.tool.base import BaseTool


class Terminate(BaseTool):
    """
    A tool that allows an agent to terminate its execution.
    
    This is useful for agents to signal that they have completed their task
    or cannot proceed further.
    """
    
    name: str = "terminate"
    description: str = "Terminate the agent's execution with a final message"
    
    async def execute(self, message: str = "Task completed") -> str:
        """
        Execute the terminate tool.
        
        Args:
            message: Final message before termination
            
        Returns:
            The termination message
        """
        return f"TERMINATING: {message}"
    
    def get_schema(self) -> Dict[str, Any]:
        """
        Get the schema for this tool.
        
        Returns:
            A dictionary describing the tool's parameters
        """
        return {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "Final message before termination"
                }
            },
            "required": []
        }
