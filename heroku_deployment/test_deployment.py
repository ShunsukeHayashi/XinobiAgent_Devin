#!/usr/bin/env python3
"""
Script to test the Heroku deployment of the note.com integration system.
"""
import os
import sys
import argparse
import requests
import time
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_url(url, max_retries=5, retry_delay=5):
    """Test if a URL is accessible."""
    logger.info(f"Testing URL: {url}")
    
    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                logger.info(f"✅ URL is accessible: {url}")
                return True
            else:
                logger.warning(f"⚠️ URL returned status code {response.status_code}: {url}")
                logger.warning(f"Response: {response.text[:100]}...")
        except requests.exceptions.RequestException as e:
            logger.warning(f"⚠️ Error accessing URL: {e}")
        
        if i < max_retries - 1:
            logger.info(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
    
    logger.error(f"❌ URL is not accessible after {max_retries} retries: {url}")
    return False

def test_gradio_interface(url):
    """Test if the Gradio interface is working."""
    logger.info("Testing Gradio interface...")
    
    try:
        response = requests.get(url, timeout=30)
        if "gradio" in response.text.lower():
            logger.info("✅ Gradio interface detected.")
            return True
        else:
            logger.error("❌ Gradio interface not detected.")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Error testing Gradio interface: {e}")
        return False

def test_initialization(url):
    """Test the initialization functionality."""
    logger.info("Testing initialization functionality...")
    
    init_url = f"{url}/api/initialize"
    try:
        response = requests.post(init_url, json={"use_mock": True}, timeout=30)
        if response.status_code == 200:
            logger.info("✅ Initialization API endpoint is working.")
            return True
        else:
            logger.error(f"❌ Initialization API endpoint returned status code {response.status_code}.")
            logger.error(f"Response: {response.text[:100]}...")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Error testing initialization API endpoint: {e}")
        return False

def test_seo_analysis(url):
    """Test the SEO analysis functionality."""
    logger.info("Testing SEO analysis functionality...")
    
    seo_url = f"{url}/api/analyze_seo"
    try:
        response = requests.post(seo_url, json={"category": "programming"}, timeout=30)
        if response.status_code == 200:
            logger.info("✅ SEO analysis API endpoint is working.")
            return True
        else:
            logger.error(f"❌ SEO analysis API endpoint returned status code {response.status_code}.")
            logger.error(f"Response: {response.text[:100]}...")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Error testing SEO analysis API endpoint: {e}")
        return False

def test_article_generation(url):
    """Test the article generation functionality."""
    logger.info("Testing article generation functionality...")
    
    generate_url = f"{url}/api/generate_article"
    try:
        response = requests.post(
            generate_url,
            json={
                "theme": "Python programming",
                "category": "programming"
            },
            timeout=60
        )
        if response.status_code == 200:
            logger.info("✅ Article generation API endpoint is working.")
            return True
        else:
            logger.error(f"❌ Article generation API endpoint returned status code {response.status_code}.")
            logger.error(f"Response: {response.text[:100]}...")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Error testing article generation API endpoint: {e}")
        return False

def test_article_posting(url):
    """Test the article posting functionality."""
    logger.info("Testing article posting functionality...")
    
    post_url = f"{url}/api/post_article"
    try:
        response = requests.post(
            post_url,
            json={
                "title": "Test Article",
                "content": "<h1>Test Article</h1><p>This is a test article.</p>",
                "tags": ["test", "article"]
            },
            timeout=60
        )
        if response.status_code == 200:
            logger.info("✅ Article posting API endpoint is working.")
            return True
        else:
            logger.error(f"❌ Article posting API endpoint returned status code {response.status_code}.")
            logger.error(f"Response: {response.text[:100]}...")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Error testing article posting API endpoint: {e}")
        return False

def test_environment_variables(url):
    """Test if the application is using environment variables correctly."""
    logger.info("Testing environment variables...")
    
    env_url = f"{url}/api/config"
    try:
        response = requests.get(env_url, timeout=30)
        if response.status_code == 200:
            config = response.json()
            logger.info("✅ Configuration API endpoint is working.")
            
            # Check if USE_MOCK is set correctly
            if "use_mock" in config:
                logger.info(f"✅ USE_MOCK environment variable is set to: {config['use_mock']}")
            else:
                logger.warning("⚠️ USE_MOCK environment variable is not set.")
            
            return True
        else:
            logger.error(f"❌ Configuration API endpoint returned status code {response.status_code}.")
            logger.error(f"Response: {response.text[:100]}...")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Error testing configuration API endpoint: {e}")
        return False

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Test Heroku deployment of note.com integration system")
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
    
    # Test if the URL is accessible
    if not test_url(url):
        sys.exit(1)
    
    # Test if the Gradio interface is working
    if not test_gradio_interface(url):
        sys.exit(1)
    
    # Test the initialization functionality
    if not test_initialization(url):
        logger.warning("⚠️ Initialization functionality test failed.")
    
    # Test the SEO analysis functionality
    if not test_seo_analysis(url):
        logger.warning("⚠️ SEO analysis functionality test failed.")
    
    # Test the article generation functionality
    if not test_article_generation(url):
        logger.warning("⚠️ Article generation functionality test failed.")
    
    # Test the article posting functionality
    if not test_article_posting(url):
        logger.warning("⚠️ Article posting functionality test failed.")
    
    # Test if the application is using environment variables correctly
    if not test_environment_variables(url):
        logger.warning("⚠️ Environment variables test failed.")
    
    logger.info("✅ Deployment testing completed.")
    logger.info(f"The application is accessible at: {url}")

if __name__ == "__main__":
    main()
