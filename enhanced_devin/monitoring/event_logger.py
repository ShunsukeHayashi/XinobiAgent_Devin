"""
Event Logger for Enhanced Devin.

This module provides logging capabilities for events in the Enhanced Devin system.
It supports structured logging, filtering, aggregation, and visualization.
"""

import logging
import json
import time
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import os
import asyncio

from pydantic import BaseModel, Field

# Configure logging
logger = logging.getLogger(__name__)


class LogEvent(BaseModel):
    """Model for a log event."""
    
    id: str = Field(description="Unique ID for the event")
    timestamp: float = Field(description="Timestamp of the event")
    level: str = Field(description="Log level (debug, info, warning, error, critical)")
    source: str = Field(description="Source of the event")
    message: str = Field(description="Event message")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Additional event data")
    tags: List[str] = Field(default_factory=list, description="Tags for the event")


class EventLogger:
    """
    Logger for events in the Enhanced Devin system.
    
    This class provides logging capabilities for events, including structured
    logging, filtering, aggregation, and visualization.
    """
    
    def __init__(self, log_file: Optional[str] = None, max_events: int = 1000, 
                min_level: str = "info"):
        """
        Initialize the event logger.
        
        Args:
            log_file: Optional file to write logs to
            max_events: Maximum number of events to keep in memory
            min_level: Minimum log level to record
        """
        self.log_file = log_file
        self.max_events = max_events
        self.min_level = min_level.lower()
        
        # Event history
        self.events: List[LogEvent] = []
        
        # Event counts by level
        self.event_counts = {
            "debug": 0,
            "info": 0,
            "warning": 0,
            "error": 0,
            "critical": 0
        }
        
        # Event ID counter
        self.event_id = 0
        
        # Level mapping
        self.level_values = {
            "debug": 10,
            "info": 20,
            "warning": 30,
            "error": 40,
            "critical": 50
        }
        
        # Set up file logging if requested
        if log_file:
            self._setup_file_logging()
    
    def _setup_file_logging(self) -> None:
        """Set up file logging."""
        # Create the directory if it doesn't exist
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Set up file handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        # Add the handler to the logger
        logger.addHandler(file_handler)
    
    def log(self, level: str, message: str, source: str, data: Optional[Dict[str, Any]] = None, 
           tags: Optional[List[str]] = None) -> Optional[LogEvent]:
        """
        Log an event.
        
        Args:
            level: Log level (debug, info, warning, error, critical)
            message: Event message
            source: Source of the event
            data: Additional event data
            tags: Tags for the event
            
        Returns:
            The logged event, or None if the level is below the minimum
        """
        # Normalize level
        level = level.lower()
        
        # Check if the level is valid
        if level not in self.level_values:
            logger.warning(f"Invalid log level: {level}")
            level = "info"
        
        # Check if the level is high enough
        if self.level_values[level] < self.level_values[self.min_level]:
            return None
        
        # Create the event
        self.event_id += 1
        event = LogEvent(
            id=f"event_{self.event_id}",
            timestamp=time.time(),
            level=level,
            source=source,
            message=message,
            data=data,
            tags=tags or []
        )
        
        # Add to history
        self.events.append(event)
        
        # Update counts
        self.event_counts[level] += 1
        
        # Trim history if needed
        if len(self.events) > self.max_events:
            self.events = self.events[-self.max_events:]
        
        # Log to file if configured
        if self.log_file:
            log_func = getattr(logger, level)
            log_func(f"[{source}] {message}")
        
        return event
    
    def debug(self, message: str, source: str, data: Optional[Dict[str, Any]] = None, 
             tags: Optional[List[str]] = None) -> Optional[LogEvent]:
        """
        Log a debug event.
        
        Args:
            message: Event message
            source: Source of the event
            data: Additional event data
            tags: Tags for the event
            
        Returns:
            The logged event, or None if the level is below the minimum
        """
        return self.log("debug", message, source, data, tags)
    
    def info(self, message: str, source: str, data: Optional[Dict[str, Any]] = None, 
            tags: Optional[List[str]] = None) -> Optional[LogEvent]:
        """
        Log an info event.
        
        Args:
            message: Event message
            source: Source of the event
            data: Additional event data
            tags: Tags for the event
            
        Returns:
            The logged event, or None if the level is below the minimum
        """
        return self.log("info", message, source, data, tags)
    
    def warning(self, message: str, source: str, data: Optional[Dict[str, Any]] = None, 
               tags: Optional[List[str]] = None) -> Optional[LogEvent]:
        """
        Log a warning event.
        
        Args:
            message: Event message
            source: Source of the event
            data: Additional event data
            tags: Tags for the event
            
        Returns:
            The logged event, or None if the level is below the minimum
        """
        return self.log("warning", message, source, data, tags)
    
    def error(self, message: str, source: str, data: Optional[Dict[str, Any]] = None, 
             tags: Optional[List[str]] = None) -> Optional[LogEvent]:
        """
        Log an error event.
        
        Args:
            message: Event message
            source: Source of the event
            data: Additional event data
            tags: Tags for the event
            
        Returns:
            The logged event, or None if the level is below the minimum
        """
        return self.log("error", message, source, data, tags)
    
    def critical(self, message: str, source: str, data: Optional[Dict[str, Any]] = None, 
                tags: Optional[List[str]] = None) -> Optional[LogEvent]:
        """
        Log a critical event.
        
        Args:
            message: Event message
            source: Source of the event
            data: Additional event data
            tags: Tags for the event
            
        Returns:
            The logged event, or None if the level is below the minimum
        """
        return self.log("critical", message, source, data, tags)
    
    def get_events(self, level: Optional[str] = None, source: Optional[str] = None, 
                  tags: Optional[List[str]] = None, start_time: Optional[float] = None, 
                  end_time: Optional[float] = None, limit: Optional[int] = None) -> List[LogEvent]:
        """
        Get events with optional filtering.
        
        Args:
            level: Optional level to filter by
            source: Optional source to filter by
            tags: Optional tags to filter by (events must have all tags)
            start_time: Optional start time for filtering
            end_time: Optional end time for filtering
            limit: Optional maximum number of events to return
            
        Returns:
            List of filtered events
        """
        # Start with all events
        filtered_events = self.events
        
        # Apply filters
        if level:
            level = level.lower()
            filtered_events = [e for e in filtered_events if e.level == level]
        
        if source:
            filtered_events = [e for e in filtered_events if e.source == source]
        
        if tags:
            filtered_events = [e for e in filtered_events if all(tag in e.tags for tag in tags)]
        
        if start_time:
            filtered_events = [e for e in filtered_events if e.timestamp >= start_time]
        
        if end_time:
            filtered_events = [e for e in filtered_events if e.timestamp <= end_time]
        
        # Apply limit
        if limit:
            filtered_events = filtered_events[-limit:]
        
        return filtered_events
    
    def get_event_counts(self) -> Dict[str, int]:
        """
        Get event counts by level.
        
        Returns:
            Dict mapping levels to counts
        """
        return self.event_counts
    
    def get_source_counts(self) -> Dict[str, int]:
        """
        Get event counts by source.
        
        Returns:
            Dict mapping sources to counts
        """
        source_counts = {}
        
        for event in self.events:
            source = event.source
            if source in source_counts:
                source_counts[source] += 1
            else:
                source_counts[source] = 1
        
        return source_counts
    
    def get_tag_counts(self) -> Dict[str, int]:
        """
        Get event counts by tag.
        
        Returns:
            Dict mapping tags to counts
        """
        tag_counts = {}
        
        for event in self.events:
            for tag in event.tags:
                if tag in tag_counts:
                    tag_counts[tag] += 1
                else:
                    tag_counts[tag] = 1
        
        return tag_counts
    
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
            csv = "id,timestamp,level,source,message,tags\n"
            
            # Add events
            for event in self.events:
                timestamp = datetime.fromtimestamp(event.timestamp).isoformat()
                tags = "|".join(event.tags)
                message = event.message.replace(",", ";").replace("\n", " ")
                
                csv += f"{event.id},{timestamp},{event.level},{event.source},{message},{tags}\n"
            
            return csv
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def reset(self) -> None:
        """Reset the logger."""
        self.events = []
        self.event_counts = {
            "debug": 0,
            "info": 0,
            "warning": 0,
            "error": 0,
            "critical": 0
        }
        self.event_id = 0
