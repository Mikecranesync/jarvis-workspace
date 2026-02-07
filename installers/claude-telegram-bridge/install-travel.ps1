#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Claude-Telegram Bridge Installer for Travel Laptop
.DESCRIPTION
    Installs Claude CLI → Telegram bridge as a Windows service
.NOTES
    Run as Administrator
    Machine: Travel Laptop (100.83.251.23)
#>

$ErrorActionPreference = "Stop"
$MACHINE_NAME = "travel-laptop"
$INSTALL_DIR = "C:\claude-telegram"
$SERVICE_NAME = "ClaudeTelegram"

Write-Host @"

╔══════════════════════════════════════════════════════════════╗
║  🤖 Claude-Telegram Bridge - Travel Laptop                   ║
╚══════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Cyan

# -----------------------------------------------------------------------------
# Get credentials
# -----------------------------------------------------------------------------
Write-Host "🔑 Configuration" -ForegroundColor Yellow
Write-Host ""

if (-not $env:TELEGRAM_BOT_TOKEN) {
    Write-Host "Get your bot token from @BotFather in Telegram" -ForegroundColor Gray
    $token = Read-Host "Enter Telegram Bot Token"
} else {
    $token = $env:TELEGRAM_BOT_TOKEN
    Write-Host "Using token from environment" -ForegroundColor Gray
}

if (-not $env:ALLOWED_USERS) {
    Write-Host "Get your user ID from @userinfobot in Telegram" -ForegroundColor Gray
    $userId = Read-Host "Enter your Telegram User ID"
} else {
    $userId = $env:ALLOWED_USERS
    Write-Host "Using user ID from environment" -ForegroundColor Gray
}

# -----------------------------------------------------------------------------
# Check Python
# -----------------------------------------------------------------------------
Write-Host "`n📦 Checking Python..." -ForegroundColor Yellow
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "Installing Python..." -ForegroundColor Yellow
    winget install Python.Python.3.12 --accept-package-agreements --accept-source-agreements
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}
python --version

# -----------------------------------------------------------------------------
# Check Claude CLI
# -----------------------------------------------------------------------------
Write-Host "`n🤖 Checking Claude CLI..." -ForegroundColor Yellow
$claude = Get-Command claude -ErrorAction SilentlyContinue
if (-not $claude) {
    Write-Host "Claude CLI not found!" -ForegroundColor Red
    Write-Host "Install from: https://claude.ai/code" -ForegroundColor Yellow
    Write-Host "Or run: winget install Anthropic.ClaudeCLI" -ForegroundColor Gray
    Read-Host "Press Enter after installing Claude CLI"
}

# Verify
try {
    claude --version
    Write-Host "Claude CLI: OK ✅" -ForegroundColor Green
} catch {
    Write-Host "Claude CLI not working. Please install it first." -ForegroundColor Red
    exit 1
}

# -----------------------------------------------------------------------------
# Create directories
# -----------------------------------------------------------------------------
Write-Host "`n📁 Creating directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $INSTALL_DIR | Out-Null
New-Item -ItemType Directory -Force -Path "$INSTALL_DIR\logs" | Out-Null

# -----------------------------------------------------------------------------
# Download bridge script
# -----------------------------------------------------------------------------
Write-Host "`n⬇️  Downloading bridge script..." -ForegroundColor Yellow
$scriptUrl = "https://raw.githubusercontent.com/Mikecranesync/jarvis-workspace/main/installers/claude-telegram-bridge/claude_telegram_bridge.py"

try {
    Invoke-WebRequest -Uri $scriptUrl -OutFile "$INSTALL_DIR\claude_telegram_bridge.py" -ErrorAction Stop
    Write-Host "Downloaded from GitHub ✅" -ForegroundColor Green
} catch {
    Write-Host "GitHub download failed, trying VPS..." -ForegroundColor Yellow
    scp root@100.68.120.99:/root/jarvis-workspace/installers/claude-telegram-bridge/claude_telegram_bridge.py "$INSTALL_DIR\claude_telegram_bridge.py"
}

# -----------------------------------------------------------------------------
# Install dependencies
# -----------------------------------------------------------------------------
Write-Host "`n📥 Installing Python dependencies..." -ForegroundColor Yellow
pip install python-telegram-bot>=20.0

# -----------------------------------------------------------------------------
# Create environment file
# -----------------------------------------------------------------------------
Write-Host "`n⚙️  Creating configuration..." -ForegroundColor Yellow
@"
TELEGRAM_BOT_TOKEN=$token
ALLOWED_USERS=$userId
MACHINE_NAME=$MACHINE_NAME
CLAUDE_WORKSPACE=$env:USERPROFILE\jarvis-workspace
"@ | Out-File -FilePath "$INSTALL_DIR\.env" -Encoding UTF8

# Create PowerShell wrapper that loads .env
@"
# Load environment
Get-Content "$INSTALL_DIR\.env" | ForEach-Object {
    if (`$_ -match "^([^=]+)=(.*)$") {
        [Environment]::SetEnvironmentVariable(`$matches[1], `$matches[2])
    }
}

# Run bridge
python "$INSTALL_DIR\claude_telegram_bridge.py"
"@ | Out-File -FilePath "$INSTALL_DIR\run-bridge.ps1" -Encoding UTF8

# Create batch launcher
@"
@echo off
powershell -ExecutionPolicy Bypass -File "$INSTALL_DIR\run-bridge.ps1"
"@ | Out-File -FilePath "$INSTALL_DIR\start-bridge.bat" -Encoding ASCII

# -----------------------------------------------------------------------------
# Install NSSM
# -----------------------------------------------------------------------------
Write-Host "`n🔧 Setting up Windows service..." -ForegroundColor Yellow
$nssmPath = "C:\nssm\nssm.exe"
if (-not (Test-Path $nssmPath)) {
    Write-Host "Downloading NSSM..." -ForegroundColor Gray
    $nssmUrl = "https://nssm.cc/release/nssm-2.24.zip"
    $nssmZip = "$env:TEMP\nssm.zip"
    Invoke-WebRequest -Uri $nssmUrl -OutFile $nssmZip
    Expand-Archive -Path $nssmZip -DestinationPath "$env:TEMP\nssm" -Force
    New-Item -ItemType Directory -Force -Path "C:\nssm" | Out-Null
    Copy-Item "$env:TEMP\nssm\nssm-2.24\win64\nssm.exe" "C:\nssm\nssm.exe"
}

# Remove existing service
& $nssmPath stop $SERVICE_NAME 2>$null
& $nssmPath remove $SERVICE_NAME confirm 2>$null

# Install service
& $nssmPath install $SERVICE_NAME powershell.exe "-ExecutionPolicy Bypass -File `"$INSTALL_DIR\run-bridge.ps1`""
& $nssmPath set $SERVICE_NAME AppDirectory $INSTALL_DIR
& $nssmPath set $SERVICE_NAME DisplayName "Claude Telegram - $MACHINE_NAME"
& $nssmPath set $SERVICE_NAME Description "Claude CLI to Telegram bridge for $MACHINE_NAME"
& $nssmPath set $SERVICE_NAME Start SERVICE_AUTO_START
& $nssmPath set $SERVICE_NAME AppStdout "$INSTALL_DIR\logs\stdout.log"
& $nssmPath set $SERVICE_NAME AppStderr "$INSTALL_DIR\logs\stderr.log"

# -----------------------------------------------------------------------------
# Start service
# -----------------------------------------------------------------------------
Write-Host "`n▶️  Starting service..." -ForegroundColor Yellow
Start-Service $SERVICE_NAME
Start-Sleep -Seconds 5

# -----------------------------------------------------------------------------
# Verify
# -----------------------------------------------------------------------------
Write-Host "`n✅ Verifying..." -ForegroundColor Yellow
$status = Get-Service $SERVICE_NAME
if ($status.Status -eq "Running") {
    Write-Host "Service: Running ✅" -ForegroundColor Green
} else {
    Write-Host "Service: $($status.Status) ⚠️" -ForegroundColor Yellow
    Write-Host "Check logs: Get-Content $INSTALL_DIR\logs\stderr.log" -ForegroundColor Gray
}

Write-Host @"

╔══════════════════════════════════════════════════════════════╗
║  ✅ Claude-Telegram Bridge Installed!                         ║
╠══════════════════════════════════════════════════════════════╣
║  Bot: @TravelJarvisBot (or whatever you named it)            ║
║  Machine: $MACHINE_NAME                                       ║
║                                                              ║
║  Commands:                                                   ║
║    Start:   Start-Service $SERVICE_NAME                       ║
║    Stop:    Stop-Service $SERVICE_NAME                        ║
║    Status:  Get-Service $SERVICE_NAME                         ║
║    Logs:    Get-Content $INSTALL_DIR\logs\stdout.log -Tail 50 ║
║                                                              ║
║  Test: Send a message to your bot in Telegram!               ║
╚══════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Green
