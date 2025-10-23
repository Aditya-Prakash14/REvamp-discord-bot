#!/bin/bash
# Render startup script

echo "Starting RevampBot..."
echo "Checking environment variables..."

if [ -z "$DISCORD_BOT_TOKEN" ]; then
    echo "ERROR: DISCORD_BOT_TOKEN is not set!"
    exit 1
fi

echo "Bot token found (length: ${#DISCORD_BOT_TOKEN})"
echo "Starting bot..."

python enhanced-revampbot.py
