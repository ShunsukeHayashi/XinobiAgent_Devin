"""
Performance Monitor for Enhanced Devin.

This module provides monitoring capabilities for performance metrics in the
Enhanced Devin system. It tracks resource usage, execution times, and other
performance indicators.
"""

import time
import psutil
import os
import platform
import logging
from typing import Dict, List, Any, Optional, Union
import asyncio
from datetime import datetime, timedelta
import json

from pydantic import BaseModel, Field

# Configure logging
logger = logging.getLogger(__name__)


class ResourceUsage(BaseModel):
    """Model for resource usage metrics."""
    
    cpu_percent: float = Field(description="CPU usage percentage")
    memory_percent: float = Field(description="Memory usage percentage")
    memory_used: int = Field(description="Memory used in bytes")
    memory_available: int = Field(description="Memory available in bytes")
    disk_usage_percent: float = Field(description="Disk usage percentage")
    disk_used: int = Field(description="Disk space used in bytes")
    disk_free: int = Field(description="Disk space free in bytes")
    network_sent: int = Field(description="Network bytes sent")
    network_received: int = Field(description="Network bytes received")
    timestamp: float = Field(description="Timestamp of the measurement")


class PerformanceMetric(BaseModel):
    """Model for a performance metric."""
    
    name: str = Field(description="Name of the metric")
    value: float = Field(description="Value of the metric")
    unit: str = Field(description="Unit of the metric")
    timestamp: float = Field(description="Timestamp of the measurement")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")


class PerformanceMonitor:
    """
    Monitor for performance metrics.
    
    This class provides monitoring capabilities for performance metrics, including
    resource usage, execution times, and other performance indicators.
    """
    
    def __init__(self, interval: float = 5.0, max_history: int = 100):
        """
        Initialize the performance monitor.
        
        Args:
            interval: Interval between resource usage measurements in seconds
            max_history: Maximum number of measurements to keep in history
        """
        self.interval = interval
        self.max_history = max_history
        self.start_time = time.time()
        
        # Resource usage history
        self.resource_history: List[ResourceUsage] = []
        
        # Custom metrics
        self.metrics: Dict[str, List[PerformanceMetric]] = {}
        
        # Monitoring task
        self._monitoring_task = None
        self._stop_monitoring = asyncio.Event()
    
    async def start_monitoring(self) -> None:
        """Start the monitoring task."""
        if self._monitoring_task is not None:
            logger.warning("Monitoring task is already running")
            return
        
        self._stop_monitoring.clear()
        self._monitoring_task = asyncio.create_task(self._monitor_resources())
        logger.info("Started performance monitoring")
    
    async def stop_monitoring(self) -> None:
        """Stop the monitoring task."""
        if self._monitoring_task is None:
            logger.warning("Monitoring task is not running")
            return
        
        self._stop_monitoring.set()
        await self._monitoring_task
        self._monitoring_task = None
        logger.info("Stopped performance monitoring")
    
    async def _monitor_resources(self) -> None:
        """Monitor resource usage at regular intervals."""
        while not self._stop_monitoring.is_set():
            try:
                # Get resource usage
                usage = self._get_resource_usage()
                
                # Add to history
                self.resource_history.append(usage)
                
                # Trim history if needed
                if len(self.resource_history) > self.max_history:
                    self.resource_history = self.resource_history[-self.max_history:]
                
                # Wait for the next interval
                try:
                    await asyncio.wait_for(self._stop_monitoring.wait(), timeout=self.interval)
                except asyncio.TimeoutError:
                    pass
            except Exception as e:
                logger.error(f"Error monitoring resources: {str(e)}")
                await asyncio.sleep(self.interval)
    
    def _get_resource_usage(self) -> ResourceUsage:
        """
        Get current resource usage.
        
        Returns:
            ResourceUsage object with current resource usage metrics
        """
        # Get CPU usage
        cpu_percent = psutil.cpu_percent(interval=0.1)
        
        # Get memory usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_used = memory.used
        memory_available = memory.available
        
        # Get disk usage
        disk = psutil.disk_usage(os.path.abspath(os.sep))
        disk_usage_percent = disk.percent
        disk_used = disk.used
        disk_free = disk.free
        
        # Get network usage
        network = psutil.net_io_counters()
        network_sent = network.bytes_sent
        network_received = network.bytes_recv
        
        # Create and return the resource usage object
        return ResourceUsage(
            cpu_percent=cpu_percent,
            memory_percent=memory_percent,
            memory_used=memory_used,
            memory_available=memory_available,
            disk_usage_percent=disk_usage_percent,
            disk_used=disk_used,
            disk_free=disk_free,
            network_sent=network_sent,
            network_received=network_received,
            timestamp=time.time()
        )
    
    def track_metric(self, name: str, value: float, unit: str, context: Optional[Dict[str, Any]] = None) -> None:
        """
        Track a custom performance metric.
        
        Args:
            name: Name of the metric
            value: Value of the metric
            unit: Unit of the metric
            context: Additional context for the metric
        """
        # Create the metric
        metric = PerformanceMetric(
            name=name,
            value=value,
            unit=unit,
            timestamp=time.time(),
            context=context
        )
        
        # Add to metrics
        if name not in self.metrics:
            self.metrics[name] = []
        
        self.metrics[name].append(metric)
        
        # Trim history if needed
        if len(self.metrics[name]) > self.max_history:
            self.metrics[name] = self.metrics[name][-self.max_history:]
    
    def get_resource_usage(self, start_time: Optional[float] = None, end_time: Optional[float] = None) -> List[ResourceUsage]:
        """
        Get resource usage history.
        
        Args:
            start_time: Optional start time for filtering
            end_time: Optional end time for filtering
            
        Returns:
            List of ResourceUsage objects
        """
        if start_time is None and end_time is None:
            return self.resource_history
        
        filtered = []
        for usage in self.resource_history:
            if start_time is not None and usage.timestamp < start_time:
                continue
            if end_time is not None and usage.timestamp > end_time:
                continue
            filtered.append(usage)
        
        return filtered
    
    def get_metrics(self, name: Optional[str] = None, start_time: Optional[float] = None, end_time: Optional[float] = None) -> Dict[str, List[PerformanceMetric]]:
        """
        Get custom metrics.
        
        Args:
            name: Optional name of the metric to get
            start_time: Optional start time for filtering
            end_time: Optional end time for filtering
            
        Returns:
            Dict mapping metric names to lists of PerformanceMetric objects
        """
        if name is not None:
            if name not in self.metrics:
                return {}
            
            if start_time is None and end_time is None:
                return {name: self.metrics[name]}
            
            filtered = []
            for metric in self.metrics[name]:
                if start_time is not None and metric.timestamp < start_time:
                    continue
                if end_time is not None and metric.timestamp > end_time:
                    continue
                filtered.append(metric)
            
            return {name: filtered}
        
        if start_time is None and end_time is None:
            return self.metrics
        
        result = {}
        for metric_name, metrics in self.metrics.items():
            filtered = []
            for metric in metrics:
                if start_time is not None and metric.timestamp < start_time:
                    continue
                if end_time is not None and metric.timestamp > end_time:
                    continue
                filtered.append(metric)
            
            if filtered:
                result[metric_name] = filtered
        
        return result
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of performance metrics.
        
        Returns:
            Dict containing performance summary
        """
        # Calculate uptime
        uptime = time.time() - self.start_time
        
        # Get latest resource usage
        latest_usage = self.resource_history[-1] if self.resource_history else None
        
        # Calculate average resource usage
        avg_cpu = sum(usage.cpu_percent for usage in self.resource_history) / len(self.resource_history) if self.resource_history else 0
        avg_memory = sum(usage.memory_percent for usage in self.resource_history) / len(self.resource_history) if self.resource_history else 0
        
        # Calculate average metrics
        avg_metrics = {}
        for name, metrics in self.metrics.items():
            avg_metrics[name] = sum(metric.value for metric in metrics) / len(metrics) if metrics else 0
        
        # Create the summary
        summary = {
            "uptime": uptime,
            "uptime_formatted": str(timedelta(seconds=int(uptime))),
            "system_info": {
                "platform": platform.platform(),
                "python_version": platform.python_version(),
                "cpu_count": psutil.cpu_count(),
                "total_memory": psutil.virtual_memory().total
            },
            "current_usage": latest_usage.dict() if latest_usage else None,
            "average_usage": {
                "cpu_percent": avg_cpu,
                "memory_percent": avg_memory
            },
            "average_metrics": avg_metrics
        }
        
        return summary
    
    def export_data(self, format: str = "json") -> str:
        """
        Export monitoring data to a specific format.
        
        Args:
            format: Format to export to (json, csv)
            
        Returns:
            Exported data as a string
        """
        if format == "json":
            data = {
                "resource_history": [usage.dict() for usage in self.resource_history],
                "metrics": {name: [metric.dict() for metric in metrics] for name, metrics in self.metrics.items()},
                "summary": self.get_summary()
            }
            return json.dumps(data, indent=2)
        elif format == "csv":
            # Create CSV for resource usage
            resource_csv = "timestamp,cpu_percent,memory_percent,memory_used,memory_available,disk_usage_percent,disk_used,disk_free,network_sent,network_received\n"
            
            for usage in self.resource_history:
                timestamp = datetime.fromtimestamp(usage.timestamp).isoformat()
                resource_csv += f"{timestamp},{usage.cpu_percent},{usage.memory_percent},{usage.memory_used},{usage.memory_available},{usage.disk_usage_percent},{usage.disk_used},{usage.disk_free},{usage.network_sent},{usage.network_received}\n"
            
            return resource_csv
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def reset(self) -> None:
        """Reset the monitor."""
        self.resource_history = []
        self.metrics = {}
        self.start_time = time.time()
