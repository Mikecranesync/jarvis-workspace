# Jarvis Remote Access Setup for Windows
# Run as Administrator - ONE TIME ONLY
# This makes the laptop permanently accessible to Jarvis

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  JARVIS REMOTE ACCESS SETUP" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# 1. Install OpenSSH Server
Write-Host "[1/5] Installing OpenSSH Server..." -ForegroundColor Yellow
$sshCapability = Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH.Server*'
if ($sshCapability.State -ne 'Installed') {
    Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
    Write-Host "  OpenSSH Server installed" -ForegroundColor Green
} else {
    Write-Host "  OpenSSH Server already installed" -ForegroundColor Green
}

# 2. Start and enable SSH service
Write-Host "[2/5] Configuring SSH Service..." -ForegroundColor Yellow
Start-Service sshd
Set-Service -Name sshd -StartupType Automatic
Write-Host "  SSH service started and set to auto-start" -ForegroundColor Green

# 3. Configure firewall
Write-Host "[3/5] Configuring Firewall..." -ForegroundColor Yellow
$firewallRule = Get-NetFirewallRule -Name "OpenSSH-Server-In-TCP" -ErrorAction SilentlyContinue
if (-not $firewallRule) {
    New-NetFirewallRule -Name "OpenSSH-Server-In-TCP" -DisplayName "OpenSSH Server (sshd)" -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
    Write-Host "  Firewall rule created" -ForegroundColor Green
} else {
    Write-Host "  Firewall rule already exists" -ForegroundColor Green
}

# 4. Add Jarvis public key
Write-Host "[4/5] Adding Jarvis SSH Key..." -ForegroundColor Yellow
$sshDir = "$env:USERPROFILE\.ssh"
$authKeysFile = "$sshDir\authorized_keys"
$jarvisKey = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILEvc+FEGGSG0yswWMPGYxh1NA5FdRAdfAkTVR1pfxwY jarvis-remote-access"

if (-not (Test-Path $sshDir)) {
    New-Item -ItemType Directory -Path $sshDir -Force | Out-Null
}

if (Test-Path $authKeysFile) {
    $existingKeys = Get-Content $authKeysFile
    if ($existingKeys -contains $jarvisKey) {
        Write-Host "  Jarvis key already present" -ForegroundColor Green
    } else {
        Add-Content -Path $authKeysFile -Value $jarvisKey
        Write-Host "  Jarvis key added" -ForegroundColor Green
    }
} else {
    Set-Content -Path $authKeysFile -Value $jarvisKey
    Write-Host "  Jarvis key added" -ForegroundColor Green
}

# Fix permissions for authorized_keys (Windows ACL)
icacls $authKeysFile /inheritance:r /grant "$env:USERNAME`:R" /grant "SYSTEM:R" | Out-Null

# 5. Set default shell to PowerShell
Write-Host "[5/5] Setting PowerShell as default SSH shell..." -ForegroundColor Yellow
New-ItemProperty -Path "HKLM:\SOFTWARE\OpenSSH" -Name DefaultShell -Value "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" -PropertyType String -Force | Out-Null
Write-Host "  Default shell set to PowerShell" -ForegroundColor Green

# Done
Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  SETUP COMPLETE!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Jarvis can now access this laptop via:" -ForegroundColor White
Write-Host "  ssh -i ~/.ssh/jarvis_laptop_key $env:USERNAME@<tailscale-ip>" -ForegroundColor Yellow
Write-Host ""
Write-Host "Test the connection from VPS with:" -ForegroundColor White
Write-Host "  ssh -i ~/.ssh/jarvis_laptop_key $env:USERNAME@$(tailscale ip -4) 'hostname'" -ForegroundColor Yellow
Write-Host ""
