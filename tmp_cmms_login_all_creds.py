import requests
import json

BASE = "http://localhost:8080"

# Try all credential sets and both types
creds_to_try = [
    {"email": "mike@cranesync.com", "password": "CraneSync2026!", "type": "user"},
    {"email": "mike@cranesync.com", "password": "CraneSync2026!", "type": "admin"},
    {"email": "mike@cranesync.com", "password": "Benjamin@2014", "type": "user"},
    {"email": "mike@cranesync.com", "password": "Benjamin@2014", "type": "admin"},
    {"email": "mike@cranesync.com", "password": "bo1ws2er12", "type": "user"},
    {"email": "mike@cranesync.com", "password": "bo1ws2er12", "type": "admin"},
]

for cred in creds_to_try:
    print(f"\nTrying {cred['email']} / {cred['password'][:4]}... with type: {cred['type']}")
    try:
        r = requests.post(f"{BASE}/auth/signin", json=cred, timeout=10)
        print(f"  Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            token = data.get("token") or data.get("access_token") or data.get("id_token")
            if not token:
                token = data.get("data", {}).get("token") if isinstance(data.get("data"), dict) else None
            
            if token:
                headers = {"Authorization": f"Bearer {token}"}
                print(f"  Token: {token[:20]}...")
                
                # Try various work order endpoints
                endpoints = [
                    "/work-orders", "/workorders", "/api/work-orders",
                    "/work-orders?page=0&size=50",
                    "/workOrders"
                ]
                for ep in endpoints:
                    try:
                        r2 = requests.get(f"{BASE}{ep}", headers=headers, timeout=10)
                        if r2.status_code == 200:
                            result = r2.json()
                            print(f"\n  === {ep}: SUCCESS ===")
                            if isinstance(result, list):
                                print(f"  Total work orders: {len(result)}")
                                for wo in result:
                                    print(f"\n  --- Work Order ---")
                                    print(json.dumps(wo, indent=2, default=str)[:800])
                            elif isinstance(result, dict):
                                content = result.get("content", result)
                                if isinstance(content, list):
                                    print(f"  Total: {len(content)}")
                                    for wo in content:
                                        print(f"\n  --- Work Order ---")
                                        print(json.dumps(wo, indent=2, default=str)[:800])
                                else:
                                    print(json.dumps(result, indent=2, default=str)[:2000])
                            break
                        else:
                            print(f"  {ep}: {r2.status_code}")
                    except Exception as e:
                        print(f"  {ep}: {e}")
            break
        else:
            print(f"  Failed: {r.text[:300]}")
    except Exception as e:
        print(f"  Error: {e}")
