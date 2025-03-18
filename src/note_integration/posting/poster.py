import asyncio
from playwright.async_api import async_playwright
import logging
import time
from ..utils.config import NOTE_EDITOR_URL, NOTE_BASE_URL, HEADLESS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NotePoster:
    """Posts articles to note.com using browser automation."""
    
    def __init__(self, auth_token):
        self.auth_token = auth_token
    
    async def post_article(self, article):
        """Post an article to note.com."""
        try:
            logger.info(f"Posting article: {article['title']}")
            
            async with async_playwright() as playwright:
                # Launch browser
                browser = await playwright.chromium.launch(headless=HEADLESS)
                context = await browser.new_context()
                
                # Set auth token cookie
                await context.add_cookies([{
                    "name": "note_gql_auth_token",
                    "value": self.auth_token,
                    "domain": ".note.com",
                    "path": "/"
                }])
                
                page = await context.new_page()
                
                # Navigate to note.com
                await page.goto(f"{NOTE_BASE_URL}")
                
                # Wait for authentication to take effect
                await page.wait_for_load_state("networkidle")
                
                # Navigate to new note page
                await page.goto(f"{NOTE_BASE_URL}/new")
                await page.wait_for_load_state("networkidle")
                
                # Wait for editor to be fully loaded
                await page.wait_for_selector('textarea[placeholder="記事タイトル"]')
                await page.wait_for_selector('[contenteditable="true"]')
                
                # Fill title
                logger.info("Filling title")
                await page.fill('textarea[placeholder="記事タイトル"]', article["title"])
                
                # Fill content
                logger.info("Filling content")
                await page.evaluate(f'document.querySelector("[contenteditable=\\"true\\"]").innerHTML = `{article["content"]}`')
                
                # Verify content was inserted
                content_inserted = await page.evaluate('document.querySelector("[contenteditable=\\"true\\"]").innerHTML')
                if not content_inserted:
                    logger.warning("Content may not have been inserted properly")
                
                # Add tags
                logger.info("Adding tags")
                for tag in article["tags"]:
                    await page.click('button[data-testid="add-tag-button"]')
                    await page.fill('input[placeholder="タグを入力"]', tag)
                    await page.press('input[placeholder="タグを入力"]', "Enter")
                
                # Set visibility to public
                logger.info("Setting visibility to public")
                await page.click('button[data-testid="visibility-selector"]')
                await page.click('button[data-testid="visibility-option-public"]')
                
                # Click publish button
                logger.info("Publishing article")
                await page.click('button span:has-text("公開に進む")')
                
                # Wait for publish to complete
                await page.wait_for_load_state("networkidle")
                
                # Get the URL of the published article
                current_url = page.url
                logger.info(f"Article published at: {current_url}")
                
                # Close browser
                await browser.close()
                
                return current_url
        except Exception as e:
            logger.error(f"Failed to post article: {str(e)}")
            raise
