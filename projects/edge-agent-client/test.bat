@echo off
REM Test script for FactoryLM Edge Agent
REM Run this to test agent functionality before installing as service

echo ====================================
echo FactoryLM Edge Agent Test
echo ====================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    echo.
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
python -c "import requests, json, uuid, socket, platform" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing dependencies...
    python -m pip install requests
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Try to install psutil for battery info
python -c "import psutil" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing psutil for battery monitoring...
    python -m pip install psutil >nul 2>&1
)

echo.
echo Starting test...
echo.

REM Run the test
python test_agent.py

echo.
echo Test completed. Check the output above for results.
echo.
pause