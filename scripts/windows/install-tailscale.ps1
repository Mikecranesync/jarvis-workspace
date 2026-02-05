# FactoryLM Tailscale Setup
# Installs Tailscale and configures for always-on operation
# Run as Administrator

param(
    [string]$AuthKey = ""  # Optional: Tailscale auth key for headless setup
)

Write-Host "🔧 Installing Tailscale..." -ForegroundColor Cyan

# Check if already installed
$tailscale = Get-Command tailscale -ErrorAction SilentlyContinue
if ($tailscale) {
    Write-Host "✅ Tailscale already installed" -ForegroundColor Green
    tailscale version
} else {
    # Download and install
    $installer = "$env:TEMP\tailscale-setup.exe"
    Write-Host "📥 Downloading Tailscale..."
    Invoke-WebRequest -Uri "https://pkgs.tailscale.com/stable/tailscale-setup-latest.exe" -OutFile $installer
    
    Write-Host "📦 Installing..."
    Start-Process -FilePath $installer -Args "/quiet" -Wait
    
    # Refresh PATH
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    
    Write-Host "✅ Tailscale installed" -ForegroundColor Green
}

# Ensure service is running
Write-Host "🔄 Ensuring Tailscale service is running..."
Set-Service -Name "Tailscale" -StartupType Automatic
Start-Service -Name "Tailscale" -ErrorAction SilentlyContinue

# Configure for stability
Write-Host "⚙️ Configuring for always-on operation..."

# If auth key provided, do headless login
if ($AuthKey) {
    tailscale up --authkey=$AuthKey --accept-routes
} else {
    Write-Host "`n📱 Run 'tailscale up' to authenticate (or provide -AuthKey)" -ForegroundColor Yellow
}

# Show status
Write-Host "`n📋 Tailscale Status:" -ForegroundColor Cyan
tailscale status

Write-Host "`n✅ Tailscale setup complete" -ForegroundColor Green
