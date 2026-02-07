"""
Push notification module using ntfy.sh for instant alerts.
"""

import requests
import logging
from typing import Optional
from config import NTFY_SERVER, format_notification

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Notifier:
    """Handles push notifications via ntfy."""
    
    def __init__(self, server: str = NTFY_SERVER):
        self.server = server
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'X-Monitor-Bot/1.0'
        })
    
    def send_notification(self, tweet_url: str, username: str) -> bool:
        """
        Send a push notification about a new tweet.
        
        Args:
            tweet_url: Full URL to the tweet
            username: X username (without @)
        
        Returns:
            True if notification sent successfully, False otherwise
        """
        try:
            notification_data = format_notification(tweet_url, username)
            topic = notification_data.pop('topic')
            
            response = self.session.post(
                f"{self.server}/{topic}",
                json=notification_data,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"✅ Notification sent successfully for {tweet_url}")
                return True
            else:
                logger.error(f"❌ Failed to send notification: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Network error sending notification: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error sending notification: {e}")
            return False
    
    def send_test_notification(self) -> bool:
        """Send a test notification to verify setup."""
        logger.info("Sending test notification...")
        return self.send_notification(
            "https://x.com/test/status/123456789",
            "test_user"
        )


def test_notifier():
    """Test the notifier module."""
    notifier = Notifier()
    success = notifier.send_test_notification()
    if success:
        print("✅ Test notification sent! Check your ntfy app.")
    else:
        print("❌ Failed to send test notification. Check your config.")


if __name__ == "__main__":
    test_notifier()
