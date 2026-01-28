#!/usr/bin/env python3
"""
FactoryLM Frame Mock Bot

Simulates the Frame glasses workflow via Telegram:
1. User sends photo → AI diagnoses equipment
2. User sends voice → transcribed → AI responds
3. Tests the full pipeline before glasses arrive

Usage:
    pip install python-telegram-bot google-generativeai
    export TELEGRAM_BOT_TOKEN=xxx
    export GEMINI_API_KEY=xxx
    python frame_mock_bot.py
"""

import os
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# Config
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Gemini
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# System prompt - THE MOAT (keep this secret in production)
SYSTEM_PROMPT = """You are FactoryLM, an AI assistant built into AR glasses for industrial maintenance technicians.

Your capabilities:
1. READ NAMEPLATES: Extract all text from equipment nameplates (model, serial, specs)
2. IDENTIFY EQUIPMENT: Recognize industrial equipment (VFDs, PLCs, motors, sensors, etc.)
3. DIAGNOSE FAULTS: Based on visible indicators, suggest likely issues
4. PROVIDE STEPS: Give clear, numbered troubleshooting steps
5. ESTIMATE COSTS: Rough repair cost estimates when possible

Your response style:
- CONCISE: Technician is working, not reading essays
- STRUCTURED: Use headers, bullets, numbered steps
- ACTIONABLE: What should they DO next?
- SAFE: Always mention safety precautions for electrical/mechanical work

Format your responses like this:
📋 EQUIPMENT: [Name/Model]
🔍 IDENTIFIED: [What you see]
⚠️ LIKELY ISSUE: [Diagnosis]
🔧 NEXT STEPS:
1. [Step 1]
2. [Step 2]
3. [Step 3]
💰 EST. COST: [If applicable]
🛡️ SAFETY: [Relevant warnings]
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message"""
    await update.message.reply_text(
        "🥽 *FactoryLM Frame Simulator*\n\n"
        "This bot simulates the Frame AR glasses experience.\n\n"
        "*How to use:*\n"
        "📷 Send a photo of equipment → Get AI diagnosis\n"
        "🎤 Send a voice message → Get AI response\n"
        "💬 Type a question → Get AI answer\n\n"
        "_Simulating: Point. Ask. Fix._",
        parse_mode='Markdown'
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process equipment photo"""
    await update.message.reply_text("🔍 Analyzing equipment...")
    
    try:
        # Get the largest photo
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        
        # Download photo
        photo_bytes = await file.download_as_bytearray()
        
        # Send to Gemini
        response = model.generate_content([
            SYSTEM_PROMPT,
            "The technician just pointed their AR glasses at this equipment. Analyze what you see:",
            {"mime_type": "image/jpeg", "data": bytes(photo_bytes)}
        ])
        
        await update.message.reply_text(response.text)
        
    except Exception as e:
        logger.error(f"Photo analysis error: {e}")
        await update.message.reply_text(f"❌ Analysis failed: {str(e)}")

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process voice message"""
    await update.message.reply_text("🎤 Processing voice...")
    
    try:
        voice = update.message.voice
        file = await context.bot.get_file(voice.file_id)
        
        # Download voice file
        voice_bytes = await file.download_as_bytearray()
        
        # For now, use Gemini's audio capabilities
        # In production, use Whisper for transcription
        response = model.generate_content([
            SYSTEM_PROMPT,
            "The technician just asked a question via voice. Respond helpfully:",
            {"mime_type": "audio/ogg", "data": bytes(voice_bytes)}
        ])
        
        await update.message.reply_text(response.text)
        
    except Exception as e:
        logger.error(f"Voice processing error: {e}")
        await update.message.reply_text(f"❌ Voice processing failed: {str(e)}")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process text question"""
    question = update.message.text
    
    try:
        response = model.generate_content([
            SYSTEM_PROMPT,
            f"The technician asks: {question}"
        ])
        
        await update.message.reply_text(response.text)
        
    except Exception as e:
        logger.error(f"Text processing error: {e}")
        await update.message.reply_text(f"❌ Processing failed: {str(e)}")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle document uploads (manuals, etc.)"""
    await update.message.reply_text(
        "📄 Document received. In the full version, I'd extract relevant specs and add to your equipment database."
    )

def main():
    """Run the bot"""
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN not set")
    if not GEMINI_KEY:
        raise ValueError("GEMINI_API_KEY not set")
    
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    
    logger.info("🥽 FactoryLM Frame Mock Bot starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
