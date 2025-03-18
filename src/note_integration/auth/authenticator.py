import asyncio
from playwright.async_api import async_playwright
import logging
import time
from ..utils.config import NOTE_USERNAME, NOTE_PASSWORD, NOTE_BASE_URL, HEADLESS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NoteAuthenticator:
    """Handles authentication with note.com and extracts JWT token."""
    
    def __init__(self):
        self.auth_token = None
        self.browser = None
        self.context = None
        self.page = None
    
    async def login(self):
        """Login to note.com and extract JWT token."""
        try:
            async with async_playwright() as playwright:
                # Launch browser
                self.browser = await playwright.chromium.launch(headless=HEADLESS)
                self.context = await self.browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                )
                self.page = await self.context.new_page()
                
                # Navigate to note.com
                logger.info("Navigating to note.com")
                await self.page.goto(f"{NOTE_BASE_URL}")
                await self.page.wait_for_load_state("networkidle")
                
                # Wait a moment to mimic human behavior
                await asyncio.sleep(2)
                
                # Try to find and click login button
                logger.info("Looking for login button")
                try:
                    # Try different selectors for login button
                    login_selectors = [
                        'a[href="/login"]',
                        'a:has-text("ログイン")',
                        'button:has-text("ログイン")',
                        '[data-testid="login-button"]'
                    ]
                    
                    for selector in login_selectors:
                        if await self.page.query_selector(selector):
                            logger.info(f"Found login button with selector: {selector}")
                            await self.page.click(selector)
                            break
                    else:
                        # If no login button found, try direct navigation
                        logger.info("No login button found, trying direct navigation")
                        await self.page.goto(f"{NOTE_BASE_URL}/login")
                    
                    await self.page.wait_for_load_state("networkidle")
                    await asyncio.sleep(2)
                    
                    # Fill login form
                    logger.info("Filling login form")
                    if await self.page.query_selector('input[type="email"]'):
                        await self.page.fill('input[type="email"]', NOTE_USERNAME)
                        await asyncio.sleep(1)
                        await self.page.click('button[type="submit"]')
                        await self.page.wait_for_load_state("networkidle")
                        await asyncio.sleep(2)
                        
                        # Fill password form
                        if await self.page.query_selector('input[type="password"]'):
                            await self.page.fill('input[type="password"]', NOTE_PASSWORD)
                            await asyncio.sleep(1)
                            await self.page.click('button[type="submit"]')
                            await self.page.wait_for_load_state("networkidle")
                            await asyncio.sleep(3)
                    else:
                        logger.error("Email input field not found")
                        raise Exception("Email input field not found")
                    
                except Exception as e:
                    logger.error(f"Error during login process: {str(e)}")
                    # Take screenshot for debugging
                    await self.page.screenshot(path="/tmp/login_error.png")
                    raise
                
                # Extract JWT token from cookies
                logger.info("Extracting JWT token")
                cookies = await self.context.cookies()
                for cookie in cookies:
                    if cookie["name"] == "note_gql_auth_token":
                        self.auth_token = cookie["value"]
                        logger.info("JWT token extracted successfully")
                        break
                
                if not self.auth_token:
                    logger.error("Failed to extract JWT token")
                    await self.page.screenshot(path="/tmp/token_error.png")
                    raise Exception("Failed to extract JWT token")
                
                # Close browser
                await self.browser.close()
                
                return self.auth_token
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            if self.browser:
                await self.browser.close()
            raise
