# 🤖 Jarvis Node - Remote Laptop Control

Control your Windows laptops from anywhere via Telegram.

## Architecture

```
📱 You (Telegram in Aruba)
        ↓
🧠 Clawdbot Gateway (VPS - Always On)
        ↓ HTTP over Tailscale
💻 Jarvis Node (PLC Laptop)     → Port 8765
💻 Jarvis Node (Travel Laptop)  → Port 8765
```

## Quick Install

### PLC Laptop

1. Open PowerShell as Administrator
2. Run:
```powershell
# Download installer
Invoke-WebRequest -Uri "http://100.68.120.99:8080/installers/install-plc-laptop.ps1" -OutFile install.ps1

# Or copy from VPS
scp root@100.68.120.99:/root/jarvis-workspace/installers/jarvis-node/install-plc-laptop.ps1 .

# Run
.\install-plc-laptop.ps1
```

### Travel Laptop

1. Open PowerShell as Administrator
2. Run:
```powershell
scp root@100.68.120.99:/root/jarvis-workspace/installers/jarvis-node/install-travel-laptop.ps1 .
.\install-travel-laptop.ps1
```

## Capabilities

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Status check |
| `/shell` | POST | Run shell command |
| `/screenshot` | GET | Take screenshot |
| `/click` | POST | Click at x,y |
| `/type` | POST | Type text |
| `/keypress` | POST | Press key(s) |
| `/camera` | GET | Capture from camera |
| `/clipboard` | POST | Read/write clipboard |
| `/file/read` | POST | Read file |
| `/file/write` | POST | Write file |
| `/file/list` | POST | List directory |
| `/processes` | GET | List processes |

## Usage Examples

### From VPS (or anywhere with Tailscale)

```bash
# Health check
curl http://100.72.2.99:8765/health

# Take screenshot
curl http://100.72.2.99:8765/screenshot | jq -r '.image_base64' | base64 -d > screen.png

# Run command
curl -X POST http://100.72.2.99:8765/shell \
  -H "Content-Type: application/json" \
  -d '{"command": "ollama list"}'

# Click at position
curl -X POST http://100.72.2.99:8765/click \
  -H "Content-Type: application/json" \
  -d '{"x": 500, "y": 300}'

# Type text
curl -X POST http://100.72.2.99:8765/type \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello from Aruba!"}'
```

## Tailscale IPs

| Device | Tailscale IP | Port |
|--------|-------------|------|
| VPS (Gateway) | 100.68.120.99 | - |
| PLC Laptop | 100.72.2.99 | 8765 |
| Travel Laptop | 100.83.251.23 | 8765 |

## Service Management

```powershell
# Status
Get-Service JarvisNode

# Start
Start-Service JarvisNode

# Stop
Stop-Service JarvisNode

# Restart
Restart-Service JarvisNode

# View logs
Get-Content C:\jarvis-node\logs\stdout.log -Tail 50 -Wait
```

## Troubleshooting

### Service won't start
```powershell
# Check logs
Get-Content C:\jarvis-node\logs\stderr.log

# Run manually to see errors
C:\jarvis-node\start-jarvis.bat
```

### Firewall issues
```powershell
# Verify rule exists
Get-NetFirewallRule -DisplayName "Jarvis Node"

# Re-add if needed
New-NetFirewallRule -DisplayName "Jarvis Node" -Direction Inbound -Protocol TCP -LocalPort 8765 -Action Allow
```

### Can't connect from VPS
1. Check Tailscale: `tailscale status`
2. Ping laptop: `ping 100.72.2.99`
3. Check service: `curl http://100.72.2.99:8765/health`

## Integration with Clawdbot

From Telegram, I (Clawdbot) can now:

```
"Screenshot PLC laptop"
→ curl http://100.72.2.99:8765/screenshot

"Run 'ollama list' on PLC laptop"
→ curl -X POST http://100.72.2.99:8765/shell -d '{"command":"ollama list"}'

"What's on the travel laptop screen?"
→ curl http://100.83.251.23:8765/screenshot
```

## Files

```
C:\jarvis-node\
├── jarvis_node.py      # Main server
├── venv\               # Python environment
├── .env                # Configuration
├── start-jarvis.bat    # Manual launcher
└── logs\
    ├── stdout.log      # Standard output
    └── stderr.log      # Errors
```
