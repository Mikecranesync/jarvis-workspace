# Trello API Setup & Troubleshooting

## Configuration

**Board:** ⚡ FactoryLM Command Center  
**Board ID:** `69792944285b43a963e9b858`  
**URL:** https://trello.com/b/3lxABXX4

### Environment Variables
```bash
TRELLO_API_KEY=55029ab0628e6d7ddc1d15bfbe73222f
TRELLO_TOKEN=ATTA21c913...  # Full token in environment
```

### List IDs
| List | ID |
|------|-----|
| 📥 Inbox | `69792946ed623aff9c3288ec` |
| 📋 Backlog | `697929460bc411801260b8f3` |
| 🏗️ In Progress | `697929459d88b2e1f87aceeb` |
| 👀 Review | `6979294559653c80b8f88837` |
| ✅ Done | `6979294563c650cad02d8f08` |
| 📦 Shipped | `697929455129a02ee8f3483c` |
| 🔬 Research | `69792946726ee75fbdaa8bc8` |

## Known Issues & Solutions

### Issue: jq parse errors on cards endpoint
**Symptom:** `jq: parse error: Invalid string: control characters`  
**Cause:** Trello card descriptions can contain control characters (newlines, etc.) that jq can't handle  
**Solution:** Use Python instead of jq for parsing:

```python
import urllib.request
import json
import os

api_key = os.environ.get('TRELLO_API_KEY')
token = os.environ.get('TRELLO_TOKEN')
board_id = '69792944285b43a963e9b858'

url = f'https://api.trello.com/1/boards/{board_id}/cards?key={api_key}&token={token}'

with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode('utf-8'))
    
for card in data:
    print(card['name'])
```

### Issue: API returns "invalid token"
**Solution:** Generate new token at https://trello.com/app-key

## Agile Agent Usage

The Agile Agent cron job should use Python for reliable parsing:
1. Fetch cards from board
2. Filter by list (Backlog, Inbox)
3. Find @jarvis mentions
4. Execute tasks following Engineering Commandments

---
*Last updated: 2026-01-29*
*Fixed by: Jarvis (Issue #9)*
