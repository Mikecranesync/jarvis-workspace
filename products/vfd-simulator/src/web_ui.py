#!/usr/bin/env python3
"""
VFD Simulator Web UI
====================
Provides a web interface for monitoring and controlling the VFD Simulator.

Author: Jarvis Agent for FactoryLM
Created: 2026-02-06
Issue: #27
"""

import asyncio
import json
import logging
from pathlib import Path

logger = logging.getLogger("VFD-WebUI")

# HTML template for the web UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VFD Simulator - FactoryLM</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #1a1a2e;
            color: #eee;
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { 
            text-align: center; 
            color: #00d4ff; 
            margin-bottom: 20px;
            font-size: 2em;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        .card {
            background: #16213e;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #0f3460;
        }
        .card h2 {
            color: #00d4ff;
            margin-bottom: 15px;
            font-size: 1.2em;
            border-bottom: 1px solid #0f3460;
            padding-bottom: 10px;
        }
        .gauge {
            text-align: center;
            padding: 20px 0;
        }
        .gauge-value {
            font-size: 3em;
            font-weight: bold;
            color: #00ff88;
        }
        .gauge-label {
            color: #888;
            font-size: 0.9em;
            margin-top: 5px;
        }
        .status-row {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #0f3460;
        }
        .status-label { color: #888; }
        .status-value { font-weight: bold; }
        .status-value.running { color: #00ff88; }
        .status-value.stopped { color: #ff6b6b; }
        .status-value.fault { color: #ff0000; animation: blink 0.5s infinite; }
        @keyframes blink { 50% { opacity: 0.5; } }
        .controls {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 15px;
        }
        button {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.2s;
        }
        button:hover { transform: scale(1.05); }
        .btn-run { background: #00ff88; color: #000; }
        .btn-stop { background: #ff6b6b; color: #fff; }
        .btn-fault { background: #ff9f43; color: #000; }
        .btn-reset { background: #54a0ff; color: #fff; }
        .slider-container { margin: 15px 0; }
        .slider-container label { display: block; margin-bottom: 8px; }
        input[type="range"] {
            width: 100%;
            height: 8px;
            border-radius: 4px;
            background: #0f3460;
            outline: none;
            -webkit-appearance: none;
        }
        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: #00d4ff;
            cursor: pointer;
        }
        .speed-display {
            text-align: center;
            font-size: 1.5em;
            margin-top: 10px;
            color: #00d4ff;
        }
        .motor-visual {
            width: 100px;
            height: 100px;
            margin: 20px auto;
            border: 4px solid #00d4ff;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }
        .motor-shaft {
            width: 20px;
            height: 60px;
            background: #00d4ff;
            position: absolute;
        }
        .motor-visual.spinning .motor-shaft {
            animation: spin linear infinite;
        }
        @keyframes spin { 100% { transform: rotate(360deg); } }
        .connection-status {
            position: fixed;
            top: 10px;
            right: 10px;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.8em;
        }
        .connection-status.connected { background: #00ff88; color: #000; }
        .connection-status.disconnected { background: #ff6b6b; color: #fff; }
    </style>
</head>
<body>
    <div class="connection-status disconnected" id="connStatus">Disconnected</div>
    
    <div class="container">
        <h1>🔧 VFD Simulator</h1>
        
        <div class="grid">
            <!-- Output Gauges -->
            <div class="card">
                <h2>Output</h2>
                <div class="gauge">
                    <div class="gauge-value" id="frequency">0.0</div>
                    <div class="gauge-label">Frequency (Hz)</div>
                </div>
                <div class="gauge">
                    <div class="gauge-value" id="rpm">0</div>
                    <div class="gauge-label">Motor RPM</div>
                </div>
            </div>
            
            <!-- Motor Visualization -->
            <div class="card">
                <h2>Motor</h2>
                <div class="motor-visual" id="motorVisual">
                    <div class="motor-shaft"></div>
                </div>
                <div class="status-row">
                    <span class="status-label">Status</span>
                    <span class="status-value" id="runStatus">STOPPED</span>
                </div>
                <div class="status-row">
                    <span class="status-label">Fault</span>
                    <span class="status-value" id="faultStatus">NO FAULT</span>
                </div>
            </div>
            
            <!-- Electrical -->
            <div class="card">
                <h2>Electrical</h2>
                <div class="status-row">
                    <span class="status-label">Output Voltage</span>
                    <span class="status-value" id="voltage">0 V</span>
                </div>
                <div class="status-row">
                    <span class="status-label">Output Current</span>
                    <span class="status-value" id="current">0.0 A</span>
                </div>
                <div class="status-row">
                    <span class="status-label">DC Bus</span>
                    <span class="status-value" id="dcBus">0 V</span>
                </div>
                <div class="status-row">
                    <span class="status-label">Run Time</span>
                    <span class="status-value" id="runTime">0.00 hrs</span>
                </div>
            </div>
            
            <!-- Controls -->
            <div class="card">
                <h2>Controls</h2>
                <div class="controls">
                    <button class="btn-run" onclick="sendCommand('run')">▶ RUN</button>
                    <button class="btn-stop" onclick="sendCommand('stop')">⏹ STOP</button>
                    <button class="btn-fault" onclick="sendCommand('fault')">⚠ INJECT FAULT</button>
                    <button class="btn-reset" onclick="sendCommand('reset')">↻ RESET</button>
                </div>
                <div class="slider-container">
                    <label>Speed Reference</label>
                    <input type="range" id="speedSlider" min="0" max="10000" value="0" 
                           oninput="updateSpeed(this.value)">
                    <div class="speed-display"><span id="speedPercent">0</span>%</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let ws = null;
        let reconnectTimer = null;
        
        function connect() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            ws = new WebSocket(`${protocol}//${window.location.host}/ws`);
            
            ws.onopen = () => {
                document.getElementById('connStatus').className = 'connection-status connected';
                document.getElementById('connStatus').textContent = 'Connected';
                if (reconnectTimer) {
                    clearInterval(reconnectTimer);
                    reconnectTimer = null;
                }
            };
            
            ws.onclose = () => {
                document.getElementById('connStatus').className = 'connection-status disconnected';
                document.getElementById('connStatus').textContent = 'Disconnected';
                if (!reconnectTimer) {
                    reconnectTimer = setInterval(connect, 2000);
                }
            };
            
            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                updateUI(data);
            };
        }
        
        function updateUI(data) {
            // Update gauges
            document.getElementById('frequency').textContent = data.output_frequency_hz.toFixed(1);
            document.getElementById('rpm').textContent = Math.round(data.motor_rpm);
            document.getElementById('voltage').textContent = Math.round(data.output_voltage_v) + ' V';
            document.getElementById('current').textContent = data.output_current_a.toFixed(2) + ' A';
            document.getElementById('dcBus').textContent = Math.round(data.dc_bus_voltage_v) + ' V';
            document.getElementById('runTime').textContent = data.run_time_hours.toFixed(2) + ' hrs';
            
            // Update status
            const runStatus = document.getElementById('runStatus');
            if (data.is_running) {
                runStatus.textContent = data.at_speed ? 'AT SPEED' : 'RAMPING';
                runStatus.className = 'status-value running';
            } else {
                runStatus.textContent = 'STOPPED';
                runStatus.className = 'status-value stopped';
            }
            
            // Update fault
            const faultStatus = document.getElementById('faultStatus');
            faultStatus.textContent = data.fault_name;
            faultStatus.className = data.fault_code !== 0 ? 'status-value fault' : 'status-value';
            
            // Update motor animation
            const motor = document.getElementById('motorVisual');
            if (data.is_running) {
                motor.classList.add('spinning');
                const speed = Math.max(0.1, 2 - (data.output_frequency_hz / 60) * 1.5);
                motor.querySelector('.motor-shaft').style.animationDuration = speed + 's';
            } else {
                motor.classList.remove('spinning');
            }
            
            // Update slider if not focused
            if (document.activeElement !== document.getElementById('speedSlider')) {
                document.getElementById('speedSlider').value = data.speed_reference;
                document.getElementById('speedPercent').textContent = Math.round(data.speed_reference / 100);
            }
        }
        
        function sendCommand(cmd) {
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({type: 'command', command: cmd}));
            }
        }
        
        function updateSpeed(value) {
            document.getElementById('speedPercent').textContent = Math.round(value / 100);
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({type: 'speed', value: parseInt(value)}));
            }
        }
        
        // Connect on load
        connect();
    </script>
</body>
</html>
"""


class WebUI:
    """Simple async web server for VFD UI"""
    
    def __init__(self, vfd, host: str = "0.0.0.0", port: int = 8080):
        self.vfd = vfd
        self.host = host
        self.port = port
        self._clients = set()
        self._running = False
    
    async def _handle_http(self, reader, writer):
        """Handle HTTP requests"""
        try:
            request = await reader.read(4096)
            request_line = request.decode().split('\r\n')[0]
            method, path, _ = request_line.split(' ')
            
            if path == '/':
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html\r\n"
                    f"Content-Length: {len(HTML_TEMPLATE)}\r\n"
                    "\r\n"
                ) + HTML_TEMPLATE
                writer.write(response.encode())
            elif path == '/api/state':
                state = json.dumps(self.vfd.get_state_dict())
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: application/json\r\n"
                    f"Content-Length: {len(state)}\r\n"
                    "\r\n"
                ) + state
                writer.write(response.encode())
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\n"
                writer.write(response.encode())
            
            await writer.drain()
        except Exception as e:
            logger.error(f"HTTP error: {e}")
        finally:
            writer.close()
            await writer.wait_closed()
    
    async def start(self):
        """Start web server"""
        self._running = True
        server = await asyncio.start_server(
            self._handle_http,
            self.host,
            self.port
        )
        logger.info(f"Web UI available at http://{self.host}:{self.port}")
        
        async with server:
            await server.serve_forever()


def create_app(vfd):
    """Create web application (for use with proper ASGI server)"""
    # This would integrate with FastAPI/Starlette for production
    # For now, returning the simple server
    return WebUI(vfd)
