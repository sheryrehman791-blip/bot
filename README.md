# X (Twitter) Account Monitoring Bot

A high-speed Python bot that monitors a specific X (Twitter) account and sends **instant push notifications** (< 10 seconds) when new posts are published.

Perfect for:
- 🪙 Crypto trading signals
- 📢 Exchange listing alerts
- ⚡ Time-sensitive announcements

## Features

- ⚡ **Near real-time detection** (~5-10 second latency)
- 📱 **Instant push notifications** via [ntfy.sh](https://ntfy.sh)
- 🔐 **Persistent browser sessions** (no API keys needed)
- 🎯 **Pinned tweet filtering** (only alerts on new content)
- 🛡️ **Robust error handling** with automatic recovery
- 🔄 **Randomized polling** to avoid detection

## Architecture

```
X Account Posts → Page Updates → Playwright Detects → Push Notification
                                      ↓
                              Compare with last_seen.txt
```

The bot uses:
- **Playwright** for browser automation (headless Chromium)
- **Authenticated sessions** for reliable access
- **ntfy** for instant push notifications
- **Polling-based monitoring** at 5-7 second intervals

## Installation

### 1. Prerequisites

- Python 3.8+
- pip

### 2. Clone & Install

```bash
cd d:\bot
pip install -r requirements.txt
playwright install chromium
```

### 3. Configure

Edit `config.py`:

```python
# Set your target account
TARGET_USERNAME = "elonmusk"  # Change this

# Set a private ntfy topic (use a random string!)
NTFY_TOPIC = "x-alerts-a8f3k2m9p1q7"  # Change this to something random
```

> [!IMPORTANT]
> Use a long, random topic name for ntfy to prevent unauthorized access to your notifications.

## Setup

### Step 1: Create Browser Session

Run the setup script to log into X once:

```bash
python session_setup.py
```

This will:
1. Open a browser window
2. Navigate to X login page
3. Wait for you to log in manually
4. Save your session to `session/` directory

### Step 2: Install ntfy App

On your phone:
- **iOS**: Download [ntfy](https://apps.apple.com/app/ntfy/id1625396347) from App Store
- **Android**: Download [ntfy](https://play.google.com/store/apps/details?id=io.heckel.ntfy) from Play Store

Subscribe to your topic (the one you set in `config.py`).

### Step 3: Test Notifications

```bash
python notifier.py
```

You should receive a test notification on your phone!

## Usage

### Start Monitoring

```bash
python monitor.py
```

The bot will:
1. Load your saved browser session
2. Navigate to the target account's profile
3. Check for new tweets every 5-7 seconds
4. Send push notifications when new posts are detected
5. Log all activity to console

### Stop Monitoring

Press `Ctrl+C` to stop the bot gracefully.

### Deploy to Cloud (24/7 Monitoring)

Want the bot to run continuously without your computer? Deploy to Railway, Render, or Fly.io!

See the **[Deployment Guide](DEPLOYMENT.md)** for step-by-step instructions.

**Quick Deploy to Railway:**
1. Push code to GitHub
2. Connect to Railway
3. Set environment variables
4. Deploy! 🚀

## How It Works

### Tweet Detection

1. **Page Load**: Loads the X profile page using authenticated session
2. **Element Selection**: Finds all tweet articles on the page
3. **Pinned Filter**: Skips any tweets marked as "Pinned"
4. **ID Extraction**: Extracts tweet ID from the URL
5. **Comparison**: Compares with last seen ID from `last_seen.txt`
6. **Notification**: If new, sends push notification and updates file

### Polling Strategy

- **Interval**: 5-7 seconds (randomized)
- **Randomization**: Avoids detection patterns
- **Expected Latency**: 6-10 seconds total

| Stage             | Time    |
|-------------------|---------|
| Tweet posted      | 0 sec   |
| X page update     | 1-3 sec |
| Bot detection     | 5-8 sec |
| Push notification | <1 sec  |

## File Structure

```
bot/
├── monitor.py          # Core monitoring engine
├── notifier.py         # Push notification handler
├── session_setup.py    # One-time session creation
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── session/            # Browser session data (auto-created)
├── last_seen.txt       # Last detected tweet ID (auto-created)
└── README.md          # This file
```

## Configuration Options

### `config.py`

| Setting | Description | Default |
|---------|-------------|---------|
| `TARGET_USERNAME` | X account to monitor | `"elonmusk"` |
| `POLL_INTERVAL_MIN` | Minimum seconds between checks | `5` |
| `POLL_INTERVAL_MAX` | Maximum seconds between checks | `7` |
| `NTFY_TOPIC` | Your private ntfy topic | `"x-alerts-..."` |
| `HEADLESS` | Run browser in background | `True` |

## Troubleshooting

### "No tweets found"

- Ensure you're logged in (run `session_setup.py` again)
- Check that the target account is public or you follow them
- Try setting `HEADLESS = False` in config.py to see what's happening

### "Failed to send notification"

- Verify your `NTFY_TOPIC` is set correctly
- Check your internet connection
- Test with `python notifier.py`

### "Browser timeout"

- Increase `BROWSER_TIMEOUT` in config.py
- Check your internet speed
- Try running with `HEADLESS = False` to debug

### Session expired

- Delete the `session/` directory
- Run `python session_setup.py` again to re-login

## Security Best Practices

✅ **DO:**
- Use a long, random ntfy topic name
- Keep `session/` directory private
- Run on a secure VPS or local machine
- Restrict file permissions on sensitive files

❌ **DON'T:**
- Share your ntfy topic publicly
- Commit `session/` to git (already in .gitignore)
- Use the bot to spam or violate X's Terms of Service

## Future Enhancements

Potential upgrades:

- 🔢 **Multi-account monitoring** (watch multiple accounts)
- 🚀 **Faster detection** (network request interception)
- 📊 **Trading integration** (webhook triggers)
- 💬 **Alternative notifications** (Telegram, Discord, SMS)
- 📈 **Analytics** (track posting patterns)

## Performance

Tested performance:
- **CPU**: ~2-5% (idle), ~10-15% (during page load)
- **Memory**: ~150-200 MB
- **Network**: ~1-2 MB per check

## License

MIT License - Use at your own risk. This bot is for educational purposes.

## Disclaimer

This bot is not affiliated with X (Twitter). Use responsibly and in accordance with X's Terms of Service. The author is not responsible for any account restrictions or bans resulting from use of this software.

---

**Built for speed. Optimized for crypto.**
