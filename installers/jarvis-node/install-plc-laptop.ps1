#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Jarvis Node Installer for PLC Laptop
.DESCRIPTION
    Installs Jarvis Node as a Windows service for remote control via Tailscale
.NOTES
    Run as Administrator
    Machine: PLC Laptop (100.72.2.99)
#>

$ErrorActionPreference = "Stop"
$MACHINE_NAME = "plc-laptop"
$PORT = 8765
$INSTALL_DIR = "C:\jarvis-node"
$WORKSPACE = "$env:USERPROFILE\jarvis-workspace"

Write-Host @"

╔══════════════════════════════════════════════════════════════╗
║  🤖 Jarvis Node Installer - PLC Laptop                       ║
╚══════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Cyan

# -----------------------------------------------------------------------------
# Step 1: Check Python
# -----------------------------------------------------------------------------
Write-Host "📦 Checking Python..." -ForegroundColor Yellow
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "❌ Python not found. Installing..." -ForegroundColor Red
    winget install Python.Python.3.12 --accept-package-agreements --accept-source-agreements
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}
python --version

# -----------------------------------------------------------------------------
# Step 2: Create directories
# -----------------------------------------------------------------------------
Write-Host "`n📁 Creating directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $INSTALL_DIR | Out-Null
New-Item -ItemType Directory -Force -Path $WORKSPACE | Out-Null

# -----------------------------------------------------------------------------
# Step 3: Create virtual environment
# -----------------------------------------------------------------------------
Write-Host "`n🐍 Creating virtual environment..." -ForegroundColor Yellow
python -m venv "$INSTALL_DIR\venv"

# -----------------------------------------------------------------------------
# Step 4: Install dependencies
# -----------------------------------------------------------------------------
Write-Host "`n📥 Installing dependencies..." -ForegroundColor Yellow
& "$INSTALL_DIR\venv\Scripts\pip.exe" install --upgrade pip
& "$INSTALL_DIR\venv\Scripts\pip.exe" install `
    fastapi `
    uvicorn `
    mss `
    pyautogui `
    opencv-python `
    pyperclip `
    pillow `
    open-interpreter

# -----------------------------------------------------------------------------
# Step 4b: Install Ollama (local LLM)
# -----------------------------------------------------------------------------
Write-Host "`n🦙 Installing Ollama..." -ForegroundColor Yellow
$ollamaPath = Get-Command ollama -ErrorAction SilentlyContinue
if (-not $ollamaPath) {
    Write-Host "   Downloading Ollama installer..." -ForegroundColor Gray
    $ollamaUrl = "https://ollama.com/download/OllamaSetup.exe"
    $ollamaInstaller = "$env:TEMP\OllamaSetup.exe"
    Invoke-WebRequest -Uri $ollamaUrl -OutFile $ollamaInstaller
    Start-Process -FilePath $ollamaInstaller -Wait
    Write-Host "   Ollama installed ✅" -ForegroundColor Green
} else {
    Write-Host "   Ollama already installed ✅" -ForegroundColor Green
}

# Pull Llama 3.2 model
Write-Host "   Pulling Llama 3.2 model (this may take a few minutes)..." -ForegroundColor Gray
Start-Process -FilePath "ollama" -ArgumentList "pull llama3.2:latest" -Wait -NoNewWindow

# -----------------------------------------------------------------------------
# Step 5: Download jarvis_node.py
# -----------------------------------------------------------------------------
Write-Host "`n⬇️  Downloading Jarvis Node..." -ForegroundColor Yellow

# For now, we'll embed it. In production, download from URL
$jarvisNodeUrl = "https://raw.githubusercontent.com/mikecranesync/factorylm/main/installers/jarvis-node/jarvis_node.py"
try {
    Invoke-WebRequest -Uri $jarvisNodeUrl -OutFile "$INSTALL_DIR\jarvis_node.py" -ErrorAction Stop
} catch {
    Write-Host "⚠️  Could not download from GitHub. Using embedded version..." -ForegroundColor Yellow
    # Fallback: Copy from VPS via Tailscale
    scp root@100.68.120.99:/root/jarvis-workspace/installers/jarvis-node/jarvis_node.py "$INSTALL_DIR\jarvis_node.py"
}

# -----------------------------------------------------------------------------
# Step 6: Create environment file
# -----------------------------------------------------------------------------
Write-Host "`n⚙️  Creating configuration..." -ForegroundColor Yellow
@"
JARVIS_MACHINE_NAME=$MACHINE_NAME
JARVIS_PORT=$PORT
JARVIS_WORKSPACE=$WORKSPACE
"@ | Out-File -FilePath "$INSTALL_DIR\.env" -Encoding UTF8

# -----------------------------------------------------------------------------
# Step 7: Create batch launcher
# -----------------------------------------------------------------------------
Write-Host "`n🚀 Creating launcher..." -ForegroundColor Yellow
@"
@echo off
cd /d $INSTALL_DIR
set JARVIS_MACHINE_NAME=$MACHINE_NAME
set JARVIS_PORT=$PORT
set JARVIS_WORKSPACE=$WORKSPACE
"$INSTALL_DIR\venv\Scripts\python.exe" "$INSTALL_DIR\jarvis_node.py"
"@ | Out-File -FilePath "$INSTALL_DIR\start-jarvis.bat" -Encoding ASCII

# -----------------------------------------------------------------------------
# Step 8: Install NSSM (if not present)
# -----------------------------------------------------------------------------
Write-Host "`n🔧 Setting up Windows service..." -ForegroundColor Yellow
$nssmPath = "C:\nssm\nssm.exe"
if (-not (Test-Path $nssmPath)) {
    Write-Host "   Downloading NSSM..." -ForegroundColor Gray
    $nssmUrl = "https://nssm.cc/release/nssm-2.24.zip"
    $nssmZip = "$env:TEMP\nssm.zip"
    Invoke-WebRequest -Uri $nssmUrl -OutFile $nssmZip
    Expand-Archive -Path $nssmZip -DestinationPath "$env:TEMP\nssm" -Force
    New-Item -ItemType Directory -Force -Path "C:\nssm" | Out-Null
    Copy-Item "$env:TEMP\nssm\nssm-2.24\win64\nssm.exe" "C:\nssm\nssm.exe"
}

# -----------------------------------------------------------------------------
# Step 9: Install service
# -----------------------------------------------------------------------------
Write-Host "   Installing service..." -ForegroundColor Gray

# Remove existing service if present
& $nssmPath stop JarvisNode 2>$null
& $nssmPath remove JarvisNode confirm 2>$null

# Install new service
& $nssmPath install JarvisNode "$INSTALL_DIR\venv\Scripts\python.exe" "`"$INSTALL_DIR\jarvis_node.py`""
& $nssmPath set JarvisNode AppDirectory $INSTALL_DIR
& $nssmPath set JarvisNode DisplayName "Jarvis Node - $MACHINE_NAME"
& $nssmPath set JarvisNode Description "Remote control agent for FactoryLM"
& $nssmPath set JarvisNode Start SERVICE_AUTO_START
& $nssmPath set JarvisNode AppEnvironmentExtra "JARVIS_MACHINE_NAME=$MACHINE_NAME" "JARVIS_PORT=$PORT" "JARVIS_WORKSPACE=$WORKSPACE"
& $nssmPath set JarvisNode AppStdout "$INSTALL_DIR\logs\stdout.log"
& $nssmPath set JarvisNode AppStderr "$INSTALL_DIR\logs\stderr.log"

New-Item -ItemType Directory -Force -Path "$INSTALL_DIR\logs" | Out-Null

# -----------------------------------------------------------------------------
# Step 10: Configure Firewall
# -----------------------------------------------------------------------------
Write-Host "`n🔥 Configuring firewall..." -ForegroundColor Yellow
Remove-NetFirewallRule -DisplayName "Jarvis Node" -ErrorAction SilentlyContinue
New-NetFirewallRule -DisplayName "Jarvis Node" -Direction Inbound -Protocol TCP -LocalPort $PORT -Action Allow | Out-Null

# -----------------------------------------------------------------------------
# Step 11: Start service
# -----------------------------------------------------------------------------
Write-Host "`n▶️  Starting service..." -ForegroundColor Yellow
Start-Service JarvisNode
Start-Sleep -Seconds 3

# -----------------------------------------------------------------------------
# Step 12: Verify
# -----------------------------------------------------------------------------
Write-Host "`n✅ Verifying installation..." -ForegroundColor Yellow
$status = Get-Service JarvisNode
if ($status.Status -eq "Running") {
    Write-Host "   Service: Running ✅" -ForegroundColor Green
} else {
    Write-Host "   Service: $($status.Status) ⚠️" -ForegroundColor Yellow
}

# Test health endpoint
try {
    $health = Invoke-RestMethod -Uri "http://localhost:$PORT/health" -Method Get
    Write-Host "   Health: $($health.status) ✅" -ForegroundColor Green
    Write-Host "   Machine: $($health.machine)" -ForegroundColor Gray
    Write-Host "   Capabilities: $($health.capabilities | ConvertTo-Json -Compress)" -ForegroundColor Gray
} catch {
    Write-Host "   Health check failed ⚠️" -ForegroundColor Yellow
}

# Get Tailscale IP
$tailscaleIp = (tailscale ip -4 2>$null)
if ($tailscaleIp) {
    Write-Host "`n🔗 Tailscale IP: $tailscaleIp" -ForegroundColor Cyan
    Write-Host "   Remote URL: http://${tailscaleIp}:$PORT" -ForegroundColor Cyan
}

Write-Host @"

╔══════════════════════════════════════════════════════════════╗
║  ✅ Jarvis Node Installed Successfully!                      ║
╠══════════════════════════════════════════════════════════════╣
║  Local:  http://localhost:$PORT/docs                          ║
║  Remote: http://${tailscaleIp}:$PORT                           ║
║                                                              ║
║  Commands:                                                   ║
║    Start:   Start-Service JarvisNode                         ║
║    Stop:    Stop-Service JarvisNode                          ║
║    Status:  Get-Service JarvisNode                           ║
║    Logs:    Get-Content $INSTALL_DIR\logs\stdout.log -Tail 50 ║
╚══════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Green
