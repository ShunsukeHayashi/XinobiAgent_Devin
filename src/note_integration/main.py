import asyncio
import argparse
import logging
from .auth.authenticator import NoteAuthenticator
from .api.note_api import NoteAPI
from .seo.analyzer import SEOAnalyzer
from .content.generator import ContentGenerator
from .posting.poster import NotePoster
from .utils.config import NOTE_USERNAME

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NoteIntegration:
    """Main application for note.com integration."""
    
    def __init__(self):
        self.auth_token = None
        self.note_api = None
        self.seo_analyzer = None
        self.content_generator = None
        self.note_poster = None
    
    async def initialize(self):
        """Initialize all components."""
        try:
            # Authenticate with note.com
            logger.info("Authenticating with note.com")
            authenticator = NoteAuthenticator()
            self.auth_token = await authenticator.login()
            
            # Initialize API client
            self.note_api = NoteAPI(self.auth_token)
            
            # Initialize SEO analyzer
            self.seo_analyzer = SEOAnalyzer(self.note_api)
            
            # Initialize content generator
            self.content_generator = ContentGenerator()
            
            # Initialize note poster
            self.note_poster = NotePoster(self.auth_token)
            
            logger.info("Initialization complete")
            return True
        except Exception as e:
            logger.error(f"Initialization failed: {str(e)}")
            return False
    
    async def run(self, theme, category):
        """Run the complete workflow."""
        try:
            # Initialize components
            init_success = await self.initialize()
            if not init_success:
                logger.error("Failed to initialize components")
                return False
            
            # Get creator info
            logger.info(f"Getting creator info for {NOTE_USERNAME}")
            if self.note_api is None:
                logger.error("API client not initialized")
                return False
            creator_info = self.note_api.get_creator_info(NOTE_USERNAME)
            logger.info(f"Creator ID: {creator_info['data']['id']}")
            
            # Analyze competitors
            logger.info(f"Analyzing competitors in category: {category}")
            if self.seo_analyzer is None:
                logger.error("SEO analyzer not initialized")
                return False
            seo_analysis = self.seo_analyzer.analyze_competitors(category)
            if not seo_analysis:
                logger.error("Failed to analyze competitors")
                return False
            
            # Generate article
            logger.info(f"Generating article for theme: {theme}")
            if self.content_generator is None:
                logger.error("Content generator not initialized")
                return False
            article = self.content_generator.generate_article(theme, seo_analysis)
            if not article:
                logger.error("Failed to generate article")
                return False
            
            # Post article
            logger.info("Posting article to note.com")
            if self.note_poster is None:
                logger.error("Note poster not initialized")
                return False
            article_url = await self.note_poster.post_article(article)
            
            logger.info(f"Article posted successfully: {article_url}")
            return article_url
        except Exception as e:
            logger.error(f"Workflow failed: {str(e)}")
            return False

async def main():
    """Command-line interface for note.com integration."""
    parser = argparse.ArgumentParser(description="Automated note.com article posting")
    parser.add_argument("--theme", required=True, help="Theme for article generation")
    parser.add_argument("--category", required=True, help="Category for SEO analysis")
    args = parser.parse_args()
    
    integration = NoteIntegration()
    result = await integration.run(args.theme, args.category)
    
    if result:
        print(f"Article posted successfully: {result}")
    else:
        print("Failed to post article")

if __name__ == "__main__":
    asyncio.run(main())
