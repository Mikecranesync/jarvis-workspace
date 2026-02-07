# FactoryLM Edge Agent Server

A FastAPI-based server for managing FactoryLM edge devices. This server provides REST API endpoints for device registration, configuration management, and status monitoring.

## Features

- **Device Management**: Register, configure, and monitor edge devices
- **SQLite Database**: Lightweight, embedded database for device storage
- **Authentication**: Simple token-based authentication
- **CORS Enabled**: Ready for web dashboard integration
- **Production Ready**: Comprehensive error handling, logging, and Docker support

## API Endpoints

### Health Check
- `GET /health` - Server health check (no auth required)

### Device Management
- `POST /api/devices/register` - Register a new device
- `GET /api/devices` - List all registered devices  
- `GET /api/devices/{id}/config` - Get device configuration
- `PUT /api/devices/{id}/config` - Update device configuration
- `POST /api/devices/{id}/heartbeat` - Update device status/heartbeat

All API endpoints require `X-Agent-Token` header for authentication.

## Quick Start

### Option 1: Run with Python

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python main.py
```

3. Server will start on http://localhost:8090

### Option 2: Run with Docker

1. Build and run:
```bash
docker build -t factorylm-edge-agent-server .
docker run -p 8090:8090 factorylm-edge-agent-server
```

### Option 3: Docker Compose

1. Create `.env` file (copy from `.env.example`)
2. Run:
```bash
docker-compose up -d
```

## Configuration

Environment variables:
- `X_AGENT_TOKEN`: Authentication token (default: `factorylm-agent-token-2025`)
- `DATABASE_PATH`: SQLite database file path (default: `./devices.db`)

## API Usage Examples

### Register a Device
```bash
curl -X POST http://localhost:8090/api/devices/register \
  -H "X-Agent-Token: factorylm-agent-token-2025" \
  -H "Content-Type: application/json" \
  -d '{
    "hostname": "PLC-LAPTOP-01", 
    "os_info": "Windows 11 Pro",
    "ip_address": "192.168.1.100"
  }'
```

### Get Device Config
```bash
curl -X GET http://localhost:8090/api/devices/{device_id}/config \
  -H "X-Agent-Token: factorylm-agent-token-2025"
```

### Send Heartbeat
```bash
curl -X POST http://localhost:8090/api/devices/{device_id}/heartbeat \
  -H "X-Agent-Token: factorylm-agent-token-2025" \
  -H "Content-Type: application/json" \
  -d '{
    "online": true,
    "battery_percent": 85,
    "plc_connection_status": "connected",
    "cpu_usage": 45.2,
    "memory_usage": 67.8
  }'
```

### List All Devices
```bash
curl -X GET http://localhost:8090/api/devices \
  -H "X-Agent-Token: factorylm-agent-token-2025"
```

## Database Schema

The SQLite database contains a single `devices` table with the following columns:

- `device_id` (TEXT, PRIMARY KEY) - Unique device identifier
- `hostname` (TEXT) - Device hostname
- `os_info` (TEXT) - Operating system information
- `ip_address` (TEXT) - Device IP address
- `mac_address` (TEXT) - Device MAC address  
- `config` (TEXT) - Device configuration as JSON
- `last_seen` (TEXT) - Last heartbeat timestamp (ISO format)
- `online` (BOOLEAN) - Device online status
- `battery_percent` (REAL) - Battery percentage (0-100)
- `plc_connection_status` (TEXT) - PLC connection status
- `cpu_usage` (REAL) - CPU usage percentage
- `memory_usage` (REAL) - Memory usage percentage
- `disk_usage` (REAL) - Disk usage percentage
- `created_at` (TEXT) - Device creation timestamp
- `updated_at` (TEXT) - Last update timestamp

## Device Configuration Schema

Each device has a configuration object with the following fields:

- `lid_close_action` (string) - Action when laptop lid closes ("do_nothing", "sleep", "hibernate", "shutdown")
- `sleep_timeout_ac` (int) - Sleep timeout when on AC power in minutes (0 = never)
- `hibernate` (bool) - Enable hibernation
- `tailscale_enabled` (bool) - Enable Tailscale VPN
- `monitoring_interval` (int) - Heartbeat interval in seconds (30-3600)

## Development

### Running Tests
```bash
python -m pytest test_api.py -v
```

### API Documentation
When the server is running, visit:
- Interactive docs: http://localhost:8090/docs  
- OpenAPI spec: http://localhost:8090/openapi.json

## Production Deployment

For production:
1. Change the default `X_AGENT_TOKEN` to a secure value
2. Use a proper reverse proxy (nginx, Traefik, etc.)
3. Enable HTTPS
4. Configure proper CORS origins (remove "*" wildcard)
5. Set up log rotation and monitoring
6. Consider using PostgreSQL instead of SQLite for higher load

## Security

- Authentication uses a simple token in the `X-Agent-Token` header
- CORS is enabled for all origins (change for production)
- Database uses SQLite with no encryption (suitable for non-sensitive data)
- No rate limiting implemented (add if needed)

## License

Part of the FactoryLM project.