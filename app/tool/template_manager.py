"""
Template Manager for Canva Slide Generator.

This module provides a template manager for handling different slide layout templates
based on content type and structure, inspired by the Gamma.app approach.
"""

from enum import Enum
from typing import Dict, Any, List, Optional, Tuple
import re
import logging

# Configure logging
logger = logging.getLogger(__name__)

class TemplateType(Enum):
    """Enum for different template types."""
    TIMELINE = "timeline"
    ARROWS = "arrows"
    CYCLE = "cycle"
    ICONS = "icons"
    BOXES = "boxes"
    BULLETS = "bullets"
    DEFAULT = "default"

class TemplateManager:
    """
    Manager for slide templates.
    
    This class provides methods for selecting and applying appropriate templates
    based on content type and structure. It is inspired by the Gamma.app approach
    to slide generation, which uses structured templates for different types of content.
    """
    
    @staticmethod
    def select_template_for_content(content: str) -> TemplateType:
        """
        Select an appropriate template type based on content analysis.
        
        Args:
            content: The content to analyze
            
        Returns:
            The selected template type
        """
        # Convert to lowercase for case-insensitive matching
        content_lower = content.lower()
        
        # Check for timeline indicators
        timeline_indicators = [
            "timeline", "chronological", "history", "evolution", "stages", "phases",
            "タイムライン", "時系列", "歴史", "進化", "段階", "フェーズ"
        ]
        for indicator in timeline_indicators:
            if indicator in content_lower:
                return TemplateType.TIMELINE
        
        # Check for process flow indicators
        flow_indicators = [
            "process", "flow", "steps", "sequence", "procedure", "workflow",
            "プロセス", "フロー", "手順", "順序", "手続き", "ワークフロー"
        ]
        for indicator in flow_indicators:
            if indicator in content_lower:
                return TemplateType.ARROWS
        
        # Check for cycle indicators
        cycle_indicators = [
            "cycle", "circular", "loop", "recurring", "iterative", "feedback",
            "サイクル", "循環", "ループ", "繰り返し", "反復", "フィードバック"
        ]
        for indicator in cycle_indicators:
            if indicator in content_lower:
                return TemplateType.CYCLE
        
        # Check for feature/benefit indicators
        feature_indicators = [
            "features", "benefits", "advantages", "highlights", "key points",
            "機能", "利点", "メリット", "ハイライト", "要点"
        ]
        for indicator in feature_indicators:
            if indicator in content_lower:
                return TemplateType.ICONS
        
        # Check for comparison/category indicators
        comparison_indicators = [
            "comparison", "versus", "categories", "types", "classification",
            "比較", "対", "カテゴリ", "種類", "分類"
        ]
        for indicator in comparison_indicators:
            if indicator in content_lower:
                return TemplateType.BOXES
        
        # Check for list indicators
        list_indicators = [
            "list", "points", "items", "bullets", "enumeration",
            "リスト", "ポイント", "項目", "箇条書き", "列挙"
        ]
        for indicator in list_indicators:
            if indicator in content_lower:
                return TemplateType.BULLETS
        
        # Default to a simple layout if no specific indicators are found
        return TemplateType.DEFAULT
    
    @staticmethod
    def extract_sections_from_prompt(prompt: str, num_sections: int = 5) -> List[Dict[str, Any]]:
        """
        Extract sections from a prompt for slide generation.
        
        Args:
            prompt: The prompt to extract sections from
            num_sections: The number of sections to extract
            
        Returns:
            List of section dictionaries with title and content
        """
        # Split the prompt into sentences
        sentences = re.split(r'[.!?。！？]', prompt)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # If we don't have enough sentences, duplicate some
        while len(sentences) < num_sections * 2:
            sentences.extend(sentences[:num_sections])
        
        # Create sections
        sections = []
        for i in range(min(num_sections, len(sentences) // 2)):
            title_idx = i * 2
            content_idx = i * 2 + 1
            
            title = sentences[title_idx]
            content = sentences[content_idx] if content_idx < len(sentences) else ""
            
            sections.append({
                "title": title,
                "content": content
            })
        
        return sections
    
    @staticmethod
    def create_template_data(
        template_type: TemplateType,
        items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Create template data for the specified template type.
        
        Args:
            template_type: The type of template to create
            items: The items to include in the template
            
        Returns:
            Template data structure
        """
        template_data = {
            "type": template_type.value,
            "items": items
        }
        
        # Add template-specific properties
        if template_type == TemplateType.ARROWS:
            template_data["orientation"] = "horizontal"
        elif template_type == TemplateType.CYCLE:
            template_data["circular"] = True
        
        return template_data
    
    @staticmethod
    def generate_image_query_for_section(section: Dict[str, Any]) -> str:
        """
        Generate an image query for a section based on its content.
        
        Args:
            section: The section to generate an image query for
            
        Returns:
            Image query string
        """
        title = section.get("title", "")
        content = section.get("content", "")
        
        # Combine title and content for the query
        query = f"{title} {content}"
        
        # Limit the query length
        if len(query) > 100:
            query = query[:97] + "..."
        
        return query
    
    @staticmethod
    def extract_items_from_section(
        section: Dict[str, Any],
        num_items: int = 4
    ) -> List[Dict[str, Any]]:
        """
        Extract items from a section for template use.
        
        Args:
            section: The section to extract items from
            num_items: The number of items to extract
            
        Returns:
            List of item dictionaries with title and description
        """
        content = section.get("content", "")
        
        # Split content into sentences
        sentences = re.split(r'[.!?。！？]', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # If we don't have enough sentences, generate some based on the title
        title = section.get("title", "")
        while len(sentences) < num_items:
            sentences.append(f"Point {len(sentences) + 1} about {title}")
        
        # Create items
        items = []
        for i in range(min(num_items, len(sentences))):
            sentence = sentences[i]
            
            # Extract a title from the sentence (first few words)
            words = sentence.split()
            item_title = " ".join(words[:min(3, len(words))])
            
            # Use the rest as description, or the full sentence if it's short
            description = sentence if len(words) <= 3 else " ".join(words[3:])
            
            items.append({
                "title": item_title,
                "description": description
            })
        
        return items
