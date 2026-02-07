#!/usr/bin/env python3
"""
Test script for FactoryLM Edge Agent
Run this to test agent functionality without installing as a service.
"""

import os
import sys
import json
import time
import uuid
import socket
import platform
import logging
from datetime import datetime
from typing import Dict, Any, Optional

import requests

# Setup logging for testing
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('EdgeAgentTest')

class EdgeAgentTester:
    """Test harness for Edge Agent functionality"""
    
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self.load_config()
        self.session = requests.Session()
        self.session.timeout = 30
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        default_config = {
            "server_url": "https://api.factorylm.com",
            "device_id": str(uuid.uuid4()),
            "hostname": socket.gethostname(),
            "heartbeat_interval": 60,
            "retry_attempts": 3,
            "retry_delay": 5
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                # Merge with defaults
                for key, value in default_config.items():
                    if key not in config or config[key] is None:
                        config[key] = value
                return config
            else:
                return default_config
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return default_config
    
    def get_system_info(self) -> Dict[str, Any]:
        """Collect system information"""
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            os_info = platform.platform()
            
            # Try to get battery info
            battery_percent = None
            try:
                import psutil
                battery = psutil.sensors_battery()
                if battery:
                    battery_percent = round(battery.percent, 1)
            except (ImportError, Exception):
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
    
    def test_registration(self) -> bool:
        """Test device registration"""
        logger.info("Testing device registration...")
        
        system_info = self.get_system_info()
        registration_data = {
            "hostname": system_info["hostname"],
            "ip_address": system_info.get("ip_address"),
            "os": system_info.get("os"),
            "agent_version": "1.0.0"
        }
        
        try:
            url = f"{self.config['server_url']}/api/devices/register"
            logger.info(f"POST {url}")
            logger.info(f"Data: {json.dumps(registration_data, indent=2)}")
            
            response = self.session.post(url, json=registration_data)
            
            logger.info(f"Response Status: {response.status_code}")
            logger.info(f"Response Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Response: {json.dumps(result, indent=2)}")
                
                device_id = result.get("device_id")
                if device_id:
                    self.config["device_id"] = device_id
                    logger.info(f"✓ Registration successful: {device_id}")
                    return True
                else:
                    logger.error("✗ Registration response missing device_id")
                    return False
            else:
                logger.error(f"✗ Registration failed: {response.status_code} {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"✗ Registration error: {e}")
            return False
    
    def test_heartbeat(self) -> Optional[Dict[str, Any]]:
        """Test heartbeat sending"""
        logger.info("Testing heartbeat...")
        
        if not self.config.get("device_id"):
            logger.error("No device_id available for heartbeat")
            return None
        
        system_info = self.get_system_info()
        heartbeat_data = {
            "status": "online",
            "timestamp": system_info["timestamp"],
            "battery_percent": system_info.get("battery_percent"),
            "system_info": system_info
        }
        
        try:
            device_id = self.config["device_id"]
            url = f"{self.config['server_url']}/api/devices/{device_id}/heartbeat"
            
            logger.info(f"POST {url}")
            logger.info(f"Data: {json.dumps(heartbeat_data, indent=2)}")
            
            response = self.session.post(url, json=heartbeat_data)
            
            logger.info(f"Response Status: {response.status_code}")
            
            if response.status_code == 200:
                logger.info("✓ Heartbeat sent successfully")
                
                # Try to get config
                config_url = f"{self.config['server_url']}/api/devices/{device_id}/config"
                logger.info(f"GET {config_url}")
                
                config_response = self.session.get(config_url)
                logger.info(f"Config Response Status: {config_response.status_code}")
                
                if config_response.status_code == 200:
                    config_data = config_response.json()
                    logger.info(f"✓ Config retrieved: {json.dumps(config_data, indent=2)}")
                    return config_data
                else:
                    logger.warning(f"Config retrieval failed: {config_response.status_code} {config_response.text}")
                    return None
            else:
                logger.error(f"✗ Heartbeat failed: {response.status_code} {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"✗ Heartbeat error: {e}")
            return None
    
    def test_power_config(self, config: Dict[str, Any]):
        """Test power configuration application (dry run)"""
        logger.info("Testing power configuration...")
        
        try:
            power_config = config.get("config", {})
            logger.info(f"Power config: {json.dumps(power_config, indent=2)}")
            
            # Simulate power config application
            lid_action = power_config.get("lid_close_action", "do_nothing")
            sleep_timeout = power_config.get("sleep_timeout_ac", 0)
            hibernate = power_config.get("hibernate", False)
            
            logger.info(f"✓ Would set lid close action to: {lid_action}")
            logger.info(f"✓ Would set AC sleep timeout to: {sleep_timeout} minutes")
            logger.info(f"✓ Would {'enable' if hibernate else 'disable'} hibernate")
            
            # On Windows, could actually test powercfg commands here
            if sys.platform == "win32":
                logger.info("Note: On Windows, would execute powercfg commands")
            
            return True
        except Exception as e:
            logger.error(f"✗ Power config error: {e}")
            return False
    
    def run_full_test(self):
        """Run complete test suite"""
        logger.info("=" * 50)
        logger.info("FactoryLM Edge Agent Test Suite")
        logger.info("=" * 50)
        
        # Display configuration
        logger.info(f"Server URL: {self.config['server_url']}")
        logger.info(f"Device ID: {self.config['device_id']}")
        logger.info(f"Hostname: {self.config['hostname']}")
        logger.info("")
        
        # Test system info collection
        logger.info("Testing system info collection...")
        system_info = self.get_system_info()
        logger.info(f"✓ System info: {json.dumps(system_info, indent=2)}")
        logger.info("")
        
        # Test registration
        registration_success = self.test_registration()
        logger.info("")
        
        if not registration_success:
            logger.error("Registration failed, skipping remaining tests")
            return False
        
        # Test heartbeat
        config_data = self.test_heartbeat()
        logger.info("")
        
        # Test config application
        if config_data:
            self.test_power_config(config_data)
        else:
            logger.warning("No config data received, skipping power config test")
        
        logger.info("")
        logger.info("=" * 50)
        logger.info("Test Complete")
        logger.info("=" * 50)
        
        return True
    
    def run_continuous_test(self, duration_minutes=5):
        """Run continuous heartbeat test"""
        logger.info(f"Running continuous test for {duration_minutes} minutes...")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        iteration = 0
        
        while time.time() < end_time:
            iteration += 1
            logger.info(f"--- Iteration {iteration} ---")
            
            config_data = self.test_heartbeat()
            if config_data:
                self.test_power_config(config_data)
            
            logger.info(f"Waiting {self.config['heartbeat_interval']} seconds...")
            time.sleep(self.config['heartbeat_interval'])
        
        logger.info("Continuous test completed")


def main():
    """Main test entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test FactoryLM Edge Agent")
    parser.add_argument("--config", default="config.json", help="Config file path")
    parser.add_argument("--continuous", type=int, help="Run continuous test for N minutes")
    parser.add_argument("--server-url", help="Override server URL")
    
    args = parser.parse_args()
    
    # Create tester
    tester = EdgeAgentTester(args.config)
    
    # Override server URL if provided
    if args.server_url:
        tester.config["server_url"] = args.server_url
        logger.info(f"Using server URL: {args.server_url}")
    
    # Run tests
    if args.continuous:
        if not tester.test_registration():
            logger.error("Registration failed, cannot run continuous test")
            return 1
        tester.run_continuous_test(args.continuous)
    else:
        success = tester.run_full_test()
        return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())