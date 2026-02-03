#!/usr/bin/env python3
"""
BALENA CLOUD SETUP
==================
Programmatic setup for Raspberry Pi fleet management

Usage:
1. Get API token from https://dashboard.balena-cloud.com/preferences/access-tokens
2. Run: python3 setup.py --token YOUR_TOKEN
"""

import os
import sys
import json
import requests
import argparse

BALENA_API = "https://api.balena-cloud.com/v7"

class BalenaClient:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def whoami(self):
        """Get current user info"""
        r = requests.get(f"{BALENA_API}/user/v1/whoami", headers=self.headers)
        return r.json() if r.status_code == 200 else {"error": r.text}
    
    def get_organizations(self):
        """List organizations"""
        r = requests.get(f"{BALENA_API}/organization", headers=self.headers)
        return r.json().get('d', []) if r.status_code == 200 else []
    
    def get_device_types(self, name_filter: str = "raspberry"):
        """List device types"""
        r = requests.get(
            f"{BALENA_API}/device_type",
            headers=self.headers,
            params={"$filter": f"contains(slug,'{name_filter}')"}
        )
        return r.json().get('d', []) if r.status_code == 200 else []
    
    def create_fleet(self, name: str, org_id: int, device_type_id: int):
        """Create a new fleet/application"""
        r = requests.post(
            f"{BALENA_API}/application",
            headers=self.headers,
            json={
                "app_name": name,
                "organization": org_id,
                "is_for__device_type": device_type_id
            }
        )
        return r.json() if r.status_code in [200, 201] else {"error": r.text, "status": r.status_code}
    
    def get_fleets(self):
        """List all fleets"""
        r = requests.get(f"{BALENA_API}/application", headers=self.headers)
        return r.json().get('d', []) if r.status_code == 200 else []
    
    def register_device(self, fleet_id: int, uuid: str):
        """Register a new device to a fleet"""
        r = requests.post(
            f"{BALENA_API}/device",
            headers=self.headers,
            json={
                "belongs_to__application": fleet_id,
                "uuid": uuid
            }
        )
        return r.json() if r.status_code in [200, 201] else {"error": r.text}
    
    def get_devices(self, fleet_id: int = None):
        """List devices"""
        url = f"{BALENA_API}/device"
        if fleet_id:
            url += f"?$filter=belongs_to__application eq {fleet_id}"
        r = requests.get(url, headers=self.headers)
        return r.json().get('d', []) if r.status_code == 200 else []
    
    def download_os_image(self, fleet_id: int, version: str = "latest"):
        """Get download URL for balenaOS image"""
        # This requires balena CLI, API doesn't directly provide download
        return {
            "note": "Use balena CLI to download image",
            "command": f"balena os download raspberrypi4-64 -o balena.img --version {version}"
        }


def main():
    parser = argparse.ArgumentParser(description="Balena Cloud Setup")
    parser.add_argument("--token", help="Balena API token")
    parser.add_argument("--action", default="status", 
                       choices=["status", "create-fleet", "list-devices", "setup"])
    parser.add_argument("--fleet-name", default="jarvis-pi-fleet")
    args = parser.parse_args()
    
    # Get token from arg or env
    token = args.token or os.getenv("BALENA_API_TOKEN")
    
    if not token:
        print("❌ No Balena API token provided")
        print("\nGet one from: https://dashboard.balena-cloud.com/preferences/access-tokens")
        print("\nThen run: python3 setup.py --token YOUR_TOKEN")
        sys.exit(1)
    
    client = BalenaClient(token)
    
    if args.action == "status":
        print("=== Balena Account ===")
        user = client.whoami()
        print(f"User: {user}")
        
        print("\n=== Organizations ===")
        orgs = client.get_organizations()
        for org in orgs:
            print(f"  - {org.get('name')} (ID: {org.get('id')})")
        
        print("\n=== Fleets ===")
        fleets = client.get_fleets()
        for fleet in fleets:
            print(f"  - {fleet.get('app_name')} (ID: {fleet.get('id')})")
        
        print("\n=== Raspberry Pi Device Types ===")
        types = client.get_device_types("raspberrypi")
        for dt in types[:5]:
            print(f"  - {dt.get('slug')} (ID: {dt.get('id')})")
    
    elif args.action == "create-fleet":
        orgs = client.get_organizations()
        if not orgs:
            print("❌ No organizations found")
            sys.exit(1)
        
        org_id = orgs[0]['id']
        
        # Get Raspberry Pi 4 device type
        types = client.get_device_types("raspberrypi4-64")
        if not types:
            print("❌ Raspberry Pi 4 device type not found")
            sys.exit(1)
        
        device_type_id = types[0]['id']
        
        print(f"Creating fleet '{args.fleet_name}'...")
        result = client.create_fleet(args.fleet_name, org_id, device_type_id)
        print(json.dumps(result, indent=2))
    
    elif args.action == "list-devices":
        devices = client.get_devices()
        print(f"=== Devices ({len(devices)}) ===")
        for d in devices:
            print(f"  - {d.get('device_name', 'unnamed')} ({d.get('uuid', '')[:8]}...) - {d.get('status')}")


if __name__ == "__main__":
    main()
