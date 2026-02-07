#!/usr/bin/env python3
"""
Claude CLI → Telegram Bridge

Lightweight bridge that connects Claude CLI to a Telegram bot.
Designed for backup Jarvis instances on laptops.

Usage:
    python claude_telegram_bridge.py --token YOUR_BOT_TOKEN --allowed-users 123456789

Environment:
    TELEGRAM_BOT_TOKEN - Bot token from @BotFather
    ALLOWED_USERS - Comma-separated user IDs (get yours from @userinfobot)
    CLAUDE_WORKSPACE - Path to workspace (optional)
"""

import os
import sys
import asyncio
import subprocess
import logging
import argparse
from pathlib import Path
from datetime import datetime

# Telegram
try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
except ImportError:
    print("Installing python-telegram-bot...")
    subprocess.run([sys.executable, "-m", "pip", "install", "python-telegram-bot>=20.0"], check=True)
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Config
ALLOWED_USERS: set[int] = set()
WORKSPACE: Path = Path.home() / "jarvis-workspace"
MACHINE_NAME: str = os.getenv("MACHINE_NAME", "laptop")

# Conversation state per user
conversations: dict[int, list[dict]] = {}


def get_claude_path() -> str:
    """Find claude CLI executable."""
    # Try common locations
    candidates = [
        "claude",  # In PATH
        str(Path.home() / ".claude" / "claude"),
        str(Path.home() / "AppData" / "Local" / "Programs" / "claude" / "claude.exe"),
        "/usr/local/bin/claude",
    ]
    
    for candidate in candidates:
        try:
            result = subprocess.run(
                [candidate, "--version"],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                return candidate
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    
    raise FileNotFoundError("Claude CLI not found. Install it first: https://claude.ai/code")


async def run_claude(message: str, user_id: int) -> str:
    """Run claude CLI with a message."""
    claude_path = get_claude_path()
    
    # Create workspace if not exists
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    
    # Build command - use --print for non-interactive mode
    cmd = [
        claude_path,
        "--print",  # Non-interactive, just print response
        message
    ]
    
    logger.info(f"Running Claude for user {user_id}: {message[:50]}...")
    
    try:
        # Run with timeout
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(WORKSPACE)
        )
        
        stdout, stderr = await asyncio.wait_for(
            process.communicate(),
            timeout=300  # 5 minute timeout
        )
        
        response = stdout.decode("utf-8", errors="replace").strip()
        
        if process.returncode != 0:
            error = stderr.decode("utf-8", errors="replace").strip()
            logger.error(f"Claude error: {error}")
            return f"❌ Error: {error[:500]}"
        
        if not response:
            return "🤔 Claude returned empty response"
        
        return response
        
    except asyncio.TimeoutExpired:
        return "⏱️ Claude timed out after 5 minutes"
    except FileNotFoundError:
        return "❌ Claude CLI not found. Is it installed?"
    except Exception as e:
        logger.exception("Claude execution error")
        return f"❌ Error: {str(e)[:200]}"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    user_id = update.effective_user.id
    
    if ALLOWED_USERS and user_id not in ALLOWED_USERS:
        await update.message.reply_text("⛔ Unauthorized")
        return
    
    await update.message.reply_text(
        f"🤖 **{MACHINE_NAME.title()} Jarvis**\n\n"
        f"Backup Claude instance running on {MACHINE_NAME}.\n\n"
        f"Just send me a message and I'll pass it to Claude CLI.\n\n"
        f"Commands:\n"
        f"/status - Check system status\n"
        f"/clear - Clear conversation history",
        parse_mode="Markdown"
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status command."""
    user_id = update.effective_user.id
    
    if ALLOWED_USERS and user_id not in ALLOWED_USERS:
        await update.message.reply_text("⛔ Unauthorized")
        return
    
    # Check Claude
    try:
        claude_path = get_claude_path()
        claude_ok = "✅"
    except FileNotFoundError:
        claude_ok = "❌"
    
    # System info
    import platform
    
    await update.message.reply_text(
        f"📊 **{MACHINE_NAME.title()} Status**\n\n"
        f"Claude CLI: {claude_ok}\n"
        f"Machine: {platform.node()}\n"
        f"OS: {platform.system()} {platform.release()}\n"
        f"Python: {platform.python_version()}\n"
        f"Workspace: {WORKSPACE}\n"
        f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        parse_mode="Markdown"
    )


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /clear command."""
    user_id = update.effective_user.id
    
    if ALLOWED_USERS and user_id not in ALLOWED_USERS:
        await update.message.reply_text("⛔ Unauthorized")
        return
    
    conversations.pop(user_id, None)
    await update.message.reply_text("🗑️ Conversation cleared")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming text messages."""
    user_id = update.effective_user.id
    
    if ALLOWED_USERS and user_id not in ALLOWED_USERS:
        logger.warning(f"Unauthorized user: {user_id}")
        await update.message.reply_text("⛔ Unauthorized. Contact admin for access.")
        return
    
    message = update.message.text
    
    # Show typing indicator
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # Run Claude
    response = await run_claude(message, user_id)
    
    # Telegram has 4096 char limit, split if needed
    if len(response) > 4000:
        chunks = [response[i:i+4000] for i in range(0, len(response), 4000)]
        for chunk in chunks:
            await update.message.reply_text(chunk)
    else:
        await update.message.reply_text(response)


def main():
    parser = argparse.ArgumentParser(description="Claude CLI → Telegram Bridge")
    parser.add_argument("--token", help="Telegram bot token")
    parser.add_argument("--allowed-users", help="Comma-separated allowed user IDs")
    parser.add_argument("--workspace", help="Claude workspace path")
    parser.add_argument("--machine-name", help="Machine identifier")
    args = parser.parse_args()
    
    # Get config from args or env
    token = args.token or os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Error: No bot token. Set TELEGRAM_BOT_TOKEN or use --token")
        sys.exit(1)
    
    global ALLOWED_USERS, WORKSPACE, MACHINE_NAME
    
    allowed = args.allowed_users or os.getenv("ALLOWED_USERS", "")
    if allowed:
        ALLOWED_USERS = {int(uid.strip()) for uid in allowed.split(",") if uid.strip()}
        logger.info(f"Allowed users: {ALLOWED_USERS}")
    else:
        logger.warning("No user restrictions - anyone can use this bot!")
    
    if args.workspace:
        WORKSPACE = Path(args.workspace)
    elif os.getenv("CLAUDE_WORKSPACE"):
        WORKSPACE = Path(os.getenv("CLAUDE_WORKSPACE"))
    
    if args.machine_name:
        MACHINE_NAME = args.machine_name
    elif os.getenv("MACHINE_NAME"):
        MACHINE_NAME = os.getenv("MACHINE_NAME")
    
    # Verify Claude is available
    try:
        claude_path = get_claude_path()
        logger.info(f"Found Claude CLI: {claude_path}")
    except FileNotFoundError:
        logger.error("Claude CLI not found! Install from https://claude.ai/code")
        sys.exit(1)
    
    logger.info(f"Starting {MACHINE_NAME} Jarvis...")
    logger.info(f"Workspace: {WORKSPACE}")
    
    # Build application
    app = Application.builder().token(token).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("clear", clear))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Run
    logger.info("Bot started. Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
