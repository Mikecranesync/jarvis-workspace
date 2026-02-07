# FactoryLM Edge Agent Dashboard

A modern, responsive web dashboard for managing FactoryLM Edge Agents.

## Features

### 📊 Real-time Monitoring
- **Device Overview**: Total, online, and offline device counts
- **Live Status**: Real-time online/offline status based on heartbeat timestamps
- **Last Seen**: Human-readable timestamps (e.g., "2m ago", "1h ago")
- **Auto-refresh**: Automatically updates every 30 seconds

### 🖥️ Device Management
- **Device List**: Clean table showing all registered devices
- **Status Indicators**: Visual online/offline status with colored icons
- **Device Details**: Hostname, IP address, device ID preview
- **Configuration**: Click any device to view and edit its configuration

### ⚙️ Configuration Editor
- **Power Management**: Lid close action, sleep timeouts, hibernate settings
- **Network**: Tailscale VPN enable/disable
- **Monitoring**: Configurable heartbeat intervals
- **Real-time Updates**: Changes saved immediately via API

### 🎨 Modern UI
- **Dark Theme**: Industrial look with dark gray/blue color scheme
- **Responsive**: Works on desktop, tablet, and mobile
- **Icons**: Font Awesome icons throughout
- **Notifications**: Success/error feedback for all actions

## Technical Stack

- **Frontend**: Single HTML file with embedded CSS and JavaScript
- **Styling**: Tailwind CSS (CDN) - no build tools required
- **Icons**: Font Awesome 6.0
- **API**: RESTful calls to FastAPI backend on port 8090

## API Integration

The dashboard expects these endpoints on `http://localhost:8090`:

```
GET  /api/devices              - List all devices
GET  /api/devices/{id}/config  - Get device configuration  
PUT  /api/devices/{id}/config  - Update device configuration
```

## Installation

### Option 1: Serve with FastAPI
Add static file serving to your FastAPI server:

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount the dashboard
app.mount("/dashboard", StaticFiles(directory="/path/to/edge-agent-dashboard"), name="dashboard")
```

Then access at: `http://localhost:8090/dashboard`

### Option 2: Simple HTTP Server
For development/testing:

```bash
cd /root/jarvis-workspace/projects/edge-agent-dashboard
python -m http.server 8080
```

Then access at: `http://localhost:8080`

## Configuration Schema

The dashboard expects device config in this format:

```json
{
  "device_id": "uuid-string",
  "hostname": "DEVICE-NAME", 
  "config": {
    "lid_close_action": "do_nothing|sleep|hibernate|shutdown",
    "sleep_timeout_ac": 0,  // seconds, 0 = never
    "hibernate": false,
    "tailscale_enabled": true,
    "monitoring_interval": 60  // seconds
  }
}
```

## Device Status Logic

A device is considered **online** if:
- `last_heartbeat` timestamp exists
- Last heartbeat was within the last 5 minutes

Otherwise, the device shows as **offline**.

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## File Structure

```
/edge-agent-dashboard/
├── index.html          # Complete dashboard (this file)
└── README.md          # This documentation
```

## Development

The dashboard is entirely self-contained in `index.html`. To modify:

1. Edit the HTML/CSS/JavaScript directly in the file
2. Refresh browser to see changes
3. No build step or compilation required

## Customization

### Colors
Modify the Tailwind config section to change the color scheme:

```javascript
tailwind.config = {
    theme: {
        extend: {
            colors: {
                'factory': {
                    'bg': '#0f172a',      // Main background
                    'card': '#1e293b',    // Card backgrounds
                    'accent': '#3b82f6',  // Primary accent
                    'success': '#10b981', // Success/online
                    'warning': '#f59e0b', // Warning
                    'danger': '#ef4444',  // Error/offline
                }
            }
        }
    }
}
```

### Refresh Interval
Change the auto-refresh interval (default 30 seconds):

```javascript
// Change 30000 to desired milliseconds
setInterval(refreshDevices, 30000);
```

### Offline Threshold
Change how long before a device is considered offline (default 5 minutes):

```javascript
function isDeviceOnline(lastHeartbeat) {
    // Change 5 to desired minutes
    const diffMinutes = (now - heartbeat) / (1000 * 60);
    return diffMinutes <= 5;
}
```

## Security Notes

- Dashboard connects to `localhost:8090` by default
- No authentication implemented (add as needed)
- CORS may need configuration for cross-origin requests
- Consider HTTPS for production deployments

## License

Part of the FactoryLM project.