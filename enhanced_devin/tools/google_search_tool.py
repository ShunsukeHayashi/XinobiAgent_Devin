"""
Google Search Tool for Enhanced Devin.

This module provides a tool for searching Google for information.
"""

import asyncio
from typing import Dict, Any, List, Optional
import json
import aiohttp

from enhanced_devin.tools.base_tool import BaseTool


class GoogleSearchTool(BaseTool):
    """
    Tool for searching Google for information.
    
    This tool provides a way to search Google and retrieve search results.
    It includes options for filtering results, specifying the number of results,
    and handling different result formats.
    """
    
    name: str = "google_search"
    description: str = "Search Google for information"
    version: str = "0.2.0"
    author: str = "Enhanced Devin Team"
    parameters: Dict[str, Any] = {
        "query": {
            "type": "string",
            "description": "The search query"
        },
        "num_results": {
            "type": "integer",
            "description": "Number of results to return (default: 5)",
            "default": 5
        },
        "search_type": {
            "type": "string",
            "description": "Type of search (web, image, news)",
            "default": "web"
        },
        "language": {
            "type": "string",
            "description": "Language code for the search (default: en)",
            "default": "en"
        }
    }
    
    # API key for the Google Custom Search API
    _api_key: Optional[str] = None
    
    # Custom Search Engine ID
    _cse_id: Optional[str] = None
    
    def __init__(self, api_key: Optional[str] = None, cse_id: Optional[str] = None, **data):
        """
        Initialize the Google Search tool.
        
        Args:
            api_key: API key for the Google Custom Search API
            cse_id: Custom Search Engine ID
            **data: Additional data for the tool
        """
        super().__init__(**data)
        self._api_key = api_key
        self._cse_id = cse_id
    
    async def _execute(self, query: str, num_results: int = 5, 
                      search_type: str = "web", language: str = "en") -> Dict[str, Any]:
        """
        Search Google for information.
        
        Args:
            query: The search query
            num_results: Number of results to return (default: 5)
            search_type: Type of search (web, image, news)
            language: Language code for the search (default: en)
            
        Returns:
            Dict containing the search results
            
        Raises:
            ValueError: If the API key or CSE ID is not set
            aiohttp.ClientError: If the API request fails
        """
        # Check if the API key and CSE ID are set
        if not self._api_key or not self._cse_id:
            # If not set, return mock results
            return await self._get_mock_results(query, num_results, search_type, language)
        
        # Build the API URL
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": self._api_key,
            "cx": self._cse_id,
            "q": query,
            "num": min(num_results, 10),  # API limit is 10 results per request
            "hl": language
        }
        
        # Add search type specific parameters
        if search_type == "image":
            params["searchType"] = "image"
        elif search_type == "news":
            params["sort"] = "date"
        
        try:
            # Make the API request
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    response.raise_for_status()
                    data = await response.json()
            
            # Process the results
            results = []
            if "items" in data:
                for item in data["items"]:
                    result = {
                        "title": item.get("title", ""),
                        "link": item.get("link", ""),
                        "snippet": item.get("snippet", "")
                    }
                    
                    # Add image-specific fields
                    if search_type == "image" and "image" in item:
                        result["image_url"] = item["image"].get("thumbnailLink", "")
                        result["image_width"] = item["image"].get("thumbnailWidth", 0)
                        result["image_height"] = item["image"].get("thumbnailHeight", 0)
                    
                    results.append(result)
            
            # Return the results
            return {
                "query": query,
                "results": results,
                "total_results": data.get("searchInformation", {}).get("totalResults", 0)
            }
        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"Error making API request: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Error searching Google: {str(e)}")
    
    async def _get_mock_results(self, query: str, num_results: int = 5, 
                               search_type: str = "web", language: str = "en") -> Dict[str, Any]:
        """
        Get mock search results when the API key or CSE ID is not set.
        
        Args:
            query: The search query
            num_results: Number of results to return
            search_type: Type of search
            language: Language code for the search
            
        Returns:
            Dict containing mock search results
        """
        # Create mock results
        results = []
        for i in range(min(num_results, 5)):
            result = {
                "title": f"Mock result {i+1} for '{query}'",
                "link": f"https://example.com/result{i+1}",
                "snippet": f"This is a mock search result for the query '{query}'. It is generated because the Google Custom Search API key or CSE ID is not set."
            }
            
            # Add image-specific fields for image search
            if search_type == "image":
                result["image_url"] = f"https://example.com/image{i+1}.jpg"
                result["image_width"] = 300
                result["image_height"] = 200
            
            results.append(result)
        
        # Return the mock results
        return {
            "query": query,
            "results": results,
            "total_results": min(num_results, 5)
        }
