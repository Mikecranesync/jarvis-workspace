# Competitive Analysis: Industrial Predictive Maintenance on GitHub
**Agent:** Research Agent  
**Timestamp:** 2026-01-29 14:13 UTC  
**Request:** Mike asked for market research on similar projects

---

## Repo 1: Predictive-Maintenance-Using-ML
**Author:** jashwanth-04  
**URL:** https://github.com/jashwanth-04/Predictive-Maintenance-Using-ML  
**Live Demo:** https://predictive-maintenance-using-machine-learning.streamlit.app/

### What They Built
- Random Forest classifier for machine failure prediction
- Streamlit web UI for input and prediction
- Uses synthetic dataset (10,000 data points, 14 features)

### Features
- Predicts: Temperature, RPM, torque, tool wear → failure yes/no
- Simple pass/fail output with confidence
- Web-based interface

### Maturity: 🟡 Prototype
- Single model (Random Forest)
- Synthetic data only
- No CMMS integration
- No real-time monitoring
- No mobile/wearables

### Gap vs FactoryLM
| They Have | They Don't Have |
|-----------|-----------------|
| ML prediction | CMMS integration |
| Web UI | Real-time PLC data |
| Demo app | Mobile/AR interface |
| | Multi-model approach |
| | Technician workflow |

---

## Repo 2: Predictive Maintenance for Industrial Robots
**Author:** mriusero  
**URL:** https://github.com/mriusero/predictive-maintenance-on-industrial-robots

### What They Built
- Predictive maintenance for robots in **nuclear fuel replacement**
- Focus on Remaining Useful Life (RUL) prediction
- Decision-making framework for robot fleet management
- Multiple models: Random Forest, LSTM, Gradient Boosting

### Features
- Phase I: Predict if robot stays operational for 6 months
- Phase II: Decide whether to replace robots before missions
- Time-series analysis with feature engineering
- Streamlit dashboard
- Docker deployment ready

### Maturity: 🟢 More Advanced
- Multi-phase approach
- Decision-making framework (not just prediction)
- Time-series ML (LSTM)
- Real scenario testing data

### Gap vs FactoryLM
| They Have | They Don't Have |
|-----------|-----------------|
| RUL prediction | Real-time integration |
| Decision framework | CMMS/ticketing |
| Multi-model | AR/wearables |
| Docker deploy | Technician UX |
| | PLC connectivity |
| | Knowledge graphs |

---

## Repo 3: AI Kavach (Hackathon Project)
**Author:** adityapotdar23  
**URL:** https://github.com/adityapotdar23/Predictive-Maintenance

### What They Built
- Hackathon project (IEEE Aeravat 1.0)
- Industrial equipment failure prediction
- Proactive maintenance scheduling

### Maturity: 🔴 Early/Hackathon
- Hackathon-quality code
- Likely prototype only

---

## Repo 4: NVIDIA DLI Workshop
**Author:** HROlive  
**URL:** https://github.com/HROlive/Applications-of-AI-for-Predictive-Maintenance

### What They Built
- Educational content from NVIDIA workshop
- XGBoost + LSTM models
- Anomaly detection with autoencoders
- RUL estimation

### Maturity: 🟡 Educational
- Training materials, not product
- Good reference for techniques
- No deployment story

---

## Repo 5: Interactive Maintenance Dashboard
**Author:** rohanmatt  
**URL:** https://github.com/rohanmatt/Predictive-Maintenance-for-Industrial-Equipment

### What They Built
- Web dashboard for predictive maintenance
- Historical data visualization
- RUL prediction
- Anomaly detection
- Maintenance status display

### Maturity: 🟡 Prototype
- Good UI/UX thinking
- Visualization focus
- No backend integration

---

## Market Summary

### What Everyone's Building
✅ ML models (Random Forest, LSTM, XGBoost)  
✅ Failure prediction (pass/fail)  
✅ RUL estimation  
✅ Web dashboards (Streamlit mostly)  
✅ Synthetic/academic datasets  

### What NOBODY Has
❌ **Real PLC integration** (your strength)  
❌ **CMMS integration** (your strength)  
❌ **AR/Smart glasses** (your roadmap)  
❌ **Technician-first UX** (your focus)  
❌ **Per-machine knowledge graphs** (your vision)  
❌ **Closed-loop learning** (your differentiator)  
❌ **Domain-specific LLM** (your endgame)  

---

## Competitive Position

```
                    ML Sophistication
                          ↑
                          │
    Academic/Research ────┼──── Enterprise Solutions
         (mriusero)       │      (PTC, IBM, SAP)
                          │
                          │     ★ FactoryLM Target
                          │       (ML + Integration + UX)
                          │
    Hackathon Projects ───┼──── Basic Demos
     (AI Kavach)          │     (jashwanth-04)
                          │
                          └────────────────────→
                              Real-World Integration
```

**Your position:** You're building the bridge between academic ML and real-world industrial deployment. That's the gap nobody's filling.

---

## Potential Collaborators/Acqui-hires

| Repo | Why Interesting |
|------|-----------------|
| mriusero | Multi-phase RUL + decision framework |
| HROlive | NVIDIA techniques reference |
| rohanmatt | UI/UX patterns for dashboards |

---

## Recommendations

1. **Don't compete on ML sophistication** — they all have decent models
2. **Win on integration** — PLC + CMMS + workflow
3. **Win on UX** — technician-first, not data-scientist-first  
4. **Win on deployment** — real equipment, not synthetic data
5. **Win on wearables** — nobody's doing AR glasses

**Your moat:** Domain expertise + full-stack integration + technician workflow

---

*These are your people, but you're ahead of them on the integration and deployment side.*
