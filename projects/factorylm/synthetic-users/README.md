# FactoryLM Synthetic Users

**Created:** 2026-01-31
**Purpose:** 46 synthetic beta testers for A/B testing FactoryLM

## Structure

```
synthetic-users/
├── personas/           # Individual user persona files
│   ├── technicians/    # 15 maintenance technicians
│   ├── managers/       # 8 maintenance managers
│   ├── plant-managers/ # 6 plant managers
│   ├── engineers/      # 5 reliability engineers
│   ├── latam/          # 5 Spanish-speaking users
│   ├── it-specialists/ # 4 IT/integration specialists
│   └── executives/     # 3 C-suite executives
├── scripts/            # Automation scripts
├── activities/         # Activity templates by role
└── logs/               # Activity logs
```

## User Breakdown

| Role | Count | Tech Comfort | Primary Activities |
|------|-------|--------------|-------------------|
| Maintenance Technician | 15 | Low-Medium | Work orders, parts lookup, mobile |
| Maintenance Manager | 8 | Medium | Scheduling, reports, team mgmt |
| Plant Manager | 6 | Medium | Analytics, KPIs, approvals |
| Reliability Engineer | 5 | High | PM schedules, failure analysis |
| LATAM Spanish Speaker | 5 | Varied | All activities in Spanish |
| IT Specialist | 4 | Very High | Integrations, imports, API |
| C-Suite Executive | 3 | Low | Dashboards, ROI reports |

## Usage

```bash
# Run single user simulation
python scripts/simulate_user.py --persona personas/technicians/bob-martinez.yaml

# Run all users (parallel)
python scripts/run_all.py --parallel 5

# Run specific role group
python scripts/run_all.py --role technicians
```

## Integration

Uses:
- browser-use for browser automation
- synthetic-user-research for persona prompting
- Whisper for voice interactions (optional)
