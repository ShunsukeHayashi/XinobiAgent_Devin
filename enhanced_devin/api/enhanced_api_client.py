"""
Enhanced Devin API Client.

This module provides a client for interacting with the Enhanced Devin API,
building upon the original Devin API client with additional capabilities.
"""

import os
import requests
import json
import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Any, Union, BinaryIO

# Configure logging
logger = logging.getLogger(__name__)


class EnhancedDevinAPIClient:
    """
    Client for interacting with the Enhanced Devin API.
    
    This client provides methods for all API endpoints and handles authentication,
    request formatting, and response parsing. It extends the original Devin API
    client with additional capabilities.
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.enhanced-devin.ai/v1"):
        """
        Initialize the Enhanced Devin API client.
        
        Args:
            api_key: API key for authentication. If not provided, will look for ENHANCED_DEVIN_API_KEY environment variable.
            base_url: Base URL for the Enhanced Devin API.
        """
        self.api_key = api_key or os.environ.get("ENHANCED_DEVIN_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set as ENHANCED_DEVIN_API_KEY environment variable")
        
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # For tracking API usage
        self.request_count = 0
        self.last_response = None
        self.request_history = []
    
    # Session Management
    
    async def create_session(self, prompt: str, playbook_id: Optional[str] = None, 
                            settings: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new session.
        
        Args:
            prompt: The initial prompt for the session
            playbook_id: Optional ID of a playbook to use
            settings: Optional settings for the session
            
        Returns:
            Session details
        """
        url = f"{self.base_url}/sessions"
        payload = {"prompt": prompt}
        
        if playbook_id:
            payload["playbook_id"] = playbook_id
        
        if settings:
            payload["settings"] = settings
        
        return await self._make_async_request("POST", url, json=payload)
    
    async def get_session(self, session_id: str) -> Dict[str, Any]:
        """
        Get details for a session.
        
        Args:
            session_id: ID of the session
            
        Returns:
            Session details
        """
        url = f"{self.base_url}/session/{session_id}"
        return await self._make_async_request("GET", url)
    
    async def list_sessions(self, limit: int = 10, offset: int = 0, 
                           filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        List sessions.
        
        Args:
            limit: Maximum number of sessions to return
            offset: Offset for pagination
            filters: Optional filters for the sessions
            
        Returns:
            List of sessions
        """
        url = f"{self.base_url}/sessions"
        params = {"limit": limit, "offset": offset}
        
        if filters:
            params.update(filters)
        
        return await self._make_async_request("GET", url, params=params)
    
    async def update_session(self, session_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a session.
        
        Args:
            session_id: ID of the session
            updates: Updates to apply to the session
            
        Returns:
            Updated session details
        """
        url = f"{self.base_url}/session/{session_id}"
        return await self._make_async_request("PATCH", url, json=updates)
    
    async def delete_session(self, session_id: str) -> Dict[str, Any]:
        """
        Delete a session.
        
        Args:
            session_id: ID of the session
            
        Returns:
            Deletion confirmation
        """
        url = f"{self.base_url}/session/{session_id}"
        return await self._make_async_request("DELETE", url)
    
    async def fork_session(self, session_id: str, name: Optional[str] = None) -> Dict[str, Any]:
        """
        Fork a session.
        
        Args:
            session_id: ID of the session to fork
            name: Optional name for the new session
            
        Returns:
            New session details
        """
        url = f"{self.base_url}/session/{session_id}/fork"
        payload = {}
        if name:
            payload["name"] = name
        
        return await self._make_async_request("POST", url, json=payload)
    
    async def merge_sessions(self, source_session_id: str, target_session_id: str) -> Dict[str, Any]:
        """
        Merge two sessions.
        
        Args:
            source_session_id: ID of the source session
            target_session_id: ID of the target session
            
        Returns:
            Merged session details
        """
        url = f"{self.base_url}/session/{target_session_id}/merge"
        payload = {"source_session_id": source_session_id}
        
        return await self._make_async_request("POST", url, json=payload)
    
    # Message Management
    
    async def send_message(self, session_id: str, content: str, 
                          attachments: Optional[List[str]] = None,
                          metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Send a message to a session.
        
        Args:
            session_id: ID of the session
            content: Content of the message
            attachments: Optional list of attachment IDs
            metadata: Optional metadata for the message
            
        Returns:
            Message details
        """
        url = f"{self.base_url}/session/{session_id}/message"
        payload = {"content": content}
        
        if attachments:
            payload["attachments"] = attachments
        
        if metadata:
            payload["metadata"] = metadata
        
        return await self._make_async_request("POST", url, json=payload)
    
    async def get_messages(self, session_id: str, limit: int = 50, 
                          before_id: Optional[str] = None,
                          filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Get messages for a session.
        
        Args:
            session_id: ID of the session
            limit: Maximum number of messages to return
            before_id: Optional message ID to get messages before
            filters: Optional filters for the messages
            
        Returns:
            List of messages
        """
        url = f"{self.base_url}/session/{session_id}/messages"
        params = {"limit": limit}
        
        if before_id:
            params["before_id"] = before_id
        
        if filters:
            params.update(filters)
        
        return await self._make_async_request("GET", url, params=params)
    
    async def update_message(self, session_id: str, message_id: str, 
                            updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a message.
        
        Args:
            session_id: ID of the session
            message_id: ID of the message
            updates: Updates to apply to the message
            
        Returns:
            Updated message details
        """
        url = f"{self.base_url}/session/{session_id}/message/{message_id}"
        return await self._make_async_request("PATCH", url, json=updates)
    
    async def delete_message(self, session_id: str, message_id: str) -> Dict[str, Any]:
        """
        Delete a message.
        
        Args:
            session_id: ID of the session
            message_id: ID of the message
            
        Returns:
            Deletion confirmation
        """
        url = f"{self.base_url}/session/{session_id}/message/{message_id}"
        return await self._make_async_request("DELETE", url)
    
    # File Management
    
    async def upload_file(self, file_path: str, description: Optional[str] = None,
                         metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Upload a file.
        
        Args:
            file_path: Path to the file
            description: Optional description of the file
            metadata: Optional metadata for the file
            
        Returns:
            File details
        """
        url = f"{self.base_url}/attachments"
        
        with open(file_path, "rb") as f:
            return await self._upload_file_async(url, f, os.path.basename(file_path), description, metadata)
    
    async def upload_file_content(self, content: Union[str, bytes], filename: str,
                                 description: Optional[str] = None,
                                 metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Upload file content.
        
        Args:
            content: Content of the file
            filename: Name of the file
            description: Optional description of the file
            metadata: Optional metadata for the file
            
        Returns:
            File details
        """
        url = f"{self.base_url}/attachments"
        
        if isinstance(content, str):
            content = content.encode("utf-8")
        
        from io import BytesIO
        file_obj = BytesIO(content)
        
        return await self._upload_file_async(url, file_obj, filename, description, metadata)
    
    async def get_file(self, file_id: str) -> Dict[str, Any]:
        """
        Get file details.
        
        Args:
            file_id: ID of the file
            
        Returns:
            File details
        """
        url = f"{self.base_url}/attachment/{file_id}"
        return await self._make_async_request("GET", url)
    
    async def download_file(self, file_id: str, output_path: Optional[str] = None) -> Union[str, bytes]:
        """
        Download a file.
        
        Args:
            file_id: ID of the file
            output_path: Optional path to save the file to
            
        Returns:
            File content if output_path is None, otherwise the output path
        """
        url = f"{self.base_url}/attachment/{file_id}/content"
        
        async with aiohttp.ClientSession() as session:
            headers = self.headers.copy()
            headers.pop("Content-Type", None)
            
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                content = await response.read()
                
                if output_path:
                    with open(output_path, "wb") as f:
                        f.write(content)
                    return output_path
                else:
                    return content
    
    async def delete_file(self, file_id: str) -> Dict[str, Any]:
        """
        Delete a file.
        
        Args:
            file_id: ID of the file
            
        Returns:
            Deletion confirmation
        """
        url = f"{self.base_url}/attachment/{file_id}"
        return await self._make_async_request("DELETE", url)
    
    # Secret Management
    
    async def list_secrets(self) -> Dict[str, Any]:
        """
        List secrets.
        
        Returns:
            List of secrets
        """
        url = f"{self.base_url}/secrets"
        return await self._make_async_request("GET", url)
    
    async def create_secret(self, name: str, value: str, 
                           description: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a secret.
        
        Args:
            name: Name of the secret
            value: Value of the secret
            description: Optional description of the secret
            
        Returns:
            Secret details
        """
        url = f"{self.base_url}/secrets"
        payload = {"name": name, "value": value}
        
        if description:
            payload["description"] = description
        
        return await self._make_async_request("POST", url, json=payload)
    
    async def delete_secret(self, secret_id: str) -> Dict[str, Any]:
        """
        Delete a secret.
        
        Args:
            secret_id: ID of the secret
            
        Returns:
            Deletion confirmation
        """
        url = f"{self.base_url}/secrets/{secret_id}"
        return await self._make_async_request("DELETE", url)
    
    # Monitoring
    
    async def get_session_usage(self, session_id: str) -> Dict[str, Any]:
        """
        Get usage metrics for a session.
        
        Args:
            session_id: ID of the session
            
        Returns:
            Usage metrics
        """
        url = f"{self.base_url}/billing/usage/session/{session_id}"
        return await self._make_async_request("GET", url)
    
    async def get_api_metrics(self, start_time: Optional[str] = None,
                             end_time: Optional[str] = None) -> Dict[str, Any]:
        """
        Get API usage metrics.
        
        Args:
            start_time: Optional start time for the metrics
            end_time: Optional end time for the metrics
            
        Returns:
            API metrics
        """
        url = f"{self.base_url}/metrics/api"
        params = {}
        
        if start_time:
            params["start_time"] = start_time
        
        if end_time:
            params["end_time"] = end_time
        
        return await self._make_async_request("GET", url, params=params)
    
    # Helper methods
    
    async def _make_async_request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """
        Make an async request to the API.
        
        Args:
            method: HTTP method
            url: URL to request
            **kwargs: Additional arguments for the request
            
        Returns:
            Response JSON
        """
        async with aiohttp.ClientSession() as session:
            headers = kwargs.pop("headers", self.headers)
            
            # Track the request
            self.request_count += 1
            request_id = self.request_count
            request_info = {
                "id": request_id,
                "method": method,
                "url": url,
                "kwargs": kwargs
            }
            self.request_history.append(request_info)
            
            try:
                async with session.request(method, url, headers=headers, **kwargs) as response:
                    response.raise_for_status()
                    
                    # Track the response
                    response_json = await response.json()
                    self.last_response = {
                        "request_id": request_id,
                        "status_code": response.status,
                        "headers": dict(response.headers),
                        "body": response_json
                    }
                    
                    return response_json
            except aiohttp.ClientResponseError as e:
                logger.error(f"Error making request to {url}: {str(e)}")
                raise
            except aiohttp.ClientError as e:
                logger.error(f"Client error making request to {url}: {str(e)}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error making request to {url}: {str(e)}")
                raise
    
    async def _upload_file_async(self, url: str, file_obj: BinaryIO, filename: str,
                               description: Optional[str] = None,
                               metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Upload a file asynchronously.
        
        Args:
            url: URL to upload to
            file_obj: File object to upload
            filename: Name of the file
            description: Optional description of the file
            metadata: Optional metadata for the file
            
        Returns:
            Response JSON
        """
        async with aiohttp.ClientSession() as session:
            headers = self.headers.copy()
            headers.pop("Content-Type", None)
            
            form_data = aiohttp.FormData()
            form_data.add_field("file", file_obj, filename=filename)
            
            if description:
                form_data.add_field("description", description)
            
            if metadata:
                form_data.add_field("metadata", json.dumps(metadata))
            
            # Track the request
            self.request_count += 1
            request_id = self.request_count
            request_info = {
                "id": request_id,
                "method": "POST",
                "url": url,
                "filename": filename
            }
            self.request_history.append(request_info)
            
            try:
                async with session.post(url, headers=headers, data=form_data) as response:
                    response.raise_for_status()
                    
                    # Track the response
                    response_json = await response.json()
                    self.last_response = {
                        "request_id": request_id,
                        "status_code": response.status,
                        "headers": dict(response.headers),
                        "body": response_json
                    }
                    
                    return response_json
            except aiohttp.ClientResponseError as e:
                logger.error(f"Error uploading file to {url}: {str(e)}")
                raise
            except aiohttp.ClientError as e:
                logger.error(f"Client error uploading file to {url}: {str(e)}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error uploading file to {url}: {str(e)}")
                raise
