#!/usr/bin/env python3
"""
FactoryLM Auto Network Detection v2.0
- Detects connected device's subnet
- Auto-configures Pi to join that network
- Maintains IP configuration (persistence fix)
"""
import subprocess
import time
import re
import threading

ETH_INTERFACE = "eth0"
FALLBACK_IP = "192.168.1.1"
FALLBACK_SUBNET = "24"
DETECT_TIMEOUT = 30

# Global to track configured IP for keepalive
configured_ip = None

def run(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return result.stdout.strip()
    except:
        return ""

def get_interface_state():
    state = run(f"cat /sys/class/net/{ETH_INTERFACE}/carrier 2>/dev/null")
    return state == "1"

def detect_neighbor_ip():
    # Method 1: ARP table
    arp_output = run(f"ip neigh show dev {ETH_INTERFACE}")
    for line in arp_output.split('\n'):
        if line and ('REACHABLE' in line or 'STALE' in line or 'DELAY' in line):
            ip = line.split()[0]
            if ip and not ip.startswith('fe80'):
                return ip
    
    # Method 2: ARP probe common IPs
    common_ips = ['192.168.137.1', '192.168.1.1', '192.168.0.1', '192.168.10.1', '10.0.0.1', '172.16.0.1']
    for ip in common_ips:
        result = run(f"arping -I {ETH_INTERFACE} -c 1 -w 1 {ip} 2>/dev/null")
        if 'reply from' in result.lower() or 'bytes from' in result.lower():
            return ip
        # Also try ping
        ping_result = run(f"ping -I {ETH_INTERFACE} -c 1 -W 1 {ip} 2>/dev/null")
        if '1 received' in ping_result:
            return ip
    
    return None

def calculate_our_ip(neighbor_ip):
    parts = neighbor_ip.split('.')
    if len(parts) != 4:
        return None, None
    
    last_octet = int(parts[3])
    our_last = 2 if last_octet == 1 else 1
    
    our_ip = f"{parts[0]}.{parts[1]}.{parts[2]}.{our_last}"
    subnet = f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
    
    return our_ip, subnet

def configure_interface(ip, prefix="24"):
    global configured_ip
    
    # Remove existing IPs
    current_ips = run(f"ip addr show {ETH_INTERFACE} | grep 'inet ' | awk '{{print $2}}'")
    for old_ip in current_ips.split('\n'):
        if old_ip:
            run(f"ip addr del {old_ip} dev {ETH_INTERFACE} 2>/dev/null")
    
    # Add new IP
    run(f"ip addr add {ip}/{prefix} dev {ETH_INTERFACE}")
    run(f"ip link set {ETH_INTERFACE} up")
    
    # Store for keepalive
    configured_ip = f"{ip}/{prefix}"
    
    print(f"✅ Configured {ETH_INTERFACE}: {ip}/{prefix}")

def ip_keepalive():
    """Background thread to maintain IP configuration"""
    global configured_ip
    while True:
        time.sleep(10)  # Check every 10 seconds
        if configured_ip:
            # Check if IP still exists
            current = run(f"ip addr show {ETH_INTERFACE} | grep 'inet ' | grep -v inet6")
            if configured_ip.split('/')[0] not in current:
                print(f"🔄 Re-applying IP: {configured_ip}")
                run(f"ip addr add {configured_ip} dev {ETH_INTERFACE} 2>/dev/null")
                run(f"ip link set {ETH_INTERFACE} up")

def start_keepalive():
    """Start background IP keepalive thread"""
    thread = threading.Thread(target=ip_keepalive, daemon=True)
    thread.start()
    print("🔒 IP keepalive started")

def main():
    print("=" * 50)
    print("🔍 FactoryLM Auto Network Detection v2.0")
    print("=" * 50)
    
    # Wait for cable
    print(f"Waiting for {ETH_INTERFACE} link...")
    for i in range(DETECT_TIMEOUT):
        if get_interface_state():
            print(f"✅ Cable connected!")
            break
        time.sleep(1)
    else:
        print(f"⚠️ No cable detected, using fallback")
        configure_interface(FALLBACK_IP, FALLBACK_SUBNET)
        start_keepalive()
        return FALLBACK_IP
    
    # Detect neighbor
    print("🔍 Scanning for connected devices...")
    
    detected_ip = None
    for attempt in range(10):
        detected_ip = detect_neighbor_ip()
        if detected_ip:
            break
        print(f"  Scan attempt {attempt + 1}/10...")
        time.sleep(2)
    
    if detected_ip:
        print(f"🎯 Detected device at: {detected_ip}")
        our_ip, subnet = calculate_our_ip(detected_ip)
        if our_ip:
            configure_interface(our_ip)
            print(f"🔗 Joined network: {subnet}")
            
            # Start keepalive to maintain IP
            start_keepalive()
            
            # Verify
            time.sleep(1)
            ping_result = run(f"ping -c 1 -W 2 {detected_ip}")
            if "1 received" in ping_result:
                print(f"✅ Connection verified! Can reach {detected_ip}")
            
            return our_ip
    
    # Fallback
    print("⚠️ No device detected, using DHCP server mode")
    configure_interface(FALLBACK_IP, FALLBACK_SUBNET)
    start_keepalive()
    return FALLBACK_IP

if __name__ == "__main__":
    configured_ip = main()
    print(f"\n🌐 Network ready: {configured_ip}")
    print("=" * 50)
