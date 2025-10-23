# Database Deployment Guide

## 🚀 Deploying Your Bot with Database

Your RevampBot uses SQLite which is automatically created when the bot starts. Here's how it works on different platforms:

---

## ✅ **How Database Works in Deployment**

### **Automatic Initialization**
- ✅ Database is created automatically on first run
- ✅ All tables are created in [`enhanced-revampbot.py`](enhanced-revampbot.py ) `init_database()` function
- ✅ No manual setup required

### **Database File Location**
- **Local**: `/Users/adityaprakash/Desktop/revampbot/revampbot.db`
- **Render**: `/opt/render/project/src/revampbot.db`
- **Railway**: In project root directory

---

## 📦 **Platform-Specific Deployment**

### **1. Render (Currently Deployed)**

#### ✅ What Happens:
1. Bot starts on Render
2. Database file `revampbot.db` is created in the working directory
3. Tables are initialized automatically
4. Bot starts tracking data

#### ⚠️ Important Notes:
- **Free Plan**: Database is ephemeral (resets on redeploy)
- **Paid Plan**: Can use persistent disks for permanent storage
- **Data Loss**: Free tier loses data when service restarts

#### 💡 Solution for Free Tier:
Since you're on the free tier, the database will reset on each deployment. This is fine for:
- Testing
- Development
- Small servers with acceptable data loss

For production, consider:
- Upgrading to paid plan with persistent disk
- Using a cloud database (PostgreSQL, MongoDB)

---

### **2. Railway**

#### ✅ What Happens:
1. Database created in project directory
2. **Persistent by default** (even on free tier!)
3. Data survives restarts and redeployments

#### Setup:
```bash
# Railway CLI (if installed)
railway up

# Or use web dashboard
1. Go to railway.app
2. Deploy from GitHub
3. Add DISCORD_BOT_TOKEN environment variable
4. Deploy!
```

**Railway is RECOMMENDED** for persistent database on free tier!

---

### **3. Local Development**

Your database is already working locally:
```bash
# Run bot
python enhanced-revampbot.py

# View database
python db_viewer.py tables

# Check data
python db_viewer.py data user_xp 10
```

---

## 🗄️ **Database Persistence Options**

### **Option 1: SQLite (Current)**
✅ **Pros:**
- Simple setup
- No external dependencies
- Fast for small-medium servers
- Included with Python

❌ **Cons:**
- Not persistent on Render free tier
- File-based (can be lost)
- Single-server only

**Best for:** Development, small bots, Railway deployments

---

### **Option 2: PostgreSQL (Recommended for Production)**

To switch to PostgreSQL for permanent storage:

1. **Update requirements.txt:**
```txt
discord.py>=2.3.0
python-dotenv>=1.0.0
aiohttp>=3.9.0
psycopg2-binary>=2.9.0
```

2. **Get PostgreSQL Database:**
   - Render: Add PostgreSQL service (free tier available)
   - Railway: Add PostgreSQL plugin
   - Supabase: Free PostgreSQL hosting

3. **Update bot code** to use PostgreSQL instead of SQLite

Would you like me to convert your bot to use PostgreSQL?

---

### **Option 3: MongoDB**

For NoSQL approach:

1. **Use MongoDB Atlas** (free tier: 512MB)
2. **Update code** to use pymongo
3. **More flexible** schema

---

## 🔧 **Current Deployment Status**

### Your Bot on Render:

```
✅ Bot: Running
✅ Database: Created (ephemeral)
⚠️  Persistence: No (free tier)
📊 Data: Resets on redeploy
```

### What Gets Saved:
- ✅ User XP: Until next redeploy
- ✅ Warnings: Until next redeploy
- ✅ Mod logs: Until next redeploy
- ✅ Configurations: Until next redeploy

### What's Permanent:
- ✅ Bot code (GitHub)
- ✅ Environment variables (Render)
- ❌ Database data (resets)

---

## 💡 **Recommended Solutions**

### **For Free Deployment with Persistence:**

1. **Switch to Railway** (BEST FREE OPTION)
   - Persistent storage on free tier
   - Easy GitHub integration
   - $5/month free credit
   - Steps:
     ```
     1. Go to railway.app
     2. Deploy from GitHub: REvamp-discord-bot
     3. Add DISCORD_BOT_TOKEN
     4. Done! Database persists automatically
     ```

2. **Use Cloud Database with Render**
   - Add PostgreSQL service on Render (free)
   - Update bot to use PostgreSQL
   - Permanent storage even on free tier

---

### **For Paid Deployment:**

1. **Render with Persistent Disk** ($7/month)
   - Add persistent disk to worker
   - Database survives redeploys
   - Reliable and fast

2. **Heroku with Postgres** ($7/month)
   - Built-in PostgreSQL
   - Automatic backups
   - High reliability

---

## 📊 **Checking Database on Render**

Since you can't SSH into free tier, you can:

### **Option 1: Add Admin Command**
Add this to your bot to export data:

```python
@commands.command()
@commands.is_owner()
async def export_db(self, ctx):
    """Export database statistics"""
    cursor = self.db.cursor()
    cursor.execute("SELECT COUNT(*) FROM user_xp")
    xp_count = cursor.fetchone()[0]
    
    embed = discord.Embed(title="Database Stats")
    embed.add_field(name="User XP Records", value=xp_count)
    await ctx.send(embed=embed)
```

### **Option 2: View Logs**
Check Render logs to see database operations

---

## 🚀 **Quick Migration to Railway**

Want persistent database for free? Switch to Railway:

1. Keep your GitHub repo as-is
2. Go to https://railway.app/new
3. Deploy from GitHub → REvamp-discord-bot
4. Add environment variables (same as Render)
5. Deploy!

**Database will persist automatically!** 🎉

---

## 📞 **Need Help?**

**Current Setup:**
- Platform: Render (Free Tier)
- Database: SQLite (Ephemeral)
- Status: Working but resets on redeploy

**Upgrade Options:**
1. Switch to Railway (free, persistent)
2. Use PostgreSQL on Render (free, persistent)
3. Upgrade Render plan ($7/month, persistent)

Let me know which option you prefer and I can help you set it up! 🚀
