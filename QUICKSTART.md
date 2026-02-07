# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Configure Your Bot

Edit `config.py`:

```python
# Set the X account you want to monitor
TARGET_USERNAME = "elonmusk"  # Change this!

# Set a PRIVATE ntfy topic (make it random!)
NTFY_TOPIC = "x-alerts-a8f3k2m9p1q7"  # Change this!
```

### Step 2: Set Up Your Browser Session

Run the session setup script:

```bash
py session_setup.py
```

This will:
1. Open a browser window
2. Take you to X login page
3. Wait for you to log in manually
4. Save your session for future use

**Important**: Complete any 2FA verification if prompted.

### Step 3: Install ntfy on Your Phone

- **iOS**: [Download from App Store](https://apps.apple.com/app/ntfy/id1625396347)
- **Android**: [Download from Play Store](https://play.google.com/store/apps/details?id=io.heckel.ntfy)

Open the app and subscribe to your topic (the one you set in `config.py`).

### Step 4: Test Notifications

```bash
py notifier.py
```

You should receive a test notification on your phone! ✅

### Step 5: Start Monitoring

```bash
py monitor.py
```

That's it! The bot is now watching for new tweets. 🎉

---

## 📱 Notification Example

When a new tweet is detected, you'll receive:

- **Title**: 🐦 New post from @username
- **Message**: Check it out: [tweet URL]
- **Click**: Opens the tweet directly

---

## ⚙️ Customization

### Change Polling Speed

In `config.py`:

```python
POLL_INTERVAL_MIN = 3  # Faster (more aggressive)
POLL_INTERVAL_MAX = 5
```

**Warning**: Too fast may trigger rate limits!

### Monitor Different Account

In `config.py`:

```python
TARGET_USERNAME = "binance"  # Any public account
```

### Debug Mode

To see what the browser is doing:

In `config.py`:

```python
HEADLESS = False  # Shows browser window
```

---

## 🔧 Troubleshooting

### "No tweets found"

- Make sure you're logged in (run `py session_setup.py` again)
- Check that the account is public or you follow them
- Try `HEADLESS = False` to see what's happening

### "Failed to send notification"

- Verify `NTFY_TOPIC` is set correctly in `config.py`
- Test with `py notifier.py`
- Check your internet connection

### Session expired

- Delete the `session/` folder
- Run `py session_setup.py` again

---

## 🛑 Stop the Bot

Press `Ctrl+C` in the terminal running `monitor.py`.

---

## 📊 Expected Performance

- **Detection Time**: 5-10 seconds after tweet is posted
- **CPU Usage**: ~2-5% idle, ~10-15% during checks
- **Memory**: ~150-200 MB
- **Network**: ~1-2 MB per check

---

## 🔐 Security Tips

✅ **DO:**
- Use a long, random ntfy topic name
- Keep your `session/` folder private
- Never commit `session/` to git (already in .gitignore)

❌ **DON'T:**
- Share your ntfy topic publicly
- Use this to spam or violate X's Terms of Service

---

**Need help?** Check the full [README.md](README.md) for detailed documentation.
