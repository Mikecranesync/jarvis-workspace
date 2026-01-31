# ShopTalk Knowledge Base

Centralized knowledge for all agents to reference.

## Structure

```
knowledge/
├── README.md           # This file
├── index.json          # Searchable index of all knowledge
├── devices/            # PLC and device profiles
├── faults/             # Fault patterns and diagnostics
├── procedures/         # Maintenance procedures
├── research/           # Technical research (symlink to brain/research)
└── config/             # System configurations
```

## Usage

All agents should use `memory_search` to query this knowledge base before answering questions about:
- PLC configurations
- Device profiles
- Fault diagnostics
- Auto-connect procedures
- Technical specifications

## Auto-Connect Knowledge

See `devices/` for PLC profiles and auto-discovery configurations.
