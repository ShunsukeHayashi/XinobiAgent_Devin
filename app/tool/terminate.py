"""
Terminate tool for agent use.
"""

from app.tool.base import BaseTool


class Terminate(BaseTool):
    """
    Tool for terminating the agent's execution.
    """
    
    name: str = "terminate"
    description: str = "Terminate the agent's execution"
    
    async def run(self, reason: str = "Task completed") -> str:
        """
        Terminate the agent's execution.
        
        Args:
            reason: The reason for termination
            
        Returns:
            A message indicating that the agent's execution has been terminated
        """
        return f"Agent execution terminated: {reason}"
