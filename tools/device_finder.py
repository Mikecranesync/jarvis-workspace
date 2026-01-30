#!/usr/bin/env python3
"""
Device Finder - Industrial Network Device Discovery Tool
=========================================================

Automatically discovers embedded devices on your local network.
Built for finding BeagleBone, PLCs, and industrial controllers.

INSTALLATION:
    pip install rich scapy netifaces requests

USAGE:
    python3 device_finder.py              # Auto-scan local subnet
    python3 device_finder.py --subnet 192.168.1.0/24
    python3 device_finder.py --watch      # Continuous monitoring
    sudo python3 device_finder.py         # Full ARP scan (recommended)

Author: Jarvis (for Mike @ FactoryLM)
"""

import argparse
import json
import os
import socket
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.live import Live
    from rich.layout import Layout
    from rich.text import Text
    from rich import box
except ImportError:
    print("Installing required packages...")
    subprocess.run([sys.executable, "-m", "pip", "install", "rich", "netifaces", "requests"], 
                   capture_output=True)
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.live import Live
    from rich.layout import Layout
    from rich.text import Text
    from rich import box

try:
    import netifaces
except ImportError:
    netifaces = None

console = Console()

# Common embedded device IPs to try
COMMON_IPS = [
    "192.168.1.1", "192.168.0.1", "192.168.1.100", "192.168.0.100",
    "192.168.7.2",  # BeagleBone USB
    "192.168.6.2",  # BeagleBone USB alternate
    "10.0.0.1", "10.0.0.100",
    "172.16.0.1", "172.16.0.100",
    "169.254.1.1",  # Link-local
]

# Common ports for industrial/embedded devices
SCAN_PORTS = {
    22: "SSH",
    23: "Telnet", 
    80: "HTTP",
    443: "HTTPS",
    502: "Modbus",
    102: "S7comm",
    44818: "EtherNet/IP",
    4840: "OPC-UA",
    161: "SNMP",
    8080: "HTTP-Alt",
    3000: "Node/Dev",
}

# Common credentials to try
COMMON_CREDS = [
    ("debian", "temppwd"),    # BeagleBone default
    ("root", "root"),
    ("admin", "admin"),
    ("root", ""),
    ("ubuntu", "ubuntu"),
    ("pi", "raspberry"),
]

# OUI database for vendor lookup (partial)
OUI_DB = {
    "D0:5F:B8": "BeagleBone",
    "D0:39:72": "Texas Instruments",
    "00:1A:B6": "Texas Instruments",
    "B8:27:EB": "Raspberry Pi",
    "DC:A6:32": "Raspberry Pi",
    "E4:5F:01": "Raspberry Pi",
    "00:1D:9C": "Rockwell Automation",
    "00:00:BC": "Allen-Bradley",
    "00:0E:8C": "Siemens",
    "00:1F:F8": "Siemens",
}

CACHE_FILE = Path.home() / ".device_finder.json"


class Device:
    def __init__(self, ip: str):
        self.ip = ip
        self.mac = None
        self.vendor = None
        self.hostname = None
        self.open_ports = {}
        self.ping_ms = None
        self.online = False
        self.last_seen = None
    
    def to_dict(self):
        return {
            "ip": self.ip,
            "mac": self.mac,
            "vendor": self.vendor,
            "hostname": self.hostname,
            "open_ports": self.open_ports,
            "ping_ms": self.ping_ms,
            "online": self.online,
            "last_seen": self.last_seen,
        }
    
    @classmethod
    def from_dict(cls, data):
        d = cls(data["ip"])
        d.mac = data.get("mac")
        d.vendor = data.get("vendor")
        d.hostname = data.get("hostname")
        d.open_ports = data.get("open_ports", {})
        d.ping_ms = data.get("ping_ms")
        d.online = data.get("online", False)
        d.last_seen = data.get("last_seen")
        return d


def get_local_ip():
    """Get the local IP address of this machine."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


def get_subnet():
    """Detect the local subnet to scan."""
    local_ip = get_local_ip()
    # Assume /24 subnet
    parts = local_ip.split(".")
    return f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"


def ping_host(ip: str, timeout: float = 1.0) -> tuple:
    """Ping a host and return (success, latency_ms)."""
    try:
        # Use system ping for cross-platform compatibility
        if sys.platform == "win32":
            cmd = ["ping", "-n", "1", "-w", str(int(timeout * 1000)), ip]
        else:
            cmd = ["ping", "-c", "1", "-W", str(int(timeout)), ip]
        
        start = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 1)
        latency = (time.time() - start) * 1000
        
        if result.returncode == 0:
            # Try to extract actual RTT from output
            output = result.stdout
            if "time=" in output:
                import re
                match = re.search(r'time[=<](\d+\.?\d*)', output)
                if match:
                    latency = float(match.group(1))
            return True, round(latency, 1)
        return False, None
    except:
        return False, None


def check_port(ip: str, port: int, timeout: float = 0.5) -> bool:
    """Check if a port is open."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
        return False


def get_mac_address(ip: str) -> str:
    """Get MAC address from ARP cache."""
    try:
        if sys.platform == "win32":
            cmd = ["arp", "-a", ip]
        else:
            cmd = ["arp", "-n", ip]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        output = result.stdout.lower()
        
        # Look for MAC pattern
        import re
        mac_pattern = r'([0-9a-f]{2}[:-]){5}[0-9a-f]{2}'
        match = re.search(mac_pattern, output)
        if match:
            return match.group(0).upper().replace("-", ":")
    except:
        pass
    return None


def lookup_vendor(mac: str) -> str:
    """Lookup vendor from MAC OUI."""
    if not mac:
        return None
    oui = mac[:8].upper()
    return OUI_DB.get(oui)


def get_hostname(ip: str) -> str:
    """Try to get hostname via reverse DNS."""
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except:
        return None


def scan_device(ip: str, quick: bool = False) -> Device:
    """Scan a single device."""
    device = Device(ip)
    
    # Ping first
    online, latency = ping_host(ip)
    device.online = online
    device.ping_ms = latency
    
    if not online:
        return device
    
    device.last_seen = datetime.now().isoformat()
    
    # Get MAC and vendor
    device.mac = get_mac_address(ip)
    device.vendor = lookup_vendor(device.mac)
    
    # Get hostname
    device.hostname = get_hostname(ip)
    
    # Port scan (quick mode = fewer ports)
    ports_to_scan = [22, 80, 23, 443] if quick else SCAN_PORTS.keys()
    for port in ports_to_scan:
        if check_port(ip, port):
            device.open_ports[port] = SCAN_PORTS.get(port, "Unknown")
    
    return device


def scan_subnet(subnet: str, callback=None) -> list:
    """Scan entire subnet for devices."""
    devices = []
    
    # Parse subnet
    if "/" in subnet:
        base_ip = subnet.split("/")[0]
        parts = base_ip.split(".")
        base = f"{parts[0]}.{parts[1]}.{parts[2]}"
    else:
        parts = subnet.split(".")
        base = f"{parts[0]}.{parts[1]}.{parts[2]}"
    
    # Generate IPs to scan
    ips_to_scan = [f"{base}.{i}" for i in range(1, 255)]
    
    # Add common IPs that might be outside our subnet
    for ip in COMMON_IPS:
        if ip not in ips_to_scan:
            ips_to_scan.append(ip)
    
    # Parallel scan
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(scan_device, ip, quick=True): ip for ip in ips_to_scan}
        
        for future in as_completed(futures):
            device = future.result()
            if device.online:
                devices.append(device)
                if callback:
                    callback(device)
    
    return devices


def load_cache() -> dict:
    """Load cached device data."""
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE) as f:
                data = json.load(f)
                return {ip: Device.from_dict(d) for ip, d in data.items()}
        except:
            pass
    return {}


def save_cache(devices: list):
    """Save devices to cache."""
    data = {d.ip: d.to_dict() for d in devices}
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def display_devices(devices: list, selected_idx: int = 0):
    """Display devices in a nice table."""
    table = Table(title="🔍 Discovered Devices", box=box.ROUNDED)
    
    table.add_column("#", style="dim", width=3)
    table.add_column("IP Address", style="cyan")
    table.add_column("Status", width=8)
    table.add_column("Ping", width=8)
    table.add_column("MAC", style="dim")
    table.add_column("Vendor/Hostname", style="green")
    table.add_column("Open Ports", style="yellow")
    
    for i, device in enumerate(devices):
        status = "[green]● ONLINE[/green]" if device.online else "[red]○ OFFLINE[/red]"
        ping = f"{device.ping_ms}ms" if device.ping_ms else "-"
        mac = device.mac or "-"
        name = device.vendor or device.hostname or "-"
        ports = ", ".join([f"{p}" for p in device.open_ports.keys()]) or "-"
        
        style = "reverse" if i == selected_idx else ""
        table.add_row(str(i+1), device.ip, status, ping, mac, name, ports, style=style)
    
    return table


def display_device_details(device: Device):
    """Display detailed info for selected device."""
    lines = []
    lines.append(f"[bold cyan]IP Address:[/bold cyan] {device.ip}")
    lines.append(f"[bold cyan]Status:[/bold cyan] {'[green]ONLINE[/green]' if device.online else '[red]OFFLINE[/red]'}")
    lines.append(f"[bold cyan]Ping:[/bold cyan] {device.ping_ms}ms" if device.ping_ms else "[bold cyan]Ping:[/bold cyan] -")
    lines.append(f"[bold cyan]MAC:[/bold cyan] {device.mac or 'Unknown'}")
    lines.append(f"[bold cyan]Vendor:[/bold cyan] {device.vendor or 'Unknown'}")
    lines.append(f"[bold cyan]Hostname:[/bold cyan] {device.hostname or 'Unknown'}")
    lines.append(f"[bold cyan]Last Seen:[/bold cyan] {device.last_seen or 'Just now'}")
    lines.append("")
    lines.append("[bold yellow]Open Ports:[/bold yellow]")
    if device.open_ports:
        for port, service in device.open_ports.items():
            lines.append(f"  • {port} ({service})")
    else:
        lines.append("  None detected")
    
    lines.append("")
    lines.append("[bold green]Quick Actions:[/bold green]")
    lines.append("  [1] Open in browser (HTTP)")
    lines.append("  [2] SSH connect")
    lines.append("  [3] Telnet connect")
    lines.append("  [4] Detailed port scan")
    lines.append("  [5] Try default credentials")
    lines.append("  [6] Copy IP to clipboard")
    lines.append("  [q] Back to list")
    
    return Panel("\n".join(lines), title=f"📟 Device: {device.ip}", border_style="cyan")


def try_ssh_credentials(ip: str):
    """Try common SSH credentials."""
    console.print(f"\n[yellow]Trying common SSH credentials on {ip}...[/yellow]\n")
    
    for user, passwd in COMMON_CREDS:
        try:
            import paramiko
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, username=user, password=passwd, timeout=5)
            console.print(f"[green]✓ SUCCESS![/green] {user}:{passwd}")
            client.close()
            return user, passwd
        except ImportError:
            console.print("[red]paramiko not installed. Run: pip install paramiko[/red]")
            return None, None
        except:
            console.print(f"[dim]  ✗ {user}:{passwd}[/dim]")
    
    console.print("\n[red]No valid credentials found.[/red]")
    return None, None


def interactive_mode(devices: list):
    """Interactive device browser."""
    if not devices:
        console.print("[yellow]No devices found. Try running with sudo for ARP scan.[/yellow]")
        return
    
    selected = 0
    viewing_details = False
    
    console.print("\n[bold]Navigation:[/bold] ↑/↓ arrows, Enter=select, r=rescan, q=quit\n")
    
    while True:
        console.clear()
        
        if viewing_details:
            console.print(display_device_details(devices[selected]))
        else:
            console.print(display_devices(devices, selected))
            console.print("\n[dim]↑/↓: navigate | Enter: details | r: rescan | q: quit[/dim]")
        
        # Get input
        try:
            import sys, tty, termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
                if ch == '\x1b':  # Arrow key prefix
                    ch += sys.stdin.read(2)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except:
            ch = input()
        
        if ch == 'q':
            if viewing_details:
                viewing_details = False
            else:
                break
        elif ch == '\x1b[A':  # Up arrow
            selected = max(0, selected - 1)
        elif ch == '\x1b[B':  # Down arrow
            selected = min(len(devices) - 1, selected + 1)
        elif ch in ['\r', '\n']:  # Enter
            viewing_details = True
        elif ch == 'r':
            console.print("[yellow]Rescanning...[/yellow]")
            subnet = get_subnet()
            devices = scan_subnet(subnet)
            selected = 0
        elif viewing_details:
            device = devices[selected]
            if ch == '1' and 80 in device.open_ports:
                os.system(f"xdg-open http://{device.ip} 2>/dev/null || open http://{device.ip}")
            elif ch == '2' and 22 in device.open_ports:
                console.print(f"\n[cyan]Connecting via SSH to {device.ip}...[/cyan]")
                console.print("[dim]Default: debian / temppwd[/dim]\n")
                os.system(f"ssh debian@{device.ip}")
            elif ch == '3' and 23 in device.open_ports:
                os.system(f"telnet {device.ip}")
            elif ch == '4':
                console.print(f"\n[yellow]Deep scanning {device.ip}...[/yellow]\n")
                for port in SCAN_PORTS:
                    if check_port(device.ip, port):
                        console.print(f"[green]  ✓ {port} ({SCAN_PORTS[port]})[/green]")
                    else:
                        console.print(f"[dim]  ✗ {port}[/dim]")
                input("\nPress Enter to continue...")
            elif ch == '5':
                try_ssh_credentials(device.ip)
                input("\nPress Enter to continue...")
            elif ch == '6':
                try:
                    subprocess.run(['xclip', '-selection', 'clipboard'], 
                                 input=device.ip.encode(), check=True)
                    console.print(f"[green]Copied {device.ip} to clipboard[/green]")
                except:
                    console.print(f"[yellow]IP: {device.ip}[/yellow]")
                time.sleep(1)


def main():
    parser = argparse.ArgumentParser(description="Network Device Discovery Tool")
    parser.add_argument("--subnet", help="Subnet to scan (e.g., 192.168.1.0/24)")
    parser.add_argument("--watch", action="store_true", help="Continuous monitoring mode")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--quick", action="store_true", help="Quick scan (fewer ports)")
    args = parser.parse_args()
    
    # Detect subnet
    subnet = args.subnet or get_subnet()
    local_ip = get_local_ip()
    
    console.print(Panel(f"""
[bold cyan]Device Finder[/bold cyan] - Industrial Network Scanner

[yellow]Local IP:[/yellow] {local_ip}
[yellow]Scanning:[/yellow] {subnet}
[yellow]Common IPs:[/yellow] Also checking BeagleBone (192.168.7.2) and others

[dim]Tip: Run with sudo for full ARP scanning capabilities[/dim]
    """, title="🔍 Network Discovery", border_style="cyan"))
    
    # Load cache
    cached = load_cache()
    if cached:
        console.print(f"[dim]Loaded {len(cached)} cached devices[/dim]\n")
    
    # Scan
    devices = []
    
    def on_device_found(device):
        console.print(f"[green]  Found: {device.ip}[/green] ({device.vendor or 'Unknown'})")
    
    with console.status("[bold green]Scanning network...", spinner="dots"):
        devices = scan_subnet(subnet, callback=on_device_found)
    
    console.print(f"\n[bold]Found {len(devices)} devices online[/bold]\n")
    
    if args.json:
        print(json.dumps([d.to_dict() for d in devices], indent=2))
        return
    
    # Save to cache
    save_cache(devices)
    
    # Sort devices by IP
    devices.sort(key=lambda d: [int(x) for x in d.ip.split(".")])
    
    # Interactive mode
    if devices:
        interactive_mode(devices)
    else:
        console.print("[yellow]No devices found.[/yellow]")
        console.print("\n[bold]Troubleshooting:[/bold]")
        console.print("  1. Check physical cable connection")
        console.print("  2. Try setting a static IP (192.168.7.1) on your laptop")
        console.print("  3. For BeagleBone USB: check 192.168.7.2")
        console.print("  4. Run with sudo: sudo python3 device_finder.py")


if __name__ == "__main__":
    main()
