"""
Base Tool for Enhanced Devin.

This module defines the BaseTool abstract class that all tool implementations
must inherit from. It provides common functionality and interfaces for all tools.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging
import time
import uuid

from pydantic import BaseModel, Field

# Configure logging
logger = logging.getLogger(__name__)


class ToolResult(BaseModel):
    """Result of a tool execution."""
    
    success: bool = Field(description="Whether the tool execution was successful")
    output: Any = Field(description="Output of the tool execution")
    error: Optional[str] = Field(default=None, description="Error message if the execution failed")
    execution_time: float = Field(description="Time taken to execute the tool in seconds")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata about the execution")


class BaseTool(ABC, BaseModel):
    """
    Abstract base class for all tools in the Enhanced Devin system.
    
    This class defines the common interface and functionality that all
    tool implementations must provide.
    """
    
    name: str = Field(description="Name of the tool")
    description: str = Field(description="Description of what the tool does")
    version: str = Field(default="0.1.0", description="Version of the tool")
    author: str = Field(default="Unknown", description="Author of the tool")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Parameters that the tool accepts")
    
    # Internal tracking
    _execution_count: int = 0
    _total_execution_time: float = 0
    _successful_executions: int = 0
    _failed_executions: int = 0
    
    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True
    
    @abstractmethod
    async def _execute(self, **kwargs) -> Any:
        """
        Execute the tool with the provided arguments.
        
        Args:
            **kwargs: Arguments to pass to the tool
            
        Returns:
            The result of executing the tool
        """
        pass
    
    async def run(self, **kwargs) -> ToolResult:
        """
        Run the tool with the provided arguments and track execution metrics.
        
        Args:
            **kwargs: Arguments to pass to the tool
            
        Returns:
            ToolResult containing the execution result and metrics
        """
        # Generate a unique execution ID
        execution_id = str(uuid.uuid4())
        
        # Log the execution start
        logger.info(f"Starting execution of tool '{self.name}' (ID: {execution_id})")
        
        # Track execution metrics
        start_time = time.time()
        self._execution_count += 1
        
        try:
            # Execute the tool
            output = await self._execute(**kwargs)
            
            # Calculate execution time
            execution_time = time.time() - start_time
            self._total_execution_time += execution_time
            self._successful_executions += 1
            
            # Log the execution success
            logger.info(f"Successfully executed tool '{self.name}' in {execution_time:.2f}s (ID: {execution_id})")
            
            # Return the result
            return ToolResult(
                success=True,
                output=output,
                execution_time=execution_time,
                metadata={
                    "execution_id": execution_id,
                    "tool_name": self.name,
                    "tool_version": self.version,
                    "parameters": kwargs
                }
            )
        except Exception as e:
            # Calculate execution time
            execution_time = time.time() - start_time
            self._total_execution_time += execution_time
            self._failed_executions += 1
            
            # Log the execution failure
            error_message = str(e)
            logger.error(f"Failed to execute tool '{self.name}': {error_message} (ID: {execution_id})")
            
            # Return the error
            return ToolResult(
                success=False,
                output=None,
                error=error_message,
                execution_time=execution_time,
                metadata={
                    "execution_id": execution_id,
                    "tool_name": self.name,
                    "tool_version": self.version,
                    "parameters": kwargs
                }
            )
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get execution metrics for the tool.
        
        Returns:
            Dict containing execution metrics
        """
        return {
            "execution_count": self._execution_count,
            "total_execution_time": self._total_execution_time,
            "average_execution_time": self._total_execution_time / self._execution_count if self._execution_count > 0 else 0,
            "successful_executions": self._successful_executions,
            "failed_executions": self._failed_executions,
            "success_rate": self._successful_executions / self._execution_count if self._execution_count > 0 else 0
        }
    
    def reset_metrics(self) -> None:
        """Reset execution metrics for the tool."""
        self._execution_count = 0
        self._total_execution_time = 0
        self._successful_executions = 0
        self._failed_executions = 0
