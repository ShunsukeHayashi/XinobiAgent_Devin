#!/usr/bin/env python3
"""
Script to test if Playwright is running in headless mode in the Heroku environment.
"""
import os
import sys
import argparse
import requests
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_headless_mode(url):
    """Test if Playwright is running in headless mode."""
    logger.info("Testing Playwright headless mode...")
    
    headless_url = f"{url}/api/test_headless"
    try:
        response = requests.get(headless_url, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if result.get("headless"):
                logger.info("✅ Playwright is running in headless mode.")
                return True
            else:
                logger.error("❌ Playwright is not running in headless mode.")
                return False
        else:
            logger.error(f"❌ Headless mode test endpoint returned status code {response.status_code}.")
            logger.error(f"Response: {response.text[:100]}...")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Error testing headless mode: {e}")
        return False

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Test Playwright headless mode in Heroku environment")
    parser.add_argument("--app-name", help="Heroku app name")
    parser.add_argument("--url", help="URL of the deployed application")
    args = parser.parse_args()
    
    if not args.app_name and not args.url:
        logger.error("Error: Either --app-name or --url must be provided.")
        sys.exit(1)
    
    # Determine the URL
    if args.url:
        url = args.url
    else:
        url = f"https://{args.app_name}.herokuapp.com"
    
    # Test if Playwright is running in headless mode
    if not test_headless_mode(url):
        logger.warning("⚠️ Playwright headless mode test failed.")
        logger.warning("This may cause issues in the Heroku environment.")
        sys.exit(1)
    
    logger.info("✅ Playwright headless mode test passed.")
    logger.info("Playwright is correctly configured for the Heroku environment.")

if __name__ == "__main__":
    main()
