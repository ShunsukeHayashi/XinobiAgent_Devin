"""
Canva API integration tool for XinobiAgent.

This module provides tools for interacting with the Canva API to create and manipulate
presentation slides programmatically based on text prompts.
"""

import asyncio
import json
import logging
import os
import re
from typing import Dict, Any, Optional, List, Tuple

import aiohttp
from pydantic import Field

from app.tool.base import BaseTool
from app.tool.template_manager import TemplateManager, TemplateType

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
            "apply_timeline_template": self.apply_timeline_template,
            "apply_arrows_template": self.apply_arrows_template,
            "apply_cycle_template": self.apply_cycle_template,
            "apply_icons_template": self.apply_icons_template,
            "apply_boxes_template": self.apply_boxes_template,
            "apply_bullets_template": self.apply_bullets_template,
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
        
    async def apply_timeline_template(
        self, 
        design_id: str, 
        page_id: str, 
        items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Apply a timeline template to a slide.
        
        Args:
            design_id: ID of the design/presentation
            page_id: ID of the page/slide
            items: List of timeline items with title, description, and optional image
            
        Returns:
            Dictionary containing the updated slide details
        """
        # In a real implementation, this would apply a timeline template
        # For now, we'll create a simple layout with the items
        
        # Add timeline items
        for i, item in enumerate(items):
            y_position = 0.3 + (i * 0.15)
            
            # Add item title
            await self.add_text(
                design_id=design_id,
                page_id=page_id,
                text=item.get("title", f"Step {i+1}"),
                position={"x": 0.2, "y": y_position},
                style={"fontSize": 24, "fontWeight": "bold"}
            )
            
            # Add item description
            await self.add_text(
                design_id=design_id,
                page_id=page_id,
                text=item.get("description", ""),
                position={"x": 0.6, "y": y_position},
                style={"fontSize": 18}
            )
        
        return {
            "design_id": design_id,
            "page_id": page_id,
            "template_type": "timeline",
            "items": items
        }
    
    async def apply_arrows_template(
        self, 
        design_id: str, 
        page_id: str, 
        items: List[Dict[str, Any]],
        orientation: str = "horizontal"
    ) -> Dict[str, Any]:
        """
        Apply an arrows template to a slide for process flows.
        
        Args:
            design_id: ID of the design/presentation
            page_id: ID of the page/slide
            items: List of process items with title, description, and optional image
            orientation: Direction of the arrows (horizontal or vertical)
            
        Returns:
            Dictionary containing the updated slide details
        """
        # In a real implementation, this would apply an arrows template
        # For now, we'll create a simple layout with the items
        
        # Add process items
        if orientation == "horizontal":
            # Horizontal layout
            for i, item in enumerate(items):
                x_position = 0.2 + (i * 0.2)
                
                # Add item title
                await self.add_text(
                    design_id=design_id,
                    page_id=page_id,
                    text=item.get("title", f"Step {i+1}"),
                    position={"x": x_position, "y": 0.4},
                    style={"fontSize": 24, "fontWeight": "bold", "textAlign": "center"}
                )
                
                # Add item description
                await self.add_text(
                    design_id=design_id,
                    page_id=page_id,
                    text=item.get("description", ""),
                    position={"x": x_position, "y": 0.5},
                    style={"fontSize": 18, "textAlign": "center"}
                )
        else:
            # Vertical layout
            for i, item in enumerate(items):
                y_position = 0.3 + (i * 0.15)
                
                # Add item title
                await self.add_text(
                    design_id=design_id,
                    page_id=page_id,
                    text=item.get("title", f"Step {i+1}"),
                    position={"x": 0.3, "y": y_position},
                    style={"fontSize": 24, "fontWeight": "bold"}
                )
                
                # Add item description
                await self.add_text(
                    design_id=design_id,
                    page_id=page_id,
                    text=item.get("description", ""),
                    position={"x": 0.6, "y": y_position},
                    style={"fontSize": 18}
                )
        
        return {
            "design_id": design_id,
            "page_id": page_id,
            "template_type": "arrows",
            "orientation": orientation,
            "items": items
        }
    
    async def apply_cycle_template(
        self, 
        design_id: str, 
        page_id: str, 
        items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Apply a cycle template to a slide for cyclical processes.
        
        Args:
            design_id: ID of the design/presentation
            page_id: ID of the page/slide
            items: List of cycle items with title, description, and optional image
            
        Returns:
            Dictionary containing the updated slide details
        """
        # In a real implementation, this would apply a cycle template
        # For now, we'll create a simple layout with the items
        
        # Calculate positions in a circle
        center_x = 0.5
        center_y = 0.5
        radius = 0.25
        num_items = len(items)
        
        for i, item in enumerate(items):
            # Calculate position on the circle
            angle = (i / num_items) * 2 * 3.14159  # Convert to radians
            x_position = center_x + radius * 0.8 * 1.5 * (0.5 - 0.5 * (1 if i % 2 == 0 else -1))
            y_position = center_y + radius * (0.5 - 0.5 * (1 if i < num_items / 2 else -1))
            
            # Add item title
            await self.add_text(
                design_id=design_id,
                page_id=page_id,
                text=item.get("title", f"Step {i+1}"),
                position={"x": x_position, "y": y_position},
                style={"fontSize": 24, "fontWeight": "bold", "textAlign": "center"}
            )
            
            # Add item description
            await self.add_text(
                design_id=design_id,
                page_id=page_id,
                text=item.get("description", ""),
                position={"x": x_position, "y": y_position + 0.07},
                style={"fontSize": 18, "textAlign": "center"}
            )
        
        return {
            "design_id": design_id,
            "page_id": page_id,
            "template_type": "cycle",
            "items": items
        }
        
    async def apply_icons_template(
        self, 
        design_id: str, 
        page_id: str, 
        items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Apply an icons template to a slide for feature highlights.
        
        Args:
            design_id: ID of the design/presentation
            page_id: ID of the page/slide
            items: List of feature items with title, description, and optional icon
            
        Returns:
            Dictionary containing the updated slide details
        """
        # In a real implementation, this would apply an icons template
        # For now, we'll create a simple layout with the items
        
        # Add feature items in a grid layout
        columns = min(3, len(items))
        rows = (len(items) + columns - 1) // columns
        
        for i, item in enumerate(items):
            col = i % columns
            row = i // columns
            
            x_position = 0.2 + (col * 0.3)
            y_position = 0.3 + (row * 0.2)
            
            # Add item title
            await self.add_text(
                design_id=design_id,
                page_id=page_id,
                text=item.get("title", f"Feature {i+1}"),
                position={"x": x_position, "y": y_position},
                style={"fontSize": 24, "fontWeight": "bold", "textAlign": "center"}
            )
            
            # Add item description
            await self.add_text(
                design_id=design_id,
                page_id=page_id,
                text=item.get("description", ""),
                position={"x": x_position, "y": y_position + 0.07},
                style={"fontSize": 18, "textAlign": "center"}
            )
        
        return {
            "design_id": design_id,
            "page_id": page_id,
            "template_type": "icons",
            "items": items
        }
        
    async def apply_boxes_template(
        self, 
        design_id: str, 
        page_id: str, 
        items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Apply a boxes template to a slide for grouped information.
        
        Args:
            design_id: ID of the design/presentation
            page_id: ID of the page/slide
            items: List of box items with title, description, and optional image
            
        Returns:
            Dictionary containing the updated slide details
        """
        # In a real implementation, this would apply a boxes template
        # For now, we'll create a simple layout with the items
        
        # Add box items in a grid layout
        columns = min(2, len(items))
        rows = (len(items) + columns - 1) // columns
        
        for i, item in enumerate(items):
            col = i % columns
            row = i // columns
            
            x_position = 0.25 + (col * 0.5)
            y_position = 0.3 + (row * 0.25)
            
            # Add item title
            await self.add_text(
                design_id=design_id,
                page_id=page_id,
                text=item.get("title", f"Category {i+1}"),
                position={"x": x_position, "y": y_position},
                style={"fontSize": 24, "fontWeight": "bold", "textAlign": "center"}
            )
            
            # Add item description
            await self.add_text(
                design_id=design_id,
                page_id=page_id,
                text=item.get("description", ""),
                position={"x": x_position, "y": y_position + 0.07},
                style={"fontSize": 18, "textAlign": "center"}
            )
        
        return {
            "design_id": design_id,
            "page_id": page_id,
            "template_type": "boxes",
            "items": items
        }
        
    async def apply_bullets_template(
        self, 
        design_id: str, 
        page_id: str, 
        items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Apply a bullets template to a slide for simple lists.
        
        Args:
            design_id: ID of the design/presentation
            page_id: ID of the page/slide
            items: List of bullet items with title, description, and optional image
            
        Returns:
            Dictionary containing the updated slide details
        """
        # In a real implementation, this would apply a bullets template
        # For now, we'll create a simple layout with the items
        
        # Add bullet items
        for i, item in enumerate(items):
            y_position = 0.3 + (i * 0.12)
            
            # Add bullet point and item text
            bullet_text = f"• {item.get('title', '')}: {item.get('description', '')}"
            
            await self.add_text(
                design_id=design_id,
                page_id=page_id,
                text=bullet_text,
                position={"x": 0.5, "y": y_position},
                style={"fontSize": 24, "textAlign": "left"}
            )
        
        return {
            "design_id": design_id,
            "page_id": page_id,
            "template_type": "bullets",
            "items": items
        }
    
    async def generate_from_prompt(
        self, 
        prompt: str, 
        num_slides: int = 5,
        design_type: str = "presentation",
        title: Optional[str] = None,
        template_type: Optional[str] = None,
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
            template_type: Optional template type to apply (timeline, arrows, cycle, etc.)
            
        Returns:
            Dictionary containing the generated presentation details
        """
        # Process the prompt to extract key points
        # For Japanese prompts, ensure proper language processing
        sections = TemplateManager.extract_sections_from_prompt(prompt, num_slides)
        
        # Create the presentation
        presentation_title = title or f"Presentation: {prompt[:30]}..."
        presentation = await self.create_presentation(presentation_title, design_type)
        design_id = presentation["id"]
        
        # Generate slides with appropriate templates based on content type
        slides = []
        
        # Create title slide
        title_slide = await self.add_slide(design_id)
        await self.add_text(
            design_id=design_id,
            page_id=title_slide["id"],
            text=presentation_title,
            position={"x": 0.5, "y": 0.4},
            style={"fontSize": 48, "textAlign": "center", "fontWeight": "bold"}
        )
        
        # Add subtitle if available
        if len(sections) > 0:
            await self.add_text(
                design_id=design_id,
                page_id=title_slide["id"],
                text=sections[0].get("content", ""),
                position={"x": 0.5, "y": 0.6},
                style={"fontSize": 24, "textAlign": "center"}
            )
        
        slides.append(title_slide)
        
        # Create content slides
        for i, section in enumerate(sections):
            if i == 0 and len(sections) > 1:  # Skip the first section if used as subtitle
                continue
                
            # Create a new slide
            slide = await self.add_slide(design_id)
            
            # Add section title
            await self.add_text(
                design_id=design_id,
                page_id=slide["id"],
                text=section.get("title", f"Slide {i+1}"),
                position={"x": 0.5, "y": 0.1},
                style={"fontSize": 36, "textAlign": "center", "fontWeight": "bold"}
            )
            
            # Determine template type for this section
            section_template_type = None
            if template_type:
                # Use specified template type if provided
                try:
                    section_template_type = TemplateType(template_type)
                except ValueError:
                    # If invalid template type, use auto-detection
                    section_template_type = TemplateManager.select_template_for_content(
                        section.get("title", "") + " " + section.get("content", "")
                    )
            else:
                # Auto-detect template type based on content
                section_template_type = TemplateManager.select_template_for_content(
                    section.get("title", "") + " " + section.get("content", "")
                )
            
            # Extract items for the template
            items = TemplateManager.extract_items_from_section(section)
            
            # Apply appropriate template based on content type
            if section_template_type == TemplateType.TIMELINE:
                await self.apply_timeline_template(design_id, slide["id"], items)
            elif section_template_type == TemplateType.ARROWS:
                await self.apply_arrows_template(design_id, slide["id"], items)
            elif section_template_type == TemplateType.CYCLE:
                await self.apply_cycle_template(design_id, slide["id"], items)
            elif section_template_type == TemplateType.ICONS:
                await self.apply_icons_template(design_id, slide["id"], items)
            elif section_template_type == TemplateType.BOXES:
                await self.apply_boxes_template(design_id, slide["id"], items)
            elif section_template_type == TemplateType.BULLETS:
                await self.apply_bullets_template(design_id, slide["id"], items)
            else:
                # Default template - just add the content as text
                await self.add_text(
                    design_id=design_id,
                    page_id=slide["id"],
                    text=section.get("content", ""),
                    position={"x": 0.5, "y": 0.5},
                    style={"fontSize": 24, "textAlign": "center"}
                )
            
            # Generate an image query for this section
            image_query = TemplateManager.generate_image_query_for_section(section)
            
            # In a real implementation, we would use an image generation API here
            # For now, we'll use a placeholder image URL
            placeholder_image_url = "https://via.placeholder.com/800x600?text=" + image_query.replace(" ", "+")
            
            # Add the image to the slide
            await self.add_image(
                design_id=design_id,
                page_id=slide["id"],
                image_url=placeholder_image_url,
                position={"x": 0.5, "y": 0.7},
                size={"width": 0.6, "height": 0.4}
            )
            
            slides.append(slide)
        
        return {
            "presentation": presentation,
            "slides": slides,
            "prompt": prompt,
            "template_type": template_type,
        }
