# RevampBot - Discord Community Bot

A feature-rich Discord bot built with discord.py for managing and engaging community servers.

## Features

- 🛡️ **Moderation Tools**: Kick, ban, and message management
- 🎯 **Server Setup**: Automated channel and role creation
- 📊 **XP/Leveling System**: Track user engagement
- 🎪 **Community Features**: Showcases, events, and collaboration tools
- 🔧 **Customizable**: Flexible configuration system

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Discord Bot Token ([Get one here](https://discord.com/developers/applications))

### Installation

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/revampbot.git
cd revampbot
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory:
```env
DISCORD_BOT_TOKEN=your_bot_token_here
BOT_PREFIX=!
DATABASE_PATH=revampbot.db
LOG_LEVEL=INFO
```

4. Run the bot:
```bash
python enhanced-revampbot.py
```

## Commands

### Core Commands
- `!help` - Show all available commands
- `!ping` - Check bot latency
- `!info` - Display bot information
- `!setup` - Server setup wizard (Admin only)

### Moderation Commands
- `!kick @user [reason]` - Kick a member
- `!ban @user [reason]` - Ban a member
- `!clear <amount>` - Delete messages

## Configuration

Edit your `.env` file to customize:
- `DISCORD_BOT_TOKEN` - Your Discord bot token
- `BOT_PREFIX` - Command prefix (default: `!`)
- `DATABASE_PATH` - SQLite database path
- `LOG_LEVEL` - Logging level (INFO, DEBUG, WARNING, ERROR)

## Project Structure

```
revampbot/
├── enhanced-revampbot.py    # Main bot file
├── bot.py                   # Alternative simplified bot
├── cogs/                    # Bot modules
│   ├── __init__.py
│   └── moderation.py
├── requirements.txt         # Python dependencies
├── Procfile                 # Deployment configuration
└── .env                     # Environment variables (not tracked)
```

## Deployment

See `quick-deploy-guide.md` for detailed deployment instructions for:
- Railway
- Replit
- Oracle Cloud
- Other hosting platforms

## Security

⚠️ **IMPORTANT**: Never commit your `.env` file or expose your bot token!

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

MIT License - feel free to use this bot for your own projects!

## Support

For issues or questions, please open an issue on GitHub.
