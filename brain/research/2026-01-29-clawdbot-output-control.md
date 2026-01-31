# Clawdbot/Moltbot Output Control & Custom Skills - Research Summary

## Key Findings

### 1. **Clawdbot Just Rebranded to Moltbot** (January 2026)
- Same project, renamed due to Anthropic trademark request
- Still uses the lobster mascot 🦞
- All references to "Clawdbot" now say "Moltbot" in official docs

---

## Real-World Examples Found

### ✅ Industrial Predictive Maintenance Examples on GitHub

**1. Predictive Maintenance System (CNC/Industrial Machinery)**
- Repo: `jashwanth-04/Predictive-Maintenance-Using-ML`
- Uses: Random Forest classifier + Streamlit UI
- Predicts machine failure from: temperature, rotational speed, torque, tool wear
- Deployed at: https://predictive-maintenance-using-machine-learning.streamlit.app/

**Key approach for output control:**
```
Dataset features → ML model → Prediction (Pass/Fail) → Streamlit display
- Structured input validation (temperature ranges, RPM bounds, etc.)
- Binary output (machine will fail yes/no)
- Confidence scores tracked
```

**2. AI-Powered Predictive Maintenance for Industrial Robotics**
- Repo: `melisasvr/AI-Powered-Predictive-Maintenance-System-for-Industrial-Robotics`
- Dashboard-based monitoring for robot maintenance needs
- Real-time alerts + historical trend analysis

**3. GitHub Actions + MLflow Automation**
- Uses GitHub Actions to trigger training on every push
- MLflow logs model metrics & artifacts
- Streamlit auto-reflects latest trained model
- Approach: Automated validation + artifact versioning

---

## How to Control Clawdbot/Moltbot Output (3 Concrete Approaches)

### **Approach 1: Build Custom Skills with SKILL.md**

**Structure:**
```
~/.clawdbot/skills/diagnose-equipment/
├── SKILL.md                 # Instructions + validation
├── validate.js             # Output schema checker
├── templates/
│   └── diagnostic-report.md # Expected format
└── scripts/
    └── cmms-integration.sh  # Send to CMMS
```

**Example SKILL.md for Equipment Diagnosis:**
```yaml
---
name: diagnose-equipment
description: Run equipment diagnostics and generate structured report
metadata: 
  moltbot:
    requires:
      bins: [jq, curl]
      env: [CMMS_API_KEY, PLC_HOST]
---

# Equipment Diagnostics Skill

## When to Use
- User asks to diagnose [equipment]
- User provides error/symptoms
- Need maintenance recommendation

## Process

1. **Gather Equipment State** (Required output: JSON)
   - Get fault codes from PLC at {{plc_host}}
   - Parse using jq for valid JSON
   
   Expected structure:
   ```json
   {
     "equipment_id": "string",
     "fault_codes": ["string"],
     "temperature": "number",
     "status": "ok|warning|critical"
   }
   ```

2. **Analyze Symptoms** (Required output: Schema)
   - Match fault codes to known failure modes
   - Calculate risk_level (0-10 scale)
   
   Required output:
   ```json
   {
     "likely_fault": "string",
     "confidence": "0-100",
     "risk_level": "0-10",
     "actions": ["string"]
   }
   ```

3. **Generate CMMS Ticket** (Validate before sending)
   - Check all required fields present
   - Use CMMS API: `curl -X POST $CMMS_API_KEY`
   - Return ticket_id or error
   
   Validation rules:
   - ticket_id must be numeric
   - created_at must be ISO8601
   - status must be one of: open|pending|assigned
```

---

### **Approach 2: Schema Validation Layer**

**Create a validation wrapper (validate.js):**
```javascript
// ~/.clawdbot/skills/diagnose-equipment/validate.js
const schema = {
  diagnosis: {
    type: "object",
    required: ["equipment_id", "likely_fault", "risk_level", "actions"],
    properties: {
      equipment_id: { type: "string", pattern: "^[A-Z]+-\\d+$" },
      likely_fault: { type: "string", minLength: 5 },
      risk_level: { type: "number", minimum: 0, maximum: 10 },
      actions: {
        type: "array",
        items: { type: "string" },
        minItems: 1
      },
      cmms_ready: { type: "boolean" }
    }
  }
};

export async function validate(aiOutput) {
  try {
    const parsed = JSON.parse(aiOutput);
    
    // Validate against schema
    const isValid = validateAgainstSchema(parsed, schema.diagnosis);
    
    if (!isValid) {
      return {
        valid: false,
        error: "Output does not match required schema",
        repairPrompt: `Your diagnosis output is incomplete. Required fields:
        - equipment_id (format: ABC-123)
        - likely_fault (string, min 5 chars)
        - risk_level (0-10)
        - actions (array of strings)
        
        Please revise and return as JSON.`
      };
    }
    
    return { valid: true, data: parsed };
  } catch (e) {
    return {
      valid: false,
      error: `JSON parse error: ${e.message}`,
      repairPrompt: "Your response was not valid JSON. Wrap diagnosis in: ```json { ... } ```"
    };
  }
}
```

**Then in SKILL.md:**
```markdown
## CRITICAL: Output Validation

After you complete diagnosis, Clawdbot will validate your output against this schema:

```json
{
  "equipment_id": "COMP-123",
  "likely_fault": "bearing wear in motor shaft",
  "risk_level": 7,
  "confidence": 92,
  "actions": [
    "replace bearing assembly within 24 hours",
    "order part BEAR-47XYZ",
    "notify technician on duty"
  ],
  "cmms_ready": true
}
```

**If validation fails**, Clawdbot will ask you to fix the JSON.
```

---

### **Approach 3: Lobster Pipelines (Deterministic Multi-Step)**

**Create a workflow file:**
```yaml
# ~/.clawdbot/skills/equipment-maintenance/workflows/full-diagnostic.lobster.yaml
name: "equipment-maintenance"
description: "Equipment diagnostics → validation → CMMS ticket → Telegram alert"

steps:
  # Step 1: PLC Diagnostics
  - id: "scan-plc"
    command: "your-cli plc-scan --equipment {{equipment_id}} --format json"
    validate: 
      schema: "fault_codes must be array"
      
  # Step 2: ML-based risk scoring
  - id: "score-risk"
    command: "ml-model score --input"
    stdin: "$step.scan-plc.json"
    output_schema:
      risk_level: { type: "number", min: 0, max: 10 }
      likely_fault: { type: "string" }
      
  # Step 3: Approval gate for critical issues
  - id: "approval-gate"
    condition: "$step.score-risk.risk_level > 7"
    halts_if: true
    resume_token_required: true
    
  # Step 4: Create CMMS ticket (only if approved)
  - id: "create-ticket"
    when: "$step.approval-gate.approved || $step.score-risk.risk_level <= 3"
    command: "cmms-api create-ticket --json"
    stdin: "$step.score-risk.json"
    output_schema:
      ticket_id: { type: "string", pattern: "^TKT-\\d+$" }
      created_at: { type: "string", format: "ISO8601" }
      
  # Step 5: Notify technician
  - id: "send-telegram"
    command: "telegram-bot send --user {{technician_id}}"
    stdin: "$step.create-ticket.json"
    format: "Ticket {{ticket_id}} created: {{likely_fault}} (Risk: {{risk_level}}/10)"
```

**Invoke with:**
```bash
clawdbot agent --skill equipment-maintenance --args "COMP-123" --thinking high
```

**Returns guaranteed structure:**
```json
{
  "status": "halted_for_approval|completed",
  "current_step": "approval-gate",
  "resume_token": "abc123xyz",
  "payload": {
    "equipment_id": "COMP-123",
    "risk_level": 8,
    "likely_fault": "bearing wear",
    "ticket_id": "TKT-4827",
    "created_at": "2026-01-29T08:53:00Z"
  }
}
```

---

## Real Community Examples (565+ Public Skills)

### Skills Closest to Your Needs:
1. **process-watch** - Monitor system processes (CPU, memory, disk I/O)
2. **uptime-kuma** - Interact with Uptime Kuma monitoring server
3. **unraid** - Query and monitor Unraid servers via GraphQL
4. **servicenow-agent** - Read-only CLI access to ServiceNow (CMMS-like)
5. **linearis** - Linear.app CLI for issue tracking (can model as tickets)

### Skills You Could Adapt:
- **github** - Shows how to `requires.bins` for dependency checking
- **docker** - Container orchestration example
- **notion** - Shows database schema validation pattern
- **jira** - CMMS integration pattern (create/update issues with validation)

---

## Agent Skills Standard (Cross-Platform)

**Moltbot skills follow the open AgentSkills spec:**
- Works in: Claude Code, Cursor, VS Code, OpenAI Codex, Gemini CLI, GitHub Copilot
- Format: YAML frontmatter + Markdown instructions + optional scripts
- Invocation: `/skill-name [args]` or auto-triggered by Claude when relevant

**Frontmatter options for output control:**
```yaml
name: my-skill
description: What this does
disable-model-invocation: false    # Claude can auto-invoke
user-invocable: true               # You can invoke manually
metadata:
  moltbot:
    requires:
      bins: [jq, curl]             # Must be installed
      env: [API_KEY, HOST]          # Must be set
      
# Control tool access:
allowed-tools:
  - Read                            # Only these tools allowed
  - Grep
  - Execute(jq)                     # Specific commands
```

---

## Connecting to A2A Framework

**Clawdbot can wrap A2A agents:**

```yaml
# ~/.clawdbot/skills/use-a2a-diagnostic/SKILL.md
---
name: a2a-diagnostic
description: Delegate to A2A diagnostic-planner agent with schema validation
metadata:
  moltbot:
    requires:
      bins: [curl]
      env: [A2A_SERVER_URL]
---

# Call A2A Agent with Input Validation

The workflow:
1. Validate your request against A2A input schema
2. POST to A2A server with equipment_id + symptoms
3. Wait for response
4. Validate response against A2A output schema
5. Format for Telegram/CMMS/user

## Input Schema (A2A AgentCard format)
```json
{
  "equipment_id": "string",
  "fault_symptoms": "string",
  "agent_card": "AgentCard identifier"
}
```

## Output Schema (A2A TaskResult format)
```json
{
  "plan_id": "string",
  "steps": [
    {
      "step_id": "string",
      "description": "string",
      "estimated_time_min": "number"
    }
  ],
  "status": "ok|error"
}
```

## Instructions

When user requests equipment diagnosis:
1. Extract equipment_id and symptoms
2. Call A2A endpoint with validated input
3. Wait for response
4. Validate response matches output schema
5. Return formatted result
```

**Handler script (TypeScript):**
```typescript
// skills/a2a-diagnostic/call-a2a.ts
import { validate } from './validate.ts';

export async function runA2ADiagnostic(equipmentId: string, symptoms: string) {
  // 1. Call A2A
  const response = await fetch(`${process.env.A2A_SERVER_URL}/agents/diagnostic-planner`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      equipment_id: equipmentId,
      fault_symptoms: symptoms,
      agent_card: 'AgentCard for diagnostic-planner'
    })
  });

  const result = await response.json();

  // 2. Validate against A2A schema
  const validation = await validate(result, {
    required: ['plan_id', 'steps'],
    schema: {
      plan_id: 'string',
      steps: 'array of {step_id, description, estimated_time_min}'
    }
  });

  if (!validation.valid) {
    throw new Error(`A2A response invalid: ${validation.error}`);
  }

  // 3. Return to Clawdbot as structured output
  return validation.data;
}
```

---

## Quick Start for Your Rivet Pro Stack

### Step 1: Create Basic Skill Structure
```bash
mkdir -p ~/.clawdbot/skills/rivet-diagnose
cd ~/.clawdbot/skills/rivet-diagnose

# Create SKILL.md with your equipment types
cat > SKILL.md << 'EOF'
---
name: rivet-diagnose
description: Diagnose industrial equipment using ML + PLC integration
metadata:
  moltbot:
    requires:
      bins: [curl, jq]
      env: [RIVET_API_URL, CMMS_API_KEY]
---

# Rivet Pro Equipment Diagnostics

## When to Use
- User asks to diagnose equipment (motors, compressors, bearings)
- User provides symptoms or fault codes
- User shares equipment photo for vision-based diagnostics

## Input
- equipment_id: "COMP-123" or "MOTOR-45" (format: TYPE-NUMBER)
- symptoms: describe what's wrong
- optionally: image_base64 (from camera/phone)

## Output (JSON - REQUIRED FORMAT)
```json
{
  "equipment_id": "string",
  "diagnosis_id": "string",
  "likely_faults": [
    {
      "component": "bearing",
      "probability": 92,
      "action": "replace"
    }
  ],
  "cmms_ready": true
}
```

## Process

### 1. Gather Equipment Data
- If PLC available: query fault codes via `curl $RIVET_API_URL/plc/scan?equipment={{equipment_id}}`
- If image provided: send to vision endpoint `curl $RIVET_API_URL/vision/analyze`
- Parse responses with `jq` to validate JSON

### 2. Analyze & Score Risk
- Match fault codes to known failure patterns
- Calculate probability (0-100) for each likely fault
- Determine risk_level (0-10 scale)

### 3. Validate Output
Before returning, verify:
- equipment_id matches format (ABC-123)
- likely_faults is non-empty array
- Each fault has: component, probability (0-100), action
- cmms_ready is boolean

### 4. Return Structured Output
Return ONLY valid JSON matching the output schema above.

## Validation Rules
- equipment_id must match pattern: ^[A-Z]+-\d+$
- probability must be 0-100
- risk_level must be 0-10
- actions must be non-empty array of strings
- cmms_ready must be boolean

## Example

User: "Diagnose COMP-123, hearing grinding noise"

Your response:
```json
{
  "equipment_id": "COMP-123",
  "diagnosis_id": "DIAG-20260129-001",
  "likely_faults": [
    {
      "component": "bearing assembly",
      "probability": 87,
      "action": "replace bearing within 24 hours"
    },
    {
      "component": "shaft alignment",
      "probability": 45,
      "action": "check alignment if bearing replacement doesn't resolve"
    }
  ],
  "cmms_ready": true
}
```
EOF
```

### Step 2: Add Validation Script
```bash
cat > validate.ts << 'EOF'
// Validate output against Rivet schema
export function validateDiagnosis(output: any) {
  const errors: string[] = [];
  
  // Check equipment_id format
  if (!output.equipment_id?.match(/^[A-Z]+-\d+$/)) {
    errors.push('Invalid equipment_id format (expected: ABC-123)');
  }
  
  // Check likely_faults structure
  if (!Array.isArray(output.likely_faults) || output.likely_faults.length === 0) {
    errors.push('likely_faults must be non-empty array');
  }
  
  // Check cmms_ready field
  if (typeof output.cmms_ready !== 'boolean') {
    errors.push('cmms_ready must be boolean');
  }
  
  // Validate each fault
  output.likely_faults?.forEach((fault: any, i: number) => {
    if (!fault.component || typeof fault.component !== 'string') {
      errors.push(`Fault ${i}: missing or invalid component`);
    }
    if (typeof fault.probability !== 'number' || fault.probability < 0 || fault.probability > 100) {
      errors.push(`Fault ${i}: probability must be 0-100`);
    }
    if (!fault.action || typeof fault.action !== 'string') {
      errors.push(`Fault ${i}: missing or invalid action`);
    }
  });
  
  return { 
    valid: errors.length === 0, 
    errors,
    repairPrompt: errors.length > 0 
      ? `Your output has validation errors:\n${errors.join('\n')}\n\nPlease fix and return valid JSON.`
      : null
  };
}

// Example usage in Clawdbot skill handler
export async function handleDiagnosis(rawOutput: string) {
  try {
    const parsed = JSON.parse(rawOutput);
    const validation = validateDiagnosis(parsed);
    
    if (!validation.valid) {
      console.error('Validation failed:', validation.errors);
      // Send repair prompt back to LLM
      return { success: false, repairPrompt: validation.repairPrompt };
    }
    
    return { success: true, data: parsed };
  } catch (e) {
    return {
      success: false,
      repairPrompt: 'Invalid JSON format. Please return properly formatted JSON.'
    };
  }
}
EOF
```

### Step 3: Create Lobster Workflow
```bash
mkdir workflows
cat > workflows/full-diagnostic.lobster.yaml << 'EOF'
name: "rivet-full-diagnostic"
description: "Complete equipment diagnostic workflow with CMMS integration"

inputs:
  equipment_id:
    type: string
    pattern: "^[A-Z]+-\\d+$"
    required: true
  symptoms:
    type: string
    required: true
  image_base64:
    type: string
    required: false

steps:
  # Step 1: Scan PLC for fault codes
  - id: "scan-plc"
    command: "curl -s ${RIVET_API_URL}/plc/scan?equipment={{equipment_id}}"
    output_format: json
    validate:
      - fault_codes must be array
      - status must be one of: ok|warning|critical
      
  # Step 2: ML-based risk scoring
  - id: "score-risk"
    command: "curl -X POST ${RIVET_API_URL}/diagnose"
    stdin: "$step.scan-plc.json"
    headers:
      Content-Type: application/json
    output_schema:
      equipment_id: { type: string }
      risk_level: { type: number, min: 0, max: 10 }
      likely_faults: { type: array, minItems: 1 }
      
  # Step 3: Approval gate for critical issues
  - id: "approval-gate"
    condition: "$step.score-risk.risk_level > 7"
    halts_if: true
    resume_token_required: true
    message: |
      ⚠️ CRITICAL ISSUE DETECTED
      Equipment: {{equipment_id}}
      Risk Level: {{risk_level}}/10
      Fault: {{likely_faults[0].component}}
      
      Reply 'approve' to create CMMS ticket
      
  # Step 4: Create CMMS ticket (only if approved or low risk)
  - id: "create-ticket"
    when: "$step.approval-gate.approved || $step.score-risk.risk_level <= 3"
    command: "curl -X POST ${CMMS_API_URL}/tickets"
    headers:
      Authorization: "Bearer ${CMMS_API_KEY}"
      Content-Type: application/json
    stdin: "$step.score-risk.json"
    output_schema:
      ticket_id: { type: string, pattern: "^TKT-\\d+$" }
      created_at: { type: string, format: ISO8601 }
      status: { type: string, enum: [open, pending, assigned] }
      
  # Step 5: Notify technician via Telegram
  - id: "send-telegram"
    command: "curl -X POST https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage"
    body:
      chat_id: "{{technician_chat_id}}"
      text: |
        ✅ Maintenance Ticket Created
        
        Ticket: {{ticket_id}}
        Equipment: {{equipment_id}}
        Issue: {{likely_faults[0].component}}
        Priority: {{risk_level > 7 ? 'CRITICAL' : 'NORMAL'}}
        Action: {{likely_faults[0].action}}
        
        View: ${CMMS_URL}/tickets/{{ticket_id}}
      parse_mode: Markdown

outputs:
  status: "$step.create-ticket.status"
  ticket_id: "$step.create-ticket.ticket_id"
  risk_level: "$step.score-risk.risk_level"
  equipment_id: "{{equipment_id}}"
EOF
```

### Step 4: Test via Clawdbot
```bash
# Terminal 1: Start gateway
clawdbot gateway --port 18789

# Terminal 2: Test basic skill
clawdbot agent \
  --message "Diagnose COMP-123, grinding noise in bearing" \
  --skill rivet-diagnose

# Terminal 3: Test full workflow
clawdbot agent \
  --workflow workflows/full-diagnostic.lobster.yaml \
  --args '{"equipment_id":"COMP-123","symptoms":"grinding noise"}'
```

---

## Clawdbot/Moltbot Architecture Overview

### How Output Control Works Internally

```
User Message (Telegram/Slack/CLI)
    ↓
Gateway (localhost:18789)
    ↓
Message Router
    ↓
Skill Matcher (finds relevant SKILL.md)
    ↓
Agent Brain (Claude/OpenAI reads skill instructions)
    ↓
Tool Execution (bash, curl, jq, custom scripts)
    ↓
Output Validator (checks against schema in SKILL.md)
    ├─ Valid → Return to user
    └─ Invalid → Send repair prompt to LLM, retry
```

**Key insight:** The SKILL.md acts as a **contract** between the LLM and your system. By specifying exact schemas, you force the LLM to produce structured, validated output.

---

## Integration with A2A Framework

### Why Combine Clawdbot + A2A?

**Clawdbot provides:**
- Multi-channel messaging (Telegram, Slack, Discord, WhatsApp)
- Local-first execution (runs on your machine/server)
- Shell access and system integration
- User-friendly skill system

**A2A provides:**
- Agent-to-agent communication protocol
- Type-safe message passing
- AgentCards (agent capability description)
- Cross-framework compatibility

### Combined Architecture

```
Technician (Telegram) 
    ↓
Clawdbot Gateway
    ↓
Clawdbot Skill: "rivet-diagnose"
    ↓
A2A Agent: "diagnostic-planner" (validates input)
    ↓
A2A Agent: "ml-analyzer" (runs prediction)
    ↓
A2A Agent: "cmms-integrator" (creates ticket)
    ↓
Clawdbot formats & sends to Telegram
    ↓
Technician receives structured report
```

**Benefits:**
1. **Type safety** at agent boundaries (A2A)
2. **Multi-channel delivery** (Clawdbot)
3. **Deterministic workflows** (Lobster)
4. **Human-in-the-loop approvals** (Lobster gates)

### Example Integration Code

```typescript
// skills/rivet-a2a-diagnostic/handler.ts
import { A2AClient } from '@a2a/client';

const a2a = new A2AClient(process.env.A2A_SERVER_URL);

export async function diagnoseViaA2A(equipmentId: string, symptoms: string) {
  // Step 1: Call A2A diagnostic-planner
  const planResult = await a2a.callAgent({
    agentCard: 'diagnostic-planner-v1',
    input: {
      equipment_id: equipmentId,
      fault_symptoms: symptoms
    },
    outputSchema: {
      plan_id: 'string',
      steps: 'array',
      risk_level: 'number'
    }
  });

  // Step 2: Validate A2A response
  if (!planResult.valid) {
    throw new Error(`A2A validation failed: ${planResult.errors}`);
  }

  // Step 3: If high risk, call ML analyzer
  if (planResult.data.risk_level > 7) {
    const analysisResult = await a2a.callAgent({
      agentCard: 'ml-analyzer-v1',
      input: {
        plan_id: planResult.data.plan_id,
        equipment_data: planResult.data
      }
    });

    return analysisResult.data;
  }

  return planResult.data;
}
```

---

## GitHub Repos for Reference

### Clawdbot/Moltbot Core
- **Main repo:** `clawdbot/clawdbot` (now redirects to `moltbot/moltbot`)
- **Lobster workflows:** `clawdbot/lobster`
- **Official docs:** https://docs.clawd.bot (or https://docs.molt.bot)

### Community Skills
- **Awesome list:** `VoltAgent/awesome-moltbot-skills` (565+ skills)
- **Skill examples:** `jdrhyne/agent-skills`

### Predictive Maintenance Examples
- **CNC maintenance:** `jashwanth-04/Predictive-Maintenance-Using-ML`
- **Robot maintenance:** `melisasvr/AI-Powered-Predictive-Maintenance-System-for-Industrial-Robotics`
- **Robot maintenance (alt):** `mriusero/predictive-maintenance-on-industrial-robots`

### A2A Protocol
- **A2A framework:** `a2aproject/A2A`
- **Agent protocol (LangChain):** `langchain-ai/agent-protocol`

---

## Key Takeaways

✅ **Clawdbot (now Moltbot) is production-ready** for industrial automation  
✅ **Skills with schemas enforce output structure** — no more LLM hallucination  
✅ **Lobster pipelines create deterministic workflows** with approval gates  
✅ **565+ community skills** provide working patterns to copy  
✅ **No existing example combines all your needs** — you're building the first industrial predictive maintenance + CMMS + Telegram + A2A integration  
✅ **A2A integration is possible** via custom skill handlers  

---

## Next Steps for Rivet Pro

1. **Install Clawdbot/Moltbot** on your dev machine
2. **Create `rivet-diagnose` skill** with schema validation
3. **Build Lobster workflow** for full diagnostic → CMMS pipeline
4. **Test with real equipment** (or Factory IO simulation)
5. **Deploy to VPS** (Hostinger or Fly.io)
6. **Wire to Telegram bot** for technician access
7. **Optional: Add A2A layer** for multi-agent coordination

---

## Resources

- **Official docs:** https://docs.clawd.bot/
- **Lobster docs:** https://docs.clawd.bot/tools/lobster
- **Skills standard:** https://code.claude.com/docs/en/skills
- **DataCamp tutorial:** https://www.datacamp.com/tutorial/moltbot-clawdbot-tutorial
- **YouTube guide:** "Clawdbot Explained in 6 minutes" (Jan 25, 2026)

---

**Last updated:** January 29, 2026  
**Research compiled for:** Rivet Pro industrial maintenance platform