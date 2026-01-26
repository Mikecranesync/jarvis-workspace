# 🚀 FactoryLM Launch Checklist

## Pre-Launch (Do This First)

### 1. Get API Keys
- [ ] **GROQ API Key**: https://console.groq.com/keys (free tier available)
- [ ] **Formspree**: https://formspree.io/register (for waitlist form)

### 2. Set Up Email Capture
- [ ] Create Formspree form
- [ ] Copy form ID
- [ ] Update `factorylm-landing/index.html` - replace `YOUR_FORM_ID`

### 3. Deploy Landing Page
```bash
cd projects/factorylm-landing
npx vercel --prod
```
- [ ] Connect custom domain: `factorylm.com`
- [ ] Verify SSL is working

### 4. Deploy Backend (Optional for MVP)
```bash
cd projects/factorylm-plc-client
npm i -g @railway/cli
railway login
railway init
railway variables set LLM_API_KEY=your-key
railway up
```
- [ ] Note the Railway URL
- [ ] Set up `api.factorylm.com` subdomain (optional)

### 5. Test Everything
- [ ] Landing page loads at factorylm.com
- [ ] Waitlist form submits (check Formspree dashboard)
- [ ] All links work
- [ ] Mobile looks good

---

## Launch Day

### Morning (Deploy)
- [ ] Final check of landing page
- [ ] Make sure Formspree is receiving submissions
- [ ] Have a few friends test the form

### Post Time (Best: Tue-Thu, 7-8 AM or 12 PM)

#### LinkedIn (Primary)
- [ ] Post from `LAUNCH_POST.md` (Option 1 recommended)
- [ ] Add 3-4 relevant hashtags
- [ ] Wait 30 min, then add first comment to boost
- [ ] Respond to all comments within first 2 hours

#### Twitter/X
- [ ] Post thread from `SOCIAL_POSTS.md`
- [ ] Pin the first tweet
- [ ] Engage with replies

#### Reddit (Space these out)
- [ ] r/PLC - Day 1
- [ ] r/automation - Day 2
- [ ] r/industrialautomation - Day 3

### Track Results
- [ ] Set up Google Analytics or Plausible on landing page
- [ ] Check Formspree for signups
- [ ] Note which channel drives most traffic

---

## Post-Launch

### Day 1-3
- [ ] Reply to ALL comments and messages
- [ ] Thank everyone who shared
- [ ] Note feature requests

### Week 1
- [ ] Send welcome email to waitlist (even if manual)
- [ ] Share any traction updates ("100 signups in 48 hours!")
- [ ] Start building most-requested features

### Week 2+
- [ ] Reach out to 5 most engaged commenters for user interviews
- [ ] Consider early access for top prospects
- [ ] Start building case studies

---

## Domains & Accounts to Set Up

| Service | URL | Purpose |
|---------|-----|---------|
| Vercel | vercel.com | Hosting |
| Railway | railway.app | Backend |
| Formspree | formspree.io | Email capture |
| GROQ | console.groq.com | LLM API |
| Namecheap/GoDaddy | - | Domain DNS |
| Plausible/GA | - | Analytics |

---

## Quick Commands

```bash
# Deploy landing page
cd projects/factorylm-landing && npx vercel --prod

# Deploy backend
cd projects/factorylm-plc-client && railway up

# Build frontend
cd projects/factorylm-plc-client/frontend && npm run build

# Run locally
cd projects/factorylm-plc-client
python -m uvicorn backend.main:app --reload --port 8000 &
cd frontend && npm run dev
```

---

## Support

Questions? Issues?
- GitHub Issues: github.com/Mikecranesync/factorylm-plc-client/issues
- Email: [your email]

**Ship it! 🚀**
