# Claude CLI → Telegram Bridge

Lightweight bridge connecting Claude CLI to Telegram. Designed for backup Jarvis instances on laptops.

## Step 1: Create Telegram Bots

You need TWO new bots (one per laptop). Open Telegram and message @BotFather:

### Travel Laptop Bot
```
/newbot
TravelJarvis
TravelJarvisBot
```
Save the token: `XXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`

### PLC Laptop Bot
```
/newbot
PLCJarvis
PLCJarvisBot
```
Save the token: `XXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`

## Step 2: Get Your User ID

Message @userinfobot in Telegram. It will reply with your user ID (a number like `8445149012`).

This restricts the bot to only respond to you.

## Step 3: Install on Laptops

### Travel Laptop (PowerShell as Admin)
```powershell
# Download installer
irm https://raw.githubusercontent.com/Mikecranesync/jarvis-workspace/main/installers/claude-telegram-bridge/install-travel.ps1 | iex

# OR manual:
$env:TELEGRAM_BOT_TOKEN = "YOUR_TRAVEL_BOT_TOKEN"
$env:ALLOWED_USERS = "8445149012"  # Your user ID
$env:MACHINE_NAME = "travel-laptop"

pip install python-telegram-bot
python claude_telegram_bridge.py
```

### PLC Laptop (PowerShell as Admin)
```powershell
$env:TELEGRAM_BOT_TOKEN = "YOUR_PLC_BOT_TOKEN"
$env:ALLOWED_USERS = "8445149012"  # Your user ID
$env:MACHINE_NAME = "plc-laptop"

pip install python-telegram-bot
python claude_telegram_bridge.py
```

## Step 4: Run as Service (Optional)

To run at startup, use Task Scheduler or NSSM.

### NSSM Method (Recommended)
```powershell
# Install NSSM
choco install nssm -y

# Create service
nssm install ClaudeTelegram python.exe C:\jarvis\claude_telegram_bridge.py
nssm set ClaudeTelegram AppEnvironmentExtra TELEGRAM_BOT_TOKEN=XXX ALLOWED_USERS=XXX MACHINE_NAME=travel-laptop
nssm start ClaudeTelegram
```

## Usage

Once running, message your laptop's bot in Telegram:

```
You: What's the weather in Florida?
TravelJarvis: [Claude response]

You: /status
TravelJarvis: 📊 Travel-Laptop Status...
```

## Commands

- `/start` - Welcome message
- `/status` - System status
- `/clear` - Clear conversation

## Troubleshooting

### "Claude CLI not found"
Install Claude CLI: https://claude.ai/code

```powershell
# Windows
winget install Anthropic.ClaudeCLI

# Or download from claude.ai/code
```

### Bot not responding
1. Check bot token is correct
2. Verify your user ID is in ALLOWED_USERS
3. Check Claude CLI works: `claude --version`

### Logs
Check the terminal where the script is running for errors.
