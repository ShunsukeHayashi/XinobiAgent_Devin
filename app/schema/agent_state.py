"""
Agent state schema for tracking agent status.
"""

from typing import Dict, List, Optional, Any, Literal
from pydantic import BaseModel, Field


class AgentState(BaseModel):
    """
    The state of an agent in the system.
    
    This tracks the agent's status, assigned tasks, and progress.
    """
    
    agent_id: str = Field(
        description="Unique identifier for the agent"
    )
    status: Literal["ready", "in_progress", "completed", "error"] = Field(
        default="ready",
        description="Current status of the agent"
    )
    assigned_tasks: List[str] = Field(
        default_factory=list,
        description="IDs of tasks assigned to this agent"
    )
    current_task: Optional[str] = Field(
        default=None,
        description="ID of the task currently being worked on"
    )
    progress: float = Field(
        default=0.0,
        description="Progress percentage (0.0 to 1.0)"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata about the agent"
    )
