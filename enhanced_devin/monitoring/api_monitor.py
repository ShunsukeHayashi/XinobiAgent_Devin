"""
API Monitor for Enhanced Devin.

This module provides monitoring capabilities for API interactions in the
Enhanced Devin system. It tracks API requests, responses, and performance metrics.
"""

import time
import json
import logging
from typing import Dict, List, Any, Optional, Union
import asyncio
from datetime import datetime

from pydantic import BaseModel, Field

# Configure logging
logger = logging.getLogger(__name__)


class APIRequest(BaseModel):
    """Model for an API request."""
    
    id: str = Field(description="Unique ID for the request")
    method: str = Field(description="HTTP method")
    url: str = Field(description="URL of the request")
    headers: Dict[str, str] = Field(description="Headers of the request")
    params: Optional[Dict[str, Any]] = Field(default=None, description="Query parameters")
    body: Optional[Any] = Field(default=None, description="Request body")
    timestamp: float = Field(description="Timestamp of the request")


class APIResponse(BaseModel):
    """Model for an API response."""
    
    request_id: str = Field(description="ID of the corresponding request")
    status_code: int = Field(description="HTTP status code")
    headers: Dict[str, str] = Field(description="Headers of the response")
    body: Optional[Any] = Field(default=None, description="Response body")
    timestamp: float = Field(description="Timestamp of the response")
    duration: float = Field(description="Duration of the request in seconds")


class APIEvent(BaseModel):
    """Model for an API event (request and response pair)."""
    
    request: APIRequest = Field(description="The API request")
    response: Optional[APIResponse] = Field(default=None, description="The API response")
    duration: Optional[float] = Field(default=None, description="Duration of the request in seconds")
    error: Optional[str] = Field(default=None, description="Error message if the request failed")


class APIMonitor:
    """
    Monitor for API interactions.
    
    This class provides monitoring capabilities for API interactions, including
    tracking requests, responses, and performance metrics.
    """
    
    def __init__(self, max_history: int = 100):
        """
        Initialize the API monitor.
        
        Args:
            max_history: Maximum number of events to keep in history
        """
        self.events: List[APIEvent] = []
        self.max_history = max_history
        self.start_time = time.time()
        
        # Performance metrics
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.total_duration = 0
        
        # Endpoint metrics
        self.endpoint_metrics: Dict[str, Dict[str, Any]] = {}
    
    def track_request(self, request_id: str, method: str, url: str, headers: Dict[str, str],
                     params: Optional[Dict[str, Any]] = None, body: Optional[Any] = None) -> APIRequest:
        """
        Track an API request.
        
        Args:
            request_id: Unique ID for the request
            method: HTTP method
            url: URL of the request
            headers: Headers of the request
            params: Query parameters
            body: Request body
            
        Returns:
            The tracked request
        """
        # Create the request object
        request = APIRequest(
            id=request_id,
            method=method,
            url=url,
            headers=self._sanitize_headers(headers),
            params=params,
            body=body,
            timestamp=time.time()
        )
        
        # Create the event
        event = APIEvent(request=request)
        
        # Add the event to the history
        self._add_event(event)
        
        # Update metrics
        self.total_requests += 1
        
        # Update endpoint metrics
        endpoint = self._get_endpoint_from_url(url)
        if endpoint not in self.endpoint_metrics:
            self.endpoint_metrics[endpoint] = {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "total_duration": 0,
                "average_duration": 0
            }
        self.endpoint_metrics[endpoint]["total_requests"] += 1
        
        return request
    
    def track_response(self, request_id: str, status_code: int, headers: Dict[str, str],
                      body: Optional[Any] = None) -> Optional[APIResponse]:
        """
        Track an API response.
        
        Args:
            request_id: ID of the corresponding request
            status_code: HTTP status code
            headers: Headers of the response
            body: Response body
            
        Returns:
            The tracked response, or None if the request was not found
        """
        # Find the event for the request
        event = self._find_event_by_request_id(request_id)
        if not event:
            logger.warning(f"Request with ID {request_id} not found")
            return None
        
        # Calculate the duration
        duration = time.time() - event.request.timestamp
        
        # Create the response object
        response = APIResponse(
            request_id=request_id,
            status_code=status_code,
            headers=self._sanitize_headers(headers),
            body=body,
            timestamp=time.time(),
            duration=duration
        )
        
        # Update the event
        event.response = response
        event.duration = duration
        
        # Update metrics
        self.total_duration += duration
        if 200 <= status_code < 300:
            self.successful_requests += 1
        else:
            self.failed_requests += 1
        
        # Update endpoint metrics
        endpoint = self._get_endpoint_from_url(event.request.url)
        if endpoint in self.endpoint_metrics:
            self.endpoint_metrics[endpoint]["total_duration"] += duration
            if 200 <= status_code < 300:
                self.endpoint_metrics[endpoint]["successful_requests"] += 1
            else:
                self.endpoint_metrics[endpoint]["failed_requests"] += 1
            self.endpoint_metrics[endpoint]["average_duration"] = (
                self.endpoint_metrics[endpoint]["total_duration"] /
                self.endpoint_metrics[endpoint]["total_requests"]
            )
        
        return response
    
    def track_error(self, request_id: str, error: str) -> None:
        """
        Track an API error.
        
        Args:
            request_id: ID of the corresponding request
            error: Error message
        """
        # Find the event for the request
        event = self._find_event_by_request_id(request_id)
        if not event:
            logger.warning(f"Request with ID {request_id} not found")
            return
        
        # Update the event
        event.error = error
        event.duration = time.time() - event.request.timestamp
        
        # Update metrics
        self.total_duration += event.duration
        self.failed_requests += 1
        
        # Update endpoint metrics
        endpoint = self._get_endpoint_from_url(event.request.url)
        if endpoint in self.endpoint_metrics:
            self.endpoint_metrics[endpoint]["total_duration"] += event.duration
            self.endpoint_metrics[endpoint]["failed_requests"] += 1
            self.endpoint_metrics[endpoint]["average_duration"] = (
                self.endpoint_metrics[endpoint]["total_duration"] /
                self.endpoint_metrics[endpoint]["total_requests"]
            )
    
    def get_events(self, limit: int = None, filter_func: callable = None) -> List[APIEvent]:
        """
        Get API events.
        
        Args:
            limit: Maximum number of events to return
            filter_func: Function to filter events
            
        Returns:
            List of API events
        """
        events = self.events
        
        # Apply filter if provided
        if filter_func:
            events = [event for event in events if filter_func(event)]
        
        # Apply limit if provided
        if limit:
            events = events[:limit]
        
        return events
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get performance metrics.
        
        Returns:
            Dict containing performance metrics
        """
        return {
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "success_rate": self.successful_requests / self.total_requests if self.total_requests > 0 else 0,
            "total_duration": self.total_duration,
            "average_duration": self.total_duration / self.total_requests if self.total_requests > 0 else 0,
            "uptime": time.time() - self.start_time,
            "requests_per_second": self.total_requests / (time.time() - self.start_time) if time.time() > self.start_time else 0,
            "endpoint_metrics": self.endpoint_metrics
        }
    
    def get_endpoint_metrics(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """
        Get metrics for a specific endpoint.
        
        Args:
            endpoint: The endpoint to get metrics for
            
        Returns:
            Dict containing endpoint metrics, or None if the endpoint was not found
        """
        return self.endpoint_metrics.get(endpoint)
    
    def reset(self) -> None:
        """Reset the monitor."""
        self.events = []
        self.start_time = time.time()
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.total_duration = 0
        self.endpoint_metrics = {}
    
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
            csv = "request_id,method,url,status_code,duration,timestamp\n"
            
            # Add events
            for event in self.events:
                status_code = event.response.status_code if event.response else "N/A"
                duration = event.duration if event.duration else "N/A"
                timestamp = datetime.fromtimestamp(event.request.timestamp).isoformat()
                
                csv += f"{event.request.id},{event.request.method},{event.request.url},{status_code},{duration},{timestamp}\n"
            
            return csv
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _add_event(self, event: APIEvent) -> None:
        """
        Add an event to the history.
        
        Args:
            event: The event to add
        """
        self.events.append(event)
        
        # Trim history if needed
        if len(self.events) > self.max_history:
            self.events = self.events[-self.max_history:]
    
    def _find_event_by_request_id(self, request_id: str) -> Optional[APIEvent]:
        """
        Find an event by request ID.
        
        Args:
            request_id: The request ID to find
            
        Returns:
            The event if found, None otherwise
        """
        for event in self.events:
            if event.request.id == request_id:
                return event
        return None
    
    def _get_endpoint_from_url(self, url: str) -> str:
        """
        Extract the endpoint from a URL.
        
        Args:
            url: The URL to extract the endpoint from
            
        Returns:
            The extracted endpoint
        """
        # Parse the URL
        from urllib.parse import urlparse
        parsed_url = urlparse(url)
        
        # Get the path
        path = parsed_url.path
        
        # Extract the endpoint (first part of the path)
        parts = path.split("/")
        if len(parts) > 1:
            return parts[1]
        return "root"
    
    def _sanitize_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
        """
        Sanitize headers to remove sensitive information.
        
        Args:
            headers: The headers to sanitize
            
        Returns:
            The sanitized headers
        """
        sanitized = headers.copy()
        
        # Mask sensitive headers
        sensitive_headers = ["authorization", "cookie", "x-api-key"]
        for header in sensitive_headers:
            if header.lower() in sanitized:
                value = sanitized[header]
                if value.lower().startswith("bearer "):
                    sanitized[header] = "Bearer [REDACTED]"
                else:
                    sanitized[header] = "[REDACTED]"
        
        return sanitized
