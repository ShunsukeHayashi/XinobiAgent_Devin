"""
Generic Agent implementation for Enhanced Devin.

This module defines the GenericAgent class that implements the Working Backwards
methodology for planning and execution.
"""

from typing import Dict, List, Any, Optional
import time
import asyncio

from enhanced_devin.core.base_agent import BaseAgent, AgentStatus


class GenericAgent(BaseAgent):
    """
    Generic Agent that implements the Working Backwards methodology.
    
    This agent starts with the end goal and works backward to the initial state,
    then executes the plan in forward order.
    """
    
    async def run(self, goal: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run the agent to achieve the specified goal.
        
        Args:
            goal: The goal to achieve
            context: Additional context for the agent
            
        Returns:
            A dictionary containing the results of the agent's execution
        """
        context = context or {}
        self._start_execution()
        
        try:
            # Planning phase
            planning_start = time.time()
            self.status = AgentStatus.PLANNING
            
            # Create plan by working backwards from the goal
            self.current_plan = await self.plan(goal, context)
            
            planning_end = time.time()
            self.performance_metrics["planning_time"] = planning_end - planning_start
            
            # Execution phase
            self.status = AgentStatus.EXECUTING
            
            # Execute each step in the plan
            for step in self.current_plan:
                if self.step_count >= self.max_steps:
                    self._log_error(f"Exceeded maximum number of steps ({self.max_steps})")
                    self._end_execution(AgentStatus.FAILED)
                    break
                
                step_start = time.time()
                try:
                    result = await self.execute_step(step)
                    step_end = time.time()
                    self._track_step(step, result, step_end - step_start)
                    self.execution_results.append(result)
                    
                    # Check if step execution failed
                    if result.get("status") == "failed":
                        self._log_error(f"Step execution failed: {result.get('error', 'Unknown error')}", step)
                        # Attempt recovery if possible
                        if not await self._attempt_recovery(step, result):
                            self._end_execution(AgentStatus.FAILED)
                            break
                except Exception as e:
                    step_end = time.time()
                    error_msg = f"Exception during step execution: {str(e)}"
                    self._log_error(error_msg, step)
                    self._track_step(step, {"status": "failed", "error": error_msg}, step_end - step_start)
                    # Attempt recovery if possible
                    if not await self._attempt_recovery(step, {"status": "failed", "error": error_msg}):
                        self._end_execution(AgentStatus.FAILED)
                        break
            
            # Check if all steps were executed successfully
            if self.status != AgentStatus.FAILED:
                self._end_execution(AgentStatus.COMPLETED)
            
            return {
                "status": self.status.value,
                "goal": goal,
                "steps_executed": self.step_count,
                "total_steps": len(self.current_plan),
                "execution_time": self.performance_metrics["execution_time"],
                "planning_time": self.performance_metrics["planning_time"],
                "results": self.execution_results,
                "errors": self.errors
            }
        
        except Exception as e:
            error_msg = f"Exception during agent execution: {str(e)}"
            self._log_error(error_msg)
            self._end_execution(AgentStatus.FAILED)
            return {
                "status": self.status.value,
                "goal": goal,
                "error": error_msg,
                "steps_executed": self.step_count,
                "execution_time": self.performance_metrics["execution_time"],
                "planning_time": self.performance_metrics.get("planning_time", 0),
                "errors": self.errors
            }
    
    async def plan(self, goal: str, context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Create a plan to achieve the specified goal using Working Backwards methodology.
        
        Args:
            goal: The goal to achieve
            context: Additional context for planning
            
        Returns:
            A list of steps to achieve the goal
        """
        context = context or {}
        
        # Step 1: Define the goal state in concrete detail
        goal_state = await self._define_goal_state(goal, context)
        
        # Step 2: Work backwards from the goal state
        backwards_steps = await self._work_backwards(goal_state, context)
        
        # Step 3: Reverse the steps to create a forward execution plan
        forward_plan = list(reversed(backwards_steps))
        
        # Step 4: Refine the plan
        refined_plan = await self._refine_plan(forward_plan, context)
        
        return refined_plan
    
    async def execute_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a single step in the plan.
        
        Args:
            step: The step to execute
            
        Returns:
            The result of executing the step
        """
        # Check if a tool is specified for this step
        if "tool" in step and step["tool"]:
            tool_name = step["tool"]
            tool = self._get_tool_by_name(tool_name)
            
            if tool:
                # Execute the tool with the step parameters
                try:
                    tool_result = await tool.run(step.get("parameters", {}))
                    return {
                        "status": "success",
                        "tool": tool_name,
                        "result": tool_result
                    }
                except Exception as e:
                    return {
                        "status": "failed",
                        "tool": tool_name,
                        "error": str(e)
                    }
            else:
                return {
                    "status": "failed",
                    "error": f"Tool '{tool_name}' not found"
                }
        
        # If no tool is specified, this is a reasoning step
        return {
            "status": "success",
            "type": "reasoning",
            "description": step.get("description", ""),
            "result": step.get("expected_outcome", "")
        }
    
    async def _define_goal_state(self, goal: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Define the goal state in concrete detail.
        
        Args:
            goal: The goal to achieve
            context: Additional context
            
        Returns:
            A dictionary describing the goal state
        """
        # In a real implementation, this would use an LLM to define the goal state
        # For now, we'll just create a simple representation
        return {
            "description": goal,
            "criteria": [
                f"The goal '{goal}' has been achieved",
                "All required steps have been completed successfully",
                "No errors have occurred during execution"
            ],
            "context": context
        }
    
    async def _work_backwards(self, goal_state: Dict[str, Any], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Work backwards from the goal state to the initial state.
        
        Args:
            goal_state: The goal state
            context: Additional context
            
        Returns:
            A list of steps in reverse order (from goal to initial state)
        """
        # In a real implementation, this would use an LLM to work backwards
        # For now, we'll just create a simple example
        
        # Start with the goal state
        current_state = goal_state
        backwards_steps = []
        
        # Simulate working backwards with 5 steps
        for i in range(5):
            # Create a step that would lead to the current state
            step = {
                "id": f"step_{5-i}",
                "description": f"Step that leads to: {current_state['description']}",
                "expected_outcome": f"Progress towards {goal_state['description']}",
                "tool": f"tool_{i}" if i < len(self.available_tools) else None,
                "parameters": {"param1": f"value{i}", "param2": f"value{i+1}"}
            }
            
            backwards_steps.append(step)
            
            # Update the current state to be the state before this step
            current_state = {
                "description": f"State before step {5-i}",
                "criteria": [f"Criterion {j}" for j in range(3)]
            }
        
        return backwards_steps
    
    async def _refine_plan(self, plan: List[Dict[str, Any]], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Refine the plan to ensure it's executable and optimal.
        
        Args:
            plan: The initial plan
            context: Additional context
            
        Returns:
            The refined plan
        """
        # In a real implementation, this would use an LLM to refine the plan
        # For now, we'll just return the original plan
        return plan
    
    async def _attempt_recovery(self, failed_step: Dict[str, Any], failure_result: Dict[str, Any]) -> bool:
        """
        Attempt to recover from a failed step.
        
        Args:
            failed_step: The step that failed
            failure_result: The result of the failed step
            
        Returns:
            True if recovery was successful, False otherwise
        """
        # In a real implementation, this would use an LLM to attempt recovery
        # For now, we'll just return False to indicate recovery failed
        return False
    
    def _get_tool_by_name(self, tool_name: str) -> Any:
        """
        Get a tool by name from the available tools.
        
        Args:
            tool_name: The name of the tool
            
        Returns:
            The tool if found, None otherwise
        """
        for tool in self.available_tools:
            if tool.name == tool_name:
                return tool
        return None
