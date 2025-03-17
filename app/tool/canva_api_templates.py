"""
Template implementations for Canva API Tool.

This module provides template implementation methods for the CanvaAPITool class.
These methods are used to apply different layout templates to slides.
"""

from typing import Dict, Any, List, Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)

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
