# FactoryLM Website Skill

## What This Does
Edit and deploy the FactoryLM marketing website from Telegram commands.

## Quick Reference

**Repo:** `https://github.com/Mikecranesync/factorylm-landing`
**Local:** `/root/jarvis-workspace/landing-page/`
**Live URL:** `https://factorylm.com`
**Hosting:** Unknown (IP 72.60.175.144) - needs investigation

## Workflow

### 1. Pull Latest
```bash
cd /root/jarvis-workspace/landing-page
git pull origin main
```

### 2. Make Edits
- Main page: `index.html`
- Blog posts: `blog/posts/*.html`
- Use `sed` for bulk find/replace
- Use direct file edits for specific changes

### 3. Commit & Push
```bash
git add -A
git commit -m "Description of change"
git push origin main
```

### 4. Verify Deployment
```bash
# Wait 30-60 seconds for deploy, then:
curl -s https://factorylm.com | grep "changed text"
```

## File Structure
```
/root/jarvis-workspace/landing-page/
├── index.html          # Main landing page
├── blog/
│   ├── index.html      # Blog listing
│   └── posts/          # Individual blog posts
│       ├── vfd-error-codes.html
│       ├── plc-programming-best-practices.html
│       └── ... (10 total)
└── .git/
```

## Common Edits

### Change Contact Email
```bash
sed -i 's/old@email.com/new@email.com/g' index.html
```

### Change Calendly Link
```bash
sed -i 's|calendly.com/old-link|calendly.com/new-link|g' index.html
```

### Update Blog Author
```bash
find blog -name "*.html" -exec sed -i 's/By Old Author/By New Author/g' {} \;
```

### Add/Edit Testimonial
Edit the testimonial section in `index.html` directly.

## Deployment (LOCKED IN ✅)

**Host:** Hostinger (72.60.175.144, Boston MA)
**SSH Key:** `~/.ssh/vps_deploy_key`
**Web Root:** `/var/www/factorylm/`

### Deploy Command (one-liner):
```bash
scp -i ~/.ssh/vps_deploy_key /root/jarvis-workspace/landing-page/index.html root@72.60.175.144:/var/www/factorylm/ && scp -i ~/.ssh/vps_deploy_key -r /root/jarvis-workspace/landing-page/blog root@72.60.175.144:/var/www/factorylm/
```

### Full Zero-Shot Process:
1. Edit files in `/root/jarvis-workspace/landing-page/`
2. `git add -A && git commit -m "message" && git push`
3. Deploy: `scp -i ~/.ssh/vps_deploy_key /root/jarvis-workspace/landing-page/* root@72.60.175.144:/var/www/factorylm/`
4. Verify: `curl -s https://factorylm.com | grep "changed text"`

## Trigger Phrases
When Mike says any of:
- "edit the website"
- "update factorylm.com"
- "change the landing page"
- "scrub the site"
- "update the marketing site"

→ Use this skill.
