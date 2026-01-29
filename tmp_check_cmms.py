import requests
import json

BASE = "http://localhost:8080"

# First authenticate
with open("/opt/plc-copilot/.env") as f:
    env = {}
    for line in f:
        if "=" in line and not line.startswith("#"):
            k, v = line.strip().split("=", 1)
            env[k] = v

# Try to find CMMS credentials
print("ENV keys:", list(env.keys()))

# Try default auth
try:
    r = requests.post(f"{BASE}/auth/signin", json={
        "email": env.get("CMMS_EMAIL", "admin@factorylm.com"),
        "password": env.get("CMMS_PASSWORD", "")
    }, timeout=5)
    print(f"Auth: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        token = data.get("token") or data.get("access_token") or data.get("id_token")
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        
        # Get work orders
        for endpoint in ["/work-orders", "/workorders", "/api/work-orders", "/api/workorders"]:
            try:
                r2 = requests.get(f"{BASE}{endpoint}", headers=headers, timeout=5)
                if r2.status_code == 200:
                    wos = r2.json()
                    print(f"\n{endpoint}: {len(wos) if isinstance(wos, list) else 'dict'} results")
                    if isinstance(wos, list):
                        for wo in wos[-5:]:
                            print(json.dumps(wo, indent=2, default=str)[:500])
                    else:
                        print(json.dumps(wos, indent=2, default=str)[:1000])
                    break
                else:
                    print(f"{endpoint}: {r2.status_code}")
            except Exception as e:
                print(f"{endpoint}: {e}")
    else:
        print(f"Auth failed: {r.text[:200]}")
except Exception as e:
    print(f"Auth error: {e}")

# Also try without auth
print("\n=== Trying without auth ===")
for endpoint in ["/work-orders", "/workorders", "/api/work-orders"]:
    try:
        r = requests.get(f"{BASE}{endpoint}", timeout=5)
        print(f"{endpoint}: {r.status_code} - {r.text[:200]}")
    except Exception as e:
        print(f"{endpoint}: {e}")
