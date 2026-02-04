# ShowUI Computer Use - PLC Laptop Setup
# Run as Administrator in PowerShell

$ErrorActionPreference = "Stop"
$INSTALL_DIR = "$env:USERPROFILE\Desktop\computer_use_ootb"

Write-Host "🏭 ShowUI Setup for PLC Laptop" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Check Python
Write-Host "`n📦 Checking Python..." -ForegroundColor Yellow
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "Python not found! Installing via winget..." -ForegroundColor Red
    winget install Python.Python.3.11
    refreshenv
}
python --version

# Clone or update repo
Write-Host "`n📥 Getting ShowUI repo..." -ForegroundColor Yellow
if (Test-Path $INSTALL_DIR) {
    Write-Host "Directory exists, updating..."
    cd $INSTALL_DIR
    git pull 2>$null || Write-Host "Not a git repo, skipping update"
} else {
    Write-Host "Cloning fresh..."
    git clone https://github.com/showlab/computer_use_ootb.git $INSTALL_DIR
    cd $INSTALL_DIR
}

# Create venv
Write-Host "`n🐍 Setting up virtual environment..." -ForegroundColor Yellow
if (-not (Test-Path "venv")) {
    python -m venv venv
}
.\venv\Scripts\Activate.ps1

# Install dependencies with pinned versions
Write-Host "`n📚 Installing dependencies (this takes a few minutes)..." -ForegroundColor Yellow
pip install --upgrade pip
pip install gradio==4.44.1
pip install "huggingface_hub<1.0"
pip install -r requirements.txt 2>$null || pip install torch torchvision pyautogui pillow

# Test CUDA
Write-Host "`n🎮 Checking GPU..." -ForegroundColor Yellow
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"None\"}')"

# Create startup script
Write-Host "`n📝 Creating startup script..." -ForegroundColor Yellow
@"
@echo off
cd /d %~dp0
call venv\Scripts\activate.bat
set PYTHONUNBUFFERED=1
python -u app.py
pause
"@ | Out-File -FilePath "$INSTALL_DIR\start-showui.bat" -Encoding ASCII

# Create CLAUDE.md for steering
Write-Host "`n🤖 Creating CLAUDE.md steering prompt..." -ForegroundColor Yellow
@"
# CLAUDE.md - ShowUI on PLC Laptop

## Purpose
Control Factory I/O and CCW via natural language for FactoryLM testing.

## Available Software
- Factory I/O (3D industrial simulation)
- CCW (Connected Components Workbench) for Allen-Bradley
- Connected to Micro820 PLC

## Test Scenarios
1. Open Factory I/O
2. Load a scene (e.g., sorting station)
3. Start simulation
4. Monitor PLC tags
5. Capture screenshots for training data

## ShowUI Config
- Planner: Claude 3.5 Sonnet (needs API key)
- Actor: ShowUI (free, local)
- GPU: Quadro P620

## Success Criteria
- Can open Factory I/O via voice command
- Can start/stop simulations
- Can capture screenshots programmatically
"@ | Out-File -FilePath "$INSTALL_DIR\CLAUDE.md" -Encoding UTF8

Write-Host "`n✅ Setup complete!" -ForegroundColor Green
Write-Host "`nTo start ShowUI:" -ForegroundColor Cyan
Write-Host "  1. Double-click: $INSTALL_DIR\start-showui.bat" -ForegroundColor White
Write-Host "  2. Or run: cd $INSTALL_DIR && .\venv\Scripts\Activate.ps1 && python app.py" -ForegroundColor White
Write-Host "`nThe public URL will be displayed once it starts." -ForegroundColor Yellow
