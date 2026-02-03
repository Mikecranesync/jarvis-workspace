#!/usr/bin/env python3
"""
FactoryLM Micro820 Zero-Shot Connection Test
With Visual Proof-of-Work for Mike

This script will:
1. Find the PLC on the network
2. Connect via Modbus (primary) or EtherNet/IP (fallback)
3. Read data to prove connection
4. Generate a simple PASS/FAIL report Mike can verify in 5 seconds
"""

import subprocess
import requests
import socket
import time
import json
import sys
from datetime import datetime

PI_IP = "100.97.210.121"
PI_API = f"http://{PI_IP}:5000"

class TestReport:
    def __init__(self):
        self.phases = []
        self.plc_ip = None
        self.protocol = None
        self.read_value = None
        
    def add(self, phase, name, passed, detail=""):
        self.phases.append({
            "phase": phase,
            "name": name,
            "passed": passed,
            "detail": detail
        })
        return passed
    
    def summary(self):
        passed = sum(1 for p in self.phases if p["passed"])
        failed = len(self.phases) - passed
        return passed, failed


def run_ssh(cmd, timeout=10):
    """Run command on Pi via SSH."""
    try:
        result = subprocess.run(
            ["ssh", "-o", "ConnectTimeout=5", "-o", "StrictHostKeyChecking=no",
             f"root@{PI_IP}", cmd],
            capture_output=True, text=True, timeout=timeout
        )
        return result.returncode == 0, result.stdout.strip()
    except:
        return False, ""


def ping(host, timeout=2):
    """Ping a host."""
    result = subprocess.run(
        ["ping", "-c", "1", "-W", str(timeout), host],
        capture_output=True
    )
    return result.returncode == 0


def check_port(host, port, timeout=2):
    """Check if TCP port is open via Pi."""
    ok, _ = run_ssh(f"timeout {timeout} bash -c 'echo > /dev/tcp/{host}/{port}' 2>/dev/null && echo OK")
    return ok


def main():
    report = TestReport()
    
    print()
    print("╔════════════════════════════════════════════════════════════╗")
    print("║       🏭 FACTORYLM MICRO820 ZERO-SHOT TEST 🏭              ║")
    print("╠════════════════════════════════════════════════════════════╣")
    print(f"║  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'):^46} ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    
    # ═══════════════════════════════════════════════════════════════════
    # PHASE 1: Infrastructure
    # ═══════════════════════════════════════════════════════════════════
    print("📡 PHASE 1: Infrastructure Check")
    print("─" * 60)
    
    # 1.1 Pi reachable
    pi_ok = ping(PI_IP)
    report.add(1, "Pi reachable (Tailscale)", pi_ok)
    print(f"  {'✅' if pi_ok else '❌'} Pi Gateway reachable via Tailscale")
    
    if not pi_ok:
        print("\n⛔ CANNOT REACH PI - Test aborted")
        return 1
    
    # 1.2 Gateway API
    try:
        r = requests.get(f"{PI_API}/health", timeout=5)
        api_ok = r.status_code == 200
    except:
        api_ok = False
    report.add(1, "Gateway API", api_ok)
    print(f"  {'✅' if api_ok else '❌'} Gateway API responding")
    
    # 1.3 Get eth0 IP/subnet
    ok, eth0_info = run_ssh("ip addr show eth0 | grep 'inet ' | awk '{print $2}'")
    if ok and eth0_info:
        eth0_ip = eth0_info.split('/')[0]
        subnet = '.'.join(eth0_ip.split('.')[:3])
        report.add(1, "eth0 configured", True, eth0_ip)
        print(f"  ✅ Pi eth0: {eth0_ip}")
    else:
        report.add(1, "eth0 configured", False)
        print("  ❌ Pi eth0 has no IP - PLC cable connected?")
        print("\n⛔ NO NETWORK TO PLC - Test aborted")
        return 1
    
    print()
    
    # ═══════════════════════════════════════════════════════════════════
    # PHASE 2: PLC Discovery
    # ═══════════════════════════════════════════════════════════════════
    print("🔍 PHASE 2: PLC Discovery")
    print("─" * 60)
    
    # Scan for PLC on common addresses
    plc_ip = None
    scan_ips = [100, 10, 1, 2, 20, 50, 254]
    print(f"  Scanning {subnet}.x for devices...")
    
    for last_octet in scan_ips:
        test_ip = f"{subnet}.{last_octet}"
        ok, _ = run_ssh(f"ping -c 1 -W 1 {test_ip}", timeout=5)
        if ok:
            plc_ip = test_ip
            break
    
    if plc_ip:
        report.add(2, "PLC found", True, plc_ip)
        report.plc_ip = plc_ip
        print(f"  ✅ Device found: {plc_ip}")
    else:
        report.add(2, "PLC found", False)
        print("  ❌ No device found on subnet")
        print("\n  💡 MICRO820 DHCP TIP:")
        print("     Micro820 defaults to DHCP mode.")
        print("     Use CCW or BOOTP to assign static IP first!")
        return 1
    
    # Check protocols
    print(f"  Checking protocols on {plc_ip}...")
    
    modbus_ok = check_port(plc_ip, 502)
    report.add(2, "Modbus TCP (502)", modbus_ok)
    print(f"  {'✅' if modbus_ok else '❌'} Port 502 (Modbus TCP)")
    
    ethernetip_ok = check_port(plc_ip, 44818)
    report.add(2, "EtherNet/IP (44818)", ethernetip_ok)
    print(f"  {'✅' if ethernetip_ok else '⚠️ '} Port 44818 (EtherNet/IP)")
    
    if not modbus_ok and not ethernetip_ok:
        print("\n  ❌ No PLC protocols responding!")
        print("     Check CCW: Modbus TCP Server enabled?")
        return 1
    
    report.protocol = "modbus" if modbus_ok else "ethernetip"
    print()
    
    # ═══════════════════════════════════════════════════════════════════
    # PHASE 3: Communication Test
    # ═══════════════════════════════════════════════════════════════════
    print("📊 PHASE 3: PLC Communication")
    print("─" * 60)
    
    # Connect via Gateway API
    try:
        r = requests.post(f"{PI_API}/plc/connect", timeout=30)
        conn_result = r.json()
        connected = conn_result.get('connected', False)
    except Exception as e:
        connected = False
        print(f"  Connection error: {e}")
    
    report.add(3, "PLC connection", connected)
    print(f"  {'✅' if connected else '❌'} PLC connection established")
    
    if connected:
        # Try reading registers
        read_success = False
        for reg in [0, 1, 100]:
            try:
                r = requests.get(f"{PI_API}/plc/read/{reg}", timeout=10)
                data = r.json()
                if data.get('value') is not None:
                    report.read_value = data['value']
                    read_success = True
                    report.add(3, f"Read register {reg}", True, f"Value: {data['value']}")
                    print(f"  ✅ Read register {reg}: {data['value']}")
                    break
            except:
                pass
        
        if not read_success:
            report.add(3, "Read any register", False)
            print("  ⚠️  Could not read registers - check CCW Modbus mapping")
    
    print()
    
    # ═══════════════════════════════════════════════════════════════════
    # PROOF OF WORK - Mike's 5-Second Verification
    # ═══════════════════════════════════════════════════════════════════
    passed, failed = report.summary()
    
    print("╔════════════════════════════════════════════════════════════╗")
    if failed == 0:
        print("║                                                            ║")
        print("║           👍 THUMBS UP BUDDY, YOU DID IT! 👍              ║")
        print("║                                                            ║")
        print("║                    ███████████████                         ║")
        print("║                   █████████████████                        ║")
        print("║                   ███████████████████                      ║")
        print("║                    █████████████████                       ║")
        print("║                     ███████████████                        ║")
        print("║                      █████████████                         ║")
        print("║                       ███████████                          ║")
        print("║                        █████████                           ║")
        print("║                         ███████                            ║")
        print("║                          █████                             ║")
        print("║                                                            ║")
        print("╠════════════════════════════════════════════════════════════╣")
        print(f"║  PLC IP: {report.plc_ip:<49} ║")
        print(f"║  Protocol: {report.protocol:<47} ║")
        if report.read_value is not None:
            print(f"║  Read Value: {str(report.read_value):<45} ║")
        print("║                                                            ║")
        print("║  🎉 MICRO820 IS ONLINE AND TALKING TO FACTORYLM! 🎉       ║")
    else:
        print("║                                                            ║")
        print("║                  ❌ TEST INCOMPLETE ❌                     ║")
        print("║                                                            ║")
        print(f"║  Passed: {passed} | Failed: {failed:<36} ║")
        print("║                                                            ║")
        if report.plc_ip:
            print(f"║  PLC found at: {report.plc_ip:<43} ║")
        else:
            print("║  PLC not found - check cable + CCW IP config              ║")
        print("║                                                            ║")
        print("║  See test output above for what failed.                    ║")
    
    print("╠════════════════════════════════════════════════════════════╣")
    print(f"║  Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'):^44} ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
