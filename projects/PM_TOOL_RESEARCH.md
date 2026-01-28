# Project Management Tool Research
### For Solo Founder + AI Assistant (Clawdbot/Jarvis) Workflow
*Researched: 2026-01-27*

---

## Current State
Using `KANBAN.md` — functional but ugly, no mobile UX, no visual board.

## Requirements
- ✅ Beautiful visual interface (mobile + desktop)
- ✅ Full API access for AI (create/update/move/comment programmatically)
- ✅ Free or cheap for a solo founder
- ✅ Multiple project boards (RideView, Rivet-PRO/Maint-NPC, FactoryLM)
- ✅ Shareable with collaborators/investors later
- ✅ Attachments, due dates, labels, checklists

---

## Comparison Table

| Feature | **Trello** | **Linear** | **Notion** | **GitHub Projects** | **Plane.so** | **Vikunja** | **Todoist** |
|---|---|---|---|---|---|---|---|
| **Free Tier** | ✅ Unlimited cards, 10 boards | ✅ 250 issues, 2 teams | ✅ Unlimited pages (solo) | ✅ Unlimited (with GitHub) | ✅ Up to 12 seats | ✅ Self-host free | ✅ 5 projects |
| **API Quality** | ⭐⭐⭐⭐⭐ REST, mature | ⭐⭐⭐⭐⭐ GraphQL + MCP | ⭐⭐⭐⭐ REST, verbose | ⭐⭐⭐⭐ GraphQL + gh CLI | ⭐⭐⭐⭐ REST, well-documented | ⭐⭐⭐ REST | ⭐⭐⭐⭐ REST |
| **Mobile App** | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐⭐ Beautiful | ⭐⭐⭐⭐ Good but heavy | ⭐⭐⭐ Usable, not great | ⭐⭐⭐ Web-based | ⭐⭐ PWA only | ⭐⭐⭐⭐⭐ Excellent |
| **Visual Appeal** | ⭐⭐⭐⭐ Clean kanban | ⭐⭐⭐⭐⭐ Stunning | ⭐⭐⭐⭐ Flexible | ⭐⭐⭐ Functional | ⭐⭐⭐⭐ Modern | ⭐⭐⭐ Basic | ⭐⭐⭐⭐ Clean |
| **Clawdbot Skill** | ✅ **EXISTS** | ❌ Build needed | ✅ **EXISTS** | ⚡ Via `gh` CLI | ❌ Build needed | ❌ Build needed | ❌ Build needed |
| **AI Full Control** | ✅ Create/move/comment/label | ✅ Full CRUD | ✅ Full CRUD | ✅ Via API/CLI | ✅ Full CRUD | ✅ Full CRUD | ✅ Full CRUD |
| **Self-Hosted** | ❌ | ❌ | ❌ | ❌ | ✅ VPS deploy | ✅ VPS deploy | ❌ |
| **Kanban Board** | ✅ Native | ✅ Native | ✅ Database view | ✅ Board layout | ✅ Native | ✅ View option | ⚠️ Board layout limited |
| **Checklists** | ✅ | ✅ Sub-issues | ✅ Toggle blocks | ✅ Task lists | ✅ Sub-issues | ✅ | ✅ Sub-tasks |
| **Attachments** | ✅ | ✅ (10MB free) | ✅ (5MB free) | ✅ | ✅ | ✅ | ⚠️ 5MB free |
| **Due Dates** | ✅ | ✅ | ✅ | ✅ Custom fields | ✅ | ✅ | ✅ |
| **Labels/Tags** | ✅ | ✅ | ✅ Multi-select | ✅ | ✅ | ✅ | ✅ |
| **Investor-Ready** | ✅ Share board link | ✅ Guest access | ✅ Public page | ⚠️ GitHub-centric | ✅ Guest access | ⚠️ Self-host only | ⚠️ Limited sharing |

---

## Detailed Analysis

### 1. 📋 Trello — ⭐ RECOMMENDED WINNER
**Free tier:** Unlimited cards, up to 10 collaborators per workspace, unlimited Power-Ups, unlimited boards (was limited, now generous). Mobile + desktop apps.

**API:** Mature REST API with full CRUD on boards, lists, cards, comments, labels, checklists, attachments. Rate limits: 300 req/10s per API key, 100 req/10s per token. Very well documented at developer.atlassian.com.

**Clawdbot Integration: ✅ SKILL ALREADY EXISTS** at `clawdbot/skills/trello/SKILL.md`. Just needs `TRELLO_API_KEY` and `TRELLO_TOKEN` env vars. All operations ready: list boards, create cards, move cards, add comments, archive cards.

**Pros:**
- Skill already built — zero development effort
- Best-in-class mobile app (iOS + Android)
- Instantly recognizable to investors/collaborators
- Drag-and-drop kanban is the gold standard
- Free tier is generous for solo use
- Power-Ups for calendar view, custom fields, etc.

**Cons:**
- Free tier limited to 10 collaborators (fine for now)
- Owned by Atlassian (corporate overhead)
- 5MB file upload on free (10MB on Standard)
- No self-hosted option

---

### 2. 📝 Notion
**Free tier:** Unlimited pages/blocks for individual use, 5MB file uploads, 7 days page history, 10 guest seats. API included.

**API:** REST API, well-documented. Databases (now "data sources") support full CRUD. Can create kanban views via database properties. Rate limit ~3 req/sec.

**Clawdbot Integration: ✅ SKILL ALREADY EXISTS** at `clawdbot/skills/notion/SKILL.md`. Supports search, create pages, update properties, query databases, add blocks.

**Pros:**
- Skill already built — zero development effort
- Most flexible tool (wiki + kanban + docs all-in-one)
- Can build project pages alongside boards
- Beautiful public pages for investor sharing
- Great for documentation alongside tasks

**Cons:**
- Mobile app is heavy/slow for quick task checking
- Kanban is a database view, not a native board — less intuitive
- API is verbose (lots of JSON for simple operations)
- 5MB file limit on free tier
- Rate limit is tight (3 req/sec)
- "Swiss army knife" — might be overkill for pure task management

---

### 3. ⚡ Linear
**Free tier:** 250 issues, 2 teams, unlimited members, 10MB file uploads, API + webhook access, MCP access.

**API:** GraphQL API, very developer-focused. Also offers MCP (Model Context Protocol) access — could integrate with AI natively. Extremely well-designed.

**Pros:**
- Most beautiful UI of any PM tool, period
- Built for developers, feels fast and modern
- MCP support means native AI integration potential
- GraphQL API is powerful
- Great keyboard shortcuts

**Cons:**
- 250 issue limit on free tier (could hit this)
- No Clawdbot skill — needs building
- No self-hosted option
- GraphQL adds complexity vs REST
- 2 team limit on free (need 3 for RideView, Rivet-PRO, FactoryLM)
- **Free tier too restrictive for 3 projects**

---

### 4. 🐙 GitHub Projects
**Free tier:** Unlimited (comes with GitHub account). Table, board, and roadmap views.

**API:** GraphQL API + `gh` CLI already installed and authenticated.

**Pros:**
- Already have GitHub — zero new accounts
- Deep integration with issues, PRs, code
- `gh` CLI already authenticated on Mike's machine
- Free forever
- Good for developer-facing workflow

**Cons:**
- No Clawdbot skill (but `gh` CLI works)
- Mobile experience is mediocre (GitHub mobile app)
- Not visually impressive for investors
- Kanban board is functional but plain
- Tightly coupled to GitHub repos
- Not intuitive for non-developers

---

### 5. ✈️ Plane.so
**Free tier:** Up to 12 seats, projects, work items, cycles, modules, kanban views, intake, estimates, pages. API included.

**API:** REST API with API key auth. Well-documented at developers.plane.so. Full CRUD on workspaces, projects, work items.

**Pros:**
- Modern Linear-like UI but more generous free tier
- Self-hostable on VPS (open source core)
- Full API with clear docs
- Kanban + list + spreadsheet views
- Good free tier for solo founder

**Cons:**
- No Clawdbot skill — needs building
- Mobile app is web-based (PWA), not native
- Younger product, less mature ecosystem
- Self-hosting adds maintenance burden
- Smaller community than Trello/Notion

---

### 6. 🦊 Vikunja
**Free tier:** Completely free (self-hosted). Cloud option available.

**API:** REST API available but documentation is sparse.

**Pros:**
- Completely free, open source (AGPLv3)
- Self-hostable on VPS
- Kanban, list, Gantt, table views
- Fast (claims <100ms interactions)
- Lightweight single binary

**Cons:**
- No Clawdbot skill — needs building
- No native mobile app (PWA only)
- Sparse API documentation
- Small community
- Looks basic compared to Trello/Linear
- Not investor-presentable
- Would need maintenance on VPS

---

### 7. 📋 Focalboard / Mattermost
**Status:** Focalboard was acquired by Mattermost and is being sunset/merged into Mattermost Boards. The standalone version is no longer actively developed.

**Verdict:** ❌ **Skip** — dying product, uncertain future. Mattermost is overkill (full chat platform) for a solo founder.

---

### 8. ✅ Todoist
**Free tier:** 5 personal projects, 5 people per project, basic board layout, 5MB file uploads.

**API:** REST API v2, well-documented, good developer experience.

**Pros:**
- Best-in-class mobile app (fast, clean)
- Great natural language input
- Good API

**Cons:**
- Only 5 projects on free tier
- Board/kanban view is secondary to list view
- Not really a project management tool — it's a to-do app
- No Clawdbot skill
- Limited sharing/collaboration on free
- Not impressive for investors

---

## Decision Matrix (Weighted)

| Criteria (Weight) | Trello | Notion | Linear | GitHub Projects | Plane.so |
|---|---|---|---|---|---|
| **Existing Clawdbot Skill (30%)** | 10 | 10 | 0 | 5 | 0 |
| **Mobile Experience (20%)** | 10 | 6 | 9 | 4 | 5 |
| **Free Tier Adequacy (15%)** | 9 | 9 | 5 | 10 | 9 |
| **Visual Appeal (15%)** | 8 | 8 | 10 | 5 | 8 |
| **Investor/Sharing (10%)** | 9 | 9 | 8 | 4 | 7 |
| **API Quality (10%)** | 9 | 7 | 10 | 8 | 8 |
| **WEIGHTED SCORE** | **9.25** | **8.25** | **5.95** | **5.55** | **5.30** |

---

## 🏆 Final Recommendation: TRELLO

### Why Trello Wins

1. **Clawdbot skill already exists** — Jarvis can start managing boards TODAY with zero development. Just set two env vars (`TRELLO_API_KEY`, `TRELLO_TOKEN`) and go.

2. **Best mobile app** — Mike opens his phone, sees beautiful kanban boards for RideView, Rivet-PRO, and FactoryLM. Drag cards around. Quick and responsive.

3. **AI workflow is proven** — The existing skill supports every operation needed:
   - Create cards → Jarvis logs new tasks
   - Move cards between lists → Jarvis updates status
   - Add comments → Jarvis logs progress/decisions
   - Archive cards → Jarvis cleans up completed work
   - Labels → Jarvis categorizes by project/priority

4. **Investor-ready** — Everyone knows Trello. Share a board link and investors immediately understand your workflow. No explanation needed.

5. **Free tier is generous** — Unlimited cards, unlimited boards, unlimited Power-Ups. The 10-collaborator limit won't matter until the team grows.

### Suggested Setup

```
Workspace: "Mike's Projects"

Board: RideView
  Lists: Backlog → In Progress → Review → Done

Board: Rivet-PRO / Maint-NPC
  Lists: Backlog → In Progress → Testing → Done

Board: FactoryLM
  Lists: Ideas → Backlog → In Progress → Done

Labels (across boards):
  🔴 Urgent  🟡 Important  🟢 Nice-to-have
  🔵 Bug  🟣 Feature  ⚪ Docs/Admin
```

### Next Steps
1. `clawdbot configure` — add `TRELLO_API_KEY` and `TRELLO_TOKEN`
2. Create the three boards in Trello (via web or Jarvis can do it via API)
3. Migrate current KANBAN.md items to Trello cards
4. Set KANBAN.md to archived/reference status
5. Jarvis starts managing all tasks through Trello API

### Runner-Up: Notion
If Mike wants an all-in-one workspace (docs + wiki + tasks + project pages), Notion is the runner-up. The Clawdbot skill exists, and it's more flexible than Trello. But for pure kanban project management with the best mobile experience, Trello wins.

---

*Research complete. Ready to set up Trello whenever Mike gives the green light.* 🚀
