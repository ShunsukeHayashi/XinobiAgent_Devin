"""
Debug Tracer for Enhanced Devin.

This module provides tracing capabilities for debugging in the Enhanced Devin system.
It allows for step-by-step execution tracing, state inspection, and breakpoints.
"""

import inspect
import sys
import traceback
import time
import logging
import asyncio
from typing import Dict, List, Any, Optional, Union, Callable, Set
import json
from datetime import datetime

from pydantic import BaseModel, Field

# Configure logging
logger = logging.getLogger(__name__)


class TraceEvent(BaseModel):
    """Model for a trace event."""
    
    id: str = Field(description="Unique ID for the event")
    type: str = Field(description="Type of event (call, return, exception, line)")
    timestamp: float = Field(description="Timestamp of the event")
    function: str = Field(description="Function name")
    module: str = Field(description="Module name")
    filename: str = Field(description="Filename")
    lineno: int = Field(description="Line number")
    locals: Optional[Dict[str, str]] = Field(default=None, description="Local variables")
    args: Optional[Dict[str, str]] = Field(default=None, description="Function arguments")
    retval: Optional[str] = Field(default=None, description="Return value")
    exception: Optional[str] = Field(default=None, description="Exception information")
    duration: Optional[float] = Field(default=None, description="Duration of the function call")


class Breakpoint(BaseModel):
    """Model for a breakpoint."""
    
    id: str = Field(description="Unique ID for the breakpoint")
    filename: str = Field(description="Filename")
    lineno: int = Field(description="Line number")
    condition: Optional[str] = Field(default=None, description="Condition for the breakpoint")
    enabled: bool = Field(default=True, description="Whether the breakpoint is enabled")
    hit_count: int = Field(default=0, description="Number of times the breakpoint has been hit")


class DebugTracer:
    """
    Tracer for debugging.
    
    This class provides tracing capabilities for debugging, including step-by-step
    execution tracing, state inspection, and breakpoints.
    """
    
    def __init__(self, max_events: int = 1000, include_locals: bool = True):
        """
        Initialize the debug tracer.
        
        Args:
            max_events: Maximum number of events to keep in history
            include_locals: Whether to include local variables in trace events
        """
        self.max_events = max_events
        self.include_locals = include_locals
        
        # Trace events
        self.events: List[TraceEvent] = []
        
        # Breakpoints
        self.breakpoints: Dict[str, Breakpoint] = {}
        
        # Call stack
        self.call_stack: List[Dict[str, Any]] = []
        
        # Filters
        self.include_modules: Set[str] = set()
        self.exclude_modules: Set[str] = set()
        
        # Tracing state
        self.is_tracing = False
        self.trace_id = 0
        self.start_time = None
        
        # Async support
        self._trace_future = None
        self._stop_tracing = asyncio.Event()
    
    def start_tracing(self, include_modules: Optional[List[str]] = None, exclude_modules: Optional[List[str]] = None) -> None:
        """
        Start tracing.
        
        Args:
            include_modules: Optional list of modules to include
            exclude_modules: Optional list of modules to exclude
        """
        if self.is_tracing:
            logger.warning("Tracing is already active")
            return
        
        # Set filters
        if include_modules:
            self.include_modules = set(include_modules)
        if exclude_modules:
            self.exclude_modules = set(exclude_modules)
        
        # Clear events
        self.events = []
        self.call_stack = []
        
        # Set tracing state
        self.is_tracing = True
        self.start_time = time.time()
        
        # Set the trace function
        sys.settrace(self._trace_function)
        
        logger.info("Started tracing")
    
    def stop_tracing(self) -> None:
        """Stop tracing."""
        if not self.is_tracing:
            logger.warning("Tracing is not active")
            return
        
        # Unset the trace function
        sys.settrace(None)
        
        # Set tracing state
        self.is_tracing = False
        
        logger.info(f"Stopped tracing. Collected {len(self.events)} events.")
    
    async def start_async_tracing(self, include_modules: Optional[List[str]] = None, exclude_modules: Optional[List[str]] = None) -> None:
        """
        Start tracing asynchronously.
        
        Args:
            include_modules: Optional list of modules to include
            exclude_modules: Optional list of modules to exclude
        """
        if self._trace_future is not None:
            logger.warning("Async tracing is already active")
            return
        
        # Start tracing
        self.start_tracing(include_modules, exclude_modules)
        
        # Create the trace future
        self._stop_tracing.clear()
        self._trace_future = asyncio.create_task(self._async_trace_task())
        
        logger.info("Started async tracing")
    
    async def stop_async_tracing(self) -> None:
        """Stop tracing asynchronously."""
        if self._trace_future is None:
            logger.warning("Async tracing is not active")
            return
        
        # Stop the trace task
        self._stop_tracing.set()
        await self._trace_future
        self._trace_future = None
        
        # Stop tracing
        self.stop_tracing()
        
        logger.info("Stopped async tracing")
    
    async def _async_trace_task(self) -> None:
        """Async trace task."""
        while not self._stop_tracing.is_set():
            # Wait for a short time
            try:
                await asyncio.wait_for(self._stop_tracing.wait(), timeout=0.1)
            except asyncio.TimeoutError:
                pass
    
    def _trace_function(self, frame, event, arg) -> Optional[Callable]:
        """
        Trace function for sys.settrace.
        
        Args:
            frame: The current frame
            event: The trace event
            arg: Additional argument
            
        Returns:
            The trace function or None
        """
        # Check if we should trace this frame
        if not self._should_trace_frame(frame):
            return None
        
        # Get frame information
        code = frame.f_code
        function_name = code.co_name
        filename = code.co_filename
        lineno = frame.f_lineno
        module_name = self._get_module_name(frame)
        
        # Handle different events
        if event == 'call':
            # Add to call stack
            call_info = {
                'function': function_name,
                'module': module_name,
                'filename': filename,
                'lineno': lineno,
                'start_time': time.time()
            }
            self.call_stack.append(call_info)
            
            # Create trace event
            trace_id = self._get_next_trace_id()
            trace_event = TraceEvent(
                id=trace_id,
                type='call',
                timestamp=time.time(),
                function=function_name,
                module=module_name,
                filename=filename,
                lineno=lineno,
                args=self._get_args(frame) if self.include_locals else None
            )
            
            # Add to events
            self._add_event(trace_event)
            
            # Check for breakpoints
            self._check_breakpoints(frame)
            
            # Return the trace function for this frame
            return self._trace_function
        
        elif event == 'return':
            # Get call info from stack
            call_info = self.call_stack.pop() if self.call_stack else None
            
            # Calculate duration
            duration = time.time() - call_info['start_time'] if call_info else None
            
            # Create trace event
            trace_id = self._get_next_trace_id()
            trace_event = TraceEvent(
                id=trace_id,
                type='return',
                timestamp=time.time(),
                function=function_name,
                module=module_name,
                filename=filename,
                lineno=lineno,
                retval=self._format_value(arg) if self.include_locals else None,
                duration=duration
            )
            
            # Add to events
            self._add_event(trace_event)
        
        elif event == 'exception':
            # Get exception info
            exc_type, exc_value, exc_traceback = arg
            
            # Create trace event
            trace_id = self._get_next_trace_id()
            trace_event = TraceEvent(
                id=trace_id,
                type='exception',
                timestamp=time.time(),
                function=function_name,
                module=module_name,
                filename=filename,
                lineno=lineno,
                exception=f"{exc_type.__name__}: {str(exc_value)}",
                locals=self._get_locals(frame) if self.include_locals else None
            )
            
            # Add to events
            self._add_event(trace_event)
        
        elif event == 'line':
            # Create trace event
            trace_id = self._get_next_trace_id()
            trace_event = TraceEvent(
                id=trace_id,
                type='line',
                timestamp=time.time(),
                function=function_name,
                module=module_name,
                filename=filename,
                lineno=lineno,
                locals=self._get_locals(frame) if self.include_locals else None
            )
            
            # Add to events
            self._add_event(trace_event)
            
            # Check for breakpoints
            self._check_breakpoints(frame)
        
        # Return the trace function for this frame
        return self._trace_function
    
    def _should_trace_frame(self, frame) -> bool:
        """
        Check if a frame should be traced.
        
        Args:
            frame: The frame to check
            
        Returns:
            True if the frame should be traced, False otherwise
        """
        # Get module name
        module_name = self._get_module_name(frame)
        
        # Check if this is our own module
        if module_name.startswith('enhanced_devin.monitoring.debug_tracer'):
            return False
        
        # Check include/exclude filters
        if self.include_modules and module_name not in self.include_modules:
            return False
        if self.exclude_modules and module_name in self.exclude_modules:
            return False
        
        return True
    
    def _get_module_name(self, frame) -> str:
        """
        Get the module name for a frame.
        
        Args:
            frame: The frame to get the module name for
            
        Returns:
            The module name
        """
        module = inspect.getmodule(frame)
        if module:
            return module.__name__
        return 'unknown'
    
    def _get_args(self, frame) -> Dict[str, str]:
        """
        Get function arguments for a frame.
        
        Args:
            frame: The frame to get arguments for
            
        Returns:
            Dict mapping argument names to formatted values
        """
        args = {}
        
        # Get argument names
        code = frame.f_code
        arg_names = code.co_varnames[:code.co_argcount]
        
        # Get argument values
        for name in arg_names:
            if name in frame.f_locals:
                args[name] = self._format_value(frame.f_locals[name])
        
        return args
    
    def _get_locals(self, frame) -> Dict[str, str]:
        """
        Get local variables for a frame.
        
        Args:
            frame: The frame to get locals for
            
        Returns:
            Dict mapping variable names to formatted values
        """
        locals_dict = {}
        
        # Get local variables
        for name, value in frame.f_locals.items():
            # Skip special variables
            if name.startswith('__') and name.endswith('__'):
                continue
            
            # Format the value
            locals_dict[name] = self._format_value(value)
        
        return locals_dict
    
    def _format_value(self, value) -> str:
        """
        Format a value for display.
        
        Args:
            value: The value to format
            
        Returns:
            Formatted value as a string
        """
        try:
            # Limit string length
            result = repr(value)
            if len(result) > 100:
                result = result[:97] + '...'
            return result
        except Exception:
            return '<error formatting value>'
    
    def _get_next_trace_id(self) -> str:
        """
        Get the next trace ID.
        
        Returns:
            The next trace ID
        """
        self.trace_id += 1
        return f"trace_{self.trace_id}"
    
    def _add_event(self, event: TraceEvent) -> None:
        """
        Add an event to the history.
        
        Args:
            event: The event to add
        """
        self.events.append(event)
        
        # Trim history if needed
        if len(self.events) > self.max_events:
            self.events = self.events[-self.max_events:]
    
    def add_breakpoint(self, filename: str, lineno: int, condition: Optional[str] = None) -> str:
        """
        Add a breakpoint.
        
        Args:
            filename: Filename for the breakpoint
            lineno: Line number for the breakpoint
            condition: Optional condition for the breakpoint
            
        Returns:
            ID of the breakpoint
        """
        # Create the breakpoint
        breakpoint_id = f"bp_{len(self.breakpoints) + 1}"
        breakpoint = Breakpoint(
            id=breakpoint_id,
            filename=filename,
            lineno=lineno,
            condition=condition,
            enabled=True,
            hit_count=0
        )
        
        # Add to breakpoints
        self.breakpoints[breakpoint_id] = breakpoint
        
        logger.info(f"Added breakpoint {breakpoint_id} at {filename}:{lineno}")
        
        return breakpoint_id
    
    def remove_breakpoint(self, breakpoint_id: str) -> bool:
        """
        Remove a breakpoint.
        
        Args:
            breakpoint_id: ID of the breakpoint to remove
            
        Returns:
            True if the breakpoint was removed, False otherwise
        """
        if breakpoint_id in self.breakpoints:
            del self.breakpoints[breakpoint_id]
            logger.info(f"Removed breakpoint {breakpoint_id}")
            return True
        
        logger.warning(f"Breakpoint {breakpoint_id} not found")
        return False
    
    def enable_breakpoint(self, breakpoint_id: str) -> bool:
        """
        Enable a breakpoint.
        
        Args:
            breakpoint_id: ID of the breakpoint to enable
            
        Returns:
            True if the breakpoint was enabled, False otherwise
        """
        if breakpoint_id in self.breakpoints:
            self.breakpoints[breakpoint_id].enabled = True
            logger.info(f"Enabled breakpoint {breakpoint_id}")
            return True
        
        logger.warning(f"Breakpoint {breakpoint_id} not found")
        return False
    
    def disable_breakpoint(self, breakpoint_id: str) -> bool:
        """
        Disable a breakpoint.
        
        Args:
            breakpoint_id: ID of the breakpoint to disable
            
        Returns:
            True if the breakpoint was disabled, False otherwise
        """
        if breakpoint_id in self.breakpoints:
            self.breakpoints[breakpoint_id].enabled = False
            logger.info(f"Disabled breakpoint {breakpoint_id}")
            return True
        
        logger.warning(f"Breakpoint {breakpoint_id} not found")
        return False
    
    def _check_breakpoints(self, frame) -> None:
        """
        Check if any breakpoints are hit.
        
        Args:
            frame: The current frame
        """
        # Get frame information
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno
        
        # Check each breakpoint
        for bp_id, bp in self.breakpoints.items():
            if not bp.enabled:
                continue
            
            if bp.filename == filename and bp.lineno == lineno:
                # Check condition if present
                if bp.condition:
                    try:
                        # Evaluate the condition in the frame's context
                        condition_result = eval(bp.condition, frame.f_globals, frame.f_locals)
                        if not condition_result:
                            continue
                    except Exception as e:
                        logger.error(f"Error evaluating breakpoint condition: {str(e)}")
                        continue
                
                # Increment hit count
                bp.hit_count += 1
                
                # Log the breakpoint hit
                logger.info(f"Hit breakpoint {bp_id} at {filename}:{lineno} (hit count: {bp.hit_count})")
                
                # You could add custom breakpoint handling here
                # For example, pause execution, notify a debugger, etc.
    
    def get_events(self, event_type: Optional[str] = None, function: Optional[str] = None, 
                  module: Optional[str] = None, limit: Optional[int] = None) -> List[TraceEvent]:
        """
        Get trace events.
        
        Args:
            event_type: Optional type of events to get
            function: Optional function name to filter by
            module: Optional module name to filter by
            limit: Optional maximum number of events to return
            
        Returns:
            List of trace events
        """
        # Filter events
        filtered_events = self.events
        
        if event_type:
            filtered_events = [e for e in filtered_events if e.type == event_type]
        
        if function:
            filtered_events = [e for e in filtered_events if e.function == function]
        
        if module:
            filtered_events = [e for e in filtered_events if e.module == module]
        
        # Apply limit
        if limit:
            filtered_events = filtered_events[-limit:]
        
        return filtered_events
    
    def get_call_tree(self) -> Dict[str, Any]:
        """
        Get a call tree from the trace events.
        
        Returns:
            Dict representing the call tree
        """
        # Build the call tree from call and return events
        root = {"name": "root", "children": []}
        stack = [root]
        
        for event in self.events:
            if event.type == "call":
                # Create a new node
                node = {
                    "name": event.function,
                    "module": event.module,
                    "filename": event.filename,
                    "lineno": event.lineno,
                    "timestamp": event.timestamp,
                    "children": []
                }
                
                # Add to the current parent
                stack[-1]["children"].append(node)
                
                # Push to the stack
                stack.append(node)
            
            elif event.type == "return":
                # Add return information to the current node
                if len(stack) > 1:  # Ensure we don't pop the root
                    node = stack[-1]
                    node["return_value"] = event.retval
                    node["duration"] = event.duration
                    
                    # Pop from the stack
                    stack.pop()
        
        return root
    
    def export_events(self, format: str = "json") -> str:
        """
        Export events to a specific format.
        
        Args:
            format: Format to export to (json, csv)
            
        Returns:
            Exported events as a string
        """
        if format == "json":
            return json.dumps([event.dict() for event in self.events], indent=2)
        elif format == "csv":
            # Create CSV header
            csv = "id,type,timestamp,function,module,filename,lineno,duration\n"
            
            # Add events
            for event in self.events:
                timestamp = datetime.fromtimestamp(event.timestamp).isoformat()
                duration = event.duration if event.duration else ""
                
                csv += f"{event.id},{event.type},{timestamp},{event.function},{event.module},{event.filename},{event.lineno},{duration}\n"
            
            return csv
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def reset(self) -> None:
        """Reset the tracer."""
        self.events = []
        self.breakpoints = {}
        self.call_stack = []
        self.trace_id = 0
