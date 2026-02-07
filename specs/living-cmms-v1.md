# Living CMMS - Architecture Specification v0.1

> **Vision:** A CMMS where every cell is alive, every user has their own AI slice, and the system proactively helps rather than waiting to be asked.

---

## 1. Core Concepts

### 1.1 The Living Cell

Every data entity in CMMS is a "living cell" - not just a database row.

```
┌─────────────────────────────────────────────────┐
│  ASSET CELL: VFD-001 (PowerFlex 525)            │
├─────────────────────────────────────────────────┤
│  Static Data:                                   │
│    - Model: 25B-D030N104                        │
│    - Serial: 12345ABC                           │
│    - Location: Line 4, Panel 3                  │
│    - Install Date: 2023-06-15                   │
│                                                 │
│  Living Connections:                            │
│    → Manufacturer Feed: rockwellautomation.com  │
│    → Firmware Watch: v7.002 (current v7.001)    │
│    → Similar Assets: 3 other PF525s in system   │
│    → Failure Patterns: 2 bearing faults in fleet│
│    → Manual: KB/manuals/pf525-user-guide.pdf    │
│                                                 │
│  Agent Tasks:                                   │
│    ⏰ Check firmware weekly                     │
│    ⏰ Scan for recalls monthly                  │
│    ⏰ Cross-reference industry failures daily   │
└─────────────────────────────────────────────────┘
```

### 1.2 User Slice (Sandboxed Context)

Each user gets an isolated "slice" of the system:

| Component | Isolated? | Shared? |
|-----------|-----------|---------|
| CMMS Data | ✅ Fully isolated | ❌ Never shared |
| Conversation History | ✅ Per-user | ❌ Never shared |
| Context Injection | ✅ Their assets only | ❌ Never shared |
| Base LLM Weights | ❌ | ✅ Shared model |
| KB (Public Manuals) | ❌ | ✅ Shared reference |

**Implementation:** 
- User ID → Tenant ID → All queries filtered
- Context window = System prompt + User's recent CMMS + User's conversation
- Zero data leakage between tenants

### 1.3 Proactive Intelligence

The system reaches out, not just responds.

**Trigger Types:**

| Trigger | Frequency | Example Message |
|---------|-----------|-----------------|
| Incomplete Entry | 4 hours after entry | "WO-1234 has no asset assigned. Is this for VFD-001 on Line 4?" |
| Firmware Update | Weekly scan | "PowerFlex 525 firmware v7.003 released. 3 units in your plant affected." |
| Pattern Detection | Daily | "3rd bearing fault on AHU motors this month. Consider vibration analysis?" |
| Stale Data | Weekly | "12 assets haven't been serviced in 180+ days. Review?" |
| New Manual | On discovery | "Found updated Micro820 programming manual. Added to your KB." |

**Anti-Spam Rules:**
- Max 3 proactive messages per day per user
- Minimum 2 hours between messages
- User can snooze for 24h/week/forever
- Priority queue: Urgent > Helpful > FYI

---

## 2. Architecture

### 2.1 System Components

```
┌─────────────────────────────────────────────────────────────┐
│                      USER DEVICES                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │ Telegram │  │ WhatsApp │  │ Web App  │                  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                  │
│       └─────────────┼─────────────┘                        │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              API GATEWAY (Auth + Routing)           │   │
│  │         Tenant isolation enforced here              │   │
│  └─────────────────────────────────────────────────────┘   │
│                     │                                       │
│       ┌─────────────┼─────────────┐                        │
│       ▼             ▼             ▼                        │
│  ┌─────────┐  ┌──────────┐  ┌──────────────┐              │
│  │ CMMS DB │  │ Vector   │  │ Message      │              │
│  │ (Tenant │  │ Store    │  │ Queue        │              │
│  │  Scoped)│  │ (RAG)    │  │ (Proactive)  │              │
│  └─────────┘  └──────────┘  └──────────────┘              │
│       │             │             │                        │
│       └─────────────┼─────────────┘                        │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              AGENT ORCHESTRATOR                      │   │
│  │  - Chat Agent (responds to user)                    │   │
│  │  - Scanner Agent (proactive discovery)              │   │
│  │  - Enrichment Agent (fetches manuals, firmware)     │   │
│  └─────────────────────────────────────────────────────┘   │
│                     │                                       │
│                     ▼                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              LLM LAYER                               │   │
│  │  ┌─────────────────────────────────────────────┐    │   │
│  │  │  Base Model: FactoryLLM (shared weights)    │    │   │
│  │  └─────────────────────────────────────────────┘    │   │
│  │                     +                                │   │
│  │  ┌─────────────────────────────────────────────┐    │   │
│  │  │  User Context: CMMS data + conversation     │    │   │
│  │  │  (injected at runtime, never persisted      │    │   │
│  │  │   in model weights)                         │    │   │
│  │  └─────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Data Flow: Proactive Message

```
1. SCHEDULER (every 4 hours per tenant)
   │
   ▼
2. SCANNER AGENT queries tenant's CMMS:
   "SELECT * FROM work_orders 
    WHERE asset_id IS NULL 
    AND created_at > NOW() - INTERVAL '24 hours'"
   │
   ▼
3. IF results found:
   │
   ▼
4. LLM generates suggestion:
   Context: [User's assets, recent WOs, preferences]
   Prompt: "Suggest asset matches for these orphan WOs"
   │
   ▼
5. JUDGE checks suggestion quality:
   - Is suggestion actionable?
   - Confidence > 70%?
   - Not duplicate of recent message?
   │
   ▼
6. MESSAGE QUEUE adds to user's outbound:
   Priority: HELPFUL
   Delay: Next allowed window
   │
   ▼
7. DELIVERY via user's preferred channel
```

### 2.3 Tenant Isolation Implementation

```python
# Every database query includes tenant filter
class TenantScopedQuery:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
    
    def assets(self):
        return Asset.query.filter_by(tenant_id=self.tenant_id)
    
    def work_orders(self):
        return WorkOrder.query.filter_by(tenant_id=self.tenant_id)

# Context injection for LLM
def build_user_context(user_id: str) -> str:
    tenant = get_tenant(user_id)
    
    return f"""
    You are assisting {user.name} at {tenant.company_name}.
    
    Their equipment:
    {summarize_assets(tenant.assets[:50])}
    
    Recent work orders:
    {summarize_work_orders(tenant.work_orders.recent(30))}
    
    Their preferences:
    - Preferred contact: {user.preferred_channel}
    - Expertise level: {user.expertise_level}
    - Quiet hours: {user.quiet_hours}
    """
```

---

## 3. Agent Specifications

### 3.1 Scanner Agent

**Purpose:** Continuously monitor tenant data for actionable insights.

**Scans:**

| Scan | Frequency | Query |
|------|-----------|-------|
| Orphan Work Orders | Every 4 hours | WOs without asset assignment |
| Overdue PMs | Daily | PM schedules past due date |
| Stale Assets | Weekly | Assets with no activity > 180 days |
| Anomaly Detection | Daily | Unusual patterns (3x normal failures, etc.) |

**Output:** Candidate messages → Judge → Delivery Queue

### 3.2 Enrichment Agent

**Purpose:** Keep asset cells alive with external data.

**Sources:**

| Source | Data | Frequency |
|--------|------|-----------|
| Manufacturer Sites | Firmware updates, recalls | Weekly |
| Industry Databases | Failure patterns, best practices | Monthly |
| User Feedback | Corrections, preferences | Real-time |

**Process:**
1. Extract equipment identifiers from CMMS (model numbers, serials)
2. Query external sources
3. Match to existing assets
4. Update living cells
5. Notify user if significant (new firmware, recall)

### 3.3 Chat Agent

**Purpose:** Handle direct user interactions.

**Context Window:**
```
[System Prompt: You are FactoryLLM...]
[Tenant Context: User's CMMS summary]
[Recent Conversation: Last 10 messages]
[Retrieved: RAG results for current query]
[User Message]
```

**Capabilities:**
- Answer questions about their equipment
- Create/update work orders
- Search their KB
- Explain error codes
- Suggest troubleshooting steps

---

## 4. Message Judgment Criteria

Every proactive message is judged before sending:

```python
PROACTIVE_MESSAGE_CRITERIA = {
    "actionable": {
        "question": "Can user take action based on this?",
        "weight": 0.3,
        "threshold": 4  # out of 5
    },
    "specific": {
        "question": "Does it reference specific assets/WOs?",
        "weight": 0.25,
        "threshold": 4
    },
    "timely": {
        "question": "Is this the right time to mention it?",
        "weight": 0.2,
        "threshold": 3
    },
    "non_duplicate": {
        "question": "Have we mentioned this recently?",
        "weight": 0.15,
        "threshold": 5  # Must be 5 (not duplicate)
    },
    "user_cares": {
        "question": "Based on history, will user value this?",
        "weight": 0.1,
        "threshold": 3
    }
}

# Weighted score must exceed 4.0 to send
```

---

## 5. MVP Scope (Phase 1)

### In Scope:
- [ ] Single-tenant (Mike's CMMS only)
- [ ] Telegram delivery
- [ ] Orphan WO detection + suggestions
- [ ] Basic asset matching
- [ ] Manual firmware check (not automated)

### Out of Scope (Phase 2+):
- Multi-tenant isolation
- Automated manufacturer scraping
- WhatsApp/Web delivery
- Full enrichment pipeline

---

## 6. Success Metrics

| Metric | Target | How Measured |
|--------|--------|--------------|
| Proactive message open rate | >60% | User responds or acknowledges |
| Suggestion acceptance rate | >40% | User accepts asset match |
| Time to WO completion | -20% | Before/after comparison |
| User NPS | >50 | Survey |
| False positive rate | <10% | Suggestions rejected as wrong |

---

## 7. Open Questions

1. **LLM Hosting:** Cloud API (simple) vs Local FactoryLLM (private)?
2. **Manufacturer Data:** Scrape or partner/API?
3. **Pricing Model:** Per-user? Per-asset? Per-message?
4. **Offline Mode:** What happens when user has no connectivity?

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | 2026-02-07 | Initial draft from conversation |

---

*Spec generated following FactoryLM Engineering Commandments. Awaiting polish cycle and judgment.*

---

## 8. Security Architecture

### 8.1 Authentication Flow

```
User → Telegram/WhatsApp → Bot Token Validates → 
  → User ID Lookup → Tenant ID Resolved →
  → All subsequent queries scoped to Tenant ID
```

### 8.2 Tenant Isolation (Defense in Depth)

| Layer | Protection |
|-------|------------|
| **API Gateway** | JWT contains tenant_id, validated on every request |
| **Database** | Row-level security (RLS) policies |
| **Application** | Tenant filter injected in ORM base query |
| **LLM Context** | Only tenant's data loaded into context |
| **Logs** | Tenant ID tagged, separate log streams |

```sql
-- PostgreSQL Row Level Security
ALTER TABLE assets ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON assets
  USING (tenant_id = current_setting('app.current_tenant')::uuid);
```

### 8.3 Data Encryption

| Data State | Method |
|------------|--------|
| At rest | AES-256 (database encryption) |
| In transit | TLS 1.3 |
| Secrets | Doppler/Vault (never in code) |
| Backups | Encrypted, tenant-separated |

---

## 9. Error Handling

### 9.1 Failure Modes

| Failure | Detection | Response | User Impact |
|---------|-----------|----------|-------------|
| LLM API down | Timeout (30s) | Retry 3x, then queue | "Thinking..." then delayed response |
| LLM returns garbage | Judge score < 2 | Discard, log, don't send | None (silent fail) |
| Database unreachable | Connection error | Circuit breaker, alert ops | "System maintenance" |
| Manufacturer site down | HTTP 5xx | Skip this cycle, retry next | None |
| Message queue full | Queue depth > 1000 | Drop low-priority, alert | Delayed proactive messages |

### 9.2 Circuit Breaker Pattern

```python
class LLMCircuitBreaker:
    def __init__(self):
        self.failures = 0
        self.threshold = 5
        self.reset_after = 300  # 5 minutes
        
    def call(self, prompt):
        if self.failures >= self.threshold:
            if time_since_last_failure() < self.reset_after:
                raise CircuitOpen("LLM circuit open")
            self.failures = 0
        
        try:
            result = llm.complete(prompt)
            self.failures = 0
            return result
        except Exception:
            self.failures += 1
            raise
```

---

## 10. Worked Example

### Scenario: Orphan Work Order Detection

**Setup:**
- User: Mike (tenant: crane_services_llc)
- 3 work orders created today, 1 missing asset assignment

**Step 1: Scanner Agent Query (runs at 14:00)**

```sql
SELECT id, title, description, created_at
FROM work_orders
WHERE tenant_id = 'crane_services_llc'
  AND asset_id IS NULL
  AND created_at > NOW() - INTERVAL '24 hours';
```

**Result:**
```json
{
  "id": "WO-2026-0847",
  "title": "VFD showing F041 fault",
  "description": "Line 4 drive tripped, needs reset and investigation",
  "created_at": "2026-02-07T10:30:00Z"
}
```

**Step 2: Asset Matching Query**

```sql
SELECT id, name, location, model 
FROM assets 
WHERE tenant_id = 'crane_services_llc'
  AND (name ILIKE '%vfd%' OR name ILIKE '%drive%')
  AND location ILIKE '%line 4%';
```

**Result:**
```json
[
  {"id": "AST-001", "name": "VFD-001", "location": "Line 4, Panel 3", "model": "PowerFlex 525"},
  {"id": "AST-019", "name": "VFD-002", "location": "Line 4, Panel 7", "model": "PowerFlex 525"}
]
```

**Step 3: LLM Suggestion Generation**

```
SYSTEM: You are FactoryLLM assisting with CMMS asset matching.

CONTEXT:
Work Order: WO-2026-0847
Title: VFD showing F041 fault
Description: Line 4 drive tripped, needs reset and investigation

Candidate Assets:
1. VFD-001 (PowerFlex 525) - Line 4, Panel 3
2. VFD-002 (PowerFlex 525) - Line 4, Panel 7

TASK: Suggest the most likely asset match. Explain briefly.

RESPONSE FORMAT:
{
  "suggested_asset": "AST-XXX",
  "confidence": 0.XX,
  "reason": "..."
}
```

**LLM Response:**
```json
{
  "suggested_asset": "AST-001",
  "confidence": 0.75,
  "reason": "F041 is a PowerFlex DC bus fault. Both VFDs are PF525 on Line 4. Panel 3 is primary drive location. Suggest VFD-001."
}
```

**Step 4: Judge Evaluation**

| Criterion | Score | Reason |
|-----------|-------|--------|
| Actionable | 5 | User can assign asset with one tap |
| Specific | 5 | References exact WO and asset |
| Timely | 4 | 3.5 hours after WO creation |
| Non-duplicate | 5 | First mention |
| User-cares | 4 | Mike always assigns assets |

**Weighted Score: 4.7** → PASS

**Step 5: Message Delivery**

```
📋 Work Order Needs Asset

WO-2026-0847: "VFD showing F041 fault"

I think this is VFD-001 (PowerFlex 525, Line 4 Panel 3).
F041 = DC bus fault, common on this model.

[✓ Assign VFD-001]  [✗ Wrong]  [Choose Different]
```

**User Response:** Taps "Assign VFD-001"

**Step 6: Learning**

```python
log_feedback(
    wo_id="WO-2026-0847",
    suggested="AST-001",
    accepted=True,
    response_time=45  # seconds
)
# This improves future suggestions for this user
```

---

## 11. Cost Model

### Per-Tenant Monthly Costs

| Component | Unit | Cost/Unit | Volume (SMB) | Monthly |
|-----------|------|-----------|--------------|---------|
| LLM API (Claude) | 1K tokens | $0.003 | 500K tokens | $1.50 |
| Database (Neon) | GB | $0.10 | 5 GB | $0.50 |
| Vector Store | 1K vectors | $0.01 | 10K | $0.10 |
| Message Delivery | message | $0.001 | 500 | $0.50 |
| Compute (scanner) | hour | $0.05 | 10 | $0.50 |
| **Total** | | | | **$3.10** |

### Pricing Tiers

| Tier | Assets | Proactive Msgs | Price | Margin |
|------|--------|----------------|-------|--------|
| Starter | 50 | 5/day | $29/mo | 90% |
| Pro | 500 | 15/day | $99/mo | 95% |
| Enterprise | Unlimited | Unlimited | Custom | 80%+ |

---

*Revision: v0.2 - Added Security, Error Handling, Worked Example, Cost Model*
