#!/usr/bin/env python3
"""
API endpoints for the note.com integration system.
"""
import os
import json
import logging
from typing import Dict, Any, Optional

from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)

async def test_headless_mode() -> Dict[str, Any]:
    """Test if Playwright is running in headless mode."""
    logger.info("Testing Playwright headless mode...")
    
    try:
        async with async_playwright() as p:
            # Launch browser in headless mode
            browser = await p.chromium.launch(headless=True)
            
            # Get browser version
            version = await browser.version()
            
            # Close browser
            await browser.close()
            
            return {
                "headless": True,
                "browser_version": version,
                "status": "success"
            }
    except Exception as e:
        logger.error(f"Error testing headless mode: {str(e)}")
        return {
            "headless": False,
            "error": str(e),
            "status": "error"
        }

async def get_config() -> Dict[str, Any]:
    """Get the application configuration."""
    logger.info("Getting application configuration...")
    
    config = {
        "use_mock": os.environ.get("USE_MOCK", "True").lower() in ["true", "1", "t", "yes"],
        "port": int(os.environ.get("PORT", 8080)),
        "environment": os.environ.get("ENVIRONMENT", "development")
    }
    
    return config

async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "The application is running."
    }

async def status() -> Dict[str, Any]:
    """Status endpoint."""
    return {
        "status": "ok",
        "version": "1.0.0",
        "environment": os.environ.get("ENVIRONMENT", "development"),
        "use_mock": os.environ.get("USE_MOCK", "True").lower() in ["true", "1", "t", "yes"]
    }
