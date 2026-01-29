# Clawdbot Gateway Watchdog for Windows
# Run as: powershell -ExecutionPolicy Bypass -File watchdog.ps1

$TelegramToken = "8387943893:AAEynugW3SP1sWs6An4aNgZParSSRBlWSJk"
$ChatId = "8445149012"
$GatewayUrl = "http://localhost:18789"
$CheckInterval = 30  # seconds
$ClawdbotPath = "clawdbot"  # Assumes in PATH

function Send-TelegramAlert {
    param([string]$Message)
    $uri = "https://api.telegram.org/bot$TelegramToken/sendMessage"
    $body = @{
        chat_id = $ChatId
        text = $Message
        parse_mode = "Markdown"
    }
    try {
        Invoke-RestMethod -Uri $uri -Method Post -Body $body -ErrorAction SilentlyContinue | Out-Null
        Write-Host "[ALERT] Sent to Telegram"
    } catch {
        Write-Host "[ERR] Telegram failed: $_"
    }
}

function Test-Gateway {
    try {
        $response = Invoke-WebRequest -Uri $GatewayUrl -TimeoutSec 10 -ErrorAction Stop
        return $response.StatusCode -eq 200
    } catch {
        return $false
    }
}

function Restart-Gateway {
    Write-Host "[ACTION] Restarting gateway..."
    try {
        # Kill any existing process
        Get-Process -Name "node" -ErrorAction SilentlyContinue | 
            Where-Object { $_.CommandLine -like "*clawdbot*" } | 
            Stop-Process -Force -ErrorAction SilentlyContinue
        
        Start-Sleep -Seconds 2
        
        # Start gateway in background
        Start-Process -FilePath "cmd.exe" -ArgumentList "/c clawdbot gateway" -WindowStyle Hidden
        return $true
    } catch {
        Write-Host "[ERR] Restart failed: $_"
        return $false
    }
}

Write-Host "=========================================="
Write-Host "CLAWDBOT GATEWAY WATCHDOG (Windows)"
Write-Host "=========================================="
Write-Host "Monitoring: $GatewayUrl"
Write-Host "Interval: ${CheckInterval}s"
Write-Host ""

$consecutiveFailures = 0
$lastAlertTime = $null

while ($true) {
    $now = Get-Date -Format "HH:mm:ss"
    $isUp = Test-Gateway
    
    if ($isUp) {
        if ($consecutiveFailures -gt 0) {
            # Just recovered
            $downtime = $consecutiveFailures * $CheckInterval
            Send-TelegramAlert "✅ *Laptop Jarvis RECOVERED*`n`nGateway back online.`nDowntime: ~${downtime}s"
        }
        $consecutiveFailures = 0
        Write-Host "[$now] Gateway: ✅ UP"
    } else {
        $consecutiveFailures++
        Write-Host "[$now] Gateway: ❌ DOWN (failures: $consecutiveFailures)"
        
        # Alert after 2 failures (60s down)
        if ($consecutiveFailures -eq 2) {
            Send-TelegramAlert "🚨 *Laptop Jarvis CRASHED*`n`nGateway not responding for 60s`nTime: $now`n`nAttempting restart..."
            
            $restarted = Restart-Gateway
            if ($restarted) {
                Send-TelegramAlert "🔄 Restart initiated for Laptop Jarvis"
            }
        }
        
        # Repeat alert every 5 min if still down
        if ($consecutiveFailures -gt 0 -and $consecutiveFailures % 10 -eq 0) {
            $downtime = $consecutiveFailures * $CheckInterval
            Send-TelegramAlert "⚠️ *Laptop Jarvis STILL DOWN*`n`nBeen down for ${downtime}s`nManual intervention needed!"
        }
    }
    
    Start-Sleep -Seconds $CheckInterval
}
