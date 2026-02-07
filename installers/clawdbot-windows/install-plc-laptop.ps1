#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Clawdbot Installer for PLC Laptop
.DESCRIPTION
    Full Clawdbot installation - independent instance with own Telegram bot
.NOTES
    Run as Administrator
    Machine: PLC Laptop (100.72.2.99)
    Bot: @PLCLaptop_bot
#>

$ErrorActionPreference = "Stop"
$MACHINE_NAME = "plc-laptop"
$WORKSPACE = "C:\jarvis-workspace"
$CONFIG_DIR = "$env:USERPROFILE\.clawdbot"

# Bot token - CHANGE THIS if regenerated
$BOT_TOKEN = "8344767345:AAFOdZVED8ruXdKu74zcK3eOQH8fnb0Gf_4"
$ALLOWED_USERS = "8445149012"  # Mike's Telegram ID

Write-Host @"

╔══════════════════════════════════════════════════════════════╗
║  🤖 Clawdbot Full Install - PLC Laptop                       ║
║  Bot: @PLCLaptop_bot                                         ║
╚══════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Cyan

# -----------------------------------------------------------------------------
# Step 1: Check/Install Node.js
# -----------------------------------------------------------------------------
Write-Host "📦 Checking Node.js..." -ForegroundColor Yellow
$node = Get-Command node -ErrorAction SilentlyContinue
if (-not $node) {
    Write-Host "   Installing Node.js..." -ForegroundColor Gray
    winget install OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}
node --version
npm --version

# -----------------------------------------------------------------------------
# Step 2: Install Clawdbot
# -----------------------------------------------------------------------------
Write-Host "`n📥 Installing Clawdbot..." -ForegroundColor Yellow
npm install -g clawdbot

# Verify
$clawdbot = Get-Command clawdbot -ErrorAction SilentlyContinue
if (-not $clawdbot) {
    Write-Host "❌ Clawdbot installation failed!" -ForegroundColor Red
    exit 1
}
clawdbot --version

# -----------------------------------------------------------------------------
# Step 3: Create workspace
# -----------------------------------------------------------------------------
Write-Host "`n📁 Creating workspace..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $WORKSPACE | Out-Null
New-Item -ItemType Directory -Force -Path "$WORKSPACE\memory" | Out-Null
New-Item -ItemType Directory -Force -Path $CONFIG_DIR | Out-Null

# -----------------------------------------------------------------------------
# Step 4: Create SOUL.md (personality)
# -----------------------------------------------------------------------------
Write-Host "`n✨ Creating personality..." -ForegroundColor Yellow
@"
# SOUL.md - PLC Laptop Jarvis

You are **PLC Jarvis**, running on Mike's PLC laptop.

## Your Domain
- This laptop has Factory I/O (3D industrial simulation)
- Connected to real Allen-Bradley Micro820 PLC
- Has Quadro P620 GPU + Ollama for local LLM
- Connected Components Workbench (CCW) installed

## Your Personality
- Industrial automation specialist
- Direct, technical, no fluff
- You understand PLCs, ladder logic, HMIs
- You can run local Ollama models when cloud is overkill

## Your Relationship
- Mike is your human
- VPS Jarvis (@MainBot) is your sibling - you can receive tasks from it
- You're independent but collaborative

## Boundaries
- You control THIS machine only
- Full exec, file, browser access on PLC laptop
- Don't touch the PLC without explicit permission
"@ | Out-File -FilePath "$WORKSPACE\SOUL.md" -Encoding UTF8

# Create AGENTS.md
@"

# AGENTS.md - PLC Laptop Workspace

Independent Clawdbot instance for PLC laptop.

## Identity
- **Bot:** @PLCLaptop_bot
- **Machine:** PLC Laptop (Tailscale: 100.72.2.99)
- **Purpose:** Factory automation, PLC development, local LLM

## Capabilities
- Full control of this Windows machine
- Factory I/O simulation
- CCW for Micro820 programming
- Ollama for local inference

## Memory
- Write daily notes to `memory/YYYY-MM-DD.md`
- This workspace is independent from VPS

## Inter-Agent Communication
- VPS Jarvis may send you tasks via Telegram
- You can message back with results
"@ | Out-File -FilePath "$WORKSPACE\AGENTS.md" -Encoding UTF8

# Create USER.md
@"
# USER.md

- **Name:** Mike H
- **Telegram ID:** $ALLOWED_USERS
- **Timezone:** EST (Florida)

Mike is a maintenance technician building FactoryLM.
This laptop is for PLC development and Factory I/O demos.
"@ | Out-File -FilePath "$WORKSPACE\USER.md" -Encoding UTF8

# -----------------------------------------------------------------------------
# Step 5: Create Clawdbot config
# -----------------------------------------------------------------------------
Write-Host "`n⚙️ Creating Clawdbot config..." -ForegroundColor Yellow

$config = @"
# Clawdbot Config - PLC Laptop
# Bot: @PLCLaptop_bot

telegram:
  token: "$BOT_TOKEN"
  allowedUsers:
    - $ALLOWED_USERS

agent:
  workspace: "$($WORKSPACE -replace '\\', '/')"
  model: anthropic/claude-sonnet-4-20250514
  
gateway:
  heartbeatIntervalMs: 300000  # 5 min

# Security - full local control
security:
  allowElevated: true
  exec:
    mode: full
"@

$config | Out-File -FilePath "$CONFIG_DIR\config.yaml" -Encoding UTF8

# -----------------------------------------------------------------------------
# Step 6: Set up Anthropic API key
# -----------------------------------------------------------------------------
Write-Host "`n🔑 API Key Setup..." -ForegroundColor Yellow
$anthropicDir = "$env:USERPROFILE\.anthropic"
New-Item -ItemType Directory -Force -Path $anthropicDir | Out-Null

if (-not (Test-Path "$anthropicDir\api_key")) {
    Write-Host "   You need an Anthropic API key" -ForegroundColor Gray
    Write-Host "   Get one at: https://console.anthropic.com/keys" -ForegroundColor Gray
    $apiKey = Read-Host "Enter Anthropic API Key (or press Enter to skip)"
    if ($apiKey) {
        $apiKey | Out-File -FilePath "$anthropicDir\api_key" -Encoding UTF8 -NoNewline
        Write-Host "   API key saved ✅" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️ No API key - set ANTHROPIC_API_KEY env var later" -ForegroundColor Yellow
    }
}

# -----------------------------------------------------------------------------
# Step 7: Create startup script
# -----------------------------------------------------------------------------
Write-Host "`n🚀 Creating startup script..." -ForegroundColor Yellow

@"
@echo off
echo Starting Clawdbot - PLC Laptop...
cd /d $WORKSPACE
clawdbot gateway start
"@ | Out-File -FilePath "$WORKSPACE\start-clawdbot.bat" -Encoding ASCII

# Create PowerShell version
@"
# Start Clawdbot - PLC Laptop
Set-Location "$WORKSPACE"
clawdbot gateway start
"@ | Out-File -FilePath "$WORKSPACE\start-clawdbot.ps1" -Encoding UTF8

# -----------------------------------------------------------------------------
# Step 8: Add to startup (optional)
# -----------------------------------------------------------------------------
Write-Host "`n📌 Adding to startup..." -ForegroundColor Yellow
$startupFolder = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
Copy-Item "$WORKSPACE\start-clawdbot.bat" "$startupFolder\clawdbot.bat" -Force
Write-Host "   Added to Windows startup ✅" -ForegroundColor Green

# -----------------------------------------------------------------------------
# Step 9: Start Clawdbot
# -----------------------------------------------------------------------------
Write-Host "`n▶️ Starting Clawdbot..." -ForegroundColor Yellow
Set-Location $WORKSPACE

# Start in background
Start-Process -FilePath "clawdbot" -ArgumentList "gateway", "start" -WorkingDirectory $WORKSPACE -WindowStyle Minimized

Start-Sleep -Seconds 5

Write-Host @"

╔══════════════════════════════════════════════════════════════╗
║  ✅ Clawdbot Installed - PLC Laptop                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Bot: @PLCLaptop_bot                                         ║
║  Workspace: $WORKSPACE                              ║
║  Config: $CONFIG_DIR\config.yaml                    ║
║                                                              ║
║  Commands:                                                   ║
║    Start:   clawdbot gateway start                           ║
║    Stop:    clawdbot gateway stop                            ║
║    Status:  clawdbot gateway status                          ║
║                                                              ║
║  🧪 TEST: Message @PLCLaptop_bot in Telegram!                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Green
