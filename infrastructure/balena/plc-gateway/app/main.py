#!/usr/bin/env python3
"""
FactoryLM PLC Gateway
Runs on Raspberry Pi Edge device
Connects to Allen-Bradley Micro820 via Ethernet/IP
Exposes REST API and MQTT for remote control
"""

import os
import json
import time
import threading
from datetime import datetime
from flask import Flask, jsonify, request
import paho.mqtt.client as mqtt

# Try to import pycomm3, gracefully handle if PLC not connected
try:
    from pycomm3 import LogixDriver
    PYCOMM3_AVAILABLE = True
except ImportError:
    PYCOMM3_AVAILABLE = False
    print("⚠️ pycomm3 not available")


app = Flask(__name__)

# Configuration from environment
PLC_IP = os.getenv('PLC_IP', '192.168.1.10')
MQTT_BROKER = os.getenv('MQTT_BROKER', '100.68.120.99')
MQTT_PORT = int(os.getenv('MQTT_PORT', '1883'))
MQTT_TOPIC_PREFIX = os.getenv('MQTT_TOPIC_PREFIX', 'factorylm/edge')
DEVICE_ID = os.getenv('DEVICE_ID', 'edge-pi-001')

# State
plc_connected = False
last_plc_data = {}
mqtt_client = None

def get_plc_connection():
    """Get PLC connection, return None if not available"""
    global plc_connected
    if not PYCOMM3_AVAILABLE:
        return None
    try:
        plc = LogixDriver(PLC_IP)
        plc.open()
        plc_connected = True
        return plc
    except Exception as e:
        plc_connected = False
        print(f"PLC connection failed: {e}")
        return None

def read_plc_tag(tag_name):
    """Read a single tag from PLC"""
    plc = get_plc_connection()
    if not plc:
        return {"error": "PLC not connected", "tag": tag_name}
    try:
        result = plc.read(tag_name)
        plc.close()
        return {
            "tag": tag_name,
            "value": result.value,
            "type": str(result.type),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {"error": str(e), "tag": tag_name}

def write_plc_tag(tag_name, value):
    """Write a value to PLC tag"""
    plc = get_plc_connection()
    if not plc:
        return {"error": "PLC not connected", "tag": tag_name}
    try:
        result = plc.write(tag_name, value)
        plc.close()
        return {
            "tag": tag_name,
            "value": value,
            "success": True,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {"error": str(e), "tag": tag_name, "success": False}

def get_plc_info():
    """Get PLC device info"""
    plc = get_plc_connection()
    if not plc:
        return {"error": "PLC not connected"}
    try:
        info = plc.get_plc_info()
        tags = plc.get_tag_list()
        plc.close()
        return {
            "info": {
                "name": info.get('name', 'Unknown'),
                "vendor": info.get('vendor', 'Unknown'),
                "product_type": info.get('product_type', 'Unknown'),
                "revision": info.get('revision', 'Unknown'),
            },
            "tag_count": len(tags) if tags else 0,
            "connected": True
        }
    except Exception as e:
        return {"error": str(e), "connected": False}

# MQTT Setup
def on_mqtt_connect(client, userdata, flags, rc):
    print(f"MQTT Connected with code {rc}")
    # Subscribe to command topic
    client.subscribe(f"{MQTT_TOPIC_PREFIX}/{DEVICE_ID}/cmd")

def on_mqtt_message(client, userdata, msg):
    """Handle incoming MQTT commands"""
    try:
        payload = json.loads(msg.payload.decode())
        cmd = payload.get('cmd')
        
        if cmd == 'read':
            tag = payload.get('tag')
            result = read_plc_tag(tag)
            client.publish(f"{MQTT_TOPIC_PREFIX}/{DEVICE_ID}/response", json.dumps(result))
        elif cmd == 'write':
            tag = payload.get('tag')
            value = payload.get('value')
            result = write_plc_tag(tag, value)
            client.publish(f"{MQTT_TOPIC_PREFIX}/{DEVICE_ID}/response", json.dumps(result))
        elif cmd == 'info':
            result = get_plc_info()
            client.publish(f"{MQTT_TOPIC_PREFIX}/{DEVICE_ID}/response", json.dumps(result))
        elif cmd == 'ping':
            client.publish(f"{MQTT_TOPIC_PREFIX}/{DEVICE_ID}/response", json.dumps({
                "pong": True,
                "device": DEVICE_ID,
                "plc_connected": plc_connected,
                "timestamp": datetime.utcnow().isoformat()
            }))
    except Exception as e:
        print(f"MQTT message error: {e}")

def start_mqtt():
    """Start MQTT client in background"""
    global mqtt_client
    try:
        mqtt_client = mqtt.Client()
        mqtt_client.on_connect = on_mqtt_connect
        mqtt_client.on_message = on_mqtt_message
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_start()
        print(f"MQTT started, connecting to {MQTT_BROKER}:{MQTT_PORT}")
    except Exception as e:
        print(f"MQTT failed to start: {e}")

# REST API Endpoints
@app.route('/')
def index():
    return jsonify({
        "service": "FactoryLM PLC Gateway",
        "device": DEVICE_ID,
        "plc_ip": PLC_IP,
        "plc_connected": plc_connected,
        "mqtt_broker": MQTT_BROKER,
        "pycomm3_available": PYCOMM3_AVAILABLE,
        "endpoints": [
            "GET /health",
            "GET /plc/info",
            "GET /plc/read/<tag>",
            "POST /plc/write",
            "GET /plc/tags"
        ]
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "device": DEVICE_ID,
        "plc_connected": plc_connected,
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/plc/info')
def plc_info():
    return jsonify(get_plc_info())

@app.route('/plc/read/<tag>')
def plc_read(tag):
    return jsonify(read_plc_tag(tag))

@app.route('/plc/write', methods=['POST'])
def plc_write():
    data = request.json
    tag = data.get('tag')
    value = data.get('value')
    if not tag or value is None:
        return jsonify({"error": "Missing tag or value"}), 400
    return jsonify(write_plc_tag(tag, value))

@app.route('/plc/tags')
def plc_tags():
    plc = get_plc_connection()
    if not plc:
        return jsonify({"error": "PLC not connected"})
    try:
        tags = plc.get_tag_list()
        plc.close()
        # Return first 50 tags to avoid huge response
        tag_list = [{"name": t.tag_name, "type": str(t.data_type)} for t in tags[:50]]
        return jsonify({"tags": tag_list, "total": len(tags)})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    print("=" * 50)
    print("FactoryLM PLC Gateway Starting...")
    print(f"  Device ID: {DEVICE_ID}")
    print(f"  PLC IP: {PLC_IP}")
    print(f"  MQTT Broker: {MQTT_BROKER}")
    print(f"  pycomm3 available: {PYCOMM3_AVAILABLE}")
    print("=" * 50)
    
    # Start MQTT in background
    start_mqtt()
    
    # Start Flask API
    app.run(host='0.0.0.0', port=5000, debug=False)

# Configure ethernet on startup (runs at container start)
import subprocess
try:
    subprocess.run(['ip', 'addr', 'add', '192.168.1.1/24', 'dev', 'eth0'], capture_output=True)
    subprocess.run(['ip', 'link', 'set', 'eth0', 'up'], capture_output=True)
    print("Configured eth0 with 192.168.1.1/24")
except Exception as e:
    print(f"Ethernet config: {e}")
