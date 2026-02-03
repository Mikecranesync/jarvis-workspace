#!/usr/bin/env python3
"""
Jarvis Network Orchestrator
===========================
Central control for all Jarvis nodes (VPS, laptops, Raspberry Pi)

Usage:
    python orchestrate.py status          # Check all nodes
    python orchestrate.py deploy <node>   # Deploy Jarvis Node to a node
    python orchestrate.py ssh <node>      # Test SSH to a node
    python orchestrate.py exec <node> <cmd>  # Run command on a node
"""

import subprocess
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional
import requests

# =============================================================================
# NODE CONFIGURATION
# =============================================================================

NODES = {
    "vps": {
        "name": "JarvisVPS",
        "ip": "100.68.120.99",
        "user": "root",
        "type": "linux",
        "ssh": True,
        "jarvis_port": None,  # VPS is the brain, not a node
        "description": "Main VPS - Clawdbot, Open Interpreter, Brain"
    },
    "plc-laptop": {
        "name": "PLC Laptop",
        "ip": "100.72.2.99",
        "user": "mike",
        "type": "windows",
        "ssh": True,
        "jarvis_port": 8765,
        "description": "PLC Laptop - Quadro P620, Ollama, RSLogix"
    },
    "travel-laptop": {
        "name": "Travel Laptop",
        "ip": "100.83.251.23",
        "user": "mike",
        "type": "windows",
        "ssh": True,
        "jarvis_port": 8765,
        "description": "Travel Laptop - Development, presentations"
    },
    "raspberry-pi": {
        "name": "Raspberry Pi",
        "ip": None,  # Dynamic - set when it joins Tailscale
        "user": "pi",
        "type": "linux",
        "ssh": True,
        "jarvis_port": 8765,
        "description": "Raspberry Pi - Camera, GPIO, sensors"
    }
}

VPS_SSH_KEY = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOY0hljziGSbgrv8E/wmCXovYypHw1IKWX5XYyw/hqvY root@srv1078052"

# =============================================================================
# HELPERS
# =============================================================================

def run_cmd(cmd: str, timeout: int = 30) -> Dict[str, Any]:
    """Run a shell command and return result"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=timeout
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "code": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Command timed out"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def ssh_cmd(node_id: str, command: str, timeout: int = 30) -> Dict[str, Any]:
    """Run command on remote node via SSH"""
    node = NODES.get(node_id)
    if not node:
        return {"success": False, "error": f"Unknown node: {node_id}"}
    
    if not node.get("ip"):
        return {"success": False, "error": f"Node {node_id} has no IP configured"}
    
    ssh_cmd = f"ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=accept-new {node['user']}@{node['ip']} \"{command}\""
    return run_cmd(ssh_cmd, timeout)


def check_jarvis_node(ip: str, port: int = 8765) -> Dict[str, Any]:
    """Check if Jarvis Node is running on a host"""
    try:
        resp = requests.get(f"http://{ip}:{port}/health", timeout=5)
        return {"online": True, "status": resp.json()}
    except:
        return {"online": False, "status": None}


def check_ssh(node_id: str) -> bool:
    """Test SSH connectivity to a node"""
    result = ssh_cmd(node_id, "echo 'ok'", timeout=10)
    return result.get("success", False) and result.get("stdout") == "ok"


# =============================================================================
# STATUS COMMANDS
# =============================================================================

def status_all():
    """Check status of all nodes"""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  🏥 Jarvis Network Status                                    ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"\nTimestamp: {datetime.utcnow().isoformat()}Z\n")
    
    print("━" * 70)
    print(f"{'Node':<20} {'IP':<16} {'SSH':<8} {'Jarvis Node':<15}")
    print("━" * 70)
    
    for node_id, node in NODES.items():
        ip = node.get("ip") or "Not set"
        
        # Check SSH
        if node.get("ip"):
            ssh_ok = check_ssh(node_id)
            ssh_status = "✅" if ssh_ok else "❌"
        else:
            ssh_status = "⏳"
        
        # Check Jarvis Node
        if node.get("jarvis_port") and node.get("ip"):
            jarvis = check_jarvis_node(node["ip"], node["jarvis_port"])
            jarvis_status = "✅ Running" if jarvis["online"] else "❌ Offline"
        else:
            jarvis_status = "N/A" if node_id == "vps" else "⏳ Pending"
        
        print(f"{node['name']:<20} {ip:<16} {ssh_status:<8} {jarvis_status:<15}")
    
    print("━" * 70)
    
    # Tailscale status
    print("\n📡 Tailscale Devices:")
    result = run_cmd("tailscale status")
    if result["success"]:
        for line in result["stdout"].split("\n")[:6]:
            print(f"   {line}")


def status_node(node_id: str):
    """Detailed status for a single node"""
    node = NODES.get(node_id)
    if not node:
        print(f"❌ Unknown node: {node_id}")
        return
    
    print(f"\n🔍 Status: {node['name']}")
    print("━" * 50)
    print(f"   IP:          {node.get('ip') or 'Not configured'}")
    print(f"   Type:        {node['type']}")
    print(f"   User:        {node['user']}")
    print(f"   Description: {node['description']}")
    
    if not node.get("ip"):
        print("\n   ⚠️  Node IP not configured")
        return
    
    # SSH test
    print("\n   SSH Test:")
    ssh_ok = check_ssh(node_id)
    print(f"   {'✅ Connected' if ssh_ok else '❌ Failed'}")
    
    # Jarvis Node test
    if node.get("jarvis_port"):
        print("\n   Jarvis Node:")
        jarvis = check_jarvis_node(node["ip"], node["jarvis_port"])
        if jarvis["online"]:
            print(f"   ✅ Running on port {node['jarvis_port']}")
            status = jarvis["status"]
            if status:
                print(f"   CPU: {status.get('cpu_percent', 'N/A')}%")
                print(f"   Memory: {status.get('memory_percent', 'N/A')}%")
        else:
            print(f"   ❌ Not running")


# =============================================================================
# DEPLOYMENT COMMANDS
# =============================================================================

def deploy_ssh_key(node_id: str):
    """Deploy VPS SSH key to a node"""
    node = NODES.get(node_id)
    if not node:
        print(f"❌ Unknown node: {node_id}")
        return
    
    print(f"\n🔑 Deploying SSH key to {node['name']}...")
    
    if node["type"] == "windows":
        print("\n⚠️  Windows requires manual setup. Run this on the Windows machine:")
        print("\n   PowerShell (as Admin):")
        print(f'   Add-Content C:\\ProgramData\\ssh\\administrators_authorized_keys "{VPS_SSH_KEY}"')
        print("   icacls C:\\ProgramData\\ssh\\administrators_authorized_keys /inheritance:r /grant \"SYSTEM:(F)\" /grant \"Administrators:(F)\"")
        print("   Restart-Service sshd")
    
    elif node["type"] == "linux":
        # For Linux, we can try to deploy via SSH if password auth is enabled
        print("\n   If password SSH is enabled, run:")
        print(f"   ssh-copy-id -i ~/.ssh/id_ed25519.pub {node['user']}@{node['ip']}")
        print("\n   Or manually add this key to ~/.ssh/authorized_keys:")
        print(f"   {VPS_SSH_KEY}")


def deploy_jarvis_node(node_id: str):
    """Deploy Jarvis Node to a remote machine"""
    node = NODES.get(node_id)
    if not node:
        print(f"❌ Unknown node: {node_id}")
        return
    
    # First check SSH
    if not check_ssh(node_id):
        print(f"❌ Cannot SSH to {node['name']}. Fix SSH first.")
        return
    
    print(f"\n🚀 Deploying Jarvis Node to {node['name']}...")
    
    if node["type"] == "windows":
        # SCP the installer script and run it
        print("   Copying installer...")
        scp_result = run_cmd(
            f"scp /root/jarvis-workspace/infrastructure/scripts/setup-ssh-key.ps1 "
            f"{node['user']}@{node['ip']}:C:/temp/",
            timeout=60
        )
        if not scp_result["success"]:
            print(f"   ❌ Failed to copy: {scp_result.get('error')}")
            return
        
        print("   Running installer...")
        # Note: PowerShell execution might need adjustment
        ssh_cmd(node_id, "powershell -ExecutionPolicy Bypass -File C:/temp/setup-ssh-key.ps1", timeout=120)
    
    elif node["type"] == "linux":
        print("   Running setup script...")
        result = ssh_cmd(
            node_id,
            "curl -sL https://raw.githubusercontent.com/mikecranesync/jarvis/main/installers/raspberry-pi/first-boot.sh | sudo bash",
            timeout=300
        )
        if result["success"]:
            print("   ✅ Deployment complete")
        else:
            print(f"   ❌ Deployment failed: {result.get('error', result.get('stderr'))}")


# =============================================================================
# EXECUTION COMMANDS
# =============================================================================

def exec_on_node(node_id: str, command: str):
    """Execute command on a remote node"""
    node = NODES.get(node_id)
    if not node:
        print(f"❌ Unknown node: {node_id}")
        return
    
    print(f"\n⚡ Executing on {node['name']}: {command}")
    print("━" * 50)
    
    result = ssh_cmd(node_id, command, timeout=60)
    
    if result["success"]:
        print(result["stdout"])
    else:
        print(f"❌ Error: {result.get('error', result.get('stderr'))}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    cmd = sys.argv[1]
    
    if cmd == "status":
        if len(sys.argv) > 2:
            status_node(sys.argv[2])
        else:
            status_all()
    
    elif cmd == "deploy":
        if len(sys.argv) < 3:
            print("Usage: orchestrate.py deploy <node>")
            return
        deploy_jarvis_node(sys.argv[2])
    
    elif cmd == "ssh":
        if len(sys.argv) < 3:
            print("Usage: orchestrate.py ssh <node>")
            return
        node_id = sys.argv[2]
        if check_ssh(node_id):
            print(f"✅ SSH to {node_id} works!")
        else:
            print(f"❌ SSH to {node_id} failed")
            deploy_ssh_key(node_id)
    
    elif cmd == "exec":
        if len(sys.argv) < 4:
            print("Usage: orchestrate.py exec <node> <command>")
            return
        exec_on_node(sys.argv[2], " ".join(sys.argv[3:]))
    
    elif cmd == "key":
        if len(sys.argv) < 3:
            print("Usage: orchestrate.py key <node>")
            return
        deploy_ssh_key(sys.argv[2])
    
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
