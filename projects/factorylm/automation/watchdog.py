#!/usr/bin/env python3
"""
Gateway Watchdog - Monitors Clawdbot instances and alerts on crashes

Features:
- Monitors local and remote gateways
- Sends Telegram alert on crash detection
- Tracks crash history
- Attempts restart on local gateway

Deploy on both laptop (watches VPS) and VPS (watches laptop via Tailscale/public IP)
"""

import os
import sys
import time
import json
import asyncio
import aiohttp
from datetime import datetime
from pathlib import Path

# Config
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8387943893:AAEynugW3SP1sWs6An4aNgZParSSRBlWSJk")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "8445149012")
CHECK_INTERVAL = 30  # seconds

# Endpoints to monitor
ENDPOINTS = {
    "laptop": {
        "url": "http://localhost:18789",
        "restart_cmd": None,  # Can't restart from VPS
        "name": "Laptop Jarvis"
    },
    "vps": {
        "url": "http://localhost:18789",  # When running on VPS
        "restart_cmd": "systemctl restart clawdbot",
        "name": "VPS Jarvis"
    }
}

# State tracking
crash_history = []
last_status = {}


async def send_telegram(text: str):
    """Send alert to Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        async with aiohttp.ClientSession() as session:
            await session.post(url, json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": text,
                "parse_mode": "Markdown"
            })
        print(f"[ALERT] Sent: {text[:50]}...")
    except Exception as e:
        print(f"[ERR] Telegram failed: {e}")


async def check_gateway(name: str, url: str) -> bool:
    """Check if gateway is responding."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    return True
    except Exception as e:
        print(f"[CHECK] {name} failed: {e}")
    return False


async def restart_gateway(name: str, cmd: str) -> bool:
    """Attempt to restart gateway."""
    if not cmd:
        return False
    
    try:
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await proc.wait()
        return proc.returncode == 0
    except Exception as e:
        print(f"[ERR] Restart failed: {e}")
        return False


async def monitor_loop():
    """Main monitoring loop."""
    global last_status
    
    print(f"🔍 Gateway Watchdog started")
    print(f"   Monitoring: {list(ENDPOINTS.keys())}")
    print(f"   Interval: {CHECK_INTERVAL}s")
    
    # Determine which endpoint to monitor based on where we're running
    hostname = os.uname().nodename if hasattr(os, 'uname') else os.environ.get('COMPUTERNAME', 'unknown')
    
    if 'srv' in hostname.lower() or 'hstgr' in hostname.lower():
        # Running on VPS - monitor local VPS gateway
        target = "vps"
        config = ENDPOINTS["vps"]
    else:
        # Running on laptop - monitor local laptop gateway  
        target = "laptop"
        config = ENDPOINTS["laptop"]
    
    print(f"   Target: {target} ({config['name']})")
    
    consecutive_failures = 0
    
    while True:
        try:
            is_up = await check_gateway(config["name"], config["url"])
            now = datetime.now().strftime("%H:%M:%S")
            
            if is_up:
                if consecutive_failures > 0:
                    # Just recovered
                    await send_telegram(
                        f"✅ *{config['name']} RECOVERED*\n\n"
                        f"Gateway is back online.\n"
                        f"Downtime: ~{consecutive_failures * CHECK_INTERVAL}s"
                    )
                consecutive_failures = 0
                last_status[target] = {"status": "up", "time": now}
                print(f"[{now}] {config['name']}: ✅ UP")
            else:
                consecutive_failures += 1
                last_status[target] = {"status": "down", "time": now, "failures": consecutive_failures}
                print(f"[{now}] {config['name']}: ❌ DOWN (failures: {consecutive_failures})")
                
                # Alert after 2 consecutive failures (60s down)
                if consecutive_failures == 2:
                    crash_history.append({
                        "target": target,
                        "time": datetime.now().isoformat(),
                        "name": config["name"]
                    })
                    
                    await send_telegram(
                        f"🚨 *{config['name']} CRASHED*\n\n"
                        f"Gateway not responding for {consecutive_failures * CHECK_INTERVAL}s\n"
                        f"Time: {now}\n\n"
                        f"Attempting restart..."
                    )
                    
                    # Try restart
                    if config["restart_cmd"]:
                        success = await restart_gateway(target, config["restart_cmd"])
                        if success:
                            await send_telegram(f"🔄 Restart command sent for {config['name']}")
                        else:
                            await send_telegram(f"❌ Restart failed for {config['name']}")
                
                # Keep alerting every 5 min if still down
                elif consecutive_failures > 0 and consecutive_failures % 10 == 0:
                    await send_telegram(
                        f"⚠️ *{config['name']} STILL DOWN*\n\n"
                        f"Been down for {consecutive_failures * CHECK_INTERVAL}s\n"
                        f"Manual intervention needed!"
                    )
            
        except Exception as e:
            print(f"[ERR] Monitor error: {e}")
        
        await asyncio.sleep(CHECK_INTERVAL)


def main():
    print("=" * 50)
    print("CLAWDBOT GATEWAY WATCHDOG")
    print("=" * 50)
    asyncio.run(monitor_loop())


if __name__ == "__main__":
    main()
