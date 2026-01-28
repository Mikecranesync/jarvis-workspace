# FactoryLM Signup API

Production-ready FastAPI backend for FactoryLM signup and user management.

## Features

✅ **FastAPI Backend** - Modern async Python web framework  
✅ **SQLite Database** - Lightweight, serverless database  
✅ **Email Validation** - Regex-based email format checking  
✅ **Duplicate Detection** - Friendly handling of existing emails  
✅ **Telegram Notifications** - Real-time signup alerts  
✅ **CORS Enabled** - Configured for factorylm.com  
✅ **Admin API** - Secure endpoint for viewing signups  
✅ **Public Stats** - Total signup count endpoint  
✅ **Production Ready** - Systemd service, logging, health checks  

## API Endpoints

### Public Endpoints

#### `POST /api/signup`
Submit a new signup form.

**Request:**
```json
{
  "name": "John Doe",
  "email": "john@company.com",
  "company": "Acme Corp",
  "role": "Engineer"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Thank you for signing up! We'll be in touch soon."
}
```

#### `GET /api/stats`
Get public signup statistics.

**Response:**
```json
{
  "total_signups": 42
}
```

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-27T19:30:00.000Z"
}
```

### Admin Endpoints

#### `GET /api/signups`
List all signups (requires API key).

**Headers:**
```
X-API-Key: factorylm-admin-2026
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@company.com",
    "company": "Acme Corp",
    "role": "Engineer",
    "created_at": "2026-01-27T19:30:00.000Z"
  }
]
```

## Configuration

### Environment Variables
- `DATABASE_PATH`: SQLite database location (default: `/opt/factorylm/data/signups.db`)
- `ADMIN_API_KEY`: Admin API key (default: `factorylm-admin-2026`)
- `TELEGRAM_BOT_TOKEN`: Telegram bot token for notifications
- `TELEGRAM_CHAT_ID`: Telegram chat ID for notifications

### CORS Configuration
- Allowed origins: `https://factorylm.com`, `https://www.factorylm.com`
- Allowed methods: `GET`, `POST`

## Installation

### Prerequisites
- Python 3.8+
- systemd (for service management)

### Quick Deploy
```bash
# Make deploy script executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

### Manual Installation
```bash
# 1. Create directories
sudo mkdir -p /opt/factorylm/api
sudo mkdir -p /opt/factorylm/data

# 2. Copy files
sudo cp main.py requirements.txt /opt/factorylm/api/

# 3. Install dependencies
cd /opt/factorylm/api
sudo python3 -m pip install -r requirements.txt

# 4. Set permissions
sudo chown -R www-data:www-data /opt/factorylm/

# 5. Install systemd service
sudo cp factorylm-api.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable factorylm-api
sudo systemctl start factorylm-api
```

## Service Management

```bash
# Start service
sudo systemctl start factorylm-api

# Stop service
sudo systemctl stop factorylm-api

# Restart service
sudo systemctl restart factorylm-api

# Check status
sudo systemctl status factorylm-api

# View logs
sudo journalctl -u factorylm-api -f
```

## Development

### Local Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python main.py
```

The API will be available at `http://127.0.0.1:8090`

### API Documentation
Once running, visit `http://127.0.0.1:8090/docs` for interactive API documentation.

## Database Schema

### signups table
```sql
CREATE TABLE signups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    company TEXT NOT NULL,
    role TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Security Features

- **Input Validation**: Pydantic models with email validation
- **API Key Protection**: Admin endpoints protected with X-API-Key header
- **CORS Configuration**: Restricted to factorylm.com domains
- **SQL Injection Prevention**: Parameterized queries
- **Error Handling**: Graceful error responses without exposing internals

## Monitoring

### Health Check
```bash
curl http://127.0.0.1:8090/health
```

### Service Status
```bash
sudo systemctl status factorylm-api
```

### Logs
```bash
sudo journalctl -u factorylm-api --since "1 hour ago"
```

## Telegram Notifications

When a new signup is submitted, a notification is automatically sent to the configured Telegram chat:

```
🏭 New FactoryLM signup!
Name: John Doe
Email: john@company.com
Company: Acme Corp
Role: Engineer
```

## License

Private - FactoryLM Internal Use Only