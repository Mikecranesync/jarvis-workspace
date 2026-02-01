# PROPOSAL: Master Network Map

**Requested by:** Mike Harp  
**Date:** 2026-02-01  
**Status:** AWAITING APPROVAL  
**Spec Source:** Voice → This Document → Automata → Code

---

## THE VISION

A **living, dynamic registry** of every connection, credential, and network granule in the FactoryLM ecosystem. Not a static document—an **agentic system** that:

1. **Auto-discovers** credentials and connections across all nodes
2. **Self-updates** when anything is created, modified, or accessed
3. **Provides API access** for all nodes to fetch what they need
4. **Maintains full audit trail** of every access and change
5. **Integrates with observability** (LangFuse + Grafana tracing)

---

## INDUSTRY STANDARD: HashiCorp Vault

The gold standard for this problem is **HashiCorp Vault**. Here's why:

| Requirement | Vault Capability |
|-------------|------------------|
| Dynamic secrets | ✅ Generates credentials on-demand, auto-expires |
| Centralized access | ✅ Single API for all nodes |
| Audit logging | ✅ Every read/write logged with who, when, what |
| Access control | ✅ Policies per node/service/user |
| Encryption | ✅ Secrets encrypted at rest and in transit |
| Secret versioning | ✅ Full history of changes |
| Auto-rotation | ✅ Can rotate credentials automatically |

**Alternative considered:** Roll our own with PostgreSQL + API. Rejected—reinventing the wheel, security risk.

---

## WHAT GETS TRACKED (Network Granules)

### Category 1: API Keys & Tokens
```
├── LLM Providers
│   ├── Anthropic (Claude) API key
│   ├── OpenAI API key
│   ├── Groq API key
│   └── Google (Gemini) API key
├── Observability
│   ├── LangFuse public/secret keys
│   ├── InfluxDB token
│   └── Grafana admin credentials
├── External Services
│   ├── Jira API token
│   ├── Trello API key
│   ├── Mautic credentials
│   └── Telegram bot token
└── Infrastructure
    ├── GitHub PAT
    ├── Tailscale auth keys
    └── Syncthing device IDs
```

### Category 2: Database Connections
```
├── PostgreSQL (rivet, cmms, portal)
├── Redis
├── InfluxDB
└── Vector DBs (future)
```

### Category 3: Service Endpoints
```
├── Internal Services
│   ├── Flowise (3001)
│   ├── n8n (5678)
│   ├── Manual Hunter (8090)
│   ├── Alarm Triage (8091)
│   └── [all automata ports]
├── External APIs
│   ├── Tavily search
│   ├── Weather API
│   └── Any future integrations
└── Hardware
    ├── BeagleBone SSH
    ├── PLC Modbus endpoint
    └── Laptop SSH endpoints
```

### Category 4: Node Identities
```
├── VPS (factorylm-prod)
│   ├── Tailscale IP
│   ├── Public IP
│   └── SSH credentials
├── PLC Laptop
│   ├── Tailscale IP
│   ├── Local IP
│   └── SSH user
├── Travel Laptop
│   └── [same structure]
├── BeagleBone
│   └── [same structure]
└── Mike's Phone
    └── Tailscale IP
```

---

## ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                    MASTER NETWORK MAP                        │
│                   (HashiCorp Vault)                         │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ Secrets     │  │ Connections │  │ Audit Log   │         │
│  │ Engine      │  │ Registry    │  │ (immutable) │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                          │                                   │
│                    Vault API                                 │
└─────────────────────────────────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
    │ Master of   │ │ Automata    │ │ Edge Nodes  │
    │ Puppets     │ │ Workers     │ │ (BeagleBone)│
    └─────────────┘ └─────────────┘ └─────────────┘
           │               │               │
           └───────────────┴───────────────┘
                           │
                    ┌──────┴──────┐
                    │ Observability│
                    │ (LangFuse +  │
                    │  Grafana)    │
                    └─────────────┘
```

---

## THE AGENTIC PROCESS

### Automaton: THE CARTOGRAPHER (Enhanced)

Currently maps code. **Enhanced to also map:**
- Network topology
- Credential dependencies
- Service connections

**Cron job (hourly):**
1. Scan all .env files across nodes
2. Scan docker-compose files for service definitions
3. Scan code for hardcoded connection strings (flag as violations)
4. Compare against Vault registry
5. Report drift: "New credential found in .env not in Vault"
6. Auto-register new discoveries (with human approval gate)

### Automaton: THE WATCHMAN (Enhanced)

Currently monitors runtime. **Enhanced to also:**
- Watch for credential access patterns
- Alert on unusual access (new node accessing old secret)
- Track credential age (rotation reminders)
- Monitor for leaked credentials in logs

### Integration with Observability

Every credential access creates a trace:
```json
{
  "trace_id": "vault-access-20260201-abc123",
  "timestamp": "2026-02-01T15:30:00Z",
  "action": "read",
  "secret_path": "kv/llm/anthropic",
  "accessor": "manual-hunter-worker",
  "node": "factorylm-prod",
  "result": "success"
}
```

→ Flows to LangFuse (if LLM-related) + InfluxDB → Grafana dashboard

---

## IMPLEMENTATION PHASES

### Phase 1: Foundation (Week 1)
- [ ] Deploy HashiCorp Vault on VPS (Docker)
- [ ] Initialize with root token
- [ ] Create initial policies (admin, read-only, per-service)
- [ ] Migrate existing .env secrets to Vault

### Phase 2: Integration (Week 2)
- [ ] Create `vault_client.py` wrapper in Master of Puppets
- [ ] Update all workers to fetch secrets from Vault
- [ ] Remove hardcoded secrets from .env files
- [ ] Set up audit log shipping to InfluxDB

### Phase 3: Discovery Agent (Week 3)
- [ ] Enhance Cartographer to scan for credentials
- [ ] Build drift detection: Vault vs reality
- [ ] Create approval workflow for new discoveries
- [ ] Dashboard: "Network Map" in Grafana

### Phase 4: Edge Nodes (Week 4)
- [ ] Vault agent on BeagleBone
- [ ] Laptop credential sync
- [ ] Auto-rotation for high-risk secrets
- [ ] Full topology visualization

---

## GRAFANA DASHBOARD: Network Map

**Panels:**
1. **Topology Graph** - Visual map of all nodes and connections
2. **Credential Health** - Age, last accessed, rotation status
3. **Access Heatmap** - Which services access which secrets
4. **Drift Alerts** - Credentials found outside Vault
5. **Audit Stream** - Live feed of all access events

---

## TRACEABILITY (Per Constitution)

| Event | Traced To | Evidence |
|-------|-----------|----------|
| Credential created | Vault audit log | Who, when, approval |
| Credential accessed | LangFuse + InfluxDB | Service, node, timestamp |
| Credential modified | Vault version history | Before/after, who |
| Credential rotated | Vault + alert | Auto or manual |
| Drift detected | Cartographer trace | Location, recommendation |

---

## SECURITY CONSIDERATIONS

1. **Vault sealed by default** - Requires unseal keys on restart
2. **No secrets in git** - Only Vault paths, never values
3. **Least privilege** - Each service gets only what it needs
4. **Audit everything** - Immutable log of all access
5. **Rotation policy** - High-risk secrets rotate automatically

---

## COST

- **HashiCorp Vault**: Free (open source)
- **Storage**: Minimal (secrets are small)
- **Complexity**: Medium (one-time setup, then automatic)

---

## DECISION REQUIRED

**Mike, approve this proposal to proceed through Automata:**

1. ✅ **APPROVE** - Spec-Maker formalizes → Weaver builds → Watchman monitors
2. ❌ **REJECT** - Provide feedback for revision
3. 🔄 **MODIFY** - What changes needed?

---

*This proposal follows Constitution Article 1: "Mike's words = The Spec"*  
*Traceability: Voice message → This document → Automata process → Production code*
