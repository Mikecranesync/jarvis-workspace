#!/usr/bin/env python3
"""
Test script for FactoryLM Edge Agent Server API
"""

import asyncio
import json
import uuid
from datetime import datetime

import httpx
import pytest

BASE_URL = "http://localhost:8090"
AUTH_TOKEN = "factorylm-agent-token-2025"

# Test client
client = httpx.AsyncClient()

async def test_health_check():
    """Test health check endpoint (no auth required)"""
    response = await client.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    print("✅ Health check passed")

async def test_auth_required():
    """Test that endpoints require authentication"""
    # Try without token
    response = await client.get(f"{BASE_URL}/api/devices")
    assert response.status_code == 422 or response.status_code == 401
    print("✅ Auth required check passed")

async def test_device_registration():
    """Test device registration"""
    registration_data = {
        "hostname": "TEST-LAPTOP-01",
        "os_info": "Windows 11 Pro",
        "ip_address": "192.168.1.100",
        "mac_address": "00:11:22:33:44:55"
    }
    
    response = await client.post(
        f"{BASE_URL}/api/devices/register",
        json=registration_data,
        headers={"X-Agent-Token": AUTH_TOKEN}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "device_id" in data
    assert "hostname" in data
    assert "config" in data
    assert data["hostname"] == "TEST-LAPTOP-01"
    
    device_id = data["device_id"]
    print(f"✅ Device registration passed - Device ID: {device_id}")
    return device_id

async def test_get_device_config(device_id: str):
    """Test getting device configuration"""
    response = await client.get(
        f"{BASE_URL}/api/devices/{device_id}/config",
        headers={"X-Agent-Token": AUTH_TOKEN}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "lid_close_action" in data
    assert "sleep_timeout_ac" in data
    assert "hibernate" in data
    assert "tailscale_enabled" in data
    assert "monitoring_interval" in data
    print("✅ Get device config passed")
    return data

async def test_update_device_config(device_id: str):
    """Test updating device configuration"""
    new_config = {
        "lid_close_action": "sleep",
        "sleep_timeout_ac": 30,
        "hibernate": True,
        "tailscale_enabled": False,
        "monitoring_interval": 120
    }
    
    response = await client.put(
        f"{BASE_URL}/api/devices/{device_id}/config",
        json=new_config,
        headers={"X-Agent-Token": AUTH_TOKEN}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "success"
    print("✅ Update device config passed")

async def test_device_heartbeat(device_id: str):
    """Test device heartbeat/status update"""
    heartbeat_data = {
        "online": True,
        "battery_percent": 85.5,
        "plc_connection_status": "connected",
        "cpu_usage": 45.2,
        "memory_usage": 67.8,
        "disk_usage": 42.1
    }
    
    response = await client.post(
        f"{BASE_URL}/api/devices/{device_id}/heartbeat",
        json=heartbeat_data,
        headers={"X-Agent-Token": AUTH_TOKEN}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "success"
    print("✅ Device heartbeat passed")

async def test_list_devices():
    """Test listing all devices"""
    response = await client.get(
        f"{BASE_URL}/api/devices",
        headers={"X-Agent-Token": AUTH_TOKEN}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0  # Should have at least our test device
    
    # Check first device structure
    device = data[0]
    assert "device_id" in device
    assert "hostname" in device
    assert "os_info" in device
    assert "last_seen" in device
    assert "online" in device
    print(f"✅ List devices passed - Found {len(data)} devices")

async def test_invalid_device_id():
    """Test operations with invalid device ID"""
    fake_id = str(uuid.uuid4())
    
    # Get config for non-existent device
    response = await client.get(
        f"{BASE_URL}/api/devices/{fake_id}/config",
        headers={"X-Agent-Token": AUTH_TOKEN}
    )
    assert response.status_code == 404
    
    # Heartbeat for non-existent device
    response = await client.post(
        f"{BASE_URL}/api/devices/{fake_id}/heartbeat",
        json={"online": True},
        headers={"X-Agent-Token": AUTH_TOKEN}
    )
    assert response.status_code == 404
    print("✅ Invalid device ID handling passed")

async def test_validation_errors():
    """Test request validation"""
    # Invalid registration data
    invalid_registration = {
        "hostname": "",  # Empty hostname should fail
        "os_info": "Windows 11"
    }
    
    response = await client.post(
        f"{BASE_URL}/api/devices/register",
        json=invalid_registration,
        headers={"X-Agent-Token": AUTH_TOKEN}
    )
    print(f"Validation test status code: {response.status_code}")
    print(f"Response: {response.text}")
    assert response.status_code == 422  # Validation error
    
    print("✅ Validation error handling passed")

async def run_all_tests():
    """Run all tests in sequence"""
    try:
        print("🚀 Starting API tests...\n")
        
        # Basic tests
        await test_health_check()
        await test_auth_required()
        
        # Device registration and management
        device_id = await test_device_registration()
        config = await test_get_device_config(device_id)
        await test_update_device_config(device_id)
        await test_device_heartbeat(device_id)
        await test_list_devices()
        
        # Error handling tests
        await test_invalid_device_id()
        await test_validation_errors()
        
        print("\n🎉 All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise
    finally:
        await client.aclose()

if __name__ == "__main__":
    # Simple test runner - for more complex testing use pytest
    asyncio.run(run_all_tests())