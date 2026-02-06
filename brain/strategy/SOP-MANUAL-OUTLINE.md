# FactoryLM SOP Manual - Master Outline
*Standard Operating Procedures for Industrial AI Platform*

**Generated:** 2026-02-06
**Status:** Phase 1 Discovery Complete

---

## Book Structure

### Part I: Foundation

**Chapter 1: System Overview**
- What is FactoryLM?
- Vision: AI for Industrial Maintenance
- The Three-Tier Architecture (Edge → Local → Cloud)
- Key Value Proposition

**Chapter 2: Architecture Deep Dive**
- System Diagram
- Data Flow (Input → Processing → Output)
- Component Inventory
- Technology Stack

### Part II: Communication Layer

**Chapter 3: Telegram Integration**
- Clawdbot Gateway Configuration
- Message Handling Pipeline
- Voice Message Processing
- User Authentication

**Chapter 4: Voice & Input Systems**
- Text-to-Speech (TTS) Configuration
- Speech-to-Text (STT) via RealtimeSTT
- Wake Word Detection
- Input Processing Pipeline

### Part III: Intelligence Layer

**Chapter 5: Claude AI Integration**
- Model Configuration
- Prompt Engineering
- Context Management
- Tool Calling Architecture

**Chapter 6: Memory Systems**
- Daily Memory Files (`memory/YYYY-MM-DD.md`)
- Long-term Memory (`MEMORY.md`)
- Knowledge Base Structure
- Memory Search & Recall

**Chapter 7: Agent Architecture**
- AGENTS.md Configuration
- SOUL.md Personality
- Heartbeat System
- Cron Jobs & Scheduled Tasks

### Part IV: Knowledge Management

**Chapter 8: Brain Structure**
- Directory Organization
- Research Documents
- Strategy Documents
- Proof Package Collection

**Chapter 9: GitHub Integration**
- Repository Management
- Issue Tracking
- Branch Strategy
- Engineering Commandments

### Part V: Industrial Integration

**Chapter 10: PLC Communication**
- Micro820 Setup
- Connected Components Workbench (CCW)
- Modbus Protocol
- I/O Mapping

**Chapter 11: VFD Control**
- DURApulse VFD Configuration
- VFD Simulator Software
- Speed/Frequency Control
- Fault Handling

**Chapter 12: Sensor Integration**
- Analog Inputs (4-20mA)
- Digital I/O
- Protocol Support (Modbus, Ethernet/IP)
- Future: IO-Link, HART

**Chapter 13: CMMS Integration**
- Work Order Creation
- Asset Management
- Photo-to-Entry Pipeline
- Maintenance Workflows

### Part VI: Simulation & Testing

**Chapter 14: Factory I/O**
- Scene Configuration
- PLC Driver Setup
- Digital Twin Concept
- Demo Scenarios

**Chapter 15: VFD Simulator**
- Installation & Setup
- Modbus TCP Server
- Web UI Operation
- PLC Integration Testing

### Part VII: Infrastructure

**Chapter 16: Network Architecture**
- Tailscale VPN Setup
- Device Inventory
- Remote Access
- Security Considerations

**Chapter 17: Server Operations**
- VPS Configuration
- Service Management
- Docker Containers
- Monitoring & Alerts

**Chapter 18: Jarvis Node System**
- Windows Installation
- Remote Control Capabilities
- Resource Monitoring
- Deployment Guide

### Part VIII: Operations

**Chapter 19: Daily Operations**
- Heartbeat Monitoring
- Health Checks
- Alert Response
- Routine Maintenance

**Chapter 20: Robot Army**
- Agent Inventory
- Task Scheduling
- Status Reporting
- Autonomous Operations

### Part IX: Demo System

**Chapter 21: YC Demo Build**
- Conveyor Hardware
- VFD + Motor Setup
- PLC Programming
- Full System Integration

**Chapter 22: Proof Package**
- Evidence Collection
- Before/After Documentation
- Video Recording
- Metrics & Results

### Appendices

**Appendix A: Quick Reference**
- Command Cheat Sheet
- Common Troubleshooting
- Key File Locations

**Appendix B: Configuration Files**
- AGENTS.md Template
- SOUL.md Template
- Clawdbot Config

**Appendix C: API Reference**
- Modbus Register Maps
- REST Endpoints
- WebSocket Protocols

---

## Source Inventory

### GitHub Repositories
- `mikecranesync/factorylm` - Main platform
- `mikecranesync/jarvis-workspace` - Workspace
- `mikecranesync/Rivet-PRO` - Product repo
- `mikecranesync/remoteme-jarvis-node` - Jarvis Node
- `mikecranesync/cmms` - CMMS fork
- `mikecranesync/clawdbot` - Clawdbot fork
- `mikecranesync/factorylm-landing` - Website

### Memory Files
- `memory/2026-01-31.md` through `memory/2026-02-05.md`
- `MEMORY.md` - Long-term memory

### Brain Documents
- `brain/strategy/` - Strategy documents
- `brain/research/` - Research documents
- `brain/specs/` - Specifications
- `brain/proof-package/` - Evidence collection

### Products
- `products/vfd-simulator/` - VFD Simulator
- `products/website/` - Website source
- `products/tier2-connect/` - Tier 2 connector

---

## Generation Plan

1. Create HTML template with consistent styling
2. Generate each chapter as separate HTML file
3. Build navigation/index page
4. Host at `factorylm.com/docs/sop/`
5. Add search functionality (future)

---

*Next: Generate Chapter 1 HTML*
