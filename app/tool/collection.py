"""
Tool collection for managing multiple tools.
"""

from typing import List, Dict, Any, Optional
from app.tool.base import BaseTool


class ToolCollection:
    """
    A collection of tools that can be used by agents.
    
    This provides a way to manage multiple tools and look them up by name.
    """
    
    def __init__(self, tools: Optional[List[BaseTool]] = None):
        """
        Initialize the tool collection.
        
        Args:
            tools: Initial list of tools to include
        """
        self.tools = tools or []
        self._tool_map = {tool.name: tool for tool in self.tools}
    
    def add_tool(self, tool: BaseTool) -> None:
        """
        Add a tool to the collection.
        
        Args:
            tool: The tool to add
        """
        self.tools.append(tool)
        self._tool_map[tool.name] = tool
    
    def get_tool(self, name: str) -> Optional[BaseTool]:
        """
        Get a tool by name.
        
        Args:
            name: The name of the tool to get
            
        Returns:
            The tool, or None if not found
        """
        return self._tool_map.get(name)
    
    def get_schemas(self) -> Dict[str, Dict[str, Any]]:
        """
        Get schemas for all tools.
        
        Returns:
            A dictionary mapping tool names to their schemas
        """
        return {tool.name: tool.get_schema() for tool in self.tools}
