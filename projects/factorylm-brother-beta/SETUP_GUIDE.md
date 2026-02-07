# FactoryLM Telegram Bot - Deployment Guide

**Target**: Deploy production-ready bot for Brother (first external beta user)  
**Timeline**: Complete setup in 1 week  
**Environment**: factorylm-prod VPS (DigitalOcean Atlanta)

---

## 🚀 Quick Start (30 minutes)

### Step 1: Create Telegram Bot
```bash
# 1. Message @BotFather on Telegram
# 2. Use command: /newbot
# 3. Choose name: "FactoryLM Assistant"  
# 4. Choose username: "FactoryLMBot" (or available variant)
# 5. Save the bot token (format: 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11)
```

### Step 2: Clone & Configure Bot Code
```bash
# SSH to production server
ssh root@factorylm-prod

# Navigate to workspace
cd /opt/factorylm

# Create bot directory
mkdir -p telegram-bot
cd telegram-bot

# Copy PLC Copilot as base (already proven to work)
cp -r /opt/plc-copilot/* .

# Create Brother-specific configuration
cat > brother_bot_config.py << 'EOF'
# Brother Beta Bot Configuration
BOT_NAME = "FactoryLM Assistant"
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # From BotFather
ALLOWED_USERS = "BROTHER_TELEGRAM_ID"  # Brother's Telegram user ID

# Brother's facility specifics
FACILITY_NAME = "Indiana Injection Molding"
EQUIPMENT_TYPES = [
    "injection_molding_machine", 
    "hydraulic_pump",
    "cooling_tower", 
    "air_compressor",
    "plc_controller"
]

# CMMS Integration (reuse existing)
CMMS_BASE_URL = "http://localhost:8080"
CMMS_EMAIL = "brother@factorylm.com" 
CMMS_PASSWORD = "secure_password_123"

# AI Services (reuse existing tokens)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
EOF
```

### Step 3: Install Dependencies & Start Bot
```bash
# Use existing Python environment
source /opt/plc-copilot/venv/bin/activate

# Install additional dependencies for Brother bot
pip install python-telegram-bot==20.7
pip install speech_recognition
pip install pyttsx3

# Create Brother bot service
cat > /etc/systemd/system/brother-bot.service << 'EOF'
[Unit]
Description=FactoryLM Brother Beta Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/factorylm/telegram-bot
ExecStart=/opt/plc-copilot/venv/bin/python brother_bot.py
Restart=always
RestartSec=10
Environment=GEMINI_API_KEY=your_existing_key

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
systemctl enable brother-bot
systemctl start brother-bot
systemctl status brother-bot
```

---

## 📋 Detailed Setup Process

### Prerequisites Checklist
- [ ] Access to factorylm-prod server (SSH key configured)
- [ ] Telegram account for bot creation  
- [ ] Brother's Telegram user ID
- [ ] CMMS running and accessible
- [ ] Existing Gemini API key working

### Phase 1: Core Bot Setup (Day 1)

#### 1.1 Environment Preparation
```bash
# Check existing services are running
systemctl status cmms-backend
systemctl status nginx  
docker ps | grep cmms

# Verify CMMS API accessible
curl -X POST http://localhost:8080/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@test.com","password":"password","type":"client"}'
```

#### 1.2 Bot Token Configuration
```bash
cd /opt/factorylm/telegram-bot

# Create secure environment file
cat > .env << 'EOF'
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
BOT_NAME=FactoryLM Assistant

# User Access Control  
ALLOWED_USERS=BROTHER_TELEGRAM_ID
ADMIN_USERS=YOUR_TELEGRAM_ID

# CMMS Connection (reuse existing)
CMMS_BASE_URL=http://localhost:8080
CMMS_EMAIL=admin@test.com
CMMS_PASSWORD=password

# AI Services
GEMINI_API_KEY=your_existing_key
OPENAI_API_KEY=your_openai_key

# Brother's Facility Context
FACILITY_NAME="Indiana Injection Molding"
TIMEZONE=America/Indiana/Indianapolis
EOF

chmod 600 .env  # Secure the environment file
```

#### 1.3 Create Brother Bot Script
```bash
cat > brother_bot.py << 'EOF'
#!/usr/bin/env python3
"""
FactoryLM Brother Beta Bot
Based on PLC Copilot with Brother-specific enhancements
"""
import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Load environment variables
load_dotenv()

# Import existing PLC Copilot functionality
import sys
sys.path.append('/opt/plc-copilot')
from photo_to_cmms_bot import (
    analyze_photo, cmms, rate_limiter, 
    handle_photo as plc_handle_photo
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_USERS = set(map(int, os.getenv("ALLOWED_USERS", "").split(",")))

async def start_command(update: Update, context):
    """Enhanced start message for Brother"""
    keyboard = [
        [InlineKeyboardButton("📸 Analyze Equipment", callback_data="analyze")],
        [InlineKeyboardButton("🔧 Create Work Order", callback_data="workorder")],
        [InlineKeyboardButton("🧩 Parts Lookup", callback_data="parts")],
        [InlineKeyboardButton("⚠️ Fault Codes", callback_data="faults")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_msg = (
        "🏭 *FactoryLM Assistant* - Brother Beta\n\n"
        "Industrial maintenance AI at your service!\n\n"
        "📸 *Photo Analysis*: Take pic → get diagnosis\n"
        "🔧 *Work Orders*: Create, track, manage\n" 
        "🧩 *Parts Lookup*: Cross-reference & inventory\n"
        "⚠️ *Fault Codes*: Instant diagnostics\n\n"
        "Send a photo of any equipment to get started!"
    )
    
    await update.message.reply_text(
        welcome_msg, 
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def help_command(update: Update, context):
    """Help command with Brother-specific examples"""
    help_text = (
        "🛠️ *FactoryLM Commands*\n\n"
        "*Photo Analysis*:\n"
        "• Send equipment photo → instant diagnosis\n"
        "• Works with: motors, drives, PLCs, pumps\n\n"
        "*Voice Commands*:\n" 
        "• Send voice message for hands-free operation\n"
        "• 'Check status of Injection Machine 3'\n\n"
        "*Text Queries*:\n"
        "• 'What is fault E-01 on Fanuc robot?'\n"
        "• 'Cross reference SKF bearing 6205'\n\n"
        "*Quick Actions*:\n"
        "/equipment - List all facility equipment\n"
        "/status - System status and recent activity\n"
        "/help - Show this help message\n\n"
        "💡 *Pro Tip*: Use voice messages while working hands-free!"
    )
    
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def equipment_command(update: Update, context):
    """List equipment specific to Brother's facility"""
    try:
        # Get assets from CMMS
        assets = cmms.list_assets()
        
        if not assets:
            await update.message.reply_text(
                "No equipment found in system. Add equipment by taking photos!"
            )
            return
            
        # Group by type for better organization
        equipment_msg = "🏭 *Indiana Injection Molding Equipment*\n\n"
        
        injection_machines = [a for a in assets if 'injection' in a.get('name', '').lower()]
        pumps = [a for a in assets if 'pump' in a.get('name', '').lower()]
        other = [a for a in assets if a not in injection_machines and a not in pumps]
        
        if injection_machines:
            equipment_msg += "*Injection Molding Machines:*\n"
            for asset in injection_machines[:5]:
                equipment_msg += f"• {asset.get('name', 'Unknown')} (#{asset.get('id')})\n"
        
        if pumps:  
            equipment_msg += "\n*Pumps & Hydraulics:*\n"
            for asset in pumps[:5]:
                equipment_msg += f"• {asset.get('name', 'Unknown')} (#{asset.get('id')})\n"
                
        if other:
            equipment_msg += "\n*Other Equipment:*\n" 
            for asset in other[:5]:
                equipment_msg += f"• {asset.get('name', 'Unknown')} (#{asset.get('id')})\n"
        
        if len(assets) > 15:
            equipment_msg += f"\n_...and {len(assets) - 15} more items_"
            
        await update.message.reply_text(equipment_msg, parse_mode="Markdown")
        
    except Exception as e:
        logger.error(f"Equipment command failed: {e}")
        await update.message.reply_text("❌ Could not retrieve equipment list.")

async def handle_photo_brother(update: Update, context):
    """Enhanced photo handling for Brother with facility context"""
    user_id = update.effective_user.id
    
    if ALLOWED_USERS and user_id not in ALLOWED_USERS:
        await update.message.reply_text(
            "🔒 Access denied. This is a private beta for facility maintenance staff."
        )
        return
        
    # Add facility context to the message
    context.user_data['facility'] = "Indiana Injection Molding"
    context.user_data['user_role'] = "maintenance_tech"
    
    # Use existing PLC Copilot photo analysis
    await plc_handle_photo(update, context)

async def handle_voice_query(update: Update, context):
    """Voice message processing for hands-free operation"""
    user_id = update.effective_user.id
    
    if ALLOWED_USERS and user_id not in ALLOWED_USERS:
        await update.message.reply_text("🔒 Access denied.")
        return
        
    try:
        # Download voice message
        voice_file = await update.message.voice.get_file()
        voice_data = await voice_file.download_as_bytearray()
        
        # For now, acknowledge and suggest text input
        await update.message.reply_text(
            "🎤 Voice message received! \n\n"
            "Voice processing coming soon. For now, please type your question or send a photo."
        )
        
    except Exception as e:
        logger.error(f"Voice processing failed: {e}")
        await update.message.reply_text("❌ Voice processing failed. Please try typing your question.")

def main():
    """Main bot application"""
    if not BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment!")
        return
        
    # Create application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("equipment", equipment_command))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo_brother))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice_query))
    
    logger.info("🤖 FactoryLM Brother Bot starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
EOF

chmod +x brother_bot.py
```

### Phase 2: Brother User Onboarding (Day 2)

#### 2.1 Get Brother's Telegram ID
```bash
# Temporarily enable open access to get Brother's ID
# Edit brother_bot.py and comment out the ALLOWED_USERS check
# Ask Brother to send /start to the bot
# Check logs to get his Telegram user ID

# Example log entry:
# INFO:root:User 123456789 (Brother) started bot

# Then update .env file with Brother's ID
echo "ALLOWED_USERS=123456789" >> .env
```

#### 2.2 Create Brother's CMMS Account
```bash
# Create Brother's account in CMMS
curl -X POST http://localhost:8080/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "brother@factorylm.com",
    "password": "TempPassword123!",
    "firstName": "Brother",
    "lastName": "Beta", 
    "companyName": "Indiana Injection Molding",
    "role": "maintenance_tech"
  }'

# Update .env with Brother's credentials
cat >> .env << 'EOF'
CMMS_BROTHER_EMAIL=brother@factorylm.com
CMMS_BROTHER_PASSWORD=TempPassword123!
EOF
```

#### 2.3 Test Basic Functionality  
```bash
# Start the bot
systemctl restart brother-bot

# Test bot is responding
curl -X GET "https://api.telegram.org/bot$BOT_TOKEN/getMe"

# Check logs
journalctl -f -u brother-bot
```

### Phase 3: Feature Enhancement (Days 3-5)

#### 3.1 Fault Code Database Setup
```bash
# Create fault code database
cd /opt/factorylm/telegram-bot

cat > setup_fault_codes.sql << 'EOF'
-- Fault code database for Brother's equipment
CREATE TABLE IF NOT EXISTS fault_codes (
    id SERIAL PRIMARY KEY,
    manufacturer VARCHAR(100),
    equipment_type VARCHAR(100), 
    code VARCHAR(50),
    description TEXT,
    solution TEXT,
    tools_required JSON,
    priority VARCHAR(20)
);

-- Common fault codes for injection molding
INSERT INTO fault_codes (manufacturer, equipment_type, code, description, solution, priority) VALUES
('Fanuc', 'Robot', 'E-01', 'Emergency Stop Active', 'Check all E-stop buttons and safety gates', 'HIGH'),
('Allen-Bradley', 'PLC', 'F072', 'Ground Fault Detected', 'Check motor leads and cable insulation', 'HIGH'),
('Siemens', 'Drive', 'A0501', 'Overcurrent Protection', 'Check motor connections and load', 'MEDIUM'),
('Hydraulic', 'Pump', 'P001', 'Low Pressure', 'Check hydraulic fluid level and filters', 'HIGH');
EOF

# Apply to CMMS database
docker exec cmms-backend psql -U postgres -d grash < setup_fault_codes.sql
```

#### 3.2 Add Brother-Specific Equipment Profiles
```bash
cat > brother_equipment.py << 'EOF'
# Brother's Facility Equipment Profiles

INJECTION_MACHINES = {
    "Machine_1": {
        "manufacturer": "Cincinnati Milacron", 
        "model": "VT-165",
        "location": "Production Floor A",
        "critical_components": ["hydraulic_pump", "heating_zones", "injection_unit"]
    },
    "Machine_2": {
        "manufacturer": "Haitian",
        "model": "MA1800III", 
        "location": "Production Floor A",
        "critical_components": ["servo_motor", "barrel_heaters", "clamp_unit"]
    }
}

PUMPS = {
    "Main_Hydraulic": {
        "manufacturer": "Rexroth",
        "model": "A10V071",
        "location": "Utility Room",
        "specs": {"pressure": "3000_psi", "flow": "45_gpm"}
    }
}

def get_equipment_context(equipment_name):
    """Return Brother-specific context for equipment"""
    # Implementation here
    pass
EOF
```

### Phase 4: Testing & Validation (Day 6)

#### 4.1 Test Checklist with Brother
```bash
# Create test script for Brother
cat > brother_test_script.sh << 'EOF'
#!/bin/bash
echo "🧪 FactoryLM Brother Bot Test Script"
echo "===================================="

echo "1. Testing bot responsiveness..."
curl -s "https://api.telegram.org/bot$BOT_TOKEN/getMe" | jq .

echo "2. Testing CMMS connection..."  
curl -s -X POST http://localhost:8080/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"brother@factorylm.com","password":"TempPassword123!","type":"client"}' \
  | jq .

echo "3. Testing Gemini Vision API..."
# Add Gemini test here

echo "4. Checking fault code database..."
docker exec cmms-backend psql -U postgres -d grash -c "SELECT COUNT(*) FROM fault_codes;"

echo "✅ All systems operational - ready for Brother testing!"
EOF

chmod +x brother_test_script.sh
./brother_test_script.sh
```

### Phase 5: Go-Live (Day 7)

#### 5.1 Production Deployment
```bash
# Final configuration check
systemctl status brother-bot
systemctl status cmms-backend
systemctl status nginx

# Enable monitoring
cat > /etc/logrotate.d/brother-bot << 'EOF'
/var/log/brother-bot.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    create 644 root root
}
EOF

# Set up backup
cat > /root/backup_brother_data.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d)
docker exec cmms-backend pg_dump -U postgres grash > /backup/brother_cmms_$DATE.sql
tar czf /backup/brother_bot_$DATE.tar.gz /opt/factorylm/telegram-bot/
EOF

chmod +x /root/backup_brother_data.sh
echo "0 2 * * * /root/backup_brother_data.sh" | crontab -
```

---

## 🔧 Troubleshooting Guide

### Common Issues

#### Bot Not Responding
```bash
# Check if bot service is running
systemctl status brother-bot

# Check logs for errors
journalctl -f -u brother-bot

# Test bot token
curl "https://api.telegram.org/bot$BOT_TOKEN/getMe"

# Restart bot service
systemctl restart brother-bot
```

#### CMMS Connection Errors
```bash
# Check CMMS container
docker ps | grep cmms
docker logs cmms-backend

# Test CMMS API directly
curl -X GET http://localhost:8080/health

# Check database connection
docker exec cmms-backend psql -U postgres -d grash -c "\dt"
```

#### Photo Analysis Failures
```bash
# Check Gemini API key
echo $GEMINI_API_KEY

# Test Gemini API
curl -X POST "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}]}'

# Check disk space for photo storage  
df -h /tmp
```

### Monitoring Commands
```bash
# Bot status dashboard
systemctl status brother-bot
journalctl -f -u brother-bot --lines=50

# System resource usage
htop
df -h
free -h

# Network connectivity
ping 8.8.8.8
curl -I https://api.telegram.org
```

---

## 📞 Support & Contacts

- **Primary Contact**: Mike (Founder)
- **Technical Support**: Telegram @username
- **Emergency**: SSH access to factorylm-prod server
- **CMMS Admin**: http://72.60.175.144/admin (if needed)

**Success Criteria**:
- [ ] Brother can successfully analyze equipment photos
- [ ] Work orders are created and tracked in CMMS  
- [ ] Bot responds to voice messages (Phase 2)
- [ ] Fault code lookup working for common equipment
- [ ] System runs stable for 7 days without intervention