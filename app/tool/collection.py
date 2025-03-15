"""
Tool collection for agent use.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from app.tool.base import BaseTool


class ToolCollection(BaseModel):
    """
    A collection of tools that can be used by an agent.
    """
    
    tools: List[BaseTool] = Field(
        default_factory=list,
        description="List of tools available to the agent"
    )
    
    def __init__(self, tools: Optional[List[BaseTool]] = None, **data):
        """
        Initialize the tool collection.
        
        Args:
            tools: List of tools to include in the collection
        """
        super().__init__(**data)
        if tools:
            self.tools = tools
    
    def get_tool(self, name: str) -> Optional[BaseTool]:
        """
        Get a tool by name.
        
        Args:
            name: Name of the tool to get
            
        Returns:
            The tool if found, None otherwise
        """
        for tool in self.tools:
            if tool.name.lower() == name.lower():
                return tool
        return None
    
    def add_tool(self, tool: BaseTool) -> None:
        """
        Add a tool to the collection.
        
        Args:
            tool: Tool to add
        """
        self.tools.append(tool)
    
    def remove_tool(self, name: str) -> bool:
        """
        Remove a tool from the collection.
        
        Args:
            name: Name of the tool to remove
            
        Returns:
            True if the tool was removed, False otherwise
        """
        for i, tool in enumerate(self.tools):
            if tool.name.lower() == name.lower():
                self.tools.pop(i)
                return True
        return False
    
    def get_tool_descriptions(self) -> List[Dict[str, Any]]:
        """
        Get descriptions of all tools in the collection.
        
        Returns:
            List of tool descriptions
        """
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters
            }
            for tool in self.tools
        ]
