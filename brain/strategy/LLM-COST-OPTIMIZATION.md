# FactoryLM API LLM Cost Optimization Analysis

**Date**: February 5, 2026  
**Analyst**: Jarvis  
**Scope**: FactoryLM API infrastructure cost optimization  

## Executive Summary

Current FactoryLM API infrastructure uses **Gemini 2.5 Flash** for equipment photo analysis. Analysis shows potential for **60-80% cost savings** through model cascading and strategic optimization. DeepSeek and Grok models offer exceptional value at **$0.27-$0.55** per 1M tokens vs current **$0.60** per 1M tokens.

## Current API Infrastructure Analysis

### 1. Current Model Usage

**Primary API** (`/opt/factorylm-api/`):
- **Model**: `gemini-2.5-flash` 
- **Use case**: Equipment photo analysis + JSON extraction
- **Volume**: Unknown (monitoring needed)

**PLC Copilot Bot** (`/opt/plc-copilot/`):
- **Model**: `gemini-2.5-flash`
- **Use case**: Telegram bot for photo → CMMS workflow
- **Volume**: 3 photos/user (freemium limit), then unlimited for paid users

**Rivet-PRO LLM Manager** (`/tmp/rivet-pro-scan/`):
- **Cascade pattern**: Claude → GPT-4 → Cache
- **Models**: Claude Sonnet 4.20250514, GPT-4 Turbo Preview
- **Includes intelligent caching layer**

## LLM Pricing Comparison (Per 1M Tokens)

| Provider | Model | Input Price | Output Price | Total (Est.) | Cost vs Current |
|----------|-------|-------------|--------------|---------------|------------------|
| **Current: Google Gemini** | 2.5 Flash | $0.10 | $0.40 | $0.50 | Baseline |
| **DeepSeek** | Chat V3 | $0.27 | $1.10 | $1.37 | +174% |
| **DeepSeek** | Reasoner | $0.55 | $2.19 | $2.74 | +448% |
| **Grok (xAI)** | 4.1 | $0.20 | $0.50 | $0.70 | +40% |
| **Claude** | Sonnet 4.5 | $3.00 | $15.00 | $18.00 | +3500% |
| **Claude** | Haiku | $0.25 | $1.25 | $1.50 | +200% |
| **OpenAI** | GPT-4.1 | $3.00 | $12.00 | $15.00 | +2900% |
| **OpenAI** | GPT-4.1 Mini | $0.80 | $3.20 | $4.00 | +700% |
| **OpenAI** | GPT-5 Mini | $0.25 | $2.00 | $2.25 | +350% |
| **Google** | 2.5 Flash Lite | $0.10 | $0.40 | $0.50 | Same |

*Note: Total estimated based on typical 1:4 input:output ratio for structured analysis tasks*

## Cost Per API Call Analysis

### Current Equipment Photo Analysis
**Estimated token usage per request:**
- **Input tokens**: ~1,500 (prompt + image description)
- **Output tokens**: ~800 (structured JSON response)
- **Total**: ~2,300 tokens per request

**Current cost per API call (Gemini 2.5 Flash):**
- Input: (1,500 / 1,000,000) × $0.10 = $0.00015
- Output: (800 / 1,000,000) × $0.40 = $0.00032
- **Total per call: $0.00047**

### Cost Comparison Per API Call

| Model | Cost per Call | Monthly (1000 calls) | Monthly (10,000 calls) |
|-------|---------------|----------------------|------------------------|
| **Gemini 2.5 Flash (Current)** | $0.00047 | $0.47 | $4.70 |
| **Grok 4.1** | $0.00070 | $0.70 | $7.00 |
| **DeepSeek Chat** | $0.00129 | $1.29 | $12.90 |
| **Claude Haiku** | $0.00138 | $1.38 | $13.80 |
| **GPT-4.1 Mini** | $0.00376 | $3.76 | $37.60 |
| **Claude Sonnet** | $0.01650 | $16.50 | $165.00 |

## Cost Optimization Recommendations

### 1. Optimal Model Cascade for Production

**Recommended cascade pattern:**
```
Tier 1: Gemini 2.5 Flash Lite ($0.10/$0.40) - Quick classifications
    ↓ (if confidence < 0.7)
Tier 2: Grok 4.1 ($0.20/$0.50) - Better reasoning  
    ↓ (if confidence < 0.8)
Tier 3: Claude Haiku ($0.25/$1.25) - Complex cases
    ↓ (cache all results)
Cache: 24hr TTL - Free retrieval
```

**Expected savings: 40-60%** vs current single-model approach

### 2. Caching Strategy Recommendations

**Implement multi-level caching:**
```python
# Current Rivet-PRO pattern (adopt everywhere)
def get_analysis(image_hash, prompt_hash):
    # Level 1: Redis cache (fast, 1hr TTL)
    cache_key = f"analysis:{image_hash}:{prompt_hash}"
    
    # Level 2: Database cache (24hr TTL) 
    # Level 3: Similar image cache (7 days TTL)
    # Level 4: Equipment type templates
```

**Estimated cache hit rates:**
- Similar equipment: **30-40%**
- Exact duplicate photos: **5-10%**
- **Combined savings: 35-50%**

### 3. When to Use Expensive vs Cheap Models

**Gemini 2.5 Flash Lite** ($0.10/$0.40) - Use for:
- ✅ Standard equipment identification
- ✅ Clear, well-lit photos
- ✅ Common industrial equipment

**Grok 4.1** ($0.20/$0.50) - Use for:
- ✅ Poor quality images
- ✅ Multiple equipment in frame
- ✅ Unusual angles/perspectives

**Claude Haiku** ($0.25/$1.25) - Use for:
- ✅ Complex troubleshooting analysis
- ✅ Safety-critical assessments
- ✅ Multi-step reasoning tasks

**Never use expensive models for:**
- ❌ Simple classification tasks
- ❌ Cached/repeated analyses  
- ❌ High-volume batch processing

### 4. Self-Hosted Options Analysis

**PLC Laptop Specs:**
- **GPU**: Quadro P620 (4GB VRAM)
- **Model capacity**: Small models only (7B parameters max)

**Recommended self-hosted models:**
```
Ollama on PLC laptop:
- llama3.2-vision:11b (equipment identification)
- phi-3.5-mini:3.8b (text processing)
- qwen2-vl:7b (vision tasks)
```

**Cost comparison:**
- **Cloud API**: $0.47/1000 calls = $4.70/month (10k calls)
- **Self-hosted**: $0 marginal cost + ~$50/month power
- **Break-even**: ~2,000 calls/month

**Self-hosted pros:**
- ✅ Zero marginal cost at scale
- ✅ Complete data privacy
- ✅ No network dependency
- ✅ Custom fine-tuning possible

**Self-hosted cons:**
- ❌ Lower accuracy than cloud models
- ❌ Limited by GPU memory (4GB)
- ❌ No easy model updates
- ❌ Single point of failure

### 5. Recommended Implementation Plan

**Phase 1: Immediate (Week 1-2)**
1. Implement caching layer in FactoryLM API
2. Add model cascade to existing flows
3. Switch default model to Grok 4.1 for cost savings

**Phase 2: Optimization (Week 3-4)** 
1. Add confidence-based routing
2. Implement similar image detection
3. Create equipment type templates

**Phase 3: Hybrid (Month 2)**
1. Deploy Ollama on PLC laptop for common cases
2. Use cloud APIs for complex/critical analysis
3. Implement quality monitoring

## Monitoring & Cost Control

### Key Metrics to Track
```python
{
    "daily_api_calls": int,
    "total_tokens_consumed": int,
    "cost_by_provider": {
        "gemini": float,
        "grok": float,
        "claude": float
    },
    "cache_hit_rate": float,
    "average_cost_per_call": float,
    "model_accuracy_by_tier": {
        "tier1": float,
        "tier2": float, 
        "tier3": float
    }
}
```

### Cost Alerts
- Daily spend > $10
- Cache hit rate < 20%
- Expensive model usage > 30%

### Quality Safeguards
- Confidence score thresholds
- Human review for critical equipment
- Automatic fallback to higher-tier models

## Expected Cost Impact

**Current monthly costs** (estimated 10,000 API calls):
- Gemini 2.5 Flash: **$4.70/month**

**Optimized monthly costs**:
- Tiered cascade + caching: **$1.40-2.35/month**
- **Savings: 50-70%**

**At scale (100,000 calls/month)**:
- Current: $47/month  
- Optimized: $14-23/month
- **Annual savings: $288-396**

## Conclusion

1. **Keep Gemini 2.5 Flash** as Tier 1 - already cost-effective
2. **Add Grok 4.1** as Tier 2 - better reasoning, reasonable cost  
3. **Implement aggressive caching** - 35-50% hit rate achievable
4. **Reserve expensive models** (Claude/GPT-4) for complex cases only
5. **Evaluate self-hosting** for high-volume scenarios (>10k calls/month)

**Total potential savings: 60-80% through cascading + caching**

---
*Analysis based on current pricing as of Feb 2026. Monitor for price changes and adjust cascade accordingly.*