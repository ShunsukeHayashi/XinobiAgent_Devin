"""
Base Agent implementation for Enhanced Devin.

This module defines the BaseAgent abstract class that all agent implementations
must inherit from. It provides common functionality and interfaces for all agents.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from enum import Enum
import time
import uuid


class AgentStatus(Enum):
    """Status of an agent."""
    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the Enhanced Devin system.
    
    This class defines the common interface and functionality that all
    agent implementations must provide.
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        available_tools: Optional[List[Any]] = None,
        max_steps: int = 10,
        debug_mode: bool = False
    ):
        """
        Initialize a new BaseAgent.
        
        Args:
            name: The name of the agent
            description: A description of the agent's purpose and capabilities
            available_tools: A list of tools available to the agent
            max_steps: Maximum number of steps the agent can take
            debug_mode: Whether to enable debug mode
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.available_tools = available_tools or []
        self.max_steps = max_steps
        self.debug_mode = debug_mode
        
        # State tracking
        self.status = AgentStatus.IDLE
        self.step_count = 0
        self.start_time = None
        self.end_time = None
        self.steps_history = []
        self.current_plan = []
        self.execution_results = []
        self.errors = []
        
        # Monitoring
        self.performance_metrics = {
            "planning_time": 0,
            "execution_time": 0,
            "tool_usage": {},
            "step_durations": []
        }
    
    @abstractmethod
    async def run(self, goal: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run the agent to achieve the specified goal.
        
        Args:
            goal: The goal to achieve
            context: Additional context for the agent
            
        Returns:
            A dictionary containing the results of the agent's execution
        """
        pass
    
    @abstractmethod
    async def plan(self, goal: str, context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Create a plan to achieve the specified goal.
        
        Args:
            goal: The goal to achieve
            context: Additional context for planning
            
        Returns:
            A list of steps to achieve the goal
        """
        pass
    
    @abstractmethod
    async def execute_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a single step in the plan.
        
        Args:
            step: The step to execute
            
        Returns:
            The result of executing the step
        """
        pass
    
    async def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the agent.
        
        Returns:
            A dictionary containing the agent's current status
        """
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status.value,
            "step_count": self.step_count,
            "max_steps": self.max_steps,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": (self.end_time - self.start_time) if self.end_time and self.start_time else None,
            "errors": self.errors
        }
    
    async def get_execution_history(self) -> List[Dict[str, Any]]:
        """
        Get the execution history of the agent.
        
        Returns:
            A list of steps executed by the agent
        """
        return self.steps_history
    
    async def get_performance_metrics(self) -> Dict[str, Any]:
        """
        Get performance metrics for the agent's execution.
        
        Returns:
            A dictionary containing performance metrics
        """
        return self.performance_metrics
    
    def _start_execution(self):
        """Start execution and initialize tracking."""
        self.start_time = time.time()
        self.status = AgentStatus.EXECUTING
        self.step_count = 0
        self.steps_history = []
        self.execution_results = []
        self.errors = []
    
    def _end_execution(self, status: AgentStatus = AgentStatus.COMPLETED):
        """End execution and finalize tracking."""
        self.end_time = time.time()
        self.status = status
        self.performance_metrics["execution_time"] = self.end_time - self.start_time
    
    def _track_step(self, step: Dict[str, Any], result: Dict[str, Any], duration: float):
        """Track a step execution."""
        self.step_count += 1
        self.steps_history.append({
            "step": step,
            "result": result,
            "duration": duration
        })
        self.performance_metrics["step_durations"].append(duration)
        
        # Track tool usage
        if "tool" in step and step["tool"]:
            tool_name = step["tool"]
            if tool_name in self.performance_metrics["tool_usage"]:
                self.performance_metrics["tool_usage"][tool_name] += 1
            else:
                self.performance_metrics["tool_usage"][tool_name] = 1
    
    def _log_error(self, error: str, step: Optional[Dict[str, Any]] = None):
        """Log an error during execution."""
        error_entry = {
            "timestamp": time.time(),
            "error": error,
            "step": step
        }
        self.errors.append(error_entry)
        if self.debug_mode:
            print(f"ERROR: {error}")
