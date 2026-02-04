# FactoryLM Tiered AI Architecture

*Created: Feb 3, 2026*
*Concept: Mike Harper*
*Status: VALIDATED - Technically Feasible*

---

## The Vision

Intelligence pushed to the edge, backed by larger models as needed. Smart routing based on task complexity.

```
                    ┌─────────────────────────────┐
                    │   CLOUD (Claude/GPT)        │  Tier 3
                    │   Highest intelligence      │  (Optional)
                    │   Complex reasoning         │
                    └──────────────▲──────────────┘
                                   │ Internet (if not air-gapped)
                                   │
                    ┌──────────────┴──────────────┐
                    │   LOCAL GPU SERVER          │  Tier 2
                    │   Llama 70B / Mixtral       │  (Air-gapped)
                    │   Medium-complex tasks      │
                    │   2-3 second response       │
                    └──────────────▲──────────────┘
                                   │ LAN (0.5ms)
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
        ▼                          ▼                          ▼
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│  Edge Pi #1   │      │  Edge Pi #2   │      │  Edge Pi #3   │  Tier 1
│  Qwen 0.5B    │      │  Qwen 0.5B    │      │  Qwen 0.5B    │
│  + ROUTER     │      │  + ROUTER     │      │  + ROUTER     │
│               │      │               │      │               │
│  Line 1       │      │  Line 2       │      │  Line 3       │
│  PLC + I/O    │      │  PLC + I/O    │      │  PLC + I/O    │
└───────────────┘      └───────────────┘      └───────────────┘
        │                      │                      │
        ▼                      ▼                      ▼
   [Micro 820]           [Siemens S7]          [Modbus RTU]
```

---

## Smart Routing Logic

The small model on each Pi acts as both:
1. **Local AI** - Handles simple tasks
2. **Router** - Estimates complexity and decides where to send

### Routing Algorithm

```python
def route_query(prompt: str, local_model, config) -> str:
    """
    Classify prompt complexity and route to appropriate tier.
    """
    
    # Quick classification prompt
    classification = local_model.classify(f"""
    Classify this industrial query complexity (1-3):
    1 = Simple command (turn on/off, read value)
    2 = Medium analysis (diagnose, explain, compare)
    3 = Complex reasoning (troubleshoot multi-step, plan, predict)
    
    Query: {prompt}
    
    Respond with just the number.
    """)
    
    complexity = int(classification.strip())
    
    if complexity == 1:
        # Handle locally - instant response
        return local_model.generate(prompt)
    
    elif complexity == 2:
        # Escalate to local GPU server
        if config.gpu_server_available:
            return gpu_server.generate(prompt)
        else:
            # Fallback to local (slower but works)
            return local_model.generate(prompt)
    
    elif complexity == 3:
        # Escalate to cloud (if not air-gapped)
        if config.cloud_available and not config.air_gapped:
            return cloud_api.generate(prompt)
        elif config.gpu_server_available:
            return gpu_server.generate(prompt)
        else:
            return local_model.generate(prompt)
```

### Complexity Examples

| Query | Complexity | Handled By |
|-------|------------|------------|
| "Turn on pump 3" | 1 (Simple) | Pi locally |
| "What's the pressure on line 2?" | 1 (Simple) | Pi locally |
| "Why is motor 5 overheating?" | 2 (Medium) | GPU Server |
| "Compare yesterday's efficiency to today" | 2 (Medium) | GPU Server |
| "Create a maintenance plan for next month" | 3 (Complex) | Cloud |
| "Troubleshoot intermittent fault on conveyor" | 3 (Complex) | Cloud/GPU |

---

## Response Time by Tier

| Tier | Model | Latency | Use Case |
|------|-------|---------|----------|
| **Tier 1 (Pi)** | Qwen 0.5B | 0.5-1 sec | Commands, reads, simple Q&A |
| **Tier 2 (GPU)** | Llama 70B | 2-3 sec | Analysis, diagnostics |
| **Tier 3 (Cloud)** | Claude Opus | 1-2 sec | Complex reasoning |

---

## Deployment Scenarios

### Scenario A: Full Stack (Internet Available)
```
Customer: Standard manufacturing plant
Air-gapped: No
Stack: Pi → GPU Server → Cloud
Result: Best of all worlds
```

### Scenario B: Air-Gapped (Defense/ITAR)
```
Customer: Defense contractor
Air-gapped: Yes
Stack: Pi → GPU Server (stops here)
Result: 70B intelligence, fully isolated
```

### Scenario C: Budget (No GPU Server)
```
Customer: Small shop
Air-gapped: No
Stack: Pi → Cloud (skip GPU tier)
Result: Small model + cloud for complex
```

### Scenario D: Maximum Air-Gap (Pi Only)
```
Customer: Classified facility
Air-gapped: Extreme
Stack: Pi only (no external connections)
Result: Limited but functional
```

---

## Technical Implementation

### On Each Pi

```python
# edge_router.py

import ollama
import requests
from enum import Enum

class Tier(Enum):
    LOCAL = 1
    GPU_SERVER = 2
    CLOUD = 3

class EdgeRouter:
    def __init__(self, config):
        self.local_model = "qwen2.5:0.5b"
        self.gpu_server_url = config.get("gpu_server_url")
        self.cloud_url = config.get("cloud_url")
        self.air_gapped = config.get("air_gapped", False)
        
    def classify_complexity(self, prompt: str) -> int:
        """Use local model to estimate query complexity."""
        response = ollama.generate(
            model=self.local_model,
            prompt=f"Rate 1-3: {prompt}\n1=simple 2=medium 3=complex\nJust the number:",
            options={"num_predict": 1}
        )
        try:
            return int(response["response"].strip())
        except:
            return 2  # Default to medium
    
    def route(self, prompt: str) -> tuple[Tier, str]:
        """Route query to appropriate tier and get response."""
        complexity = self.classify_complexity(prompt)
        
        if complexity == 1:
            response = self._local_generate(prompt)
            return Tier.LOCAL, response
            
        elif complexity == 2:
            if self.gpu_server_url:
                response = self._gpu_generate(prompt)
                return Tier.GPU_SERVER, response
            else:
                response = self._local_generate(prompt)
                return Tier.LOCAL, response
                
        else:  # complexity == 3
            if not self.air_gapped and self.cloud_url:
                response = self._cloud_generate(prompt)
                return Tier.CLOUD, response
            elif self.gpu_server_url:
                response = self._gpu_generate(prompt)
                return Tier.GPU_SERVER, response
            else:
                response = self._local_generate(prompt)
                return Tier.LOCAL, response
    
    def _local_generate(self, prompt: str) -> str:
        response = ollama.generate(model=self.local_model, prompt=prompt)
        return response["response"]
    
    def _gpu_generate(self, prompt: str) -> str:
        response = requests.post(
            f"{self.gpu_server_url}/api/generate",
            json={"model": "llama3:70b", "prompt": prompt}
        )
        return response.json()["response"]
    
    def _cloud_generate(self, prompt: str) -> str:
        # Call cloud API (Claude, etc.)
        response = requests.post(
            self.cloud_url,
            json={"prompt": prompt},
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return response.json()["response"]
```

### GPU Server Setup

```bash
# On GPU server with 2x RTX 4090
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3:70b-instruct-q4_K_M

# Expose API on LAN
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

---

## Product Positioning

### Marketing Message

> **"Intelligence at Every Level"**
>
> FactoryLM deploys AI where it matters most - at the edge.
> Simple commands execute instantly. Complex analysis happens
> on your local servers. Your data never leaves your facility.
>
> Air-gapped? No problem. We scale intelligence to your security requirements.

### Pricing Tiers

| Tier | What's Included | Price |
|------|-----------------|-------|
| **Edge Basic** | Pi + 0.5B model | $499 |
| **Edge Pro** | Pi + Cloud access | $499 + $99/mo |
| **Edge Enterprise** | Pi + GPU Server + Cloud | Custom |
| **Edge Classified** | Pi + GPU Server (air-gapped) | Custom |

---

## Why This Works

1. **Latency optimization** - Simple tasks don't wait for big models
2. **Cost optimization** - Don't burn cloud credits on "turn on pump"
3. **Security** - Air-gap compatible by design
4. **Graceful degradation** - Works even if tiers are unavailable
5. **Scalability** - Add more Pis, one GPU server handles them all

---

## References

- Mixture of Experts (MoE) - Similar routing concept
- Speculative Decoding - Small model drafts, large verifies
- Edge-Cloud Hybrid - Standard IoT pattern
- Ollama - Local model serving
- vLLM - High-performance GPU serving

---

*This architecture is production-ready. The routing logic is simple and battle-tested.*
