import asyncio
from playwright.async_api import async_playwright
import logging
import time
import os
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
            # Create screenshots directory if it doesn't exist
            os.makedirs("/tmp/note_screenshots", exist_ok=True)
            
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
                await self.page.screenshot(path="/tmp/note_screenshots/01_homepage.png")
                
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
                        '[data-testid="login-button"]',
                        'a.p-header__login'
                    ]
                    
                    login_button_found = False
                    for selector in login_selectors:
                        if await self.page.query_selector(selector):
                            logger.info(f"Found login button with selector: {selector}")
                            await self.page.click(selector)
                            login_button_found = True
                            break
                    
                    if not login_button_found:
                        # If no login button found, try direct navigation
                        logger.info("No login button found, trying direct navigation")
                        await self.page.goto(f"{NOTE_BASE_URL}/login")
                    
                    await self.page.wait_for_load_state("networkidle")
                    await asyncio.sleep(2)
                    await self.page.screenshot(path="/tmp/note_screenshots/02_login_page.png")
                    
                    # Check for various login form elements
                    logger.info("Checking login form elements")
                    
                    # Try different selectors for email input
                    email_selectors = [
                        'input[type="email"]',
                        'input[name="email"]',
                        'input[placeholder*="メール"]',
                        'input[placeholder*="email"]',
                        'input.p-login__input'
                    ]
                    
                    email_input_found = False
                    for selector in email_selectors:
                        email_input = await self.page.query_selector(selector)
                        if email_input:
                            logger.info(f"Found email input with selector: {selector}")
                            await self.page.fill(selector, NOTE_USERNAME)
                            email_input_found = True
                            break
                    
                    if not email_input_found:
                        # Try to find any input field
                        all_inputs = await self.page.query_selector_all('input')
                        if len(all_inputs) > 0:
                            logger.info(f"Found {len(all_inputs)} input fields, trying first one")
                            await all_inputs[0].fill(NOTE_USERNAME)
                            email_input_found = True
                    
                    if not email_input_found:
                        logger.error("Email input field not found")
                        html_content = await self.page.content()
                        with open("/tmp/note_screenshots/login_page_html.txt", "w") as f:
                            f.write(html_content)
                        raise Exception("Email input field not found")
                    
                    # Try different selectors for submit button
                    submit_selectors = [
                        'button[type="submit"]',
                        'button.p-login__button',
                        'button:has-text("次へ")',
                        'button:has-text("ログイン")'
                    ]
                    
                    submit_button_found = False
                    for selector in submit_selectors:
                        submit_button = await self.page.query_selector(selector)
                        if submit_button:
                            logger.info(f"Found submit button with selector: {selector}")
                            await self.page.click(selector)
                            submit_button_found = True
                            break
                    
                    if not submit_button_found:
                        logger.error("Submit button not found")
                        raise Exception("Submit button not found")
                    
                    await self.page.wait_for_load_state("networkidle")
                    await asyncio.sleep(2)
                    await self.page.screenshot(path="/tmp/note_screenshots/03_password_page.png")
                    
                    # Try different selectors for password input
                    password_selectors = [
                        'input[type="password"]',
                        'input[name="password"]',
                        'input[placeholder*="パスワード"]',
                        'input[placeholder*="password"]'
                    ]
                    
                    password_input_found = False
                    for selector in password_selectors:
                        password_input = await self.page.query_selector(selector)
                        if password_input:
                            logger.info(f"Found password input with selector: {selector}")
                            await self.page.fill(selector, NOTE_PASSWORD)
                            password_input_found = True
                            break
                    
                    if not password_input_found:
                        # Try to find any input field
                        all_inputs = await self.page.query_selector_all('input')
                        if len(all_inputs) > 0:
                            logger.info(f"Found {len(all_inputs)} input fields, trying first one")
                            await all_inputs[0].fill(NOTE_PASSWORD)
                            password_input_found = True
                    
                    if not password_input_found:
                        logger.error("Password input field not found")
                        raise Exception("Password input field not found")
                    
                    # Try different selectors for login button
                    login_button_selectors = [
                        'button[type="submit"]',
                        'button.p-login__button',
                        'button:has-text("ログイン")',
                        'button:has-text("サインイン")'
                    ]
                    
                    login_button_found = False
                    for selector in login_button_selectors:
                        login_button = await self.page.query_selector(selector)
                        if login_button:
                            logger.info(f"Found login button with selector: {selector}")
                            await self.page.click(selector)
                            login_button_found = True
                            break
                    
                    if not login_button_found:
                        logger.error("Login button not found")
                        raise Exception("Login button not found")
                    
                    await self.page.wait_for_load_state("networkidle")
                    await asyncio.sleep(3)
                    await self.page.screenshot(path="/tmp/note_screenshots/04_logged_in.png")
                    
                except Exception as e:
                    logger.error(f"Error during login process: {str(e)}")
                    # Take screenshot for debugging
                    await self.page.screenshot(path="/tmp/note_screenshots/error.png")
                    raise
                
                # Extract JWT token from cookies
                logger.info("Extracting JWT token")
                cookies = await self.context.cookies()
                
                # Save cookies for debugging
                with open("/tmp/note_screenshots/cookies.txt", "w") as f:
                    for cookie in cookies:
                        f.write(f"{cookie['name']}: {cookie['value']}\n")
                
                for cookie in cookies:
                    if cookie["name"] == "note_gql_auth_token":
                        self.auth_token = cookie["value"]
                        logger.info("JWT token extracted successfully")
                        break
                
                if not self.auth_token:
                    logger.error("Failed to extract JWT token")
                    await self.page.screenshot(path="/tmp/note_screenshots/token_error.png")
                    raise Exception("Failed to extract JWT token")
                
                # Close browser
                await self.browser.close()
                
                return self.auth_token
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            if self.browser:
                await self.browser.close()
            raise
