# FactoryLM Telegram Bot - Technical Architecture

## 🏗️ System Overview

The FactoryLM Telegram Bot leverages existing infrastructure and extends PLC Copilot capabilities for comprehensive maintenance support.

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Telegram      │    │  FactoryLM      │    │     CMMS        │
│   Mini App      │◄──►│  Bot Engine     │◄──►│   (Atlas)       │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                       ▲                       ▲
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Telegram Web    │    │   AI Services   │    │   Equipment     │
│ App Framework   │    │  (Gemini 2.5)   │    │   Database      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 🤖 Bot Configuration

### Telegram Bot Setup
- **Bot Token**: Create via @BotFather
- **Bot Username**: `@FactoryLMBot` (or similar available name)  
- **Commands**: `/start`, `/help`, `/status`, `/equipment`, `/workorders`
- **Inline Keyboards**: Quick action buttons for common tasks
- **Mini App URL**: `https://factorylm.com/telegram-app/` 

### Bot Permissions
- **Send Messages**: Core bot communication
- **Send Photos**: Equipment documentation
- **Voice Messages**: TTS responses for hands-free operation
- **Inline Queries**: Quick equipment search across chats
- **Group Chat Support**: Team collaboration features

---

## 🔧 Backend Services

### 1. Message Router & Handler
**Location**: `/opt/factorylm/services/telegram-bot/`

```python
# Core message processing
@dp.message_handler(content_types=['photo'])
async def handle_photo_analysis(message):
    # Route to existing PLC Copilot photo analysis
    result = await plc_copilot.analyze_equipment_photo(
        photo=message.photo[-1],
        user_context=get_user_context(message.from_user.id)
    )
    await send_analysis_result(message, result)

@dp.message_handler(content_types=['voice'])  
async def handle_voice_query(message):
    # Voice-to-text → NLP → response
    text = await speech_to_text(message.voice)
    response = await process_natural_language_query(text)
    await send_voice_response(message, response)
```

### 2. Equipment Analysis Engine
**Reuse Existing**: `/opt/plc-copilot/photo_to_cmms_bot.py`

**Enhancements Needed**:
- Brother-specific equipment profiles (injection molding)
- Voice query processing 
- Fault code database integration
- Parts cross-reference APIs

### 3. CMMS Integration Layer
**Existing**: Atlas CMMS at `http://localhost:8080`

**Key Endpoints**:
```
POST /auth/signin                    # Authentication
GET  /assets/mini                   # Asset list
POST /assets                        # Create asset
POST /work-orders                   # Create work order
POST /work-orders/search            # Search work orders
GET  /assets/{id}                   # Asset details
```

**New Endpoints Needed**:
```
GET  /equipment/fault-codes         # Fault code lookup
GET  /parts/cross-reference         # Parts compatibility
GET  /maintenance/procedures        # Step-by-step guides
```

---

## 🧠 AI Services Stack

### Computer Vision (Equipment Analysis)
- **Primary**: Google Gemini 2.5 Flash Vision
- **Backup**: Claude 3 Haiku Vision (cost optimization)
- **Local Fallback**: Ollama LLaVA on PLC laptop (offline mode)

**Processing Pipeline**:
```
Photo → Image Enhancement → Gemini Analysis → Equipment Database Lookup → CMMS Integration
```

### Natural Language Processing
- **Voice Recognition**: OpenAI Whisper API
- **Intent Classification**: Custom fine-tuned model for maintenance queries
- **Response Generation**: GPT-4o for contextual responses
- **Text-to-Speech**: ElevenLabs for natural voice responses

### Knowledge Graph
```
Equipment ←→ Manufacturer ←→ Parts ←→ Procedures ←→ Fault Codes
    ↓             ↓            ↓          ↓           ↓
 Location    Specifications  Inventory  Videos    Solutions
```

---

## 📱 Telegram Mini App

### Frontend Framework
- **Base**: Pure HTML5/CSS3/JavaScript (no complex frameworks)
- **UI Library**: Telegram Web App SDK
- **Responsive**: Mobile-first design for plant floor use
- **Offline**: Service Worker for basic functionality without network

### Key Screens
1. **Equipment Scanner**: Camera integration for photo analysis
2. **Work Order Dashboard**: Active, pending, completed tasks  
3. **Parts Lookup**: Search and cross-reference interface
4. **Fault Code Directory**: Searchable diagnostic database
5. **Voice Assistant**: Push-to-talk interface

### Mini App Integration
```javascript
// Initialize Telegram Web App
Telegram.WebApp.ready();

// Equipment photo analysis
async function analyzeEquipment(photoData) {
    const result = await fetch('/api/analyze-equipment', {
        method: 'POST',
        body: photoData,
        headers: {
            'X-Telegram-Init-Data': Telegram.WebApp.initData
        }
    });
    return result.json();
}

// Voice command processing  
async function processVoiceCommand(audioBlob) {
    const response = await fetch('/api/voice-query', {
        method: 'POST', 
        body: audioBlob
    });
    return response.json();
}
```

---

## 💾 Database Schema

### User Profiles
```sql
CREATE TABLE telegram_users (
    telegram_id BIGINT PRIMARY KEY,
    username VARCHAR(50),
    first_name VARCHAR(100),
    facility_name VARCHAR(200),
    role VARCHAR(50),
    permissions JSON,
    preferences JSON,
    created_at TIMESTAMP
);
```

### Equipment Context
```sql
CREATE TABLE user_equipment_context (
    user_id BIGINT,
    equipment_id INT,
    last_accessed TIMESTAMP,
    work_session JSON,
    FOREIGN KEY (user_id) REFERENCES telegram_users(telegram_id),
    FOREIGN KEY (equipment_id) REFERENCES assets(id)
);
```

### Fault Code Database
```sql
CREATE TABLE fault_codes (
    id SERIAL PRIMARY KEY,
    manufacturer VARCHAR(100),
    equipment_type VARCHAR(100),
    code VARCHAR(50),
    description TEXT,
    solution TEXT,
    tools_required JSON,
    safety_notes TEXT,
    video_url VARCHAR(500)
);
```

---

## 🔐 Security & Authentication

### User Authentication
1. **Telegram OAuth**: Automatic via Web App init data
2. **Data Validation**: Verify Telegram signature
3. **Session Management**: JWT tokens for API access  
4. **Permission System**: Role-based access (Maintenance, Supervisor, Admin)

### Data Protection
- **At Rest**: PostgreSQL encryption, encrypted backups
- **In Transit**: HTTPS/TLS 1.3 for all API calls
- **PII Handling**: Minimal data collection, GDPR compliance
- **Audit Logging**: All work order and equipment access logged

---

## 🚀 Deployment Architecture

### Production Environment
- **Primary Server**: factorylm-prod (DigitalOcean Atlanta)  
- **Bot Process**: Systemd service with auto-restart
- **Database**: PostgreSQL 15 with replication
- **File Storage**: Digital Ocean Spaces for images/attachments
- **Monitoring**: Prometheus + Grafana dashboards

### Development/Testing
- **Test Bot**: Separate token for development
- **Staging CMMS**: Copy of production data (anonymized)
- **Local Development**: Docker compose environment

### Edge Computing (Optional)
- **PLC Laptop**: Offline vision processing with Ollama
- **Raspberry Pi**: Plant floor deployment for low-latency response
- **Data Sync**: Background synchronization when connectivity available

---

## 📊 Performance Requirements

### Response Times
- **Photo Analysis**: < 15 seconds end-to-end
- **Voice Queries**: < 5 seconds for common questions
- **Database Lookups**: < 2 seconds for equipment info
- **Work Order Creation**: < 10 seconds complete flow

### Scalability Targets  
- **Concurrent Users**: 50 maintenance techs across shifts
- **Daily Photos**: 500+ equipment images processed
- **Voice Queries**: 200+ per day during peak hours
- **Database Growth**: 10GB+ equipment/maintenance data

### Reliability
- **Uptime**: 99.5% availability (plant operations critical)
- **Data Backup**: Daily automated backups with 30-day retention
- **Failover**: Automatic restart on service failure
- **Offline Mode**: Core functions available without internet

---

## 🔄 Integration Points

### Existing FactoryLM Systems
- **PLC Copilot**: Reuse photo analysis engine
- **CMMS**: Direct API integration for work orders
- **Master of Puppets**: Leverage existing agent infrastructure
- **Jarvis Nodes**: Remote equipment monitoring capabilities

### External Integrations (Future)
- **Equipment Vendors**: Allen-Bradley, Siemens, ABB APIs
- **Parts Suppliers**: McMaster-Carr, Grainger inventory APIs  
- **Training Systems**: Integration with maintenance training platforms
- **Safety Systems**: LOTO procedure databases

### Communication Protocols
- **REST APIs**: Primary integration method
- **WebSockets**: Real-time equipment status updates
- **MQTT**: Plant floor sensor data (future)
- **Modbus/OPC-UA**: Direct PLC communication (via Jarvis nodes)