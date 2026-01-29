import json

with open("/root/.clawdbot/clawdbot.json") as f:
    cfg = json.load(f)

cfg["channels"]["telegram"]["botToken"] = "7926253676:AAHBUkpQoM04Itl7Uh_Ge1Au9LSg0Fp9ttk"

with open("/root/.clawdbot/clawdbot.json", "w") as f:
    json.dump(cfg, f, indent=2)

print("botToken updated")
