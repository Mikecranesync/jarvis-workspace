"""
FactoryLM Signup API Backend
FastAPI application for user signup and management
"""
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, validator
import sqlite3
import re
from datetime import datetime
from typing import Optional, List
import requests
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="FactoryLM Signup API", version="1.0.0")

# CORS configuration for factorylm.com
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://factorylm.com", "https://www.factorylm.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Configuration
DATABASE_PATH = "/opt/factorylm/data/signups.db"
ADMIN_API_KEY = "factorylm-admin-2026"
TELEGRAM_BOT_TOKEN = "8519329029:AAEbztWcFXky4P7sB8xouQZRoVQO-aNhwFM"
TELEGRAM_CHAT_ID = "8445149012"

# Pydantic models
class SignupRequest(BaseModel):
    name: str
    email: str
    company: str
    role: str
    
    @validator('email')
    def validate_email(cls, v):
        # Basic email regex validation
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, v):
            raise ValueError('Invalid email format')
        return v.lower().strip()
    
    @validator('name', 'company', 'role')
    def validate_strings(cls, v):
        if not v or not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip()

class SignupResponse(BaseModel):
    success: bool
    message: str

class SignupRecord(BaseModel):
    id: int
    name: str
    email: str
    company: str
    role: str
    created_at: str

class StatsResponse(BaseModel):
    total_signups: int

# Database functions
def init_database():
    """Initialize the SQLite database and create tables if they don't exist."""
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    with sqlite3.connect(DATABASE_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS signups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                company TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def check_duplicate_email(email: str) -> bool:
    """Check if email already exists in database."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.execute("SELECT 1 FROM signups WHERE email = ?", (email,))
        return cursor.fetchone() is not None

def insert_signup(signup: SignupRequest) -> int:
    """Insert new signup record and return the ID."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.execute("""
            INSERT INTO signups (name, email, company, role, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (signup.name, signup.email, signup.company, signup.role, datetime.utcnow().isoformat()))
        conn.commit()
        return cursor.lastrowid

def get_all_signups() -> List[SignupRecord]:
    """Get all signup records from database."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("""
            SELECT id, name, email, company, role, created_at
            FROM signups
            ORDER BY created_at DESC
        """)
        rows = cursor.fetchall()
        
        return [SignupRecord(
            id=row['id'],
            name=row['name'],
            email=row['email'],
            company=row['company'],
            role=row['role'],
            created_at=row['created_at']
        ) for row in rows]

def get_signup_count() -> int:
    """Get total number of signups."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.execute("SELECT COUNT(*) FROM signups")
        return cursor.fetchone()[0]

# Telegram notification
def send_telegram_notification(signup: SignupRequest):
    """Send Telegram notification for new signup."""
    try:
        message = f"""🏭 New FactoryLM signup!
Name: {signup.name}
Email: {signup.email}
Company: {signup.company}
Role: {signup.role}"""
        
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        logger.info(f"Telegram notification sent for signup: {signup.email}")
        
    except Exception as e:
        logger.error(f"Failed to send Telegram notification: {e}")
        # Don't fail the signup if notification fails

# API Key dependency
def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """Verify the admin API key."""
    if x_api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return x_api_key

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_database()
    logger.info("Database initialized successfully")

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "FactoryLM Signup API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": [
            "POST /api/signup - Submit new signup",
            "GET /api/signups - List all signups (admin)",
            "GET /api/stats - Public signup statistics"
        ]
    }

@app.post("/api/signup", response_model=SignupResponse)
async def create_signup(signup: SignupRequest):
    """Create a new signup record."""
    try:
        # Check for duplicate email
        if check_duplicate_email(signup.email):
            return SignupResponse(
                success=False,
                message="This email address is already registered. Please use a different email or contact support if you believe this is an error."
            )
        
        # Insert new signup
        signup_id = insert_signup(signup)
        
        # Send Telegram notification (non-blocking)
        send_telegram_notification(signup)
        
        logger.info(f"New signup created: {signup.email} (ID: {signup_id})")
        
        return SignupResponse(
            success=True,
            message="Thank you for signing up! We'll be in touch soon."
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating signup: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/signups", response_model=List[SignupRecord])
async def list_signups(api_key: str = Depends(verify_api_key)):
    """List all signups (admin endpoint)."""
    try:
        signups = get_all_signups()
        logger.info(f"Admin accessed signups list: {len(signups)} records")
        return signups
    except Exception as e:
        logger.error(f"Error listing signups: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/stats", response_model=StatsResponse)
async def get_stats():
    """Get public signup statistics."""
    try:
        total_signups = get_signup_count()
        return StatsResponse(total_signups=total_signups)
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Test database connection
        with sqlite3.connect(DATABASE_PATH) as conn:
            conn.execute("SELECT 1")
        
        return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8090)