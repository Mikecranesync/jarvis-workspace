import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import urllib.request, urllib.parse, json

KEY='55029ab0628e6d7ddc1d15bfbe73222f'
TOKEN='ATTA21c9138e8d7ddbdde41f94a969cdab79ec966d5875f4f4b286cdd14d2c7083bb6510E2EF'

# Get a card
r = urllib.request.urlopen(f'https://api.trello.com/1/boards/69792944285b43a963e9b858/cards?key={KEY}&token={TOKEN}&fields=name,shortLink')
cards = json.loads(r.read())
card = cards[1]  # Use second card for variety
print(f"Card: {card['name']}")

# Post @jarvis comment via Trello API (this should trigger the webhook)
data = urllib.parse.urlencode({
    'text': '@jarvis real webhook test - this should arrive in Telegram!',
    'key': KEY,
    'token': TOKEN
}).encode()
req = urllib.request.Request(f'https://api.trello.com/1/cards/{card["id"]}/actions/comments', data=data, method='POST')
r = urllib.request.urlopen(req)
result = json.loads(r.read())
print(f"Comment posted: {result['id']}")
print("Waiting for Trello webhook to fire...")
