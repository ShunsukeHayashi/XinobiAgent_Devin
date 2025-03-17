"""
Canva API integration tool for XinobiAgent.

This module provides tools for interacting with the Canva API to create and manipulate
presentation slides programmatically based on text prompts.
"""

import asyncio
import json
import logging
import os
from typing import Dict, Any, Optional, List

import aiohttp
from pydantic import Field

from app.tool.base import BaseTool

# Configure logging
logger = logging.getLogger(__name__)

class CanvaAPITool(BaseTool):
    """
    Tool for interacting with the Canva API to create and manipulate presentation slides.
    
    This tool provides methods for:
    - Creating new presentations
    - Adding slides to presentations
    - Adding text to slides
    - Adding images to slides
    - Applying templates to slides
    
    Authentication is handled via OAuth 2.0.
    """
    
    name: str = Field(default="canva_api", description="Canva API Tool")
    description: str = Field(
        default="Tool for creating and manipulating Canva presentations based on text prompts",
    )
    api_key: Optional[str] = Field(
        default=None,
        description="Canva API key for authentication",
    )
    base_url: str = Field(
        default="https://api.canva.com",
        description="Base URL for the Canva API",
    )
    
    def __init__(self, api_key: Optional[str] = None, **data):
        """
        Initialize the Canva API tool.
        
        Args:
            api_key: Canva API key for authentication
        """
        super().__init__(**data)
        self.api_key = api_key or os.environ.get("CANVA_API_KEY")
        
        if not self.api_key:
            logger.warning("No Canva API key provided. Authentication will fail.")
    
    async def run(self, action: str, **kwargs) -> str:
        """
        Run the specified Canva API action with the provided arguments.
        
        Args:
            action: The action to perform (create_presentation, add_slide, etc.)
            **kwargs: Arguments specific to the action
            
        Returns:
            JSON string containing the result of the action
        """
        actions = {
            "create_presentation": self.create_presentation,
            "add_slide": self.add_slide,
            "add_text": self.add_text,
            "add_image": self.add_image,
            "apply_template": self.apply_template,
            "generate_from_prompt": self.generate_from_prompt,
        }
        
        if action not in actions:
            return json.dumps({
                "error": f"Unknown action: {action}",
                "available_actions": list(actions.keys()),
            })
        
        try:
            result = await actions[action](**kwargs)
            return json.dumps(result)
        except Exception as e:
            logger.exception(f"Error executing Canva API action {action}: {e}")
            return json.dumps({
                "error": str(e),
                "action": action,
            })
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make a request to the Canva API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            data: Request data
            params: Query parameters
            
        Returns:
            Response data as a dictionary
        """
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
                params=params,
            ) as response:
                response_data = await response.json()
                
                if response.status >= 400:
                    error_message = response_data.get("message", "Unknown error")
                    raise Exception(f"Canva API error: {error_message} (Status: {response.status})")
                
                return response_data
    
    async def create_presentation(self, title: str, design_type: str = "presentation") -> Dict[str, Any]:
        """
        Create a new presentation in Canva.
        
        Args:
            title: Title of the presentation
            design_type: Type of design to create (default: presentation)
            
        Returns:
            Dictionary containing the created presentation details
        """
        # Note: This is a placeholder implementation based on expected API behavior
        # Actual implementation will depend on the specific Canva API endpoints
        data = {
            "title": title,
            "design_type": design_type,
        }
        
        # This endpoint is hypothetical and would need to be updated based on actual Canva API
        return await self._make_request("POST", "/v1/designs", data=data)
    
    async def add_slide(self, design_id: str, template_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Add a new slide to a presentation.
        
        Args:
            design_id: ID of the design/presentation
            template_id: Optional template ID to apply to the slide
            
        Returns:
            Dictionary containing the created slide details
        """
        data = {}
        if template_id:
            data["template_id"] = template_id
        
        # This endpoint is hypothetical and would need to be updated based on actual Canva API
        return await self._make_request("POST", f"/v1/designs/{design_id}/pages", data=data)
    
    async def add_text(
        self, 
        design_id: str, 
        page_id: str, 
        text: str, 
        position: Dict[str, float],
        style: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Add text to a slide.
        
        Args:
            design_id: ID of the design/presentation
            page_id: ID of the page/slide
            text: Text content to add
            position: Position of the text (x, y coordinates)
            style: Optional styling information
            
        Returns:
            Dictionary containing the created text element details
        """
        data = {
            "type": "text",
            "content": text,
            "position": position,
        }
        
        if style:
            data["style"] = style
        
        # This endpoint is hypothetical and would need to be updated based on actual Canva API
        return await self._make_request(
            "POST", 
            f"/v1/designs/{design_id}/pages/{page_id}/elements", 
            data=data
        )
    
    async def add_image(
        self, 
        design_id: str, 
        page_id: str, 
        image_url: str, 
        position: Dict[str, float],
        size: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        """
        Add an image to a slide.
        
        Args:
            design_id: ID of the design/presentation
            page_id: ID of the page/slide
            image_url: URL of the image to add
            position: Position of the image (x, y coordinates)
            size: Optional size information (width, height)
            
        Returns:
            Dictionary containing the created image element details
        """
        data = {
            "type": "image",
            "url": image_url,
            "position": position,
        }
        
        if size:
            data["size"] = size
        
        # This endpoint is hypothetical and would need to be updated based on actual Canva API
        return await self._make_request(
            "POST", 
            f"/v1/designs/{design_id}/pages/{page_id}/elements", 
            data=data
        )
    
    async def apply_template(self, design_id: str, page_id: str, template_id: str) -> Dict[str, Any]:
        """
        Apply a template to a slide.
        
        Args:
            design_id: ID of the design/presentation
            page_id: ID of the page/slide
            template_id: ID of the template to apply
            
        Returns:
            Dictionary containing the updated slide details
        """
        data = {
            "template_id": template_id,
        }
        
        # This endpoint is hypothetical and would need to be updated based on actual Canva API
        return await self._make_request(
            "PATCH", 
            f"/v1/designs/{design_id}/pages/{page_id}", 
            data=data
        )
    
    async def generate_from_prompt(
        self, 
        prompt: str, 
        num_slides: int = 5,
        design_type: str = "presentation",
        title: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate a complete presentation from a text prompt.
        
        This is a high-level method that combines multiple API calls to create
        a complete presentation based on a text prompt.
        
        Args:
            prompt: Text prompt describing the desired presentation
            num_slides: Number of slides to generate
            design_type: Type of design to create
            title: Optional title for the presentation
            
        Returns:
            Dictionary containing the generated presentation details
        """
        # In a real implementation, this would likely involve:
        # 1. Processing the prompt to extract key points (possibly using an LLM)
        # 2. Creating a new presentation
        # 3. Generating appropriate slides based on the extracted points
        # 4. Adding text and images to each slide
        # 5. Applying appropriate templates
        
        # For now, we'll implement a simplified version that creates a presentation
        # with placeholder slides
        
        # Create the presentation
        presentation_title = title or f"Presentation: {prompt[:30]}..."
        presentation = await self.create_presentation(presentation_title, design_type)
        design_id = presentation["id"]
        
        # Generate slides
        slides = []
        for i in range(num_slides):
            slide = await self.add_slide(design_id)
            slides.append(slide)
        
        return {
            "presentation": presentation,
            "slides": slides,
            "prompt": prompt,
        }
