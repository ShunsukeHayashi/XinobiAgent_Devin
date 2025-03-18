import asyncio
import sys
import os
import logging
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.note_integration.utils.config import NOTE_USERNAME, NOTE_PASSWORD, NOTE_BASE_URL, OPENAI_API_KEY

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_config():
    """Test configuration loading."""
    try:
        logger.info("Testing configuration loading")
        
        # Check if credentials are loaded
        if NOTE_USERNAME and NOTE_PASSWORD:
            logger.info("Note.com credentials loaded successfully")
        else:
            logger.error("Failed to load note.com credentials")
            return False
        
        # Check if OpenAI API key is loaded
        if OPENAI_API_KEY:
            logger.info("OpenAI API key loaded successfully")
        else:
            logger.error("Failed to load OpenAI API key")
            return False
        
        logger.info("Configuration test passed")
        return True
    except Exception as e:
        logger.error(f"Configuration test failed: {str(e)}")
        return False

async def run_tests():
    """Run all tests."""
    # Test configuration
    config_result = await test_config()
    if not config_result:
        logger.error("Configuration test failed, aborting further tests")
        return False
    
    logger.info("Basic tests passed successfully")
    return True

if __name__ == "__main__":
    result = asyncio.run(run_tests())
    if result:
        print("All basic tests passed successfully")
    else:
        print("Basic tests failed")
