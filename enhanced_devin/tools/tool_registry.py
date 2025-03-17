"""
Tool Registry for Enhanced Devin.

This module provides a registry for tools that can be used by agents in the
Enhanced Devin system. It supports dynamic tool discovery, versioning, and
dependency management.
"""

import importlib
import inspect
import os
import sys
from typing import Dict, List, Optional, Any, Type, Callable, Set
import logging
from pathlib import Path

from pydantic import BaseModel, Field

# Configure logging
logger = logging.getLogger(__name__)


class ToolMetadata(BaseModel):
    """Metadata for a tool in the registry."""
    
    name: str = Field(description="Name of the tool")
    version: str = Field(description="Version of the tool")
    description: str = Field(description="Description of what the tool does")
    author: str = Field(description="Author of the tool")
    dependencies: List[str] = Field(default_factory=list, description="Dependencies of the tool")
    tags: List[str] = Field(default_factory=list, description="Tags for categorizing the tool")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Parameters that the tool accepts")
    examples: List[Dict[str, Any]] = Field(default_factory=list, description="Examples of using the tool")


class ToolRegistry:
    """
    Registry for tools that can be used by agents.
    
    This registry supports dynamic tool discovery, versioning, and dependency management.
    """
    
    def __init__(self):
        """Initialize the tool registry."""
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.tool_paths: Dict[str, str] = {}
        self.loaded_modules: Set[str] = set()
    
    def register_tool(self, tool_class: Type, metadata: Optional[ToolMetadata] = None) -> None:
        """
        Register a tool with the registry.
        
        Args:
            tool_class: The tool class to register
            metadata: Optional metadata for the tool
        """
        # Get the tool name
        tool_name = getattr(tool_class, "name", tool_class.__name__)
        
        # Create default metadata if not provided
        if metadata is None:
            metadata = ToolMetadata(
                name=tool_name,
                version="0.1.0",
                description=getattr(tool_class, "description", tool_class.__doc__ or ""),
                author="Unknown",
                dependencies=[],
                tags=[],
                parameters=getattr(tool_class, "parameters", {}),
                examples=[]
            )
        
        # Register the tool
        self.tools[tool_name] = {
            "class": tool_class,
            "metadata": metadata
        }
        
        logger.info(f"Registered tool: {tool_name} (v{metadata.version})")
    
    def unregister_tool(self, tool_name: str) -> bool:
        """
        Unregister a tool from the registry.
        
        Args:
            tool_name: Name of the tool to unregister
            
        Returns:
            True if the tool was unregistered, False otherwise
        """
        if tool_name in self.tools:
            del self.tools[tool_name]
            logger.info(f"Unregistered tool: {tool_name}")
            return True
        return False
    
    def get_tool(self, tool_name: str) -> Optional[Type]:
        """
        Get a tool by name.
        
        Args:
            tool_name: Name of the tool to get
            
        Returns:
            The tool class if found, None otherwise
        """
        if tool_name in self.tools:
            return self.tools[tool_name]["class"]
        return None
    
    def get_tool_metadata(self, tool_name: str) -> Optional[ToolMetadata]:
        """
        Get metadata for a tool.
        
        Args:
            tool_name: Name of the tool to get metadata for
            
        Returns:
            The tool metadata if found, None otherwise
        """
        if tool_name in self.tools:
            return self.tools[tool_name]["metadata"]
        return None
    
    def list_tools(self) -> List[str]:
        """
        List all registered tools.
        
        Returns:
            List of tool names
        """
        return list(self.tools.keys())
    
    def get_tools_by_tag(self, tag: str) -> List[str]:
        """
        Get tools by tag.
        
        Args:
            tag: Tag to filter by
            
        Returns:
            List of tool names with the specified tag
        """
        return [
            tool_name
            for tool_name, tool_info in self.tools.items()
            if tag in tool_info["metadata"].tags
        ]
    
    def discover_tools(self, directory: str) -> List[str]:
        """
        Discover tools in a directory.
        
        Args:
            directory: Directory to search for tools
            
        Returns:
            List of discovered tool names
        """
        discovered_tools = []
        
        # Get the absolute path to the directory
        directory_path = Path(directory).resolve()
        
        # Add the directory to the Python path
        if str(directory_path) not in sys.path:
            sys.path.append(str(directory_path))
        
        # Iterate through Python files in the directory
        for file_path in directory_path.glob("**/*.py"):
            # Skip __init__.py files
            if file_path.name == "__init__.py":
                continue
            
            # Get the module name
            module_path = file_path.relative_to(directory_path)
            module_name = str(module_path.with_suffix("")).replace(os.sep, ".")
            
            try:
                # Import the module
                module = importlib.import_module(module_name)
                self.loaded_modules.add(module_name)
                
                # Find tool classes in the module
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and hasattr(obj, "run") and callable(getattr(obj, "run")):
                        # Check if the class has a name attribute
                        if hasattr(obj, "name"):
                            tool_name = obj.name
                        else:
                            tool_name = name
                        
                        # Register the tool
                        self.register_tool(obj)
                        discovered_tools.append(tool_name)
                        
                        # Store the tool path
                        self.tool_paths[tool_name] = str(file_path)
            except Exception as e:
                logger.error(f"Error discovering tools in {module_name}: {str(e)}")
        
        return discovered_tools
    
    def reload_tool(self, tool_name: str) -> bool:
        """
        Reload a tool.
        
        Args:
            tool_name: Name of the tool to reload
            
        Returns:
            True if the tool was reloaded, False otherwise
        """
        if tool_name not in self.tool_paths:
            return False
        
        try:
            # Get the module name
            file_path = Path(self.tool_paths[tool_name])
            directory_path = file_path.parent
            
            # Add the directory to the Python path
            if str(directory_path) not in sys.path:
                sys.path.append(str(directory_path))
            
            # Get the module name
            module_path = file_path.relative_to(directory_path.parent)
            module_name = str(module_path.with_suffix("")).replace(os.sep, ".")
            
            # Reload the module
            module = importlib.import_module(module_name)
            importlib.reload(module)
            
            # Find the tool class in the module
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and hasattr(obj, "run") and callable(getattr(obj, "run")):
                    # Check if this is the tool we're looking for
                    if hasattr(obj, "name") and obj.name == tool_name:
                        # Re-register the tool
                        metadata = self.get_tool_metadata(tool_name)
                        self.register_tool(obj, metadata)
                        return True
            
            return False
        except Exception as e:
            logger.error(f"Error reloading tool {tool_name}: {str(e)}")
            return False
    
    def check_dependencies(self, tool_name: str) -> Dict[str, bool]:
        """
        Check if dependencies for a tool are satisfied.
        
        Args:
            tool_name: Name of the tool to check dependencies for
            
        Returns:
            Dict mapping dependency names to whether they are satisfied
        """
        if tool_name not in self.tools:
            return {}
        
        metadata = self.tools[tool_name]["metadata"]
        dependencies = metadata.dependencies
        
        result = {}
        for dependency in dependencies:
            # Check if the dependency is a Python package
            try:
                importlib.import_module(dependency)
                result[dependency] = True
            except ImportError:
                # Check if the dependency is another tool
                if dependency in self.tools:
                    result[dependency] = True
                else:
                    result[dependency] = False
        
        return result
    
    def create_tool_instance(self, tool_name: str, **kwargs) -> Optional[Any]:
        """
        Create an instance of a tool.
        
        Args:
            tool_name: Name of the tool to create an instance of
            **kwargs: Arguments to pass to the tool constructor
            
        Returns:
            An instance of the tool if successful, None otherwise
        """
        if tool_name not in self.tools:
            return None
        
        tool_class = self.tools[tool_name]["class"]
        
        try:
            return tool_class(**kwargs)
        except Exception as e:
            logger.error(f"Error creating instance of tool {tool_name}: {str(e)}")
            return None
    
    def get_tool_chain(self, tool_names: List[str]) -> List[Any]:
        """
        Create a chain of tool instances.
        
        Args:
            tool_names: Names of the tools to chain
            
        Returns:
            List of tool instances
        """
        chain = []
        
        for tool_name in tool_names:
            tool_instance = self.create_tool_instance(tool_name)
            if tool_instance:
                chain.append(tool_instance)
        
        return chain
