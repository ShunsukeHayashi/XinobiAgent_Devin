import asyncio
import sys
import os
import logging
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.note_integration.auth.authenticator import NoteAuthenticator
from src.note_integration.api.note_api import NoteAPI
from src.note_integration.seo.analyzer import SEOAnalyzer
from src.note_integration.content.generator import ContentGenerator
from src.note_integration.posting.poster import NotePoster
from src.note_integration.utils.config import NOTE_USERNAME

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_authentication():
    """Test authentication with note.com."""
    try:
        logger.info("Testing authentication")
        authenticator = NoteAuthenticator()
        auth_token = await authenticator.login()
        
        if auth_token:
            logger.info("Authentication successful")
            return auth_token
        else:
            logger.error("Authentication failed")
            return None
    except Exception as e:
        logger.error(f"Authentication test failed: {str(e)}")
        return None

async def test_api_interaction(auth_token):
    """Test API interaction with note.com."""
    try:
        logger.info("Testing API interaction")
        note_api = NoteAPI(auth_token)
        
        # Get creator info
        creator_info = note_api.get_creator_info(NOTE_USERNAME)
        if creator_info and "data" in creator_info and "id" in creator_info["data"]:
            logger.info(f"API interaction successful - Creator ID: {creator_info['data']['id']}")
            return note_api
        else:
            logger.error("API interaction failed")
            return None
    except Exception as e:
        logger.error(f"API interaction test failed: {str(e)}")
        return None

async def test_seo_analysis(note_api):
    """Test SEO analysis of competitor content."""
    try:
        logger.info("Testing SEO analysis")
        seo_analyzer = SEOAnalyzer(note_api)
        
        # Test category
        test_category = "programming"
        
        # Analyze competitors
        seo_analysis = seo_analyzer.analyze_competitors(test_category)
        
        if seo_analysis:
            logger.info("SEO analysis successful")
            logger.info(f"Top keywords: {list(seo_analysis['top_keywords'].keys())[:5]}")
            return seo_analysis
        else:
            logger.error("SEO analysis failed")
            return None
    except Exception as e:
        logger.error(f"SEO analysis test failed: {str(e)}")
        return None

def test_content_generation(seo_analysis):
    """Test content generation based on SEO analysis."""
    try:
        logger.info("Testing content generation")
        content_generator = ContentGenerator()
        
        # Test theme
        test_theme = "Python programming tips"
        
        # Generate article
        article = content_generator.generate_article(test_theme, seo_analysis)
        
        if article and "title" in article and "content" in article and "tags" in article:
            logger.info("Content generation successful")
            logger.info(f"Title: {article['title']}")
            logger.info(f"Content length: {len(article['content'])} characters")
            logger.info(f"Tags: {article['tags']}")
            return article
        else:
            logger.error("Content generation failed")
            return None
    except Exception as e:
        logger.error(f"Content generation test failed: {str(e)}")
        return None

async def test_article_posting(auth_token, article):
    """Test article posting to note.com."""
    try:
        logger.info("Testing article posting")
        note_poster = NotePoster(auth_token)
        
        # Post article
        article_url = await note_poster.post_article(article)
        
        if article_url:
            logger.info("Article posting successful")
            logger.info(f"Article URL: {article_url}")
            return article_url
        else:
            logger.error("Article posting failed")
            return None
    except Exception as e:
        logger.error(f"Article posting test failed: {str(e)}")
        return None

async def run_tests():
    """Run all tests."""
    # Test authentication
    auth_token = await test_authentication()
    if not auth_token:
        logger.error("Authentication test failed, aborting further tests")
        return False
    
    # Test API interaction
    note_api = await test_api_interaction(auth_token)
    if not note_api:
        logger.error("API interaction test failed, aborting further tests")
        return False
    
    # Test SEO analysis
    seo_analysis = await test_seo_analysis(note_api)
    if not seo_analysis:
        logger.error("SEO analysis test failed, aborting further tests")
        return False
    
    # Test content generation
    article = test_content_generation(seo_analysis)
    if not article:
        logger.error("Content generation test failed, aborting further tests")
        return False
    
    # Test article posting
    article_url = await test_article_posting(auth_token, article)
    if not article_url:
        logger.error("Article posting test failed")
        return False
    
    logger.info("All tests passed successfully")
    return True

if __name__ == "__main__":
    result = asyncio.run(run_tests())
    if result:
        print("All tests passed successfully")
    else:
        print("Tests failed")
