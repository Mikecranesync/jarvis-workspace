import json

with open("/root/.clawdbot/clawdbot.json") as f:
    cfg = json.load(f)

tg = cfg["channels"]["telegram"]
print(json.dumps(tg, indent=2))
