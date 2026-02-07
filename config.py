"""
Configuration settings for the X (Twitter) monitoring bot.
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Target X account to monitor
TARGET_USERNAME = os.getenv("TARGET_USERNAME", "brenthewolf")  # Change this to your target account

# Polling settings
POLL_INTERVAL_MIN = int(os.getenv("POLL_INTERVAL_MIN", "5"))  # Minimum seconds between checks
POLL_INTERVAL_MAX = int(os.getenv("POLL_INTERVAL_MAX", "7"))  # Maximum seconds between checks

# Notification settings
NTFY_TOPIC = os.getenv("NTFY_TOPIC", "x-alerts-change-this-to-random-string")  # IMPORTANT: Change to a random, private topic
NTFY_SERVER = "https://ntfy.sh"  # Default ntfy server

# Browser session settings
SESSION_DIR = BASE_DIR / "session"
SESSION_DIR.mkdir(exist_ok=True)

# Persistence
LAST_SEEN_FILE = BASE_DIR / "last_seen.txt"

# X URLs
X_BASE_URL = "https://x.com"
X_PROFILE_URL = f"{X_BASE_URL}/{TARGET_USERNAME}"

# Browser settings
HEADLESS = os.getenv("HEADLESS", "True").lower() == "true"  # Set to False for debugging
BROWSER_TIMEOUT = 30000  # 30 seconds

# Notification message template
def format_notification(tweet_url: str, username: str) -> dict:
    """Format notification message for ntfy."""
    return {
        "topic": NTFY_TOPIC,
        "title": f"🐦 New post from @{username}",
        "message": f"Check it out: {tweet_url}",
        "priority": 4,  # High priority
        "tags": ["bird", "twitter"],
        "click": tweet_url  # Make notification clickable
    }
