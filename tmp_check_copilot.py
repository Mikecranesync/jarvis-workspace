import sqlite3
import os

# Check the bot's conversation/data
db = sqlite3.connect("/opt/plc-copilot/users.db")
cur = db.cursor()

# List tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print("Tables:", tables)

for t in tables:
    cur.execute(f"SELECT COUNT(*) FROM {t}")
    print(f"  {t}: {cur.fetchone()[0]} rows")

# Check telegram_usage for recent messages
cur.execute("SELECT * FROM telegram_usage ORDER BY rowid DESC LIMIT 10")
cols = [d[0] for d in cur.description]
print(f"\nRecent telegram_usage ({', '.join(cols)}):")
for row in cur.fetchall():
    print(f"  {row}")

db.close()

# Check if there's a separate case study file or KB entry
print("\n=== Checking for case study files ===")
for root, dirs, files in os.walk("/opt/plc-copilot"):
    for f in files:
        path = os.path.join(root, f)
        mtime = os.path.getmtime(path)
        # Files modified in last hour
        if mtime > __import__('time').time() - 3600:
            print(f"  Recently modified: {path} ({os.path.getsize(path)} bytes)")

# Check KB for case studies
kb_db = sqlite3.connect("/opt/plc-copilot/kb_harvester/kb_industrial.db")
kc = kb_db.cursor()
kc.execute("SELECT id, title, created_at FROM kb_articles ORDER BY id DESC LIMIT 10")
print("\nLatest KB articles:")
for row in kc.fetchall():
    print(f"  {row}")

# Search for case study content
kc.execute("SELECT id, title, content FROM kb_articles WHERE title LIKE '%case%' OR content LIKE '%case study%'")
case_studies = kc.fetchall()
print(f"\nCase study articles found: {len(case_studies)}")
for cs in case_studies:
    print(f"  [{cs[0]}] {cs[1]}")
    print(f"    {cs[2][:200]}...")

kb_db.close()
