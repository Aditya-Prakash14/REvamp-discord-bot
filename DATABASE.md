# RevampBot Database Documentation

## ✅ Database Status: **SETUP COMPLETE**

Your SQLite database is fully configured and ready to use!

- **Database File**: `revampbot.db`
- **Location**: `/Users/adityaprakash/Desktop/revampbot/`
- **Tables**: 7 core tables + 1 system table
- **Status**: All tables created with proper indexes

---

## 📊 Database Tables

### 1. **user_xp** - User Experience & Leveling
Tracks user activity and experience points.

| Column | Type | Description |
|--------|------|-------------|
| user_id | INTEGER | Discord user ID (Primary Key) |
| guild_id | INTEGER | Discord server ID (Primary Key) |
| xp | INTEGER | Total experience points |
| level | INTEGER | Current user level |
| last_message | TIMESTAMP | Last message timestamp |

**Usage**: Automatically tracks when users send messages.

---

### 2. **guild_config** - Server Configuration
Stores server-specific settings.

| Column | Type | Description |
|--------|------|-------------|
| guild_id | INTEGER | Discord server ID (Primary Key) |
| config_data | TEXT | JSON configuration data |
| created_at | TIMESTAMP | When config was created |
| updated_at | TIMESTAMP | Last update time |

**Usage**: Stores welcome messages, mod roles, auto-mod settings, etc.

---

### 3. **moderation_logs** - Moderation Actions
Logs all moderation actions for audit trail.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Log ID (Auto-increment) |
| guild_id | INTEGER | Server ID |
| moderator_id | INTEGER | Moderator's user ID |
| target_user_id | INTEGER | Target user ID |
| action_type | TEXT | kick, ban, warn, timeout, etc. |
| reason | TEXT | Reason for action |
| timestamp | TIMESTAMP | When action occurred |

**Usage**: Tracks all mod actions like kicks, bans, warnings.

---

### 4. **user_warnings** - Warning System
Manages user warnings.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Warning ID (Auto-increment) |
| user_id | INTEGER | Warned user ID |
| guild_id | INTEGER | Server ID |
| moderator_id | INTEGER | Moderator who issued warning |
| reason | TEXT | Warning reason |
| created_at | TIMESTAMP | When warning was issued |
| active | BOOLEAN | Is warning still active |

**Usage**: Track user warnings, implement auto-ban after X warnings.

---

### 5. **showcase_projects** - Project Showcases
User project submissions.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Project ID (Auto-increment) |
| user_id | INTEGER | Project owner ID |
| guild_id | INTEGER | Server ID |
| project_name | TEXT | Project name |
| description | TEXT | Project description |
| github_url | TEXT | GitHub URL (optional) |
| tags | TEXT | Project tags/categories |
| created_at | TIMESTAMP | Submission date |

**Usage**: `!showcase MyProject "Cool app"` command.

---

### 6. **event_rsvp** - Event Management
Track event RSVPs.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | RSVP ID (Auto-increment) |
| user_id | INTEGER | User who RSVP'd |
| guild_id | INTEGER | Server ID |
| event_name | TEXT | Event name |
| event_date | TIMESTAMP | Event date/time |
| status | TEXT | going, maybe, not_going |
| created_at | TIMESTAMP | RSVP timestamp |

**Usage**: `!rsvp EventName` command.

---

### 7. **custom_commands** - Custom Commands
Server-specific custom commands.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Command ID (Auto-increment) |
| guild_id | INTEGER | Server ID |
| command_name | TEXT | Command trigger |
| response | TEXT | Command response |
| created_by | INTEGER | Creator user ID |
| created_at | TIMESTAMP | Creation date |

**Usage**: Create custom commands like `!rules` → "Read #rules channel".

---

## 🔧 Database Management

### View Database Info
```bash
python db_viewer.py tables
```

### View Table Schema
```bash
python db_viewer.py schema user_xp
python db_viewer.py schema moderation_logs
```

### View Table Data
```bash
python db_viewer.py data user_xp 20
python db_viewer.py data moderation_logs 50
```

---

## 🛠️ Manual Database Access

### Using SQLite Command Line
```bash
sqlite3 revampbot.db

# List all tables
.tables

# View table structure
.schema user_xp

# Query data
SELECT * FROM user_xp WHERE guild_id = YOUR_GUILD_ID;

# Get top users by XP
SELECT user_id, level, xp FROM user_xp 
WHERE guild_id = YOUR_GUILD_ID 
ORDER BY xp DESC LIMIT 10;

# Get moderation logs
SELECT * FROM moderation_logs 
WHERE guild_id = YOUR_GUILD_ID 
ORDER BY timestamp DESC LIMIT 20;

# Exit
.quit
```

---

## 📈 Performance Features

**Indexes Created:**
- ✅ `idx_user_xp_guild` - Fast guild lookups
- ✅ `idx_showcase_guild` - Fast showcase queries
- ✅ `idx_rsvp_guild` - Fast RSVP queries
- ✅ `idx_mod_logs_guild` - Fast mod log queries
- ✅ `idx_warnings_user` - Fast warning lookups

---

## 🔒 Backup & Security

### Backup Database
```bash
# Create backup
cp revampbot.db backups/revampbot_backup_$(date +%Y%m%d_%H%M%S).db

# Or use SQLite backup
sqlite3 revampbot.db ".backup backups/revampbot_backup.db"
```

### Restore from Backup
```bash
cp backups/revampbot_backup_20231024.db revampbot.db
```

### Security Notes
- ✅ Database file is in `.gitignore` (not committed to GitHub)
- ✅ Contains no sensitive user data (passwords, tokens, etc.)
- ✅ User IDs are Discord IDs (public information)
- ⚠️ Backup regularly for production use

---

## 🚀 Ready to Use!

Your database is fully set up and ready. The bot will automatically:
- ✅ Track user XP when they send messages
- ✅ Log all moderation actions
- ✅ Store server configurations
- ✅ Save showcases, RSVPs, and warnings

No additional setup needed - just run your bot! 🎉

---

## 📞 Troubleshooting

**Database locked error?**
- Stop the bot before accessing database manually
- Only one connection can write at a time

**Missing data?**
- Check table with: `python db_viewer.py data TABLE_NAME`
- Check bot logs: `tail -f revampbot.log`

**Corrupt database?**
- Restore from backup
- Or delete and bot will recreate: `rm revampbot.db`

---

**Database Version**: 1.0  
**Last Updated**: October 24, 2025  
**Status**: ✅ Production Ready
