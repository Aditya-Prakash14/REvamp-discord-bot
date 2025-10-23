#!/bin/bash
# Pre-deployment script for Render
# Ensures database and dependencies are ready

echo "🚀 Starting RevampBot deployment preparation..."

# Check Python version
echo "📍 Python version:"
python --version

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Initialize database
echo "🗄️ Setting up database..."
python -c "
import sqlite3
import os

db_path = os.getenv('DATABASE_PATH', 'revampbot.db')
print(f'Creating database: {db_path}')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create all tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_xp (
        user_id INTEGER,
        guild_id INTEGER,
        xp INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1,
        last_message TIMESTAMP,
        total_messages INTEGER DEFAULT 0,
        PRIMARY KEY (user_id, guild_id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS guild_config (
        guild_id INTEGER PRIMARY KEY,
        config_data TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS showcase_projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        guild_id INTEGER,
        project_name TEXT,
        description TEXT,
        github_url TEXT,
        tags TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS event_rsvp (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        guild_id INTEGER,
        event_name TEXT,
        event_date TIMESTAMP,
        status TEXT DEFAULT 'going',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS moderation_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER,
        moderator_id INTEGER,
        target_user_id INTEGER,
        action_type TEXT,
        reason TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_warnings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        guild_id INTEGER,
        moderator_id INTEGER,
        reason TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        active BOOLEAN DEFAULT 1
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS custom_commands (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER,
        command_name TEXT,
        response TEXT,
        created_by INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(guild_id, command_name)
    )
''')

# Create indexes
cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_xp_guild ON user_xp(guild_id)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_showcase_guild ON showcase_projects(guild_id)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_rsvp_guild ON event_rsvp(guild_id)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_mod_logs_guild ON moderation_logs(guild_id)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_warnings_user ON user_warnings(user_id, guild_id)')

conn.commit()
conn.close()

print('✅ Database initialized successfully!')
"

# Check if database was created
if [ -f "$DATABASE_PATH" ] || [ -f "revampbot.db" ]; then
    echo "✅ Database file created"
    ls -lh revampbot.db 2>/dev/null || ls -lh $DATABASE_PATH 2>/dev/null
else
    echo "⚠️  Database file not found, will be created on first run"
fi

# Check environment variables
echo ""
echo "🔍 Checking environment variables..."
if [ -z "$DISCORD_BOT_TOKEN" ]; then
    echo "❌ DISCORD_BOT_TOKEN not set!"
    exit 1
else
    echo "✅ DISCORD_BOT_TOKEN is set (length: ${#DISCORD_BOT_TOKEN})"
fi

echo "✅ Deployment preparation complete!"
echo "🚀 Ready to start bot..."
