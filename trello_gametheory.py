import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import urllib.request, urllib.parse, json

KEY='55029ab0628e6d7ddc1d15bfbe73222f'
TOKEN='ATTA21c9138e8d7ddbdde41f94a969cdab79ec966d5875f4f4b286cdd14d2c7083bb6510E2EF'

with open('C:/Users/hharp/clawd/trello_board.json') as f:
    cfg = json.load(f)

inbox_list = cfg['lists']['\U0001f4e5 Inbox']

desc = """Game Theory Engine — Mike's Personal Strategic Advisor

**What:** Brain dump life situations during commute → Jarvis analyzes through game theory → returns optimal moves

**How it works:**
- Mike texts/voice dumps during 1hr commute (each way)
- Jarvis identifies: Players, Strategies, Payoffs, Nash Equilibria
- Returns: The Game → Analysis → Optimal Move → Next Action
- Tracks ongoing "games" in ACTIVE_GAMES.md

**Frameworks:** Nash Equilibrium, Dominant Strategy, Prisoner's Dilemma, Signaling, Coalition Building, Second-Order Thinking, Minimax, Option Value

**Domains:** Workplace politics, business strategy, family planning, negotiations, career moves

**Status:** Framework built. Ready for brain dumps."""

data = urllib.parse.urlencode({
    'idList': inbox_list,
    'name': '\u265f\ufe0f Game Theory Engine — Personal Strategic Advisor',
    'desc': desc,
    'key': KEY,
    'token': TOKEN
}).encode()

req = urllib.request.Request('https://api.trello.com/1/cards', data=data, method='POST')
r = urllib.request.urlopen(req)
card = json.loads(r.read())
print(f"Card created: {card['shortUrl']}")
