@echo off
:: FactoryLM Always-On Setup
:: Double-click to run (will request admin)

:: Check for admin rights
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo.
echo ========================================
echo  FactoryLM Always-On Configuration
echo ========================================
echo.

:: Run the PowerShell script
powershell -ExecutionPolicy Bypass -File "%~dp0configure-lid-close.ps1"

echo.
pause
