#!/usr/bin/env python3
"""
Test script for Heroku deployment of the note.com integration system.
"""
import os
import sys
import logging
import asyncio
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.note_integration.web.app import NoteWebUI
from src.note_integration.web.api_endpoints import test_headless_mode, get_config, health_check, status

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_heroku_deployment():
    """Test the Heroku deployment."""
    try:
        # Test headless mode
        logger.info("Testing headless mode...")
        headless_result = await test_headless_mode()
        logger.info(f"Headless mode result: {headless_result}")
        
        if not headless_result.get("headless"):
            logger.error("❌ Headless mode test failed.")
            return False
        
        # Test configuration
        logger.info("Testing configuration...")
        config_result = await get_config()
        logger.info(f"Configuration result: {config_result}")
        
        # Test health check
        logger.info("Testing health check...")
        health_result = await health_check()
        logger.info(f"Health check result: {health_result}")
        
        # Test status
        logger.info("Testing status...")
        status_result = await status()
        logger.info(f"Status result: {status_result}")
        
        # Test web UI
        logger.info("Testing web UI...")
        ui = NoteWebUI(use_mock=True)
        
        # Test initialization
        logger.info("Testing initialization...")
        init_result = await ui.initialize()
        logger.info(f"Initialization result: {init_result}")
        
        if "❌" in init_result:
            logger.error("❌ Initialization test failed.")
            return False
        
        # Test SEO analysis
        logger.info("Testing SEO analysis...")
        category = "programming"
        seo_result = await ui.analyze_seo(category)
        logger.info(f"SEO analysis result: {seo_result}")
        
        if "❌" in seo_result:
            logger.error("❌ SEO analysis test failed.")
            return False
        
        logger.info("All tests passed successfully.")
        return True
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_heroku_deployment())
    if result:
        print("✅ All tests passed successfully.")
        sys.exit(0)
    else:
        print("❌ Tests failed.")
        sys.exit(1)
