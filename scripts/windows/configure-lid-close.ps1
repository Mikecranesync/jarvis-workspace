# FactoryLM Device Configuration
# Prevents sleep on lid close for remote-controlled devices
# Run as Administrator

Write-Host "🔧 Configuring power settings for always-on operation..." -ForegroundColor Cyan

# 1. Set lid close action to "Do Nothing" (both AC and DC)
# LIDACTION: 0=Nothing, 1=Sleep, 2=Hibernate, 3=Shutdown
powercfg -setacvalueindex SCHEME_CURRENT SUB_BUTTONS LIDACTION 0
powercfg -setdcvalueindex SCHEME_CURRENT SUB_BUTTONS LIDACTION 0

# 2. Disable sleep when plugged in (set to 0 = never)
powercfg -change -standby-timeout-ac 0

# 3. Disable hibernate (frees disk space too)
powercfg -h off

# 4. Keep display on when plugged in (optional - set to 0 for never, or 5 for 5 min)
powercfg -change -monitor-timeout-ac 5

# 5. Disable USB selective suspend (prevents USB devices from sleeping)
powercfg -setacvalueindex SCHEME_CURRENT 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0

# 6. Apply changes
powercfg -setactive SCHEME_CURRENT

# 7. Verify settings
Write-Host "`n✅ Settings applied. Current lid close action:" -ForegroundColor Green
powercfg -query SCHEME_CURRENT SUB_BUTTONS LIDACTION | Select-String "Current AC Power Setting Index|Current DC Power Setting Index"

Write-Host "`n📋 Full power config:" -ForegroundColor Yellow
powercfg /batteryreport /duration 1 2>$null
powercfg -list

Write-Host "`n🎯 Done! Laptop will stay running with lid closed." -ForegroundColor Green
Write-Host "   - Lid close: Do Nothing"
Write-Host "   - Sleep when plugged in: Never"
Write-Host "   - Hibernate: Disabled"
Write-Host "   - Display timeout: 5 minutes"
