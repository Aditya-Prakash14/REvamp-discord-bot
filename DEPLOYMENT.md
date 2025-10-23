# 🚀 Deploy Your RevampBot - Step by Step Guide

## Option 1: Railway (RECOMMENDED - Easiest & Free)

Railway offers $5/month free credit which is enough for a Discord bot.

### Step-by-Step Deployment:

#### 1. Sign Up for Railway
- Go to **https://railway.app**
- Click "Login" → Sign in with GitHub
- Authorize Railway to access your GitHub account

#### 2. Create New Project
- Click **"New Project"**
- Select **"Deploy from GitHub repo"**
- Choose your repository: **Aditya-Prakash14/REvamp-discord-bot**
- Railway will automatically detect it's a Python project

#### 3. Add Environment Variables
- Once the project is created, click on your deployment
- Go to **"Variables"** tab
- Click **"+ New Variable"**
- Add the following:

```
DISCORD_BOT_TOKEN = your_discord_bot_token_here
BOT_PREFIX = !
DATABASE_PATH = revampbot.db
LOG_LEVEL = INFO
```

**⚠️ IMPORTANT**: Replace `your_discord_bot_token_here` with your actual Discord bot token from the `.env` file!

#### 4. Deploy
- Click **"Deploy"** 
- Wait 2-3 minutes for the build to complete
- Check the **"Logs"** tab - you should see:
  ```
  INFO - REvampbot#4542 has connected to Discord!
  INFO - Connected to 1 guilds
  ```

#### 5. Keep It Running 24/7
- Railway automatically keeps your bot running
- Your bot will restart automatically if it crashes
- Monitor usage in the Railway dashboard

### ✅ Done! Your bot is now live 24/7!

---

## Option 2: Render (Free Alternative)

### Step-by-Step:

1. **Sign Up**: Go to https://render.com and sign in with GitHub
2. **New Web Service**: 
   - Click "New +" → "Web Service"
   - Connect your GitHub repo: **REvamp-discord-bot**
3. **Configure**:
   - Name: `revampbot`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python enhanced-revampbot.py`
4. **Environment Variables**: Add same variables as Railway
5. **Create Web Service**: Click create and wait for deployment

---

## Option 3: Heroku (Paid but reliable)

### Quick Deploy:

1. Install Heroku CLI:
```bash
brew tap heroku/brew && brew install heroku
```

2. Login:
```bash
heroku login
```

3. Create app:
```bash
cd /Users/adityaprakash/Desktop/revampbot
heroku create revampbot-discord
```

4. Set environment variables:
```bash
heroku config:set DISCORD_BOT_TOKEN=your_discord_bot_token_here
heroku config:set BOT_PREFIX=!
heroku config:set DATABASE_PATH=revampbot.db
heroku config:set LOG_LEVEL=INFO
```

**Note**: Replace `your_discord_bot_token_here` with your actual token

5. Deploy:
```bash
git push heroku main
heroku ps:scale worker=1
```

6. Check logs:
```bash
heroku logs --tail
```

---

## 📊 Platform Comparison

| Platform | Free Tier | 24/7 Uptime | Setup Difficulty |
|----------|-----------|-------------|------------------|
| **Railway** | $5/month credit | ✅ Yes | ⭐ Easy |
| **Render** | 750 hrs/month | ✅ Yes | ⭐⭐ Easy |
| **Heroku** | Paid only | ✅ Yes | ⭐⭐ Medium |

---

## 🔍 Troubleshooting

### Bot Not Connecting?
1. Check logs for errors
2. Verify `DISCORD_BOT_TOKEN` is correct
3. Ensure bot has proper intents enabled in Discord Developer Portal

### Bot Crashes?
1. Check deployment logs
2. Verify all dependencies in `requirements.txt`
3. Make sure Python version is 3.8+

### Database Issues?
1. Ensure `DATABASE_PATH` variable is set
2. Check if platform supports SQLite (Railway & Render do)

---

## 🎉 Post-Deployment

Once deployed, your bot will:
- ✅ Run 24/7 automatically
- ✅ Auto-restart on crashes
- ✅ Be accessible from any Discord server
- ✅ Save data to persistent database

**Test your bot** by typing `!help` in your Discord server!

---

## 📈 Monitoring

- Railway: Check dashboard for logs and metrics
- Render: View logs in the dashboard
- Heroku: Use `heroku logs --tail`

---

## 🔒 Security Reminder

- Never share your `DISCORD_BOT_TOKEN`
- If token is leaked, regenerate it in Discord Developer Portal
- Keep `.env` file in `.gitignore` (already done)

---

Need help? Check the logs or open an issue on GitHub!
