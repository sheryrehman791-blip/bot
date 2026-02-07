# 🚀 Deploy to Railway (24/7 Monitoring)

This guide shows you how to deploy your X monitoring bot to **Railway** so it runs continuously in the cloud.

## Why Deploy to the Cloud?

- ✅ **24/7 uptime** - Never miss a tweet
- ✅ **No local machine needed** - Runs in the cloud
- ✅ **Automatic restarts** - Recovers from errors
- ✅ **Free tier available** - Railway offers $5/month free credit

---

## 🎯 Quick Deploy to Railway

### Step 1: Prepare Your Repository

1. **Initialize Git** (if not already done):
   ```bash
   cd d:\bot
   git init
   git add .
   git commit -m "Initial commit - X monitoring bot"
   ```

2. **Push to GitHub**:
   - Create a new repository on GitHub
   - Push your code:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/x-monitor-bot.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy on Railway

1. **Go to [Railway.app](https://railway.app)** and sign in with GitHub

2. **Click "New Project"** → **"Deploy from GitHub repo"**

3. **Select your repository** (`x-monitor-bot`)

4. **Railway will automatically detect the Dockerfile** and start building

### Step 3: Configure Environment Variables

In Railway dashboard:

1. Go to your project → **Variables** tab
2. Add these environment variables:

| Variable | Value | Example |
|----------|-------|---------|
| `TARGET_USERNAME` | X account to monitor | `brenthewolf` |
| `NTFY_TOPIC` | Your private ntfy topic | `x-alerts-a8f3k2m9p1q7` |
| `POLL_INTERVAL_MIN` | Min seconds between checks | `5` |
| `POLL_INTERVAL_MAX` | Max seconds between checks | `7` |
| `HEADLESS` | Run browser in background | `True` |

3. Click **Deploy** to restart with new variables

### Step 4: Handle X Login Session

> [!WARNING]
> **Important**: Railway deployments are stateless, so you need to handle the X login session differently.

#### Option A: Use Session Cookies (Recommended)

1. **Run session setup locally first**:
   ```bash
   py session_setup.py
   ```

2. **Get your session cookies**:
   - After logging in, the `session/` folder contains your cookies
   - You'll need to encode these and add as environment variable

3. **Add to Railway**:
   - This is complex - see "Advanced Session Management" below

#### Option B: Use X API (Alternative)

- Consider using X's official API for production deployments
- Requires API keys but more reliable for cloud deployments

---

## 🔧 Alternative: Deploy to Render

### Quick Deploy to Render

1. **Go to [Render.com](https://render.com)** and sign in

2. **New Web Service** → Connect your GitHub repo

3. **Configure**:
   - **Name**: `x-monitor-bot`
   - **Environment**: `Docker`
   - **Plan**: Free tier
   - **Start Command**: `python monitor.py`

4. **Add Environment Variables** (same as Railway above)

5. **Deploy**

---

## 🔧 Alternative: Deploy to Fly.io

### Quick Deploy to Fly.io

1. **Install Fly CLI**:
   ```bash
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
   ```

2. **Login and Launch**:
   ```bash
   fly auth login
   fly launch
   ```

3. **Set Environment Variables**:
   ```bash
   fly secrets set TARGET_USERNAME=brenthewolf
   fly secrets set NTFY_TOPIC=x-alerts-a8f3k2m9p1q7
   fly secrets set HEADLESS=True
   ```

4. **Deploy**:
   ```bash
   fly deploy
   ```

---

## ⚠️ Important Considerations for Cloud Deployment

### Session Management Challenge

The biggest challenge with cloud deployment is **X login session persistence**:

- Cloud platforms restart containers frequently
- The `session/` folder gets wiped on restart
- You'll need to re-authenticate each time

### Solutions:

1. **Volume Mounting** (Railway/Render):
   - Mount a persistent volume for `session/` folder
   - Railway: Add volume in dashboard
   - Render: Use persistent disks

2. **Environment Variable Session** (Advanced):
   - Export cookies to base64
   - Store as environment variable
   - Restore on startup

3. **Use X API Instead** (Recommended for Production):
   - Apply for X API access
   - Use official API for monitoring
   - More reliable for cloud deployments

---

## 📊 Monitoring Your Deployment

### Railway Dashboard

- **Logs**: View real-time logs to see tweet detections
- **Metrics**: Monitor CPU/memory usage
- **Deployments**: Track deployment history

### Expected Logs

```
2026-02-07 10:00:00 - INFO - 🚀 Initializing browser...
2026-02-07 10:00:05 - INFO - ✅ Browser initialized
2026-02-07 10:00:10 - INFO - 🔄 Reloading https://x.com/brenthewolf
2026-02-07 10:00:15 - INFO - ✓ No new tweets (latest: 1234567890)
2026-02-07 10:00:20 - INFO - ⏳ Waiting 6.2 seconds...
```

When a new tweet is detected:
```
2026-02-07 10:05:30 - INFO - 🎉 NEW TWEET DETECTED: https://x.com/brenthewolf/status/9876543210
2026-02-07 10:05:31 - INFO - ✅ Notification sent successfully
```

---

## 💰 Cost Estimates

| Platform | Free Tier | Paid Tier |
|----------|-----------|-----------|
| **Railway** | $5/month credit | ~$5-10/month |
| **Render** | 750 hours/month free | $7/month |
| **Fly.io** | 3 shared VMs free | ~$5/month |

**Recommendation**: Start with Railway's free tier ($5 credit) - should be enough for this bot.

---

## 🔐 Security Best Practices

When deploying to the cloud:

✅ **DO:**
- Use environment variables for all secrets
- Keep your ntfy topic private
- Use a strong, random ntfy topic name
- Monitor logs for suspicious activity

❌ **DON'T:**
- Commit `session/` folder to git (already in .gitignore)
- Share your Railway/Render dashboard publicly
- Use the same ntfy topic across multiple bots

---

## 🐛 Troubleshooting Cloud Deployment

### "Browser timeout" in logs

- Increase `BROWSER_TIMEOUT` in config.py
- Cloud servers may have slower network

### "Session expired" errors

- Session cookies expired
- Need to re-authenticate (see session management above)

### High memory usage

- Normal for Playwright (~200-300 MB)
- Ensure you're on a plan with at least 512 MB RAM

### Bot keeps restarting

- Check Railway logs for errors
- Verify environment variables are set correctly
- Ensure Dockerfile builds successfully

---

## 🎯 Recommended Deployment Flow

1. ✅ **Test locally first** - Make sure everything works
2. ✅ **Set up ntfy** - Install app and subscribe to topic
3. ✅ **Create GitHub repo** - Push your code
4. ✅ **Deploy to Railway** - Connect repo and deploy
5. ✅ **Set environment variables** - Configure in Railway dashboard
6. ✅ **Handle session** - Use persistent volume or API
7. ✅ **Monitor logs** - Verify bot is working
8. ✅ **Test with real tweet** - Wait for @brenthewolf to post

---

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app)
- [Render Documentation](https://render.com/docs)
- [Fly.io Documentation](https://fly.io/docs)
- [Playwright in Docker](https://playwright.dev/docs/docker)

---

**Your bot will now run 24/7 in the cloud!** 🚀
