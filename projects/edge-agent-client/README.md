# FactoryLM Edge Agent - Windows Client

The FactoryLM Edge Agent is a lightweight Windows service that connects Windows devices to the FactoryLM management platform. It handles device registration, configuration management, and status reporting.

## Features

- **Windows Service**: Runs automatically in the background with auto-start
- **Device Registration**: Automatically registers with FactoryLM server on first run
- **Heartbeat Monitoring**: Sends status updates every 60 seconds
- **Configuration Management**: Receives and applies power management settings
- **Retry Logic**: Robust error handling with exponential backoff
- **Offline Caching**: Caches configuration for offline operation
- **Power Management**: Configures lid close actions, sleep timeouts, and hibernate settings
- **Battery Monitoring**: Reports battery status (if available)

## Quick Installation

Run this one-liner in PowerShell **as Administrator**:

```powershell
irm https://raw.githubusercontent.com/Mikecranesync/factorylm/main/agents/edge-agent-client/install.ps1 | iex
```

### Custom Server URL

To connect to a custom server:

```powershell
irm https://raw.githubusercontent.com/Mikecranesync/factorylm/main/agents/edge-agent-client/install.ps1 -OutFile install.ps1
.\install.ps1 -ServerUrl "https://your-server.com"
```

## Manual Installation

### Prerequisites

- Windows 10/11 or Windows Server 2016+
- Administrator privileges
- Internet connection

### Steps

1. **Download the installer**:
   ```powershell
   Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Mikecranesync/factorylm/main/agents/edge-agent-client/install.ps1" -OutFile "install.ps1"
   ```

2. **Run installer as Administrator**:
   ```powershell
   .\install.ps1
   ```

3. **Verify installation**:
   ```powershell
   Get-Service FactoryLMEdgeAgent
   ```

## Configuration

The agent uses a JSON configuration file located at:
`C:\Program Files\FactoryLM\EdgeAgent\config.json`

### Default Configuration

```json
{
  "server_url": "https://api.factorylm.com",
  "device_id": null,
  "hostname": null,
  "heartbeat_interval": 60,
  "retry_attempts": 3,
  "retry_delay": 5
}
```

### Configuration Options

| Setting | Description | Default |
|---------|-------------|---------|
| `server_url` | FactoryLM server URL | `https://api.factorylm.com` |
| `device_id` | Unique device identifier (auto-generated) | `null` |
| `hostname` | Device hostname (auto-detected) | `null` |
| `heartbeat_interval` | Heartbeat frequency in seconds | `60` |
| `retry_attempts` | Number of retry attempts on failure | `3` |
| `retry_delay` | Delay between retries in seconds | `5` |

## Power Management Features

The agent can configure various Windows power settings:

### Lid Close Actions
- `do_nothing` - No action when lid is closed
- `sleep` - Put computer to sleep
- `hibernate` - Hibernate the computer
- `shutdown` - Shutdown the computer

### Sleep Timeouts
- Configure AC power sleep timeout (in minutes)
- 0 = never sleep

### Hibernate
- Enable or disable hibernate functionality

## Service Management

### Start/Stop Service
```powershell
# Start service
Start-Service FactoryLMEdgeAgent

# Stop service
Stop-Service FactoryLMEdgeAgent

# Restart service
Restart-Service FactoryLMEdgeAgent

# Check status
Get-Service FactoryLMEdgeAgent
```

### Service Configuration
```powershell
# Set service to automatic startup
Set-Service FactoryLMEdgeAgent -StartupType Automatic

# Set service to manual startup
Set-Service FactoryLMEdgeAgent -StartupType Manual
```

## Logging

Logs are written to: `C:\Program Files\FactoryLM\EdgeAgent\edge_agent.log`

### Log Levels
- **INFO**: Normal operation events
- **ERROR**: Error conditions
- **DEBUG**: Detailed debugging (enable in code)

### View Recent Logs
```powershell
Get-Content "C:\Program Files\FactoryLM\EdgeAgent\edge_agent.log" -Tail 50
```

## Uninstallation

Run the uninstaller script:
```powershell
& "C:\Program Files\FactoryLM\EdgeAgent\uninstall.ps1"
```

Or manually remove the service:
```powershell
# Stop service
Stop-Service FactoryLMEdgeAgent -Force

# Remove service
python "C:\Program Files\FactoryLM\EdgeAgent\edge_agent_service.py" remove

# Remove files
Remove-Item "C:\Program Files\FactoryLM\EdgeAgent" -Recurse -Force
```

## Troubleshooting

### Service Won't Start

1. Check Python installation:
   ```powershell
   python --version
   ```

2. Check dependencies:
   ```powershell
   python -m pip list | findstr "requests pywin32 psutil"
   ```

3. Check logs:
   ```powershell
   Get-Content "C:\Program Files\FactoryLM\EdgeAgent\edge_agent.log" -Tail 20
   ```

4. Test manually:
   ```powershell
   cd "C:\Program Files\FactoryLM\EdgeAgent"
   python edge_agent_service.py debug
   ```

### Network Connectivity Issues

1. Test server connectivity:
   ```powershell
   Test-NetConnection api.factorylm.com -Port 443
   ```

2. Check firewall settings:
   - Allow outbound connections on ports 80/443
   - Whitelist server domain in corporate firewall

3. Check proxy settings if behind corporate proxy

### Registration Issues

1. Verify server URL in config.json
2. Check server logs for registration errors
3. Ensure device has internet connectivity
4. Try manual registration with fresh device_id

### Permission Issues

1. Ensure service runs as SYSTEM account
2. Check power management permissions:
   ```powershell
   whoami /priv | findstr "SeShutdownPrivilege"
   ```

## API Endpoints

The agent communicates with these server endpoints:

- `POST /api/devices/register` - Device registration
- `POST /api/devices/{id}/heartbeat` - Status updates
- `GET /api/devices/{id}/config` - Configuration retrieval

## File Structure

```
C:\Program Files\FactoryLM\EdgeAgent\
├── edge_agent_service.py    # Main service script
├── requirements.txt         # Python dependencies
├── config.json             # Configuration file
├── cache.json              # Offline cache
├── edge_agent.log          # Log file
└── uninstall.ps1           # Uninstaller script
```

## Dependencies

- **Python 3.8+**: Core runtime
- **requests**: HTTP communication
- **pywin32**: Windows service integration
- **psutil**: System information (optional)

## Security Considerations

- Service runs as SYSTEM account
- All communication uses HTTPS
- Device IDs are UUID4 format
- No sensitive data stored in logs
- Configuration can be encrypted (future feature)

## Development

### Testing Locally
```powershell
cd "C:\Program Files\FactoryLM\EdgeAgent"
python edge_agent_service.py debug
```

### Service Registration
```powershell
# Install service
python edge_agent_service.py --startup=auto install

# Remove service  
python edge_agent_service.py remove
```

## Support

- **Documentation**: https://docs.factorylm.com
- **GitHub**: https://github.com/Mikecranesync/factorylm
- **Issues**: https://github.com/Mikecranesync/factorylm/issues