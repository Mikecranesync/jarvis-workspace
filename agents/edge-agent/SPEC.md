# FactoryLM Edge Agent - Spec

## Overview
Lightweight agent that runs on Windows devices, calls home to FactoryLM server, receives configuration, and reports status.

## Components

### 1. Edge Agent (Windows Service)
- **Language:** Python (easier for MVP) or Go (production)
- **Install:** `irm https://get.factorylm.com/agent | iex`
- **Runs as:** Windows Service (auto-start)

**Behaviors:**
- On first run: Register with server (hostname, IP, OS info)
- Every 60s: Pull config from server
- Every 60s: Send heartbeat (online, battery %, PLC connection status)
- On config change: Apply settings (power, Tailscale, etc.)

### 2. Server API (VPS)
- **Framework:** FastAPI
- **Database:** SQLite (MVP) or PostgreSQL
- **Port:** 8090

**Endpoints:**
```
POST /api/devices/register     - New device registration
GET  /api/devices/{id}/config  - Get device config
POST /api/devices/{id}/heartbeat - Device status update
GET  /api/devices              - List all devices
PUT  /api/devices/{id}/config  - Update device config
```

### 3. Web Dashboard
- **Stack:** Simple HTML + Tailwind (no React needed for MVP)
- **Features:**
  - Device list with status (online/offline)
  - Click device → view/edit config
  - Last seen timestamp

## Config Schema
```json
{
  "device_id": "uuid",
  "hostname": "PLC-LAPTOP",
  "config": {
    "lid_close_action": "do_nothing",
    "sleep_timeout_ac": 0,
    "hibernate": false,
    "tailscale_enabled": true,
    "monitoring_interval": 60
  }
}
```

## MVP Scope (4 hours)
1. ✅ Server API with SQLite
2. ✅ Simple web dashboard
3. ✅ Python agent for Windows
4. ✅ PowerShell one-liner installer

## Out of Scope (v2)
- Agent auto-update
- Role-based access
- Multi-tenant
