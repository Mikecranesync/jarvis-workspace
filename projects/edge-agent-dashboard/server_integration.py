"""
Example FastAPI integration for the FactoryLM Edge Agent Dashboard

This shows how to serve the dashboard at /dashboard endpoint.
Add this to your main FastAPI server.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI(title="FactoryLM Edge Agent API")

# Get the directory where this file is located
DASHBOARD_DIR = os.path.dirname(os.path.abspath(__file__))

# Mount the dashboard static files
app.mount("/dashboard/static", StaticFiles(directory=DASHBOARD_DIR), name="dashboard_static")

@app.get("/dashboard")
@app.get("/dashboard/")
async def dashboard():
    """Serve the main dashboard page"""
    return FileResponse(os.path.join(DASHBOARD_DIR, "index.html"))

# Example API endpoints (implement these in your main server)
@app.get("/api/devices")
async def list_devices():
    """List all registered devices"""
    # TODO: Implement actual device listing
    return [
        {
            "device_id": "550e8400-e29b-41d4-a716-446655440000",
            "hostname": "PLC-LAPTOP-001",
            "ip_address": "192.168.1.100",
            "last_heartbeat": "2024-01-15T10:30:00Z",
            "status": "online"
        },
        {
            "device_id": "550e8400-e29b-41d4-a716-446655440001", 
            "hostname": "FACTORY-HMI-02",
            "ip_address": "192.168.1.101",
            "last_heartbeat": "2024-01-15T09:45:00Z",
            "status": "offline"
        }
    ]

@app.get("/api/devices/{device_id}/config")
async def get_device_config(device_id: str):
    """Get device configuration"""
    # TODO: Implement actual config retrieval
    return {
        "device_id": device_id,
        "config": {
            "lid_close_action": "do_nothing",
            "sleep_timeout_ac": 0,
            "hibernate": False,
            "tailscale_enabled": True,
            "monitoring_interval": 60
        }
    }

@app.put("/api/devices/{device_id}/config")
async def update_device_config(device_id: str, config_data: dict):
    """Update device configuration"""
    # TODO: Implement actual config update
    print(f"Updating config for device {device_id}: {config_data}")
    return {"success": True, "message": "Configuration updated"}

if __name__ == "__main__":
    import uvicorn
    
    print("Starting FactoryLM Edge Agent Server...")
    print("Dashboard available at: http://localhost:8090/dashboard")
    print("API documentation at: http://localhost:8090/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8090)