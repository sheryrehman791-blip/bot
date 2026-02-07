"""
One-time setup script to create authenticated browser session.
Run this once to log into X manually and save the session.
"""

import asyncio
import logging
from playwright.async_api import async_playwright
from config import SESSION_DIR, X_BASE_URL

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def setup_session():
    """Launch browser for manual X login and save session."""
    logger.info("🚀 Starting session setup...")
    logger.info(f"📁 Session will be saved to: {SESSION_DIR}")
    
    playwright = await async_playwright().start()
    
    # Launch browser in headed mode (visible)
    context = await playwright.chromium.launch_persistent_context(
        user_data_dir=str(SESSION_DIR),
        headless=False,  # Must be visible for manual login
        viewport={'width': 1280, 'height': 720}
    )
    
    page = await context.new_page()
    
    logger.info("🌐 Navigating to X login page...")
    await page.goto(f"{X_BASE_URL}/login")
    
    print("\n" + "="*60)
    print("📋 INSTRUCTIONS:")
    print("="*60)
    print("1. Log into your X account in the browser window")
    print("2. Complete any 2FA or verification steps")
    print("3. Wait until you see your home feed")
    print("4. Press ENTER in this terminal to save the session")
    print("="*60 + "\n")
    
    input("Press ENTER after you've logged in...")
    
    logger.info("💾 Saving session...")
    await context.close()
    
    logger.info("✅ Session saved successfully!")
    logger.info(f"📁 Session data stored in: {SESSION_DIR}")
    logger.info("\n🎉 Setup complete! You can now run monitor.py")
    
    await playwright.stop()


if __name__ == "__main__":
    asyncio.run(setup_session())
