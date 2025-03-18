#!/usr/bin/env python3
"""
Test script for note.com integration web UI.
"""
import os
import sys
import logging
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.note_integration.web.app import NoteWebUI

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_web_ui():
    """Test the web UI functionality."""
    try:
        # Set environment variables if not already set
        if not os.environ.get("NOTE_USERNAME"):
            os.environ["NOTE_USERNAME"] = "shunsuke_ai"
        
        if not os.environ.get("NOTE_PASSWORD"):
            os.environ["NOTE_PASSWORD"] = "Jin156762syun@"
        
        if not os.environ.get("OPENAI_API_KEY") and os.environ.get("API_Key"):
            api_key = os.environ.get("API_Key")
            if api_key:
                os.environ["OPENAI_API_KEY"] = api_key
        
        # Create web UI instance
        ui = NoteWebUI()
        
        # Test initialization
        logger.info("Testing initialization...")
        init_result = await ui.initialize()
        logger.info(f"Initialization result: {init_result}")
        
        if "❌" in init_result:
            logger.error("Initialization failed")
            return False
        
        # Test SEO analysis
        logger.info("Testing SEO analysis...")
        category = "programming"
        seo_result = await ui.analyze_seo(category)
        logger.info(f"SEO analysis result: {seo_result}")
        
        if "❌" in seo_result:
            logger.error("SEO analysis failed")
            return False
        
        logger.info("All tests passed successfully")
        return True
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    import asyncio
    result = asyncio.run(test_web_ui())
    if result:
        print("All tests passed successfully")
    else:
        print("Tests failed")
