"""Register Trello webhook for the FactoryLM Command Center board."""
import urllib.request
import json

KEY = '55029ab0628e6d7ddc1d15bfbe73222f'
TOKEN = 'ATTA21c9138e8d7ddbdde41f94a969cdab79ec966d5875f4f4b286cdd14d2c7083bb6510E2EF'
BOARD_ID = '69792944285b43a963e9b858'
CALLBACK_URL = 'https://72-60-175-144.sslip.io/trello-webhook'

# List existing webhooks
req = urllib.request.Request(
    f'https://api.trello.com/1/tokens/{TOKEN}/webhooks?key={KEY}',
    method='GET'
)
try:
    r = urllib.request.urlopen(req)
    existing = json.loads(r.read())
    print(f"Existing webhooks: {len(existing)}")
    for wh in existing:
        print(f"  - {wh['id']}: {wh.get('description', '')} -> {wh.get('callbackURL', '')}")
except Exception as e:
    print(f"Error listing: {e}")

# Register new webhook
data = json.dumps({
    "description": "Jarvis @mention listener",
    "callbackURL": CALLBACK_URL,
    "idModel": BOARD_ID,
    "active": True
}).encode()

req = urllib.request.Request(
    f'https://api.trello.com/1/webhooks?key={KEY}&token={TOKEN}',
    data=data,
    method='POST',
    headers={"Content-Type": "application/json"}
)

try:
    r = urllib.request.urlopen(req)
    result = json.loads(r.read())
    print(f"\nWebhook registered!")
    print(f"   ID: {result['id']}")
    print(f"   Callback: {result['callbackURL']}")
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"\nFailed: {e.code} - {body}")
