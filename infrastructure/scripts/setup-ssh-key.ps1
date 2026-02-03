#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Add JarvisVPS SSH key to Windows for remote access
.DESCRIPTION
    This script adds the VPS public key to administrators_authorized_keys
    allowing Jarvis to SSH into this machine remotely
.NOTES
    Run as Administrator
#>

$ErrorActionPreference = "Stop"

Write-Host @"

╔══════════════════════════════════════════════════════════════╗
║  🔐 JarvisVPS SSH Key Setup                                  ║
╚══════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Cyan

# The VPS public key
$VPS_KEY = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOY0hljziGSbgrv8E/wmCXovYypHw1IKWX5XYyw/hqvY root@srv1078052"

# Paths
$SSH_DIR = "C:\ProgramData\ssh"
$AUTH_KEYS = "$SSH_DIR\administrators_authorized_keys"

# Step 1: Ensure OpenSSH is installed
Write-Host "📦 Checking OpenSSH Server..." -ForegroundColor Yellow
$sshd = Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH.Server*'
if ($sshd.State -ne 'Installed') {
    Write-Host "   Installing OpenSSH Server..." -ForegroundColor Gray
    Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
}
Write-Host "   OpenSSH Server: Installed ✅" -ForegroundColor Green

# Step 2: Start and enable SSH service
Write-Host "`n🚀 Configuring SSH Service..." -ForegroundColor Yellow
Start-Service sshd -ErrorAction SilentlyContinue
Set-Service -Name sshd -StartupType 'Automatic'
Write-Host "   SSH Service: Running ✅" -ForegroundColor Green

# Step 3: Create SSH directory if needed
if (-not (Test-Path $SSH_DIR)) {
    New-Item -ItemType Directory -Path $SSH_DIR -Force | Out-Null
}

# Step 4: Add the VPS key
Write-Host "`n🔑 Adding VPS Key..." -ForegroundColor Yellow

# Check if key already exists
$existingKeys = ""
if (Test-Path $AUTH_KEYS) {
    $existingKeys = Get-Content $AUTH_KEYS -Raw
}

if ($existingKeys -like "*$VPS_KEY*") {
    Write-Host "   Key already present ✅" -ForegroundColor Green
} else {
    Add-Content -Path $AUTH_KEYS -Value $VPS_KEY
    Write-Host "   Key added ✅" -ForegroundColor Green
}

# Step 5: Fix permissions (CRITICAL for Windows SSH)
Write-Host "`n🔒 Setting Permissions..." -ForegroundColor Yellow

# Remove inheritance and set correct permissions
icacls $AUTH_KEYS /inheritance:r /grant "SYSTEM:(F)" /grant "Administrators:(F)" | Out-Null
Write-Host "   Permissions set ✅" -ForegroundColor Green

# Step 6: Configure sshd_config for key auth
Write-Host "`n⚙️  Configuring SSH Settings..." -ForegroundColor Yellow
$sshdConfig = "$SSH_DIR\sshd_config"

# Enable PubkeyAuthentication
$config = Get-Content $sshdConfig
$config = $config -replace '#?PubkeyAuthentication.*', 'PubkeyAuthentication yes'
$config | Set-Content $sshdConfig

# Restart SSH to apply changes
Restart-Service sshd
Write-Host "   SSH configured and restarted ✅" -ForegroundColor Green

# Step 7: Configure firewall
Write-Host "`n🛡️  Configuring Firewall..." -ForegroundColor Yellow
$rule = Get-NetFirewallRule -Name "OpenSSH-Server-In-TCP" -ErrorAction SilentlyContinue
if (-not $rule) {
    New-NetFirewallRule -Name "OpenSSH-Server-In-TCP" -DisplayName "OpenSSH Server (sshd)" -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22 | Out-Null
}
Write-Host "   Firewall rule: Active ✅" -ForegroundColor Green

# Step 8: Show status
Write-Host @"

╔══════════════════════════════════════════════════════════════╗
║  ✅ SETUP COMPLETE                                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  VPS can now SSH into this machine.                         ║
║                                                              ║
║  Test from VPS:                                              ║
║    ssh mike@$(hostname)                                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Green

# Verify
Write-Host "📋 Verification:" -ForegroundColor Cyan
Write-Host "   SSH Service: $((Get-Service sshd).Status)"
Write-Host "   Auth Keys: $(Test-Path $AUTH_KEYS)"
Write-Host "   Key Present: $($existingKeys -like "*$VPS_KEY*" -or (Get-Content $AUTH_KEYS -Raw) -like "*$VPS_KEY*")"
