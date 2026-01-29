import json

with open("/root/.clawdbot/clawdbot.json") as f:
    cfg = json.load(f)

cfg["channels"]["telegram"]["chatId"] = "8445149012"

with open("/root/.clawdbot/clawdbot.json", "w") as f:
    json.dump(cfg, f, indent=2)

print("Chat ID set to 8445149012")
