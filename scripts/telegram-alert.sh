#!/bin/bash
# Telegram Alert Webhook
# Sends messages directly to Telegram via Bot API

BOT_TOKEN="8387943893:AAEynugW3SP1sWs6An4aNgZParSSRBlWSJk"
CHAT_ID="8445149012"

MESSAGE="$1"

if [ -z "$MESSAGE" ]; then
    echo "Usage: $0 'message text'"
    exit 1
fi

# URL encode the message for safety
ENCODED_MESSAGE=$(python3 -c "import urllib.parse; print(urllib.parse.quote('''$MESSAGE'''))")

# Send via Telegram Bot API
curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
    -d "chat_id=${CHAT_ID}" \
    -d "text=${MESSAGE}" \
    -d "parse_mode=HTML" \
    > /dev/null

if [ $? -eq 0 ]; then
    echo "Alert sent to Telegram"
else
    echo "Failed to send alert"
    exit 1
fi
