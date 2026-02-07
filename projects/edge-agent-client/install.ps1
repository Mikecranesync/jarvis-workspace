#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Installs FactoryLM Edge Agent as a Windows Service

.DESCRIPTION
    Downloads Python (if needed), installs dependencies, and registers the FactoryLM Edge Agent 
    as a Windows service with auto-start capability.

.PARAMETER ServerUrl
    FactoryLM server URL (default: https://api.factorylm.com)

.PARAMETER InstallPath
    Installation directory (default: C:\Program Files\FactoryLM\EdgeAgent)

.EXAMPLE
    .\install.ps1
    .\install.ps1 -ServerUrl "https://custom.factorylm.com" -InstallPath "C:\FactoryLM"
#>

param(
    [string]$ServerUrl = "https://api.factorylm.com",
    [string]$InstallPath = "C:\Program Files\FactoryLM\EdgeAgent"
)

# Configuration
$PYTHON_VERSION = "3.11.8"
$PYTHON_URL = "https://www.python.org/ftp/python/$PYTHON_VERSION/python-$PYTHON_VERSION-amd64.exe"
$SERVICE_NAME = "FactoryLMEdgeAgent"
$GITHUB_REPO = "https://raw.githubusercontent.com/Mikecranesync/factorylm/main/agents/edge-agent-client"

Write-Host "=== FactoryLM Edge Agent Installer ===" -ForegroundColor Green
Write-Host "Server URL: $ServerUrl"
Write-Host "Install Path: $InstallPath"
Write-Host ""

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Error "This script must be run as Administrator. Right-click and 'Run as Administrator'."
    exit 1
}

# Function to check if Python is installed
function Test-PythonInstalled {
    try {
        $pythonVersion = & python --version 2>$null
        if ($pythonVersion -match "Python 3\.([89]|1[0-9])") {
            Write-Host "Python is already installed: $pythonVersion" -ForegroundColor Green
            return $true
        } else {
            Write-Host "Python version is too old or not found: $pythonVersion" -ForegroundColor Yellow
            return $false
        }
    } catch {
        Write-Host "Python is not installed" -ForegroundColor Yellow
        return $false
    }
}

# Function to install Python
function Install-Python {
    Write-Host "Downloading Python $PYTHON_VERSION..." -ForegroundColor Yellow
    
    $tempFile = "$env:TEMP\python-installer.exe"
    try {
        Invoke-WebRequest -Uri $PYTHON_URL -OutFile $tempFile -UseBasicParsing
        
        Write-Host "Installing Python..." -ForegroundColor Yellow
        $installArgs = @(
            "/quiet"
            "InstallAllUsers=1"
            "PrependPath=1"
            "Include_test=0"
            "Include_doc=0"
            "Include_dev=0"
            "Include_launcher=1"
            "InstallLauncherAllUsers=1"
        )
        
        $process = Start-Process -FilePath $tempFile -ArgumentList $installArgs -Wait -PassThru
        
        if ($process.ExitCode -eq 0) {
            Write-Host "Python installed successfully" -ForegroundColor Green
            
            # Refresh PATH
            $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
        } else {
            throw "Python installation failed with exit code: $($process.ExitCode)"
        }
    } catch {
        Write-Error "Failed to install Python: $_"
        exit 1
    } finally {
        if (Test-Path $tempFile) {
            Remove-Item $tempFile -Force
        }
    }
}

# Function to stop and remove existing service
function Remove-ExistingService {
    try {
        $service = Get-Service -Name $SERVICE_NAME -ErrorAction SilentlyContinue
        if ($service) {
            Write-Host "Stopping existing service..." -ForegroundColor Yellow
            Stop-Service -Name $SERVICE_NAME -Force -ErrorAction SilentlyContinue
            
            Write-Host "Removing existing service..." -ForegroundColor Yellow
            & sc.exe delete $SERVICE_NAME
            Start-Sleep -Seconds 2
        }
    } catch {
        Write-Warning "Could not remove existing service: $_"
    }
}

# Function to download agent files
function Download-AgentFiles {
    Write-Host "Creating installation directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null
    
    $files = @(
        "edge_agent_service.py",
        "requirements.txt"
    )
    
    foreach ($file in $files) {
        try {
            Write-Host "Downloading $file..." -ForegroundColor Yellow
            $url = "$GITHUB_REPO/$file"
            $destination = Join-Path $InstallPath $file
            Invoke-WebRequest -Uri $url -OutFile $destination -UseBasicParsing
        } catch {
            Write-Error "Failed to download $file from $url : $_"
            exit 1
        }
    }
    
    # Create config.json with custom server URL
    Write-Host "Creating configuration file..." -ForegroundColor Yellow
    $config = @{
        server_url = $ServerUrl
        device_id = $null
        hostname = $null
        heartbeat_interval = 60
        retry_attempts = 3
        retry_delay = 5
    }
    
    $configPath = Join-Path $InstallPath "config.json"
    $config | ConvertTo-Json -Depth 10 | Set-Content -Path $configPath
}

# Function to install Python dependencies
function Install-Dependencies {
    Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
    
    $requirementsPath = Join-Path $InstallPath "requirements.txt"
    
    try {
        # Upgrade pip first
        & python -m pip install --upgrade pip
        
        # Install requirements
        & python -m pip install -r $requirementsPath
        
        Write-Host "Dependencies installed successfully" -ForegroundColor Green
    } catch {
        Write-Error "Failed to install dependencies: $_"
        exit 1
    }
}

# Function to install and start service
function Install-Service {
    Write-Host "Installing Windows service..." -ForegroundColor Yellow
    
    $servicePath = Join-Path $InstallPath "edge_agent_service.py"
    
    try {
        # Install service using pywin32
        & python $servicePath --startup=auto install
        
        Write-Host "Starting service..." -ForegroundColor Yellow
        Start-Service -Name $SERVICE_NAME
        
        # Check service status
        $service = Get-Service -Name $SERVICE_NAME
        if ($service.Status -eq "Running") {
            Write-Host "Service installed and started successfully!" -ForegroundColor Green
        } else {
            Write-Warning "Service installed but not running. Status: $($service.Status)"
        }
    } catch {
        Write-Error "Failed to install service: $_"
        exit 1
    }
}

# Function to create uninstaller
function Create-Uninstaller {
    $uninstallScript = @'
#Requires -RunAsAdministrator
Write-Host "=== FactoryLM Edge Agent Uninstaller ===" -ForegroundColor Red

try {
    # Stop service
    Stop-Service -Name "FactoryLMEdgeAgent" -Force -ErrorAction SilentlyContinue
    
    # Remove service
    & python "INSTALL_PATH\edge_agent_service.py" remove
    
    Write-Host "Service removed successfully" -ForegroundColor Green
    
    # Remove files (optional)
    $response = Read-Host "Remove installation files? (y/N)"
    if ($response -eq "y" -or $response -eq "Y") {
        Remove-Item -Path "INSTALL_PATH" -Recurse -Force
        Write-Host "Installation files removed" -ForegroundColor Green
    }
    
} catch {
    Write-Error "Uninstall failed: $_"
}

Read-Host "Press Enter to continue..."
'@
    
    $uninstallScript = $uninstallScript.Replace("INSTALL_PATH", $InstallPath)
    $uninstallPath = Join-Path $InstallPath "uninstall.ps1"
    $uninstallScript | Set-Content -Path $uninstallPath
    
    Write-Host "Uninstaller created: $uninstallPath" -ForegroundColor Green
}

# Function to show firewall warning
function Show-FirewallWarning {
    Write-Host ""
    Write-Host "=== IMPORTANT: Firewall Configuration ===" -ForegroundColor Yellow
    Write-Host "The Edge Agent needs to communicate with:"
    Write-Host "  • Server: $ServerUrl"
    Write-Host "  • Ports: 80, 443 (HTTP/HTTPS)"
    Write-Host ""
    Write-Host "If you have a corporate firewall, you may need to:"
    Write-Host "  1. Whitelist the server URL"
    Write-Host "  2. Allow outbound connections on ports 80/443"
    Write-Host "  3. Configure proxy settings if required"
    Write-Host ""
}

# Main installation flow
try {
    Write-Host "Step 1: Checking Python installation..." -ForegroundColor Cyan
    if (-not (Test-PythonInstalled)) {
        Install-Python
    }
    
    Write-Host ""
    Write-Host "Step 2: Removing existing service (if any)..." -ForegroundColor Cyan
    Remove-ExistingService
    
    Write-Host ""
    Write-Host "Step 3: Downloading agent files..." -ForegroundColor Cyan
    Download-AgentFiles
    
    Write-Host ""
    Write-Host "Step 4: Installing dependencies..." -ForegroundColor Cyan
    Install-Dependencies
    
    Write-Host ""
    Write-Host "Step 5: Installing and starting service..." -ForegroundColor Cyan
    Install-Service
    
    Write-Host ""
    Write-Host "Step 6: Creating uninstaller..." -ForegroundColor Cyan
    Create-Uninstaller
    
    Write-Host ""
    Write-Host "=== Installation Complete! ===" -ForegroundColor Green
    Write-Host "Service Name: $SERVICE_NAME"
    Write-Host "Install Path: $InstallPath"
    Write-Host "Server URL: $ServerUrl"
    Write-Host ""
    Write-Host "Logs: $InstallPath\edge_agent.log"
    Write-Host "Config: $InstallPath\config.json"
    Write-Host "Uninstall: $InstallPath\uninstall.ps1"
    Write-Host ""
    
    # Show service status
    $service = Get-Service -Name $SERVICE_NAME
    Write-Host "Current Status: $($service.Status)" -ForegroundColor $(if ($service.Status -eq "Running") { "Green" } else { "Red" })
    
    Show-FirewallWarning
    
} catch {
    Write-Error "Installation failed: $_"
    Write-Host "Check the logs for more details: $InstallPath\edge_agent.log"
    exit 1
}

Write-Host ""
Read-Host "Press Enter to continue..."