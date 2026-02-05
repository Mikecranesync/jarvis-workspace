# FactoryLM Device Bootstrap
# One script to configure a Windows device for remote operation
# Run as Administrator: irm https://raw.githubusercontent.com/Mikecranesync/jarvis-workspace/main/scripts/windows/bootstrap.ps1 | iex

param(
    [string]$TailscaleKey = "",
    [switch]$SkipTailscale
)

$ErrorActionPreference = "Stop"

Write-Host @"

╔═══════════════════════════════════════════════════════════╗
║           FactoryLM Device Bootstrap v1.0                 ║
║       Enterprise-grade config for small business          ║
╚═══════════════════════════════════════════════════════════╝

"@ -ForegroundColor Cyan

# Check admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "❌ Please run as Administrator" -ForegroundColor Red
    Write-Host "   Right-click PowerShell → Run as Administrator" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Running as Administrator" -ForegroundColor Green
Write-Host ""

# ============================================
# 1. Power Management
# ============================================
Write-Host "═══ Step 1: Power Management ═══" -ForegroundColor Yellow

# Lid close → Do Nothing
Write-Host "  Setting lid close action to 'Do Nothing'..."
powercfg -setacvalueindex SCHEME_CURRENT SUB_BUTTONS LIDACTION 0
powercfg -setdcvalueindex SCHEME_CURRENT SUB_BUTTONS LIDACTION 0

# Never sleep when plugged in
Write-Host "  Disabling sleep when plugged in..."
powercfg -change -standby-timeout-ac 0

# Disable hibernate
Write-Host "  Disabling hibernate..."
powercfg -h off

# Display timeout (5 min when plugged in, saves power but stays running)
Write-Host "  Setting display timeout to 5 minutes..."
powercfg -change -monitor-timeout-ac 5

# USB selective suspend off
Write-Host "  Disabling USB selective suspend..."
powercfg -setacvalueindex SCHEME_CURRENT 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0

# Apply
powercfg -setactive SCHEME_CURRENT

Write-Host "  ✅ Power settings configured" -ForegroundColor Green
Write-Host ""

# ============================================
# 2. Tailscale
# ============================================
if (-not $SkipTailscale) {
    Write-Host "═══ Step 2: Tailscale VPN ═══" -ForegroundColor Yellow
    
    $tailscale = Get-Command tailscale -ErrorAction SilentlyContinue
    if (-not $tailscale) {
        Write-Host "  📥 Downloading Tailscale..."
        $installer = "$env:TEMP\tailscale-setup.exe"
        Invoke-WebRequest -Uri "https://pkgs.tailscale.com/stable/tailscale-setup-latest.exe" -OutFile $installer
        
        Write-Host "  📦 Installing Tailscale..."
        Start-Process -FilePath $installer -Args "/quiet" -Wait
        
        # Refresh PATH
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    }
    
    # Ensure service runs
    Set-Service -Name "Tailscale" -StartupType Automatic -ErrorAction SilentlyContinue
    Start-Service -Name "Tailscale" -ErrorAction SilentlyContinue
    
    if ($TailscaleKey) {
        tailscale up --authkey=$TailscaleKey --accept-routes
    }
    
    Write-Host "  ✅ Tailscale configured" -ForegroundColor Green
} else {
    Write-Host "═══ Step 2: Tailscale (skipped) ═══" -ForegroundColor DarkGray
}
Write-Host ""

# ============================================
# 3. Windows Defender Exclusions (for dev tools)
# ============================================
Write-Host "═══ Step 3: Defender Exclusions ═══" -ForegroundColor Yellow

$exclusions = @(
    "$env:USERPROFILE\.ollama",
    "$env:USERPROFILE\AppData\Local\Tailscale",
    "C:\ProgramData\Tailscale"
)

foreach ($path in $exclusions) {
    if (Test-Path $path) {
        Add-MpPreference -ExclusionPath $path -ErrorAction SilentlyContinue
        Write-Host "  Added exclusion: $path"
    }
}
Write-Host "  ✅ Defender exclusions configured" -ForegroundColor Green
Write-Host ""

# ============================================
# 4. System Info
# ============================================
Write-Host "═══ Device Info ═══" -ForegroundColor Yellow
$computerName = $env:COMPUTERNAME
$ip = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.InterfaceAlias -notlike "*Loopback*" } | Select-Object -First 1).IPAddress
$tailscaleIP = tailscale ip -4 2>$null

Write-Host "  Computer Name: $computerName"
Write-Host "  Local IP: $ip"
if ($tailscaleIP) {
    Write-Host "  Tailscale IP: $tailscaleIP" -ForegroundColor Cyan
}
Write-Host ""

# ============================================
# Done
# ============================================
Write-Host @"
╔═══════════════════════════════════════════════════════════╗
║                    ✅ Setup Complete                      ║
╠═══════════════════════════════════════════════════════════╣
║  • Lid close: Do Nothing                                  ║
║  • Sleep (plugged in): Never                              ║
║  • Hibernate: Disabled                                    ║
║  • Tailscale: Installed & Running                         ║
║  • USB Power: Always On                                   ║
╠═══════════════════════════════════════════════════════════╣
║  This device will stay online with the lid closed.        ║
║  VPS will alert via Telegram if it goes offline.          ║
╚═══════════════════════════════════════════════════════════╝
"@ -ForegroundColor Green

# If Tailscale not authenticated, remind user
$tsStatus = tailscale status 2>&1
if ($tsStatus -like "*Logged out*" -or $tsStatus -like "*not logged in*") {
    Write-Host "`n⚠️  Tailscale not authenticated. Run: tailscale up" -ForegroundColor Yellow
}
