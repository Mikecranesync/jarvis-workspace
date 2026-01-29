import json

with open("/root/.clawdbot/clawdbot.json") as f:
    cfg = json.load(f)

tg = cfg["channels"]["telegram"]
for key in ["token", "chatId"]:
    if key in tg:
        del tg[key]
        print(f"Removed {key}")

with open("/root/.clawdbot/clawdbot.json", "w") as f:
    json.dump(cfg, f, indent=2)

print("Config cleaned")
print("botToken:", tg.get("botToken", "NOT SET")[:20] + "...")
