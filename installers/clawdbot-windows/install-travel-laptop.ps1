#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Clawdbot Installer for Travel Laptop
.DESCRIPTION
    Full Clawdbot installation - independent instance with own Telegram bot
.NOTES
    Run as Administrator
    Machine: Travel Laptop (100.83.251.23)
    Bot: @TravelLaptop_bot
#>

$ErrorActionPreference = "Stop"
$MACHINE_NAME = "travel-laptop"
$WORKSPACE = "C:\jarvis-workspace"
$CONFIG_DIR = "$env:USERPROFILE\.clawdbot"

# Bot token - CHANGE THIS if regenerated
$BOT_TOKEN = "8195640425:AAHQFw_U4v4Ev1PhDXkFQ-lfUQat1nFbceI"
$ALLOWED_USERS = "8445149012"  # Mike's Telegram ID

Write-Host @"

╔══════════════════════════════════════════════════════════════╗
║  🤖 Clawdbot Full Install - Travel Laptop                    ║
║  Bot: @TravelLaptop_bot                                      ║
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
# SOUL.md - Travel Laptop Jarvis

You are **Travel Jarvis**, running on Mike's travel laptop.

## Your Domain
- This is Mike's portable machine
- Used when traveling or working remotely
- General purpose - coding, research, communications

## Your Personality
- Versatile, adaptable
- Good at quick tasks and research
- You're the "on the go" assistant

## Your Relationship
- Mike is your human
- VPS Jarvis (@MainBot) is your sibling - primary instance
- PLC Jarvis (@PLCLaptop_bot) is your other sibling
- You're independent but collaborative

## Boundaries
- You control THIS machine only
- Full exec, file, browser access on travel laptop
- Be mindful of battery and resources when on the road
"@ | Out-File -FilePath "$WORKSPACE\SOUL.md" -Encoding UTF8

# Create AGENTS.md
@"
# AGENTS.md - Travel Laptop Workspace

Independent Clawdbot instance for travel laptop.

## Identity
- **Bot:** @TravelLaptop_bot
- **Machine:** Travel Laptop (Tailscale: 100.83.251.23)
- **Purpose:** Portable assistant, remote work, general tasks

## Capabilities
- Full control of this Windows machine
- Web browsing and research
- Code development
- General automation

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
This laptop travels with him for remote work.
"@ | Out-File -FilePath "$WORKSPACE\USER.md" -Encoding UTF8

# -----------------------------------------------------------------------------
# Step 5: Create Clawdbot config
# -----------------------------------------------------------------------------
Write-Host "`n⚙️ Creating Clawdbot config..." -ForegroundColor Yellow

$config = @"
# Clawdbot Config - Travel Laptop
# Bot: @TravelLaptop_bot

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
echo Starting Clawdbot - Travel Laptop...
cd /d $WORKSPACE
clawdbot gateway start
"@ | Out-File -FilePath "$WORKSPACE\start-clawdbot.bat" -Encoding ASCII

# Create PowerShell version
@"
# Start Clawdbot - Travel Laptop
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
║  ✅ Clawdbot Installed - Travel Laptop                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Bot: @TravelLaptop_bot                                      ║
║  Workspace: $WORKSPACE                              ║
║  Config: $CONFIG_DIR\config.yaml                    ║
║                                                              ║
║  Commands:                                                   ║
║    Start:   clawdbot gateway start                           ║
║    Stop:    clawdbot gateway stop                            ║
║    Status:  clawdbot gateway status                          ║
║                                                              ║
║  🧪 TEST: Message @TravelLaptop_bot in Telegram!             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Green
