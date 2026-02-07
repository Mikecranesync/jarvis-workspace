#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Development utility script for FactoryLM Edge Agent

.DESCRIPTION
    Provides common development tasks like install, uninstall, test, logs, etc.

.PARAMETER Action
    Action to perform: install, uninstall, test, logs, status, restart

.PARAMETER ServerUrl
    Custom server URL for testing

.EXAMPLE
    .\dev.ps1 install
    .\dev.ps1 test
    .\dev.ps1 logs
    .\dev.ps1 status
#>

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("install", "uninstall", "test", "logs", "status", "restart", "stop", "start")]
    [string]$Action,
    
    [string]$ServerUrl = "https://api.factorylm.com"
)

$SERVICE_NAME = "FactoryLMEdgeAgent"
$INSTALL_PATH = "C:\Program Files\FactoryLM\EdgeAgent"

function Show-Status {
    Write-Host "=== FactoryLM Edge Agent Status ===" -ForegroundColor Cyan
    
    try {
        $service = Get-Service -Name $SERVICE_NAME -ErrorAction SilentlyContinue
        if ($service) {
            Write-Host "Service: $($service.Status)" -ForegroundColor $(if ($service.Status -eq "Running") { "Green" } else { "Red" })
            Write-Host "Startup Type: $($service.StartType)"
        } else {
            Write-Host "Service: Not Installed" -ForegroundColor Red
        }
    } catch {
        Write-Host "Service: Error checking status" -ForegroundColor Red
    }
    
    if (Test-Path $INSTALL_PATH) {
        Write-Host "Install Path: Exists" -ForegroundColor Green
        
        $configPath = Join-Path $INSTALL_PATH "config.json"
        if (Test-Path $configPath) {
            $config = Get-Content $configPath | ConvertFrom-Json
            Write-Host "Server URL: $($config.server_url)"
            Write-Host "Device ID: $($config.device_id)"
        }
    } else {
        Write-Host "Install Path: Missing" -ForegroundColor Red
    }
    
    Write-Host ""
}

function Install-Agent {
    Write-Host "Installing FactoryLM Edge Agent..." -ForegroundColor Yellow
    
    if (Test-Path ".\install.ps1") {
        & .\install.ps1 -ServerUrl $ServerUrl
    } else {
        Write-Error "install.ps1 not found in current directory"
    }
}

function Uninstall-Agent {
    Write-Host "Uninstalling FactoryLM Edge Agent..." -ForegroundColor Yellow
    
    try {
        # Stop service
        Stop-Service -Name $SERVICE_NAME -Force -ErrorAction SilentlyContinue
        
        # Remove service
        if (Test-Path (Join-Path $INSTALL_PATH "edge_agent_service.py")) {
            & python (Join-Path $INSTALL_PATH "edge_agent_service.py") remove
        }
        
        # Remove files
        if (Test-Path $INSTALL_PATH) {
            Remove-Item -Path $INSTALL_PATH -Recurse -Force
        }
        
        Write-Host "Agent uninstalled successfully" -ForegroundColor Green
    } catch {
        Write-Error "Uninstall failed: $_"
    }
}

function Test-Agent {
    Write-Host "Testing FactoryLM Edge Agent..." -ForegroundColor Yellow
    
    if (Test-Path ".\test_agent.py") {
        $args = @()
        if ($ServerUrl -ne "https://api.factorylm.com") {
            $args += "--server-url", $ServerUrl
        }
        
        & python test_agent.py @args
    } else {
        Write-Error "test_agent.py not found in current directory"
    }
}

function Show-Logs {
    Write-Host "=== Recent Logs ===" -ForegroundColor Cyan
    
    $logPath = Join-Path $INSTALL_PATH "edge_agent.log"
    if (Test-Path $logPath) {
        Get-Content $logPath -Tail 50
    } else {
        Write-Warning "Log file not found: $logPath"
    }
}

function Control-Service {
    param([string]$ServiceAction)
    
    try {
        $service = Get-Service -Name $SERVICE_NAME -ErrorAction SilentlyContinue
        if (-not $service) {
            Write-Error "Service not installed"
            return
        }
        
        switch ($ServiceAction) {
            "start" {
                Write-Host "Starting service..." -ForegroundColor Yellow
                Start-Service -Name $SERVICE_NAME
                Write-Host "Service started" -ForegroundColor Green
            }
            "stop" {
                Write-Host "Stopping service..." -ForegroundColor Yellow
                Stop-Service -Name $SERVICE_NAME -Force
                Write-Host "Service stopped" -ForegroundColor Green
            }
            "restart" {
                Write-Host "Restarting service..." -ForegroundColor Yellow
                Restart-Service -Name $SERVICE_NAME -Force
                Write-Host "Service restarted" -ForegroundColor Green
            }
        }
        
        # Show updated status
        Start-Sleep -Seconds 2
        Show-Status
        
    } catch {
        Write-Error "Service operation failed: $_"
    }
}

# Main action dispatcher
switch ($Action) {
    "install" { Install-Agent }
    "uninstall" { Uninstall-Agent }
    "test" { Test-Agent }
    "logs" { Show-Logs }
    "status" { Show-Status }
    "start" { Control-Service "start" }
    "stop" { Control-Service "stop" }
    "restart" { Control-Service "restart" }
    default { Write-Error "Unknown action: $Action" }
}