# ShowUI Computer Use - PLC Laptop Setup
# Run as Administrator in PowerShell

$ErrorActionPreference = "Continue"
$INSTALL_DIR = "$env:USERPROFILE\Desktop\computer_use_ootb"

Write-Host "ShowUI Setup for PLC Laptop" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Check Python
Write-Host "`nChecking Python..." -ForegroundColor Yellow
try {
    python --version
} catch {
    Write-Host "Python not found! Please install Python 3.11 first" -ForegroundColor Red
    exit 1
}

# Clone or update repo
Write-Host "`nGetting ShowUI repo..." -ForegroundColor Yellow
if (Test-Path $INSTALL_DIR) {
    Write-Host "Directory exists, using existing..."
    Set-Location $INSTALL_DIR
} else {
    Write-Host "Cloning fresh..."
    git clone https://github.com/showlab/computer_use_ootb.git $INSTALL_DIR
    Set-Location $INSTALL_DIR
}

# Create venv
Write-Host "`nSetting up virtual environment..." -ForegroundColor Yellow
if (-not (Test-Path "venv")) {
    python -m venv venv
}
& .\venv\Scripts\Activate.ps1

# Install dependencies with pinned versions
Write-Host "`nInstalling dependencies..." -ForegroundColor Yellow
pip install --upgrade pip
pip install gradio==4.44.1
pip install "huggingface_hub<1.0"
pip install torch torchvision pyautogui pillow

# Test CUDA
Write-Host "`nChecking GPU..." -ForegroundColor Yellow
python -c "import torch; print('CUDA:', torch.cuda.is_available())"

# Create startup script
Write-Host "`nCreating startup script..." -ForegroundColor Yellow
$startScript = @"
@echo off
cd /d %~dp0
call venv\Scripts\activate.bat
set PYTHONUNBUFFERED=1
python -u app.py
pause
"@
$startScript | Out-File -FilePath "$INSTALL_DIR\start-showui.bat" -Encoding ASCII

Write-Host "`nSetup complete!" -ForegroundColor Green
Write-Host "To start: Double-click start-showui.bat" -ForegroundColor Cyan
Write-Host "Or run: python app.py" -ForegroundColor Cyan
