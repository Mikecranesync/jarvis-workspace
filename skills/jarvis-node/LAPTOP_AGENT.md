# Jarvis Node - Laptop Agent Guide

Instructions for setting up and running Jarvis Node on a Windows laptop.

## Quick Install

Open PowerShell as Administrator and run:
```powershell
irm https://factorylm.com/install-node.ps1 | iex
```

## What Gets Installed

- **Location**: `C:\JarvisNode\`
- **Main script**: `jarvis_node.py`
- **Dependencies**: websockets, pyautogui, pillow

## Manual Start

If the node disconnects or you need to restart:
```powershell
python C:\JarvisNode\jarvis_node.py
```

You should see:
```
Jarvis Node 'YOURCOMPUTERNAME' connecting to ws://100.102.30.102:8765...
Connected and registered as 'YOURCOMPUTERNAME'
```

## Run at Startup (Optional)

To make Jarvis Node start automatically:

1. Press Win+R, type `shell:startup`
2. Create a file `jarvis-node.bat` with:
```batch
@echo off
python C:\JarvisNode\jarvis_node.py
```

## Troubleshooting

### "Connection refused" error:
- VPS server might be down
- Check Tailscale connection: `tailscale status`

### Node keeps disconnecting:
- Long shell commands can timeout
- VPS might have restarted

### "Python not found":
- Run installer again, or install Python manually:
  ```powershell
  winget install Python.Python.3.11
  ```

## Security Notes

- The agent allows remote control of your computer
- Only connects to the specified VPS via Tailscale
- No data is sent except to the VPS
- Close the Python window to disconnect

## Capabilities

When connected, the VPS can:
- Take screenshots of your screen
- Click anywhere on screen
- Type text
- Press keyboard shortcuts
- Run PowerShell/CMD commands

This is intentional - it's how Jarvis helps you remotely!
