#!/usr/bin/env python3
"""
FactoryLM Edge Agent - Windows Service
Registers with FactoryLM server, sends heartbeats, and applies configuration.
"""

import os
import sys
import json
import time
import uuid
import logging
import socket
import platform
import subprocess
import threading
from datetime import datetime
from typing import Dict, Optional, Any

import requests
import win32service
import win32serviceutil
import win32api
import win32con
import win32event
import servicemanager


# Configuration
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache.json')
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'edge_agent.log')

# Default configuration
DEFAULT_CONFIG = {
    "server_url": "https://api.factorylm.com",
    "device_id": None,
    "hostname": socket.gethostname(),
    "heartbeat_interval": 60,
    "retry_attempts": 3,
    "retry_delay": 5
}

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('FactoryLMEdgeAgent')


class EdgeAgentService(win32serviceutil.ServiceFramework):
    """Windows Service for FactoryLM Edge Agent"""
    
    _svc_name_ = "FactoryLMEdgeAgent"
    _svc_display_name_ = "FactoryLM Edge Agent"
    _svc_description_ = "Manages communication with FactoryLM server and applies device configurations"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.running = True
        self.config = self.load_config()
        self.session = requests.Session()
        self.session.timeout = 30
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                # Merge with defaults
                for key, value in DEFAULT_CONFIG.items():
                    if key not in config:
                        config[key] = value
                return config
            else:
                return DEFAULT_CONFIG.copy()
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return DEFAULT_CONFIG.copy()
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def load_cache(self) -> Dict[str, Any]:
        """Load cached data"""
        try:
            if os.path.exists(CACHE_FILE):
                with open(CACHE_FILE, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Error loading cache: {e}")
            return {}
    
    def save_cache(self, data: Dict[str, Any]):
        """Save data to cache"""
        try:
            with open(CACHE_FILE, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving cache: {e}")
    
    def get_system_info(self) -> Dict[str, Any]:
        """Collect system information"""
        try:
            # Get IP addresses
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            # Get OS info
            os_info = platform.platform()
            
            # Get battery info (if available)
            battery_percent = None
            try:
                import psutil
                battery = psutil.sensors_battery()
                if battery:
                    battery_percent = round(battery.percent, 1)
            except ImportError:
                # psutil not available, skip battery info
                pass
            except Exception:
                # Battery info not available
                pass
            
            return {
                "hostname": hostname,
                "ip_address": local_ip,
                "os": os_info,
                "battery_percent": battery_percent,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return {"hostname": socket.gethostname(), "timestamp": datetime.utcnow().isoformat()}
    
    def register_device(self) -> Optional[str]:
        """Register device with server and return device_id"""
        system_info = self.get_system_info()
        
        registration_data = {
            "hostname": system_info["hostname"],
            "ip_address": system_info.get("ip_address"),
            "os": system_info.get("os"),
            "agent_version": "1.0.0"
        }
        
        for attempt in range(self.config["retry_attempts"]):
            try:
                url = f"{self.config['server_url']}/api/devices/register"
                logger.info(f"Registering device with {url}")
                
                response = self.session.post(url, json=registration_data)
                response.raise_for_status()
                
                result = response.json()
                device_id = result.get("device_id")
                
                if device_id:
                    self.config["device_id"] = device_id
                    self.save_config()
                    logger.info(f"Device registered successfully: {device_id}")
                    return device_id
                else:
                    logger.error("Registration response missing device_id")
                    
            except Exception as e:
                logger.error(f"Registration attempt {attempt + 1} failed: {e}")
                if attempt < self.config["retry_attempts"] - 1:
                    time.sleep(self.config["retry_delay"])
        
        logger.error("Device registration failed after all attempts")
        return None
    
    def send_heartbeat(self) -> Optional[Dict[str, Any]]:
        """Send heartbeat and return server config"""
        if not self.config.get("device_id"):
            logger.warning("No device_id, attempting registration")
            if not self.register_device():
                return None
        
        system_info = self.get_system_info()
        heartbeat_data = {
            "status": "online",
            "timestamp": system_info["timestamp"],
            "battery_percent": system_info.get("battery_percent"),
            "system_info": system_info
        }
        
        for attempt in range(self.config["retry_attempts"]):
            try:
                device_id = self.config["device_id"]
                url = f"{self.config['server_url']}/api/devices/{device_id}/heartbeat"
                
                response = self.session.post(url, json=heartbeat_data)
                response.raise_for_status()
                
                logger.debug("Heartbeat sent successfully")
                
                # Try to get config
                config_url = f"{self.config['server_url']}/api/devices/{device_id}/config"
                config_response = self.session.get(config_url)
                config_response.raise_for_status()
                
                return config_response.json()
                
            except Exception as e:
                logger.error(f"Heartbeat attempt {attempt + 1} failed: {e}")
                if attempt < self.config["retry_attempts"] - 1:
                    time.sleep(self.config["retry_delay"])
        
        logger.error("Heartbeat failed after all attempts")
        return None
    
    def apply_power_config(self, config: Dict[str, Any]):
        """Apply power configuration using powercfg"""
        try:
            power_config = config.get("config", {})
            
            # Configure lid close action
            lid_action = power_config.get("lid_close_action", "do_nothing")
            lid_mapping = {
                "do_nothing": "0",
                "sleep": "1", 
                "hibernate": "2",
                "shutdown": "3"
            }
            
            if lid_action in lid_mapping:
                for power_scheme in ["SCHEME_CURRENT", "SCHEME_BALANCED", "SCHEME_MIN", "SCHEME_MAX"]:
                    try:
                        cmd = f'powercfg /setacvalueindex {power_scheme} SUB_BUTTONS LIDACTION {lid_mapping[lid_action]}'
                        subprocess.run(cmd, shell=True, check=True, capture_output=True)
                        cmd = f'powercfg /setdcvalueindex {power_scheme} SUB_BUTTONS LIDACTION {lid_mapping[lid_action]}'
                        subprocess.run(cmd, shell=True, check=True, capture_output=True)
                    except subprocess.CalledProcessError:
                        # Scheme might not exist, continue
                        pass
                
                # Apply the settings
                subprocess.run('powercfg /setactive SCHEME_CURRENT', shell=True, check=True, capture_output=True)
                logger.info(f"Lid close action set to: {lid_action}")
            
            # Configure sleep timeout
            sleep_timeout_ac = power_config.get("sleep_timeout_ac", 0)
            if isinstance(sleep_timeout_ac, int):
                # Convert minutes to seconds, 0 means never
                timeout_seconds = sleep_timeout_ac * 60 if sleep_timeout_ac > 0 else 0
                cmd = f'powercfg /change standby-timeout-ac {sleep_timeout_ac}'
                subprocess.run(cmd, shell=True, check=True, capture_output=True)
                logger.info(f"AC sleep timeout set to: {sleep_timeout_ac} minutes")
            
            # Configure hibernate
            hibernate_enabled = power_config.get("hibernate", False)
            hibernate_cmd = "powercfg /hibernate on" if hibernate_enabled else "powercfg /hibernate off"
            subprocess.run(hibernate_cmd, shell=True, check=True, capture_output=True)
            logger.info(f"Hibernate {'enabled' if hibernate_enabled else 'disabled'}")
            
        except Exception as e:
            logger.error(f"Error applying power configuration: {e}")
    
    def apply_config(self, server_config: Dict[str, Any]):
        """Apply configuration received from server"""
        try:
            cached_config = self.load_cache().get("last_config", {})
            
            # Only apply if config changed
            if server_config != cached_config:
                logger.info("Configuration changed, applying updates")
                
                # Apply power settings
                self.apply_power_config(server_config)
                
                # Cache the applied config
                cache_data = self.load_cache()
                cache_data["last_config"] = server_config
                cache_data["last_applied"] = datetime.utcnow().isoformat()
                self.save_cache(cache_data)
                
                logger.info("Configuration applied successfully")
            else:
                logger.debug("Configuration unchanged")
                
        except Exception as e:
            logger.error(f"Error applying configuration: {e}")
    
    def worker_thread(self):
        """Main worker thread"""
        logger.info("FactoryLM Edge Agent starting...")
        
        # Generate device_id if not present
        if not self.config.get("device_id"):
            self.config["device_id"] = str(uuid.uuid4())
            self.save_config()
        
        # Initial registration
        if not self.register_device():
            logger.error("Initial registration failed, will retry on heartbeat")
        
        # Main loop
        while self.running:
            try:
                # Send heartbeat and get config
                server_config = self.send_heartbeat()
                
                if server_config:
                    # Apply configuration
                    self.apply_config(server_config)
                
                # Wait for next interval or stop signal
                interval = self.config.get("heartbeat_interval", 60)
                if win32event.WaitForSingleObject(self.hWaitStop, interval * 1000) == win32event.WAIT_OBJECT_0:
                    break
                    
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                # Wait a bit before retrying
                if win32event.WaitForSingleObject(self.hWaitStop, 10000) == win32event.WAIT_OBJECT_0:
                    break
        
        logger.info("FactoryLM Edge Agent stopped")
    
    def SvcStop(self):
        """Stop the service"""
        logger.info("Service stop requested")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.running = False
        win32event.SetEvent(self.hWaitStop)
    
    def SvcDoRun(self):
        """Start the service"""
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        
        # Start worker thread
        worker = threading.Thread(target=self.worker_thread)
        worker.daemon = True
        worker.start()
        
        # Wait for stop signal
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)


def main():
    """Main entry point"""
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(EdgeAgentService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(EdgeAgentService)


if __name__ == '__main__':
    main()