"""
Base tool class for the XinobiAgent framework.
"""

from typing import Dict, Any, Optional


class BaseTool:
    """
    Base class for all tools in the XinobiAgent framework.
    """
    
    name: str = "base_tool"
    description: str = "Base tool class"
    parameters: Dict[str, Any] = {}
    
    def __init__(self, **data):
        """Initialize the tool."""
        for key, value in data.items():
            setattr(self, key, value)
    
    async def run(self, *args, **kwargs):
        """
        Run the tool.
        
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method")
