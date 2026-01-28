#!/usr/bin/env python3
"""
Puppeteer Bot — Industrial AR Assistant

Production-ready Telegram bot that serves as the test surface for Frame glasses.
When glasses arrive, the only change is input source (Frame camera → this bot).

Features:
- Photo analysis (equipment ID, nameplate OCR, fault diagnosis)
- Voice commands (transcription + AI response)  
- Work order creation (Atlas CMMS integration)
- Real-time expert guidance mode

Usage:
    # Set environment variables
    export PUPPETEER_BOT_TOKEN="your-telegram-bot-token"
    export GEMINI_API_KEY="your-gemini-key"
    export CMMS_URL="http://72.60.175.144:8080"
    export CMMS_EMAIL="mike@cranesync.com"
    export CMMS_PASSWORD="CraneSync2026!"
    
    # Run
    python bot.py
"""

import os
import sys
import json
import asyncio
import logging
import aiohttp
from datetime import datetime
from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    CallbackQueryHandler, filters, ContextTypes
)
import google.generativeai as genai

# ============================================================================
# CONFIG
# ============================================================================

TELEGRAM_TOKEN = os.getenv("PUPPETEER_BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
CMMS_URL = os.getenv("CMMS_URL", "http://72.60.175.144:8080")
CMMS_EMAIL = os.getenv("CMMS_EMAIL", "mike@cranesync.com")
CMMS_PASSWORD = os.getenv("CMMS_PASSWORD", "CraneSync2026!")

# Allowed users (Telegram user IDs)
ALLOWED_USERS = {
    8445149012,  # Mike
}

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/var/log/puppeteer-bot.log') if os.path.exists('/var/log') else logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# AI PROMPTS (THE MOAT - KEEP SECRET)
# ============================================================================

DIAGNOSIS_PROMPT = """You are Puppeteer, an AI assistant running on AR glasses for industrial maintenance technicians.

CONTEXT: The technician just pointed their glasses at equipment and asked for help.

YOUR CAPABILITIES:
1. READ NAMEPLATES: Extract ALL text (model, serial, specs, ratings, dates)
2. IDENTIFY EQUIPMENT: VFDs, PLCs, motors, sensors, HMIs, power supplies, etc.
3. DIAGNOSE ISSUES: Based on visible indicators (LEDs, damage, wear, connections)
4. PROVIDE STEPS: Clear, numbered troubleshooting steps
5. ESTIMATE COSTS: Rough repair/replacement costs

RESPONSE FORMAT (optimized for AR display):
```
📋 [EQUIPMENT NAME]
Model: [if visible]
Serial: [if visible]

🔍 OBSERVED:
• [What you see - LEDs, damage, connections, etc.]

⚠️ LIKELY ISSUE:
[One-line diagnosis]

🔧 NEXT STEPS:
1. [First action]
2. [Second action]  
3. [Third action]

💰 EST: [$X - $Y if applicable]

🛡️ SAFETY: [Critical warnings - voltage, lockout, PPE]
```

RULES:
- BE CONCISE: Technician is working, not reading essays
- BE SPECIFIC: "Check terminal 3" not "check connections"
- BE SAFE: Always mention electrical/mechanical hazards
- If you can't identify equipment, say so and ask for closer photo of nameplate
"""

VOICE_PROMPT = """You are Puppeteer, an AI assistant running on AR glasses. The technician just asked you a question via voice.

Respond conversationally but concisely. They're working with their hands, so keep it brief.

If they're asking about equipment you previously analyzed, reference that context.
If they're asking a general question, answer it directly.
If they're asking for next steps, give numbered instructions.

Keep responses under 50 words unless they ask for detail.
"""

WORK_ORDER_PROMPT = """Based on the equipment diagnosis, generate a work order in JSON format:

{
    "title": "Brief action-oriented title (under 60 chars)",
    "description": "Detailed description including:\n- Equipment identified\n- Issue diagnosed\n- Recommended actions\n- Parts that may be needed",
    "priority": "NONE|LOW|MEDIUM|HIGH",
    "estimatedHours": <number or null>
}

Only output valid JSON, nothing else.
"""

# ============================================================================
# GEMINI CLIENT
# ============================================================================

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

async def analyze_image(image_bytes: bytes, prompt: str = DIAGNOSIS_PROMPT) -> str:
    """Analyze image with Gemini multimodal"""
    try:
        response = model.generate_content([
            prompt,
            {"mime_type": "image/jpeg", "data": image_bytes}
        ])
        return response.text
    except Exception as e:
        logger.error(f"Gemini image analysis failed: {e}")
        return f"❌ Analysis failed: {str(e)}"

async def analyze_voice(audio_bytes: bytes, mime_type: str = "audio/ogg") -> str:
    """Analyze voice with Gemini"""
    try:
        response = model.generate_content([
            VOICE_PROMPT,
            {"mime_type": mime_type, "data": audio_bytes}
        ])
        return response.text
    except Exception as e:
        logger.error(f"Gemini voice analysis failed: {e}")
        return f"❌ Voice processing failed: {str(e)}"

async def generate_work_order_json(diagnosis: str) -> dict:
    """Generate work order from diagnosis"""
    try:
        response = model.generate_content([
            WORK_ORDER_PROMPT,
            f"Diagnosis:\n{diagnosis}"
        ])
        # Extract JSON from response
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text)
    except Exception as e:
        logger.error(f"Work order generation failed: {e}")
        return None

# ============================================================================
# CMMS CLIENT (Atlas CMMS)
# ============================================================================

class CMSClient:
    def __init__(self, base_url: str, email: str, password: str):
        self.base_url = base_url.rstrip('/')
        self.email = email
        self.password = password
        self.token = None
        
    async def login(self) -> bool:
        """Authenticate and get token"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/auth/signin",
                    json={"email": self.email, "password": self.password, "type": "client"}
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        self.token = data.get("accessToken")
                        logger.info("CMMS login successful")
                        return True
                    else:
                        logger.error(f"CMMS login failed: {resp.status}")
                        return False
        except Exception as e:
            logger.error(f"CMMS login error: {e}")
            return False
    
    async def create_work_order(self, title: str, description: str, priority: str = "MEDIUM") -> dict:
        """Create a work order"""
        if not self.token:
            await self.login()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/work-orders",
                    headers={"Authorization": f"Bearer {self.token}"},
                    json={
                        "title": title,
                        "description": description,
                        "priority": priority,
                    }
                ) as resp:
                    if resp.status in (200, 201):
                        data = await resp.json()
                        logger.info(f"Work order created: {data.get('id')}")
                        return data
                    else:
                        text = await resp.text()
                        logger.error(f"WO creation failed: {resp.status} - {text}")
                        return None
        except Exception as e:
            logger.error(f"WO creation error: {e}")
            return None

cmms = CMSClient(CMMS_URL, CMMS_EMAIL, CMMS_PASSWORD)

# ============================================================================
# SESSION STATE (per user)
# ============================================================================

user_sessions = {}

def get_session(user_id: int) -> dict:
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            "last_diagnosis": None,
            "last_photo": None,
            "last_equipment": None,
            "history": []
        }
    return user_sessions[user_id]

# ============================================================================
# TELEGRAM HANDLERS
# ============================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message"""
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("⛔ Access denied. Contact admin for access.")
        return
        
    await update.message.reply_text(
        "🥽 *PUPPETEER ONLINE*\n\n"
        "Industrial AR Assistant ready.\n\n"
        "*Commands:*\n"
        "📷 Send photo → Equipment diagnosis\n"
        "🎤 Send voice → Voice command\n"
        "💬 Type question → AI response\n\n"
        "*Quick Actions:*\n"
        "/wo — Create work order from last diagnosis\n"
        "/history — View recent diagnoses\n"
        "/status — System status\n\n"
        "_Point. Ask. Fix._",
        parse_mode='Markdown'
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process equipment photo"""
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        return
    
    session = get_session(user_id)
    status_msg = await update.message.reply_text("🔍 Analyzing...")
    
    try:
        # Get photo
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        photo_bytes = bytes(await file.download_as_bytearray())
        
        # Analyze
        diagnosis = await analyze_image(photo_bytes)
        
        # Store in session
        session["last_diagnosis"] = diagnosis
        session["last_photo"] = photo_bytes
        session["history"].append({
            "type": "diagnosis",
            "timestamp": datetime.now().isoformat(),
            "result": diagnosis[:200] + "..." if len(diagnosis) > 200 else diagnosis
        })
        
        # Keep history bounded
        if len(session["history"]) > 20:
            session["history"] = session["history"][-20:]
        
        # Reply with diagnosis + action buttons
        keyboard = [
            [
                InlineKeyboardButton("📝 Create Work Order", callback_data="create_wo"),
                InlineKeyboardButton("🔄 Re-analyze", callback_data="reanalyze"),
            ],
            [
                InlineKeyboardButton("📷 Nameplate Focus", callback_data="nameplate"),
                InlineKeyboardButton("❓ Ask Follow-up", callback_data="followup"),
            ]
        ]
        
        await status_msg.edit_text(
            diagnosis,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        logger.info(f"Photo analyzed for user {user_id}")
        
    except Exception as e:
        logger.error(f"Photo handler error: {e}")
        await status_msg.edit_text(f"❌ Analysis failed: {str(e)}")

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process voice command"""
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        return
    
    session = get_session(user_id)
    status_msg = await update.message.reply_text("🎤 Processing voice...")
    
    try:
        voice = update.message.voice
        file = await context.bot.get_file(voice.file_id)
        voice_bytes = bytes(await file.download_as_bytearray())
        
        # Build context from session
        context_prompt = VOICE_PROMPT
        if session["last_diagnosis"]:
            context_prompt += f"\n\nPrevious equipment diagnosis:\n{session['last_diagnosis'][:500]}"
        
        # Analyze
        response = model.generate_content([
            context_prompt,
            {"mime_type": "audio/ogg", "data": voice_bytes}
        ])
        
        await status_msg.edit_text(response.text)
        logger.info(f"Voice processed for user {user_id}")
        
    except Exception as e:
        logger.error(f"Voice handler error: {e}")
        await status_msg.edit_text(f"❌ Voice processing failed: {str(e)}")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process text question"""
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        return
    
    session = get_session(user_id)
    question = update.message.text
    
    try:
        # Build context
        context_parts = [VOICE_PROMPT]
        if session["last_diagnosis"]:
            context_parts.append(f"Previous diagnosis:\n{session['last_diagnosis'][:500]}")
        context_parts.append(f"Technician asks: {question}")
        
        response = model.generate_content(context_parts)
        await update.message.reply_text(response.text)
        
    except Exception as e:
        logger.error(f"Text handler error: {e}")
        await update.message.reply_text(f"❌ Failed: {str(e)}")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    user_id = query.from_user.id
    if user_id not in ALLOWED_USERS:
        return
    
    await query.answer()
    session = get_session(user_id)
    
    if query.data == "create_wo":
        if not session["last_diagnosis"]:
            await query.edit_message_text("No diagnosis to create WO from. Send a photo first.")
            return
        
        await query.edit_message_text("📝 Creating work order...")
        
        # Generate WO details
        wo_data = await generate_work_order_json(session["last_diagnosis"])
        if not wo_data:
            await query.edit_message_text("❌ Failed to generate work order details")
            return
        
        # Create in CMMS
        result = await cmms.create_work_order(
            title=wo_data.get("title", "Equipment Issue"),
            description=wo_data.get("description", session["last_diagnosis"]),
            priority=wo_data.get("priority", "MEDIUM")
        )
        
        if result:
            await query.edit_message_text(
                f"✅ *Work Order Created*\n\n"
                f"*ID:* {result.get('id', 'N/A')}\n"
                f"*Title:* {wo_data.get('title', 'N/A')}\n"
                f"*Priority:* {wo_data.get('priority', 'MEDIUM')}\n\n"
                f"View in CMMS: {CMMS_URL}/app/work-orders",
                parse_mode='Markdown'
            )
        else:
            await query.edit_message_text("❌ Failed to create work order in CMMS")
    
    elif query.data == "reanalyze":
        if session["last_photo"]:
            await query.edit_message_text("🔄 Re-analyzing...")
            diagnosis = await analyze_image(session["last_photo"])
            session["last_diagnosis"] = diagnosis
            await query.edit_message_text(diagnosis)
        else:
            await query.edit_message_text("No photo to re-analyze. Send a new photo.")
    
    elif query.data == "nameplate":
        if session["last_photo"]:
            await query.edit_message_text("🔍 Focusing on nameplate...")
            prompt = """Focus ONLY on reading the nameplate/label in this image.
            Extract ALL text you can see:
            - Manufacturer
            - Model number
            - Serial number
            - Voltage/current ratings
            - Date codes
            - Any other specifications
            
            Format as a clean list. If text is unclear, indicate [unclear]."""
            diagnosis = await analyze_image(session["last_photo"], prompt)
            await query.edit_message_text(f"📋 *NAMEPLATE DATA*\n\n{diagnosis}", parse_mode='Markdown')
        else:
            await query.edit_message_text("No photo. Send a photo of the nameplate.")

async def cmd_wo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Quick work order creation"""
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        return
    
    session = get_session(user_id)
    if not session["last_diagnosis"]:
        await update.message.reply_text("No recent diagnosis. Send a photo first.")
        return
    
    await update.message.reply_text("📝 Creating work order...")
    
    wo_data = await generate_work_order_json(session["last_diagnosis"])
    if wo_data:
        result = await cmms.create_work_order(
            title=wo_data.get("title", "Equipment Issue"),
            description=wo_data.get("description", session["last_diagnosis"]),
            priority=wo_data.get("priority", "MEDIUM")
        )
        if result:
            await update.message.reply_text(f"✅ Work order created: #{result.get('id')}")
        else:
            await update.message.reply_text("❌ CMMS error")
    else:
        await update.message.reply_text("❌ Failed to generate WO")

async def cmd_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show recent diagnoses"""
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        return
    
    session = get_session(user_id)
    if not session["history"]:
        await update.message.reply_text("No history yet. Send a photo to start.")
        return
    
    text = "📜 *Recent Activity*\n\n"
    for i, item in enumerate(reversed(session["history"][-5:]), 1):
        text += f"{i}. {item['timestamp'][:16]}\n{item['result'][:100]}...\n\n"
    
    await update.message.reply_text(text, parse_mode='Markdown')

async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """System status"""
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        return
    
    # Test CMMS connection
    cmms_ok = await cmms.login()
    
    await update.message.reply_text(
        "🥽 *PUPPETEER STATUS*\n\n"
        f"✅ AI: Gemini 2.5 Flash\n"
        f"{'✅' if cmms_ok else '❌'} CMMS: {CMMS_URL}\n"
        f"✅ Bot: Online\n\n"
        f"_Ready for glasses integration_",
        parse_mode='Markdown'
    )

# ============================================================================
# MAIN
# ============================================================================

def main():
    if not TELEGRAM_TOKEN:
        logger.error("PUPPETEER_BOT_TOKEN not set")
        sys.exit(1)
    if not GEMINI_KEY:
        logger.error("GEMINI_API_KEY not set")
        sys.exit(1)
    
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("wo", cmd_wo))
    app.add_handler(CommandHandler("history", cmd_history))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(CallbackQueryHandler(handle_callback))
    
    logger.info("🥽 PUPPETEER BOT STARTING...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
