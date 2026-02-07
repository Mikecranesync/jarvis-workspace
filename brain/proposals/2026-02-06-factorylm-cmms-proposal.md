# PROPOSAL: FactoryLM CMMS
**Date:** 2026-02-06
**Status:** DRAFT - Awaiting Mike's Approval
**Priority:** High

---

## EXECUTIVE SUMMARY

Build a custom CMMS that looks like Atlas but is **simpler, faster, and Telegram-native**. No more auth bugs. No more fighting upstream code.

---

## ATLAS CMMS TECH STACK (What We're Cloning)

### Frontend
| Component | Atlas Uses | Our Choice |
|-----------|-----------|------------|
| Framework | React 17 | **React 18** (latest) |
| UI Library | **MUI v5** (Material UI) | **MUI v5** (same look!) |
| State | Redux Toolkit | Redux Toolkit or Zustand |
| Styling | Emotion + MUI themes | Same |
| Icons | MUI Icons | Same |
| Data Grid | MUI X Data Grid Pro | MUI X Data Grid |
| Calendar | FullCalendar | FullCalendar |
| Charts | (various) | Recharts |

### Backend
| Component | Atlas Uses | Our Choice |
|-----------|-----------|------------|
| Framework | Spring Boot 3 (Java) | **FastAPI (Python)** ⚡ |
| Database | PostgreSQL | PostgreSQL |
| Auth | OAuth2/JWT | Simple JWT |
| File Storage | MinIO/S3 | MinIO or local |
| Email | SMTP/SendGrid | SMTP |

### Why FastAPI Instead of Spring Boot?
1. **I can maintain it** - Python is my native language
2. **Faster development** - 3x fewer lines of code
3. **Telegram integration** - Native Python, no bridging
4. **PLC Copilot integration** - Same stack, shared code

---

## ATLAS STYLING (Exact Colors)

### Primary Theme: "PureLightTheme"
```javascript
themeColors = {
  primary: '#5569ff',    // Blue-purple
  secondary: '#6E759F',  // Grey-purple  
  success: '#57CA22',    // Green
  warning: '#FFA319',    // Orange
  error: '#FF1943',      // Red
  info: '#33C2FF',       // Light blue
  black: '#223354',      // Dark blue-grey
  white: '#ffffff',
  bodyBg: '#f2f5f9'      // Light grey background
}
```

### Sidebar Design
- White background
- Blue-purple active items (#5569ff)
- Grey text (#6E759F)
- Light grey dividers (#f2f5f9)

### Gradients (For Cards/Headers)
- Blue: `linear-gradient(135deg, #6B73FF 0%, #000DFF 100%)`
- Success: `linear-gradient(135deg, #FFF720 0%, #3CD500 100%)`

---

## PROPOSED ARCHITECTURE

```
┌─────────────────────────────────────────────────────────┐
│                    FACTORYLM CMMS                       │
├─────────────────────────────────────────────────────────┤
│  FRONTEND (React + MUI v5)                              │
│  ├── Same Atlas styling/themes                          │
│  ├── Simpler component structure                        │
│  └── Mobile-first responsive                            │
├─────────────────────────────────────────────────────────┤
│  BACKEND (FastAPI + Python)                             │
│  ├── REST API (OpenAPI/Swagger)                         │
│  ├── PostgreSQL database                                │
│  ├── JWT auth (simple, no OAuth complexity)             │
│  └── Telegram bot integration (native)                  │
├─────────────────────────────────────────────────────────┤
│  INTEGRATIONS                                           │
│  ├── Telegram → Work orders via chat                    │
│  ├── PLC Copilot → Photo-to-ticket                      │
│  ├── Jarvis → AI-assisted maintenance                   │
│  └── Factory I/O → Digital twin status                  │
└─────────────────────────────────────────────────────────┘
```

---

## CORE FEATURES (MVP)

### Phase 1: Foundation (Week 1)
- [ ] User auth (JWT, simple login)
- [ ] Work order CRUD
- [ ] Asset/equipment registry
- [ ] Location hierarchy
- [ ] Basic dashboard

### Phase 2: Operations (Week 2)
- [ ] Work order assignment
- [ ] Status workflow (Open → In Progress → Complete)
- [ ] Photo attachments
- [ ] Parts/inventory tracking
- [ ] Preventive maintenance schedules

### Phase 3: Intelligence (Week 3)
- [ ] Telegram bot commands
- [ ] AI work order creation from photos
- [ ] Reporting/analytics
- [ ] Export (CSV, PDF)

---

## DEPLOYMENT

| Service | Host | Purpose |
|---------|------|---------|
| Frontend | Hetzner | React app (nginx) |
| Backend | Hetzner | FastAPI (uvicorn) |
| Database | Hetzner | PostgreSQL |
| Files | Hetzner | MinIO (S3-compatible) |

**Estimated resources:** 2GB RAM, 20GB disk

---

## TIMELINE

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| Design | 2 days | UI mockups, DB schema |
| Backend MVP | 3 days | API + auth + core models |
| Frontend MVP | 4 days | React app with Atlas styling |
| Integration | 2 days | Telegram + PLC Copilot |
| Testing | 2 days | Bug fixes, polish |
| **TOTAL** | **~2 weeks** | Production-ready CMMS |

---

## COST

| Item | Cost |
|------|------|
| Development | $0 (robot army) |
| Hosting (Hetzner) | ~$15/mo (already have) |
| Domain | $0 (use subdomain) |
| **Total** | **$0 upfront, $15/mo** |

---

## DECISION NEEDED

**Option A:** Start immediately (delays YC demo focus)
**Option B:** Queue for after Feb 9 demo deadline
**Option C:** Spike a quick prototype (1 day) to validate, then full build later

---

## ROBOT ARMY ASSIGNMENT

Once approved:
1. **Jarvis (Main)** - Project management, code review
2. **Hetzner Workers** - Backend API development
3. **Frontend Sub-agent** - React/MUI components
4. **Integration Agent** - Telegram + PLC Copilot hooks

---

*Awaiting your go/no-go, boss.* 🤖
