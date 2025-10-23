"""
Database Manager for RevampBot
Handles all database operations with proper error handling
"""

import sqlite3
import logging
import json
from datetime import datetime, timezone
from typing import Optional, Dict, List
import os

class DatabaseManager:
    """Manages all database operations for RevampBot"""
    
    def __init__(self, db_path: str = "revampbot.db"):
        self.db_path = db_path
        self.logger = logging.getLogger('RevampBot.Database')
        self.connection: Optional[sqlite3.Connection] = None
        
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self.logger.info(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            self.logger.error(f"Database connection error: {e}")
            raise
            
    def initialize_schema(self):
        """Create all necessary tables"""
        if not self.connection:
            self.connect()
            
        try:
            cursor = self.connection.cursor()
            
            # User XP and Leveling Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_xp (
                    user_id INTEGER NOT NULL,
                    guild_id INTEGER NOT NULL,
                    xp INTEGER DEFAULT 0,
                    level INTEGER DEFAULT 1,
                    last_message TIMESTAMP,
                    total_messages INTEGER DEFAULT 0,
                    PRIMARY KEY (user_id, guild_id)
                )
            ''')
            
            # Guild Configuration Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS guild_config (
                    guild_id INTEGER PRIMARY KEY,
                    config_data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Showcase Projects Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS showcase_projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    guild_id INTEGER NOT NULL,
                    project_name TEXT NOT NULL,
                    description TEXT,
                    github_url TEXT,
                    tags TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Event RSVP Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS event_rsvp (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    guild_id INTEGER NOT NULL,
                    event_name TEXT NOT NULL,
                    event_date TIMESTAMP,
                    status TEXT DEFAULT 'going',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Moderation Logs Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS moderation_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id INTEGER NOT NULL,
                    moderator_id INTEGER NOT NULL,
                    target_user_id INTEGER NOT NULL,
                    action_type TEXT NOT NULL,
                    reason TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # User Warnings Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_warnings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    guild_id INTEGER NOT NULL,
                    moderator_id INTEGER NOT NULL,
                    reason TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    active BOOLEAN DEFAULT 1
                )
            ''')
            
            # Custom Commands Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS custom_commands (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id INTEGER NOT NULL,
                    command_name TEXT NOT NULL,
                    response TEXT NOT NULL,
                    created_by INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(guild_id, command_name)
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_xp_guild ON user_xp(guild_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_showcase_guild ON showcase_projects(guild_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_rsvp_guild ON event_rsvp(guild_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_mod_logs_guild ON moderation_logs(guild_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_warnings_user ON user_warnings(user_id, guild_id)')
            
            self.connection.commit()
            self.logger.info("Database schema initialized successfully")
            print("✅ Database schema initialized successfully")
            
        except sqlite3.Error as e:
            self.logger.error(f"Schema initialization error: {e}")
            self.connection.rollback()
            raise
            
    def get_user_xp(self, user_id: int, guild_id: int) -> Optional[Dict]:
        """Get user XP data"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                'SELECT * FROM user_xp WHERE user_id = ? AND guild_id = ?',
                (user_id, guild_id)
            )
            row = cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            self.logger.error(f"Error getting user XP: {e}")
            return None
            
    def update_user_xp(self, user_id: int, guild_id: int, xp: int, level: int):
        """Update user XP and level"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO user_xp (user_id, guild_id, xp, level, last_message, total_messages)
                VALUES (?, ?, ?, ?, ?, 1)
                ON CONFLICT(user_id, guild_id) DO UPDATE SET
                    xp = ?,
                    level = ?,
                    last_message = ?,
                    total_messages = total_messages + 1
            ''', (user_id, guild_id, xp, level, datetime.now(timezone.utc), 
                  xp, level, datetime.now(timezone.utc)))
            self.connection.commit()
        except sqlite3.Error as e:
            self.logger.error(f"Error updating user XP: {e}")
            
    def get_leaderboard(self, guild_id: int, limit: int = 10) -> List[Dict]:
        """Get XP leaderboard for a guild"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT user_id, xp, level, total_messages
                FROM user_xp
                WHERE guild_id = ?
                ORDER BY xp DESC
                LIMIT ?
            ''', (guild_id, limit))
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            self.logger.error(f"Error getting leaderboard: {e}")
            return []
            
    def get_guild_config(self, guild_id: int) -> Optional[Dict]:
        """Get guild configuration"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT config_data FROM guild_config WHERE guild_id = ?', (guild_id,))
            row = cursor.fetchone()
            return json.loads(row['config_data']) if row else None
        except sqlite3.Error as e:
            self.logger.error(f"Error getting guild config: {e}")
            return None
            
    def set_guild_config(self, guild_id: int, config: Dict):
        """Set guild configuration"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO guild_config (guild_id, config_data, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(guild_id) DO UPDATE SET
                    config_data = ?,
                    updated_at = ?
            ''', (guild_id, json.dumps(config), datetime.now(timezone.utc),
                  json.dumps(config), datetime.now(timezone.utc)))
            self.connection.commit()
        except sqlite3.Error as e:
            self.logger.error(f"Error setting guild config: {e}")
            
    def add_warning(self, user_id: int, guild_id: int, moderator_id: int, reason: str):
        """Add a warning to a user"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO user_warnings (user_id, guild_id, moderator_id, reason)
                VALUES (?, ?, ?, ?)
            ''', (user_id, guild_id, moderator_id, reason))
            self.connection.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            self.logger.error(f"Error adding warning: {e}")
            return None
            
    def get_user_warnings(self, user_id: int, guild_id: int) -> List[Dict]:
        """Get user warnings"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT * FROM user_warnings 
                WHERE user_id = ? AND guild_id = ? AND active = 1
                ORDER BY created_at DESC
            ''', (user_id, guild_id))
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            self.logger.error(f"Error getting warnings: {e}")
            return []
            
    def log_moderation_action(self, guild_id: int, moderator_id: int, 
                            target_user_id: int, action_type: str, reason: str = None):
        """Log a moderation action"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO moderation_logs (guild_id, moderator_id, target_user_id, action_type, reason)
                VALUES (?, ?, ?, ?, ?)
            ''', (guild_id, moderator_id, target_user_id, action_type, reason))
            self.connection.commit()
        except sqlite3.Error as e:
            self.logger.error(f"Error logging moderation action: {e}")
            
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.logger.info("Database connection closed")


def setup_database(db_path: str = "revampbot.db"):
    """Setup the database with all tables"""
    print(f"🔧 Setting up RevampBot database: {db_path}")
    print("=" * 60)
    
    db = DatabaseManager(db_path)
    db.connect()
    db.initialize_schema()
    
    print("\n✅ Database setup completed successfully!")
    print(f"📁 Database file: {os.path.abspath(db_path)}")
    print(f"📊 File size: {os.path.getsize(db_path)} bytes")
    
    print("\n📋 Tables created:")
    tables = [
        ("user_xp", "User experience and leveling"),
        ("guild_config", "Server configurations"),
        ("showcase_projects", "User project showcases"),
        ("event_rsvp", "Event RSVPs"),
        ("moderation_logs", "Moderation action logs"),
        ("user_warnings", "User warnings"),
        ("custom_commands", "Custom server commands")
    ]
    
    for table_name, description in tables:
        print(f"  ✓ {table_name:20} - {description}")
    
    print("\n🚀 Database is ready to use!")
    db.close()
    

if __name__ == "__main__":
    setup_database()
