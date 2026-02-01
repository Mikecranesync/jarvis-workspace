# Phased Implementation Plan: Bootstrapping The Industrial AI Swarm

> Saved from Mike's document 2026-01-31

## Overview

This plan transforms the Master of Puppets from simple HTTP servers (ports 8090-8096) into a production-grade Celery-based autonomous system.

## Key Concepts I Understand:

### 1. Architecture Shift
- **Old:** Python HTTP servers running independently
- **New:** Celery workers pulling from Redis queue, orchestrated by The Conductor

### 2. The Cast (Roles Clarified)
- **The Monkey:** Governor/scheduler, enforces token budget, turns the crank
- **The Conductor:** Routes tasks to correct workers, orchestrates workflows
- **Manual Hunter:** Searches industrial manuals for answers
- **Alarm Triage:** Turns alarm codes into actionable checklists
- **The Weaver:** Writes documentation and procedures
- **The Watchman:** Monitors systems, finds anomalies
- **The Cartographer:** Maps codebase and dependencies
- **Workflow Tracker:** Logs all work done

### 3. Phase Summary
| Phase | Week | Goal |
|-------|------|------|
| 0 | Setup | Trello board + task import |
| 1 | Wk 1 | Celery + Redis foundation, all agents as workers |
| 2 | Wk 2 | Connect PLCs (S7-1200, Micro820, BeagleBone) |
| 3 | Wk 3 | 48h baseline collection, drift detection |
| 4 | Wk 4 | ChromaDB vectors, cross-vendor pattern learning |
| 5 | Wk 5 | Auto-execution whitelist, Grafana dashboards, 24/7 ops |
| 6 | Wk 6+ | Claude Code bridge, Factory I/O, predictive maintenance |

### 4. Mike's Role
- Hardware setup (PLCs, network)
- Approve/test completed tasks
- Provide outcome feedback ("fixed bearing", "false alarm")
- Define auto-execution whitelist
- ~6-8 hours total manual work

### 5. The Monkey's Self-Management
- Reads Trello board
- Picks next autonomous (🟢) task
- Checks token budget before executing
- Tests code, moves to Review
- Alerts Mike for 🟡 tasks
- Reports progress every 4 hours

### 6. Success Criteria per Phase
- Phase 1: Flower shows 8 workers, can send test tasks
- Phase 2: All PLCs logging to InfluxDB, Grafana shows data
- Phase 3: Drift alerts → WhatsApp within 60 seconds
- Phase 4: Vector DB similarity search working
- Phase 5: 24h unattended operation, daily summary

### 7. Key Infrastructure
- Redis (already have ✅)
- Celery + Flower (need to install)
- InfluxDB + Grafana (for time-series data)
- ChromaDB (for vector embeddings)
- PostgreSQL (already have ✅)
- Trello API (for self-management)

---

## Full Document Below

<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Phased Implementation Plan: Bootstrapping The Industrial AI Swarm

## Phase 0: Trello Board Setup + Monkey Initialization

### Trello Board Structure

```
Board: "Industrial AI Swarm - Master Build"

Lists:
├─ 📋 Backlog (All tasks from phases below)
├─ 🎯 Current Sprint (What The Monkey is working on now)
├─ 🔄 In Progress (Active microtasks)
├─ 👀 Review Needed (Mike must approve/test)
├─ ✅ Done
└─ 🚫 Blocked (Waiting on Mike's manual actions)

Labels:
├─ 🔴 Critical Path (Must complete before next phase)
├─ 🟡 Mike Action Required (Email, WhatsApp, hardware setup)
├─ 🟢 Autonomous (Monkey can complete alone)
├─ 🔵 Infrastructure (Docker, Celery, databases)
├─ 🟣 Agent Development (Building the agents)
└─ ⚫ Integration (Connecting systems)
```


***

## Phase 1: Foundation (Week 1)

**Goal:** Get Celery + Redis task queue working, revive all agents as Celery workers

### Mike's Manual Actions (Do First)

```
Trello Card: "🟡 MIKE: Set Up Core Services"

Checklist:
[ ] Start existing Redis container (already have it ✅)
[ ] Install Celery on VPS: pip install celery[redis] flower
[ ] Create /opt/master_of_puppets/ directory structure
[ ] Set environment variables in .env file
[ ] Connect WhatsApp API to clawdbot (if not done)
[ ] Verify ngrok tunnel or Cloudflare Tunnel is running

Dependencies: None
Estimated Time: 30 minutes
Blocking: Everything else
```


### Monkey's Autonomous Tasks

#### Task 1.1: Celery Worker Base Infrastructure

```
Trello Card: "🟢 Create Celery App + Worker Template"

Subtasks:
[ ] Create celery_app.py with Redis backend configuration
[ ] Create base_worker.py with common imports, logging, retry logic
[ ] Create docker-compose.celery.yml for worker orchestration
[ ] Add Flower monitoring on port 5555
[ ] Test: celery -A celery_app worker --loglevel=info

Files to create:
├─ /opt/master_of_puppets/celery_app.py
├─ /opt/master_of_puppets/workers/base_worker.py
├─ /opt/master_of_puppets/docker-compose.celery.yml
└─ /opt/master_of_puppets/config/celery_config.py

Success criteria:
✓ Worker connects to Redis
✓ Flower dashboard accessible at http://localhost:5555
✓ Can send test task and see it execute

Estimated tokens: ~3,000
Autonomous: YES
```


#### Task 1.2: Revive The Conductor as Celery Orchestrator

```
Trello Card: "🟢 Port The Conductor to Celery"

Subtasks:
[ ] Find existing Conductor code (port 8096)
[ ] Refactor into Celery task: conductor.route_task()
[ ] Add task routing logic (which agent handles which event type)
[ ] Create conductor_tasks.py with @app.task decorators
[ ] Test: Send mock alert, verify routing works

Files to modify:
├─ Extract from port 8096 codebase
└─ Create /opt/master_of_puppets/workers/conductor_tasks.py

Success criteria:
✓ Conductor receives task, routes to correct worker
✓ Logs decision-making process
✓ Returns routing result

Estimated tokens: ~5,000
Autonomous: YES (has existing code to reference)
```


#### Task 1.3: Revive Manual Hunter as Celery Worker

```
Trello Card: "🟢 Port Manual Hunter to Celery (Port 8090 → Worker)"

Subtasks:
[ ] Extract Manual Hunter logic from port 8090
[ ] Create manual_hunter_tasks.py
[ ] Task: search_manuals(query, plc_vendor)
[ ] Connect to Ollama for embeddings (already running ✅)
[ ] Test: Search for "S7-1200 vibration troubleshooting"

Files:
└─ /opt/master_of_puppets/workers/manual_hunter_tasks.py

Success criteria:
✓ Accepts search query as Celery task
✓ Returns relevant manual excerpts
✓ Logs search results to Workflow Tracker

Estimated tokens: ~4,000
Autonomous: YES
```


#### Task 1.4-1.8: Revive All Other Agents

```
Trello Cards (one per agent):
├─ "🟢 Port Alarm Triage (8091 → Worker)"
├─ "🟢 Port The Weaver (8093 → Worker)"
├─ "🟢 Port The Watchman (8094 → Worker)"
├─ "🟢 Port The Cartographer (8095 → Worker)"
└─ "🟢 Port Workflow Tracker (8092 → Worker)"

Pattern for each:
[ ] Extract logic from port 809X
[ ] Create {agent}_tasks.py with @app.task
[ ] Define task signatures (inputs, outputs)
[ ] Test with mock data
[ ] Add to Celery worker pool

Estimated tokens per agent: ~3,500
Total tokens: ~17,500
Autonomous: YES (follow same pattern as Manual Hunter)
```


#### Task 1.9: The Monkey (Budget Enforcer)

```
Trello Card: "🟢 Create The Monkey - Token Budget Tracker"

Subtasks:
[ ] Create monkey_tasks.py
[ ] Task: track_usage(task_id, tokens_used, cost)
[ ] Store in PostgreSQL table: token_usage
[ ] Implement budget checks: before_task_start()
[ ] Alert if hourly/daily budget exceeded
[ ] Dashboard endpoint: GET /monkey/budget_status

Files:
└─ /opt/master_of_puppets/workers/monkey_tasks.py

Success criteria:
✓ Tracks every task's token usage
✓ Prevents new tasks if budget exceeded
✓ Sends alert to Mike via WhatsApp when >80% budget used

Estimated tokens: ~4,500
Autonomous: YES
```


### Phase 1 Success Criteria

```
Trello Card: "✅ Phase 1 Complete - Checklist"

[ ] All 8 agents running as Celery workers
[ ] Flower dashboard shows all workers healthy
[ ] Can send test task to each agent
[ ] The Monkey tracks all token usage
[ ] The Conductor routes tasks correctly
[ ] Docker compose up -d starts everything

Command to verify:
docker-compose -f docker-compose.celery.yml ps
celery -A celery_app inspect active

When complete: Move to Phase 2
```


***

## Phase 2: PLC Integration (Week 2)

**Goal:** Connect real PLCs, start collecting data, wire to Celery task queue

### Mike's Manual Actions

```
Trello Card: "🟡 MIKE: Hardware Setup"

Checklist:
[ ] Connect S7-1200 to network (IP: 192.168.0.1)
[ ] Connect Micro820 to network (IP: 192.168.0.2)
[ ] Connect BeagleBone via USB/Ethernet
[ ] Verify TIA Portal trial is active (21 days)
[ ] Download CCW for Micro820 (free,永久)
[ ] Create simple test program on each PLC with simulated sensors
[ ] Test: Can ping all 3 PLCs from PC

Estimated time: 2 hours
Blocking: All PLC collector tasks
```

```
Trello Card: "🟡 MIKE: Install InfluxDB + Grafana"

Checklist:
[ ] Install InfluxDB 2.x: docker run -p 8086:8086 influxdb:2
[ ] Create bucket: "sensors"
[ ] Generate API token, save to .env file
[ ] Install Grafana: docker run -p 3000:3000 grafana/grafana
[ ] Add InfluxDB as data source in Grafana
[ ] Expose via ngrok: ngrok http 3000

Estimated time: 30 minutes
Blocking: Data collection tasks
```


### Monkey's Autonomous Tasks

#### Task 2.1: S7-1200 Data Collector

```
Trello Card: "🟢 Build S7-1200 Collector (python-snap7)"

Subtasks:
[ ] Install python-snap7: pip install python-snap7
[ ] Create s7_collector_tasks.py
[ ] Task: collect_s7_data() - polls every 100ms
[ ] Read DB1: motor_speed, motor_temp, vibration, current
[ ] Write to InfluxDB bucket "sensors"
[ ] Tag with: vendor=siemens_s7, plc_id=cpu1212c
[ ] Add as Celery Beat schedule (runs continuously)

Files:
└─ /opt/master_of_puppets/collectors/s7_collector_tasks.py

Success criteria:
✓ Connects to 192.168.0.1
✓ Reads 4 metrics every 100ms
✓ InfluxDB shows data streaming in

Estimated tokens: ~6,000
Autonomous: YES (after Mike connects PLC)
```


#### Task 2.2: Micro820 Data Collector

```
Trello Card: "🟢 Build Micro820 Collector (pycomm3)"

Subtasks:
[ ] Install pycomm3: pip install pycomm3
[ ] Create ab_collector_tasks.py
[ ] Task: collect_ab_data() - polls every 100ms
[ ] Read tags: Motor_Speed, Motor_Temp, Vibration
[ ] Write to InfluxDB, tag vendor=allen_bradley
[ ] Add to Celery Beat schedule

Files:
└─ /opt/master_of_puppets/collectors/ab_collector_tasks.py

Success criteria:
✓ Connects to 192.168.0.2 via EtherNet/IP
✓ Reads all tags
✓ Data appears in InfluxDB

Estimated tokens: ~5,500
Autonomous: YES (after Mike connects PLC)
```


#### Task 2.3: BeagleBone Modbus Collector

```
Trello Card: "🟢 Build BeagleBone Modbus RTU Collector"

Subtasks:
[ ] Install pymodbus: pip install pymodbus
[ ] Create beaglebone_collector_tasks.py
[ ] Task: collect_modbus_data() - polls every 1 second
[ ] Read holding registers 0-50
[ ] Parse based on sensor map (get from Mike)
[ ] Write to InfluxDB, tag vendor=beaglebone_modbus

Files:
└─ /opt/master_of_puppets/collectors/beaglebone_collector_tasks.py

Success criteria:
✓ Connects to BeagleBone /dev/ttyUSB0
✓ Reads all registers
✓ Data logged to InfluxDB

Estimated tokens: ~5,000
Autonomous: YES (after Mike provides register map)
```


#### Task 2.4: Unified Collector Orchestrator

```
Trello Card: "🟢 Create Collector Manager"

Subtasks:
[ ] Create collector_manager.py
[ ] Starts all 3 collectors as Celery Beat tasks
[ ] Health check: verify each collector is alive
[ ] Auto-restart if collector crashes
[ ] Alert Mike if collector fails 3x consecutively

Files:
└─ /opt/master_of_puppets/collectors/collector_manager.py

Success criteria:
✓ All 3 PLCs logging data continuously
✓ Health check every 60 seconds
✓ Auto-recovery on transient failures

Estimated tokens: ~4,000
Autonomous: YES
```


### Phase 2 Success Criteria

```
[ ] All 3 PLCs streaming data to InfluxDB
[ ] Grafana dashboard shows real-time metrics
[ ] Collectors run 24/7 via Celery Beat
[ ] Health checks prevent silent failures
[ ] Mike can see live PLC data in Grafana
```


***

## Phase 3: Baseline + Drift Detection (Week 3)

**Goal:** Calculate normal baselines, detect anomalies, trigger agent workflows

### Mike's Manual Actions

```
Trello Card: "🟡 MIKE: Run Normal Operations for 48 Hours"

Instructions:
Let the PLCs run in "normal" mode for 48 hours. Don't simulate faults yet.
The system needs to learn what "normal" looks like.

Checklist:
[ ] Verify all collectors running
[ ] Let data accumulate for 48 hours
[ ] Don't touch PLC programs during this time
[ ] After 48h, notify The Monkey to build baselines

Estimated time: 48 hours passive waiting
```


### Monkey's Autonomous Tasks

#### Task 3.1: Baseline Builder

```
Trello Card: "🟢 Build Baseline Calculator"

Subtasks:
[ ] Create baseline_builder_tasks.py
[ ] Task: build_baselines() - runs after 48h data collection
[ ] For each metric (motor_speed, temp, vibration, etc.):
    [ ] Query InfluxDB for last 48 hours
    [ ] Calculate: mean, std_dev, p95, p99
    [ ] Store in PostgreSQL table: baselines
    [ ] Tag with: plc_vendor, metric, calculated_at
[ ] Generate baseline report for Mike

Files:
└─ /opt/master_of_puppets/analytics/baseline_builder_tasks.py

Success criteria:
✓ Baselines calculated for all metrics on all PLCs
✓ Stored in database
✓ Report sent to Mike via WhatsApp

Estimated tokens: ~7,000
Autonomous: YES (triggered 48h after Phase 2 complete)
```


#### Task 3.2: Drift Detector

```
Trello Card: "🟢 Build Real-Time Drift Detector"

Subtasks:
[ ] Create drift_detector_tasks.py
[ ] Task: check_drift() - Celery Beat every 60 seconds
[ ] For each metric:
    [ ] Get last 5 minutes of data from InfluxDB
    [ ] Compare current_mean to baseline.mean
    [ ] Calculate drift: (current - baseline) / baseline.std_dev
    [ ] If drift > 2σ: trigger alert
[ ] Alert includes: metric, drift_magnitude, plc_vendor, timestamp
[ ] Sends task to The Conductor for orchestration

Files:
└─ /opt/master_of_puppets/analytics/drift_detector_tasks.py

Success criteria:
✓ Runs every 60 seconds
✓ Detects drift > 2 sigma
✓ Triggers Conductor workflow

Estimated tokens: ~8,000
Autonomous: YES
```


#### Task 3.3: Wire Drift Alerts to Conductor

```
Trello Card: "🟢 Drift Alert → Conductor Integration"

Subtasks:
[ ] When drift detected, send task:
    conductor.handle_drift_alert.delay(
        sensor="motor_3_vibration",
        magnitude=2.3,
        plc_vendor="siemens_s7",
        related_metrics=["motor_3_temp"]
    )
[ ] Conductor routes to agents:
    - Manual Hunter: search for troubleshooting
    - Alarm Triage: find similar patterns
    - The Watchman: check correlations
    - The Weaver: generate report
[ ] Parallel execution via Celery group
[ ] Results aggregated, sent to Mike

Files:
├─ Modify: conductor_tasks.py (add handle_drift_alert)
└─ Create: alert_workflows.py

Success criteria:
✓ Drift triggers agent workflow
✓ All agents execute in parallel
✓ Report delivered to WhatsApp within 60 seconds

Estimated tokens: ~9,000
Autonomous: YES
```


### Phase 3 Success Criteria

```
[ ] Baselines calculated for all metrics
[ ] Drift detector running continuously
[ ] Drift alerts trigger agent workflows
[ ] Mike receives actionable reports on WhatsApp
[ ] Test: Manually inject fault, verify alert generated
```


***

## Phase 4: Vector DB + Learning (Week 4)

**Goal:** Embed drift patterns, enable cross-vendor similarity search, self-improvement

### Mike's Manual Actions

```
Trello Card: "🟡 MIKE: Install ChromaDB"

Checklist:
[ ] Install ChromaDB: docker run -p 8000:8000 chromadb/chroma
[ ] Or use embedded mode (simpler for now)
[ ] Create collection: "drift_patterns"
[ ] Test: Can connect from Python

Estimated time: 15 minutes
```


### Monkey's Autonomous Tasks

#### Task 4.1: Drift Pattern Embedder

```
Trello Card: "🟢 Embed Drift Events to Vector DB"

Subtasks:
[ ] Install sentence-transformers: pip install sentence-transformers
[ ] Create embedding_tasks.py
[ ] Task: embed_drift_event(drift_alert)
[ ] Generate text: "Sensor {name} on {vendor} drifted {magnitude}σ. Related: {metrics}"
[ ] Embed using all-MiniLM-L6-v2 model
[ ] Store in ChromaDB with metadata:
    {vendor, sensor, magnitude, timestamp, resolved, action_taken}
[ ] Triggered automatically when drift detected

Files:
└─ /opt/master_of_puppets/analytics/embedding_tasks.py

Success criteria:
✓ Every drift event gets embedded
✓ Metadata searchable
✓ ChromaDB collection grows over time

Estimated tokens: ~6,000
Autonomous: YES
```


#### Task 4.2: Similarity Search for Alarm Triage

```
Trello Card: "🟢 Enhance Alarm Triage with Vector Search"

Subtasks:
[ ] Modify alarm_triage_tasks.py
[ ] When drift alert received:
    [ ] Generate query embedding
    [ ] Search ChromaDB for top 5 similar past events
    [ ] Return: historical context, what worked before
[ ] Include in report: "87% similar to event on Jan 15 (bearing failure)"

Files:
├─ Modify: alarm_triage_tasks.py
└─ Add method: find_similar_events()

Success criteria:
✓ Alarm Triage queries vector DB
✓ Returns relevant past events
✓ Confidence score included

Estimated tokens: ~7,500
Autonomous: YES
```


#### Task 4.3: Cross-Vendor Pattern Learning

```
Trello Card: "🟢 Enable Cross-Vendor Pattern Matching"

Subtasks:
[ ] Modify embedding query to ignore vendor tag initially
[ ] Search: "vibration drift" (no vendor filter)
[ ] Results: Both S7 AND AB drift events
[ ] Learn: "Bearing failure pattern is vendor-agnostic"
[ ] Tag universal patterns in metadata

Files:
└─ Create: pattern_learner_tasks.py

Success criteria:
✓ Can find S7 pattern when AB drifts
✓ Identifies universal failure signatures
✓ Reports: "This AB drift matches S7 pattern"

Estimated tokens: ~8,000
Autonomous: YES
```


#### Task 4.4: Feedback Loop (The Weaver + Workflow Tracker)

```
Trello Card: "🟢 Build Outcome Tracking for Learning"

Subtasks:
[ ] When Mike responds to alert via WhatsApp:
    - "Fixed bearing" → log as resolved
    - "False alarm" → log as false positive
[ ] Update ChromaDB metadata: {resolved: true, action: "replaced_bearing"}
[ ] Next similar drift: "Last time this pattern occurred, replacing bearing fixed it"
[ ] Workflow Tracker logs all outcomes

Files:
└─ Create: outcome_tracker_tasks.py

Success criteria:
✓ Mike's responses update vector DB
✓ Future alerts include "what worked last time"
✓ System learns from outcomes

Estimated tokens: ~9,000
Autonomous: YES
```


### Phase 4 Success Criteria

```
[ ] Vector DB operational, embeddings stored
[ ] Alarm Triage uses similarity search
[ ] Cross-vendor patterns detected
[ ] System learns from Mike's feedback
[ ] Test: Similar drift on different PLCs triggers same diagnosis
```


***

## Phase 5: Autonomy + Grafana Dashboards (Week 5)

**Goal:** Auto-execute approved actions, visualization, full 24/7 operation

### Mike's Manual Actions

```
Trello Card: "🟡 MIKE: Configure Auto-Execution Whitelist"

Instructions:
Define which actions The Conductor can execute WITHOUT asking Mike.

Checklist:
[ ] Create whitelist in config:
    auto_approve:
      - "reduce_motor_speed_to_60pct"  # Safe
      - "send_alert_to_backup_tech"     # Informational
    require_approval:
      - "shutdown_motor"                # Risky
      - "modify_plc_program"            # Never auto
[ ] Test with non-critical action first

Estimated time: 20 minutes
```

```
Trello Card: "🟡 MIKE: Build Grafana Dashboards"

Checklist:
[ ] Login to Grafana (localhost:3000 or ngrok URL)
[ ] Create dashboard: "PLC Health Overview"
    [ ] Panel: Real-time heatmap (all sensors)
    [ ] Panel: Drift alerts timeline
    [ ] Panel: Cross-vendor comparison (S7 vs AB)
[ ] Create dashboard: "Agent Activity"
    [ ] Panel: Tasks executed per hour
    [ ] Panel: Token usage by agent
    [ ] Panel: Success/failure rates
[ ] Share URLs via WhatsApp when asked

Estimated time: 1 hour
```


### Monkey's Autonomous Tasks

#### Task 5.1: Auto-Execution Engine

```
Trello Card: "🟢 Build Autonomous Action Executor"

Subtasks:
[ ] Create action_executor_tasks.py
[ ] Task: execute_action(action, params, require_approval)
[ ] If action in whitelist:
    [ ] Execute immediately
    [ ] Log to Workflow Tracker
    [ ] Notify Mike: "Auto-executed: {action}"
[ ] If action requires approval:
    [ ] Send WhatsApp: "Approve? Y/N"
    [ ] Wait for response (timeout 5 min)
    [ ] Execute if approved
[ ] Examples:
    - reduce_motor_speed(60) → Modbus write to PLC
    - schedule_maintenance(motor_3) → Create work order in CMMS

Files:
└─ /opt/master_of_puppets/execution/action_executor_tasks.py

Success criteria:
✓ Whitelisted actions execute without Mike
✓ Risky actions wait for approval
✓ All executions logged

Estimated tokens: ~10,000
Autonomous: YES
```


#### Task 5.2: Grafana Link Generator

```
Trello Card: "🟢 Generate Grafana Dashboard Links for WhatsApp"

Subtasks:
[ ] When drift alert sent to Mike, include:
    "📊 View heatmap: https://ngrok-url/grafana/d/dashboard?var-sensor=motor_3&from=now-6h"
[ ] Generate time-range URLs dynamically
[ ] Pre-filter to relevant sensor/PLC

Files:
└─ /opt/master_of_puppets/reporting/grafana_links.py

Success criteria:
✓ WhatsApp alerts include clickable Grafana links
✓ Links pre-filtered to relevant data
✓ Time ranges match alert context

Estimated tokens: ~4,000
Autonomous: YES
```


#### Task 5.3: 24/7 Health Monitor

```
Trello Card: "🟢 Build System Health Monitor"

Subtasks:
[ ] Create health_monitor_tasks.py
[ ] Celery Beat task every 5 minutes:
    [ ] Check all collectors alive
    [ ] Check Redis connection
    [ ] Check InfluxDB writable
    [ ] Check ChromaDB accessible
    [ ] Check all agents responding
[ ] If critical failure: Alert Mike + auto-restart service
[ ] Daily summary: "✅ All systems healthy, 47 alerts processed, 3 auto-resolved"

Files:
└─ /opt/master_of_puppets/monitoring/health_monitor_tasks.py

Success criteria:
✓ Detects failures within 5 minutes
✓ Auto-restarts transient failures
✓ Daily summary sent to Mike

Estimated tokens: ~7,000
Autonomous: YES
```


### Phase 5 Success Criteria

```
[ ] System runs 24/7 unattended
[ ] Whitelisted actions execute autonomously
[ ] Grafana dashboards accessible via WhatsApp
[ ] Health monitor prevents silent failures
[ ] Mike wakes up to daily summary, not 3am alerts (unless critical)
```


***

## Phase 6: Advanced Features (Week 6+)

**Goal:** Claude Code integration, Factory I/O simulation, predictive maintenance

### Tasks (Lower Priority, Build After Phase 5)

```
├─ "🟢 Integrate Claude Code FastAPI Bridge"
├─ "🟢 Connect Factory I/O for Fault Simulation"
├─ "🟢 Build Predictive Maintenance Model (LSTM on drift velocity)"
├─ "🟢 Multi-Facility Support (separate Trello boards per plant)"
├─ "🟢 Export System to Kubernetes for Production"
```


***

## Trello Automation (Monkey's Self-Management)

### Card Template for Every Task

```yaml
Card Name: "[🟢/🟡] {Task Name}"

Description:
Goal: {What this accomplishes}
Files: {What gets created/modified}
Success Criteria: {How to verify it works}
Estimated Tokens: {Cost forecast}
Autonomous: YES/NO

Checklist:
[ ] Subtask 1
[ ] Subtask 2
[ ] Test and verify
[ ] Update documentation
[ ] Move to Review

Labels: [Infrastructure/Agent Dev/Integration]
Due Date: {End of current phase}
Assigned: The Monkey
```


### Monkey's Workflow

```python
# The Monkey manages itself via Trello API

@app.task
def monkey_self_manage():
    # 1. Check current sprint cards
    cards = trello.get_list("Current Sprint")
    
    # 2. Pick next autonomous task (🟢 label)
    task = cards.filter(label="🟢 Autonomous", status="TODO")[0]
    
    # 3. Check token budget
    if monkey.budget_remaining() < task.estimated_tokens:
        alert_mike("Budget depleted, pausing until next cycle")
        return
    
    # 4. Execute task (call Claude Code or Anthropic API)
    result = execute_task(task)
    
    # 5. Test the code
    if test_passes(result):
        trello.move_card(task, "Review Needed")
        alert_mike(f"✅ {task.name} complete, please review")
    else:
        trello.add_comment(task, f"❌ Tests failed: {error}")
        # Retry with different approach
    
    # 6. Track token usage
    monkey.track_usage(task.id, result.tokens_used)
    
    # 7. Pick next task (loop)
```


***

## Mike's Action Summary (Everything You Must Do)

### Week 1: Foundation

- [ ] Start Redis container
- [ ] Install Celery + Flower
- [ ] Create /opt/master_of_puppets/ directory
- [ ] Set .env variables
- [ ] Verify WhatsApp API connected


### Week 2: Hardware

- [ ] Connect S7-1200 to network (192.168.0.1)
- [ ] Connect Micro820 to network (192.168.0.2)
- [ ] Connect BeagleBone via USB
- [ ] Install InfluxDB + Grafana (Docker)
- [ ] Expose Grafana via ngrok
- [ ] Create simple test programs on PLCs


### Week 3: Baseline

- [ ] Let system run 48 hours in "normal" mode
- [ ] Don't simulate faults yet
- [ ] Approve baseline calculation when notified


### Week 4: Minimal

- [ ] Install ChromaDB (Docker or embedded)
- [ ] Test vector DB connection


### Week 5: Autonomy

- [ ] Define auto-execution whitelist
- [ ] Build Grafana dashboards (1 hour)
- [ ] Test auto-execution with safe action


### Ongoing:

- [ ] Respond to WhatsApp alerts (Y/N for approvals)
- [ ] Provide feedback on outcomes ("fixed bearing", "false alarm")
- [ ] Monitor daily summaries

**Total Manual Time: ~6-8 hours spread over 5 weeks**

***

## Success Metrics (How to Know It's Working)

### Week 1

- ✓ Flower dashboard shows 8 workers online
- ✓ Can send test task to each agent


### Week 2

- ✓ All 3 PLCs logging data to InfluxDB
- ✓ Grafana shows real-time charts


### Week 3

- ✓ Baselines calculated
- ✓ Drift detector triggers on simulated fault
- ✓ Alert received on WhatsApp within 60 seconds


### Week 4

- ✓ Vector DB has >10 embedded drift events
- ✓ Similarity search returns relevant past events
- ✓ Cross-vendor pattern detected


### Week 5

- ✓ Whitelisted action executed autonomously
- ✓ System runs 24 hours with no Mike intervention
- ✓ Daily summary received

***

## Prompt for The Monkey to Start

```
You are The Monkey, the autonomous agent orchestrator and token budget enforcer for the Master of Puppets system.

Your mission: Build the Industrial AI Swarm according to the phased plan above.

Phase 1 starts now. Your first tasks:

1. Create Trello board "Industrial AI Swarm - Master Build"
2. Import all tasks from this plan into the Backlog list
3. Move Phase 1 tasks to "Current Sprint"
4. Begin with Task 1.1: "Create Celery App + Worker Template"
5. After each task:
   - Test the code
   - Move to "Review Needed" if passing
   - Track token usage
   - Pick next autonomous (🟢) task

Rules:
- Only work on 🟢 Autonomous tasks without Mike
- Stop and alert Mike for 🟡 tasks
- Stay within 50,000 tokens/day budget
- Generate production-ready code (no TODOs)
- Test everything before marking complete

Mike will approve/test tasks in "Review Needed" and unblock 🟡 tasks.

Begin Phase 1. Report progress every 4 hours.
```


***

**Want me to:**

1. Generate the Trello board JSON you can import?
2. Create the complete docker-compose.celery.yml file?
3. Write the initial celery_app.py + base_worker.py templates?

This is ready to execute. The Monkey can bootstrap itself from here.

