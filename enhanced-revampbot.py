# Enhanced RevampBot - Secure, Modular, and Feature-Rich Discord Bot
# Author: Enhanced by AI Assistant
# Version: 2.0

import discord
from discord.ext import commands, tasks
from discord.utils import get
import asyncio
import sqlite3
import json
import logging
import os
import random
import datetime
from dotenv import load_dotenv
from typing import Optional, List, Dict, Any
import aiohttp
from dataclasses import dataclass

# Load environment variables
load_dotenv()

# Configuration
@dataclass
class BotConfig:
    prefix: str = "!"
    database_path: str = "revampbot.db"
    log_level: str = "INFO"
    max_xp_per_message: int = 5
    cooldown_seconds: int = 5
    
    @classmethod
    def from_env(cls):
        return cls(
            prefix=os.getenv('BOT_PREFIX', '!'),
            database_path=os.getenv('DATABASE_PATH', 'revampbot.db'),
            log_level=os.getenv('LOG_LEVEL', 'INFO'),
            max_xp_per_message=int(os.getenv('MAX_XP_PER_MESSAGE', '5')),
            cooldown_seconds=int(os.getenv('COOLDOWN_SECONDS', '5'))
        )

# Enhanced Bot Class
class EnhancedRevampBot(commands.Bot):
    def __init__(self, config: BotConfig):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        
        super().__init__(
            command_prefix=config.prefix,
            intents=intents,
            help_command=None  # We'll create a custom help command
        )
        
        self.config = config
        self.start_time = datetime.datetime.utcnow()
        
        # Setup logging
        self.setup_logging()
        
        # Initialize database
        self.init_database()
        
        # Load server configurations
        self.server_configs = {}
        
        # Session for HTTP requests
        self.session: Optional[aiohttp.ClientSession] = None
        
    def setup_logging(self):
        """Setup enhanced logging system"""
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=getattr(logging, self.config.log_level),
            format=log_format,
            handlers=[
                logging.FileHandler('revampbot.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('RevampBot')
        
    def init_database(self):
        """Initialize SQLite database with proper schema"""
        try:
            self.db = sqlite3.connect(self.config.database_path)
            self.db.execute('''
                CREATE TABLE IF NOT EXISTS user_xp (
                    user_id INTEGER,
                    guild_id INTEGER,
                    xp INTEGER DEFAULT 0,
                    level INTEGER DEFAULT 1,
                    last_message TIMESTAMP,
                    PRIMARY KEY (user_id, guild_id)
                )
            ''')
            
            self.db.execute('''
                CREATE TABLE IF NOT EXISTS guild_config (
                    guild_id INTEGER PRIMARY KEY,
                    config_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.db.execute('''
                CREATE TABLE IF NOT EXISTS showcase_projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    guild_id INTEGER,
                    project_name TEXT,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.db.execute('''
                CREATE TABLE IF NOT EXISTS event_rsvp (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    guild_id INTEGER,
                    event_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.db.commit()
            self.logger.info("Database initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Database initialization failed: {e}")
            
    async def setup_hook(self):
        """Setup hook called when bot starts"""
        self.session = aiohttp.ClientSession()
        
        # Load all cogs
        await self.load_cogs()
        
        # Start background tasks
        self.periodic_tasks.start()
        
        self.logger.info("Bot setup completed successfully")
        
    async def load_cogs(self):
        """Load all bot cogs/extensions"""
        cogs = [
            'cogs.moderation',
            'cogs.leveling',
            'cogs.events',
            'cogs.community',
            'cogs.utility'
        ]
        
        for cog in cogs:
            try:
                await self.load_extension(cog)
                self.logger.info(f"Loaded cog: {cog}")
            except Exception as e:
                self.logger.error(f"Failed to load cog {cog}: {e}")
                
    async def on_ready(self):
        """Called when bot is ready"""
        self.logger.info(f'{self.user} has connected to Discord!')
        self.logger.info(f'Connected to {len(self.guilds)} guilds')
        
        # Set bot presence
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{len(self.guilds)} servers | {self.config.prefix}help"
            )
        )
        
    async def on_guild_join(self, guild):
        """Called when bot joins a new guild"""
        self.logger.info(f"Joined new guild: {guild.name} (ID: {guild.id})")
        
        # Create default configuration for new guild
        await self.create_default_guild_config(guild)
        
    async def create_default_guild_config(self, guild):
        """Create default configuration for a new guild"""
        default_config = {
            'auto_setup': False,  # Changed from destructive auto-setup
            'welcome_channel': None,
            'log_channel': None,
            'level_up_notifications': True,
            'auto_roles': [],
            'moderation': {
                'auto_mod': False,
                'spam_detection': True,
                'invite_filtering': False
            }
        }
        
        try:
            self.db.execute(
                'INSERT OR REPLACE INTO guild_config (guild_id, config_data) VALUES (?, ?)',
                (guild.id, json.dumps(default_config))
            )
            self.db.commit()
            
            # Send welcome message to system channel if available
            if guild.system_channel:
                embed = discord.Embed(
                    title="👋 Welcome to RevampBot!",
                    description=(
                        "Thank you for adding RevampBot to your server! "
                        f"Use `{self.config.prefix}setup` to configure the bot for your community."
                    ),
                    color=discord.Color.blue()
                )
                embed.add_field(
                    name="Getting Started",
                    value=f"`{self.config.prefix}help` - View all commands\n"
                          f"`{self.config.prefix}setup` - Server setup wizard",
                    inline=False
                )
                await guild.system_channel.send(embed=embed)
                
        except Exception as e:
            self.logger.error(f"Failed to create default config for guild {guild.id}: {e}")
            
    @tasks.loop(hours=24)
    async def periodic_tasks(self):
        """Periodic maintenance and automated tasks"""
        self.logger.info("Running periodic maintenance tasks")
        
        # Update bot presence with current stats
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{len(self.guilds)} servers | {self.config.prefix}help"
            )
        )
        
        # Clean up old data, send announcements, etc.
        await self.cleanup_old_data()
        
    async def cleanup_old_data(self):
        """Clean up old database entries"""
        try:
            # Remove RSVP entries older than 30 days
            cutoff_date = datetime.datetime.utcnow() - datetime.timedelta(days=30)
            self.db.execute(
                'DELETE FROM event_rsvp WHERE created_at < ?',
                (cutoff_date,)
            )
            self.db.commit()
            self.logger.info("Cleaned up old RSVP data")
        except Exception as e:
            self.logger.error(f"Error during data cleanup: {e}")
            
    async def close(self):
        """Cleanup when bot shuts down"""
        if self.session:
            await self.session.close()
        if hasattr(self, 'db'):
            self.db.close()
        await super().close()
        self.logger.info("Bot shutdown completed")

# Core Commands (moved to main bot class for essential functionality)
class CoreCommands(commands.Cog):
    def __init__(self, bot: EnhancedRevampBot):
        self.bot = bot
        
    @commands.command(name='help')
    async def help_command(self, ctx):
        """Enhanced help command with embeds"""
        embed = discord.Embed(
            title="🤖 RevampBot Commands",
            description="Here are all available commands organized by category:",
            color=discord.Color.blue()
        )
        
        # Core commands
        embed.add_field(
            name="🔧 Core Commands",
            value=(
                f"`{self.bot.config.prefix}help` - Show this help message\n"
                f"`{self.bot.config.prefix}ping` - Check bot latency\n"
                f"`{self.bot.config.prefix}info` - Bot information\n"
                f"`{self.bot.config.prefix}setup` - Server setup wizard"
            ),
            inline=False
        )
        
        # Community commands
        embed.add_field(
            name="🌟 Community",
            value=(
                f"`{self.bot.config.prefix}rolemenu` - Role selection menu\n"
                f"`{self.bot.config.prefix}showcase` - Showcase your project\n"
                f"`{self.bot.config.prefix}buddy` - Find a coding buddy\n"
                f"`{self.bot.config.prefix}rsvp` - RSVP to events"
            ),
            inline=False
        )
        
        embed.set_footer(text=f"Use {self.bot.config.prefix}help [command] for detailed information")
        await ctx.send(embed=embed)
        
    @commands.command(name='ping')
    async def ping(self, ctx):
        """Check bot latency"""
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Bot latency: {latency}ms",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        
    @commands.command(name='info')
    async def bot_info(self, ctx):
        """Display bot information"""
        uptime = datetime.datetime.utcnow() - self.bot.start_time
        
        embed = discord.Embed(
            title="🤖 RevampBot Information",
            color=discord.Color.blue()
        )
        embed.add_field(name="Version", value="2.0 Enhanced", inline=True)
        embed.add_field(name="Servers", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Uptime", value=str(uptime).split('.')[0], inline=True)
        embed.add_field(name="Language", value="Python 3.8+", inline=True)
        embed.add_field(name="Library", value="discord.py", inline=True)
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        
        await ctx.send(embed=embed)

# Safe setup command (replaces destructive server wipe)
@commands.command(name='setup')
@commands.has_permissions(administrator=True)
async def setup_server(self, ctx):
    """Safe server setup wizard"""
    embed = discord.Embed(
        title="🔧 Server Setup Wizard",
        description="This will help you configure RevampBot for your server.",
        color=discord.Color.orange()
    )
    embed.add_field(
        name="⚠️ Important",
        value="This setup will create channels and roles. Make sure you have backups if needed.",
        inline=False
    )
    embed.add_field(
        name="Options",
        value=(
            "React with ✅ to proceed with setup\n"
            "React with ❌ to cancel"
        ),
        inline=False
    )
    
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('✅')
    await msg.add_reaction('❌')
    
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ['✅', '❌']
    
    try:
        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        
        if str(reaction.emoji) == '✅':
            await self.perform_safe_setup(ctx)
        else:
            await ctx.send("Setup cancelled.")
            
    except asyncio.TimeoutError:
        await ctx.send("Setup timed out.")

async def perform_safe_setup(self, ctx):
    """Perform safe server setup without destructive actions"""
    guild = ctx.guild
    
    try:
        # Create categories and channels only if they don't exist
        setup_log = []
        
        # Server structure (same as original but safe)
        server_structure = [
            ("👋 Welcome", [
                ("👋・welcome", "text"),
                ("📜・rules", "text"),
                ("😎・introductions", "text"),
                ("🌟・role-selection", "text")
            ]),
            ("📣 Announcements", [
                ("📣・announcements", "text"),
                ("🎫・events", "text")
            ]),
            ("🏠 Community", [
                ("🏠・general", "text"),
                ("🥤・lounge", "text"),
                ("🏆・showcase", "text"),
                ("🤝・collaborations", "text")
            ]),
            ("💻 Tech Hub", [
                ("💻・coding-help", "text"),
                ("📚・resources", "text"),
                ("🌐・web-dev", "text"),
                ("🧠・ml-ai", "text")
            ])
        ]
        
        for category_name, channels in server_structure:
            # Check if category exists
            category = discord.utils.get(guild.categories, name=category_name)
            if not category:
                category = await guild.create_category(category_name)
                setup_log.append(f"✅ Created category: {category_name}")
            
            for channel_name, channel_type in channels:
                if channel_type == "text":
                    if not discord.utils.get(guild.text_channels, name=channel_name):
                        await guild.create_text_channel(channel_name, category=category)
                        setup_log.append(f"✅ Created text channel: {channel_name}")
                
        # Create roles safely
        role_configs = [
            ("Member", discord.Color.blue()),
            ("Web Dev", discord.Color.green()),
            ("ML/AI Enthusiast", discord.Color.purple()),
            ("Community Helper", discord.Color.orange())
        ]
        
        for role_name, color in role_configs:
            if not discord.utils.get(guild.roles, name=role_name):
                await guild.create_role(name=role_name, color=color)
                setup_log.append(f"✅ Created role: {role_name}")
        
        # Send setup completion message
        embed = discord.Embed(
            title="🎉 Setup Completed!",
            description="Your server has been configured successfully.",
            color=discord.Color.green()
        )
        
        if setup_log:
            embed.add_field(
                name="Changes Made",
                value='\n'.join(setup_log[:10]),  # Limit to first 10 entries
                inline=False
            )
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Setup failed: {str(e)}")
        self.bot.logger.error(f"Setup failed for guild {guild.id}: {e}")

def main():
    """Main function to run the bot"""
    # Load configuration
    config = BotConfig.from_env()
    
    # Get bot token from environment
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print("❌ Error: DISCORD_BOT_TOKEN environment variable is required!")
        print("Please create a .env file with your bot token.")
        return
    
    # Create and run bot
    bot = EnhancedRevampBot(config)
    
    try:
        bot.run(token)
    except discord.LoginFailure:
        bot.logger.error("Failed to login - check your bot token")
    except KeyboardInterrupt:
        bot.logger.info("Bot stopped by user")
    except Exception as e:
        bot.logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()