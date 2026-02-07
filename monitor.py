"""
Core monitoring engine for X (Twitter) account tracking.
Uses Playwright to monitor account pages and detect new tweets.
"""

import asyncio
import logging
import random
import re
from pathlib import Path
from typing import Optional
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

from config import (
    TARGET_USERNAME,
    X_PROFILE_URL,
    SESSION_DIR,
    LAST_SEEN_FILE,
    POLL_INTERVAL_MIN,
    POLL_INTERVAL_MAX,
    HEADLESS,
    BROWSER_TIMEOUT
)
from notifier import Notifier

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class XMonitor:
    """Monitors an X account for new tweets."""
    
    def __init__(self):
        self.notifier = Notifier()
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.last_seen_id: Optional[str] = None
        
    async def initialize_browser(self):
        """Initialize Playwright browser with persistent session."""
        logger.info("🚀 Initializing browser...")
        
        playwright = await async_playwright().start()
        
        # Launch browser with persistent context and memory optimizations
        self.context = await playwright.chromium.launch_persistent_context(
            user_data_dir=str(SESSION_DIR),
            headless=HEADLESS,
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            # Memory optimization flags
            args=[
                '--disable-dev-shm-usage',  # Overcome limited resource problems
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',  # Required for Docker
                '--disable-setuid-sandbox',
                '--disable-gpu',  # Reduce memory usage
                '--disable-software-rasterizer',
                '--disable-extensions',
                '--disable-background-networking',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-breakpad',
                '--disable-component-extensions-with-background-pages',
                '--disable-features=TranslateUI,BlinkGenPropertyTrees',
                '--disable-ipc-flooding-protection',
                '--disable-renderer-backgrounding',
                '--enable-features=NetworkService,NetworkServiceInProcess',
                '--force-color-profile=srgb',
                '--hide-scrollbars',
                '--metrics-recording-only',
                '--mute-audio',
                '--no-first-run',
                '--disable-crash-reporter',
            ]
        )
        
        # Set default timeout
        self.context.set_default_timeout(BROWSER_TIMEOUT)
        
        # Create or get page
        if len(self.context.pages) > 0:
            self.page = self.context.pages[0]
        else:
            self.page = await self.context.new_page()
        
        logger.info("✅ Browser initialized")
    
    def load_last_seen_id(self) -> Optional[str]:
        """Load the last seen tweet ID from disk."""
        if LAST_SEEN_FILE.exists():
            try:
                last_id = LAST_SEEN_FILE.read_text().strip()
                logger.info(f"📖 Loaded last seen ID: {last_id}")
                return last_id
            except Exception as e:
                logger.error(f"❌ Error loading last seen ID: {e}")
        return None
    
    def save_last_seen_id(self, tweet_id: str):
        """Save the last seen tweet ID to disk."""
        try:
            LAST_SEEN_FILE.write_text(tweet_id)
            logger.info(f"💾 Saved last seen ID: {tweet_id}")
        except Exception as e:
            logger.error(f"❌ Error saving last seen ID: {e}")
    
    async def extract_latest_tweet_id(self) -> Optional[str]:
        """
        Extract the latest non-pinned tweet ID from the page.
        
        Returns:
            Tweet ID string or None if no tweets found
        """
        try:
            # Wait for tweets to load
            await self.page.wait_for_selector('article[data-testid="tweet"]', timeout=10000)
            
            # Get all tweet articles
            tweets = await self.page.query_selector_all('article[data-testid="tweet"]')
            
            for tweet in tweets:
                # Check if tweet is pinned
                pinned_label = await tweet.query_selector('[data-testid="socialContext"]')
                if pinned_label:
                    pinned_text = await pinned_label.inner_text()
                    if "Pinned" in pinned_text:
                        logger.debug("⏭️  Skipping pinned tweet")
                        continue
                
                # Extract tweet URL
                link = await tweet.query_selector('a[href*="/status/"]')
                if link:
                    href = await link.get_attribute('href')
                    # Extract tweet ID from URL: /username/status/1234567890
                    match = re.search(r'/status/(\d+)', href)
                    if match:
                        tweet_id = match.group(1)
                        logger.debug(f"🔍 Found tweet ID: {tweet_id}")
                        return tweet_id
            
            logger.warning("⚠️  No non-pinned tweets found")
            return None
            
        except Exception as e:
            logger.error(f"❌ Error extracting tweet ID: {e}")
            return None
    
    async def check_for_new_tweet(self) -> bool:
        """
        Check if there's a new tweet and send notification if found.
        
        Returns:
            True if new tweet detected, False otherwise
        """
        try:
            # Reload the page to get latest content
            logger.info(f"🔄 Reloading {X_PROFILE_URL}")
            await self.page.goto(X_PROFILE_URL, wait_until='networkidle')
            
            # Extract latest tweet ID
            latest_id = await self.extract_latest_tweet_id()
            
            if not latest_id:
                logger.warning("⚠️  Could not extract tweet ID")
                return False
            
            # Check if this is a new tweet
            if self.last_seen_id is None:
                # First run - just save the ID
                logger.info(f"🆕 First run - setting baseline: {latest_id}")
                self.last_seen_id = latest_id
                self.save_last_seen_id(latest_id)
                return False
            
            if latest_id != self.last_seen_id:
                # New tweet detected!
                tweet_url = f"{X_PROFILE_URL}/status/{latest_id}"
                logger.info(f"🎉 NEW TWEET DETECTED: {tweet_url}")
                
                # Send notification
                self.notifier.send_notification(tweet_url, TARGET_USERNAME)
                
                # Update last seen ID
                self.last_seen_id = latest_id
                self.save_last_seen_id(latest_id)
                
                return True
            else:
                logger.info(f"✓ No new tweets (latest: {latest_id})")
                return False
                
        except Exception as e:
            error_msg = str(e)
            
            # Check if it's a page crash
            if "Page crashed" in error_msg or "Target closed" in error_msg:
                logger.error(f"❌ Browser crashed: {error_msg}")
                logger.info("🔄 Reinitializing browser...")
                
                try:
                    # Close crashed context
                    if self.context:
                        await self.context.close()
                    
                    # Reinitialize browser
                    await self.initialize_browser()
                    logger.info("✅ Browser reinitialized successfully")
                    
                except Exception as reinit_error:
                    logger.error(f"❌ Failed to reinitialize browser: {reinit_error}")
            else:
                logger.error(f"❌ Error checking for new tweet: {e}")
            
            return False
    
    async def run(self):
        """Main monitoring loop."""
        logger.info(f"👀 Starting monitor for @{TARGET_USERNAME}")
        
        try:
            # Initialize browser
            await self.initialize_browser()
            
            # Load last seen ID
            self.last_seen_id = self.load_last_seen_id()
            
            # Main loop
            while True:
                await self.check_for_new_tweet()
                
                # Random delay to avoid detection
                delay = random.uniform(POLL_INTERVAL_MIN, POLL_INTERVAL_MAX)
                logger.info(f"⏳ Waiting {delay:.1f} seconds...")
                await asyncio.sleep(delay)
                
        except KeyboardInterrupt:
            logger.info("⏹️  Monitoring stopped by user")
        except Exception as e:
            logger.error(f"❌ Fatal error: {e}")
            raise
        finally:
            if self.context:
                await self.context.close()
                logger.info("🔒 Browser closed")


async def main():
    """Entry point for the monitoring bot."""
    monitor = XMonitor()
    await monitor.run()


if __name__ == "__main__":
    asyncio.run(main())
