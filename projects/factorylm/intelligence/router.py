#!/usr/bin/env python3
"""
Intelligent Cost Router for FactoryLM

Routes requests through cheapest → most expensive models with quality gates.
Only escalates when cheaper model fails quality check.

Tiers:
1. FREE: Ollama (local LLaVA, llama3.2)
2. CHEAP: Groq (free tier), DeepSeek (~$0.001/call)  
3. PREMIUM: Gemini, Claude (when quality matters)

Usage:
    router = IntelligentRouter()
    result = await router.process(prompt, image_path)
    # Returns best result at lowest cost
"""

import os
import json
import asyncio
import aiohttp
import base64
from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from enum import Enum

# ============================================================================
# CONFIG
# ============================================================================

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyAGRt1kKdBygARiiCv7TiA_tpf4hUjtkJI")

class Tier(Enum):
    FREE = 1      # Ollama local
    CHEAP = 2     # Groq, DeepSeek
    PREMIUM = 3   # Gemini, Claude


@dataclass
class ModelResult:
    """Result from a model call."""
    success: bool
    content: str
    provider: str
    tier: Tier
    cost: float  # Estimated cost in USD
    quality_score: float  # 0-1
    raw_response: Any = None
    error: str = None


@dataclass 
class QualityCheck:
    """Result of quality gate check."""
    passed: bool
    score: float
    reasons: List[str]


# ============================================================================
# QUALITY JUDGE
# ============================================================================

class QualityJudge:
    """Evaluates response quality to decide if escalation needed."""
    
    def __init__(self, min_score: float = 0.6):
        self.min_score = min_score
    
    def evaluate(self, result: ModelResult, expected_format: str = "json") -> QualityCheck:
        """
        Evaluate response quality.
        
        Checks:
        - Format validity (JSON parseable if expected)
        - Content length (not empty/too short)
        - Completeness (key fields present)
        - Coherence (basic sanity checks)
        """
        score = 0.0
        reasons = []
        checks_passed = 0
        total_checks = 4
        
        content = result.content or ""
        
        # 1. Format check
        if expected_format == "json":
            try:
                # Try to extract JSON
                text = content
                if "```json" in text:
                    text = text.split("```json")[1].split("```")[0]
                elif "```" in text:
                    text = text.split("```")[1].split("```")[0]
                
                parsed = json.loads(text)
                checks_passed += 1
                
                # Check for key fields
                key_fields = ["text_content", "summary", "document_type"]
                fields_present = sum(1 for f in key_fields if parsed.get(f))
                if fields_present >= 2:
                    checks_passed += 0.5
                    
            except (json.JSONDecodeError, IndexError):
                reasons.append("Invalid JSON format")
        else:
            # Plain text - just check it exists
            if len(content) > 20:
                checks_passed += 1
        
        # 2. Content length check
        if len(content) > 100:
            checks_passed += 1
        elif len(content) > 50:
            checks_passed += 0.5
        else:
            reasons.append("Response too short")
        
        # 3. Not an error/refusal
        error_indicators = ["i cannot", "i'm unable", "error", "failed", "sorry"]
        if not any(ind in content.lower()[:100] for ind in error_indicators):
            checks_passed += 1
        else:
            reasons.append("Possible error or refusal")
        
        # 4. Has actual content (not just boilerplate)
        if any(char.isdigit() for char in content) or len(content) > 200:
            checks_passed += 1
        else:
            reasons.append("May lack specific content")
        
        score = checks_passed / total_checks
        passed = score >= self.min_score
        
        if passed:
            reasons = ["Quality check passed"]
        
        return QualityCheck(passed=passed, score=score, reasons=reasons)


# ============================================================================
# MODEL PROVIDERS
# ============================================================================

async def call_ollama(prompt: str, image_path: str = None, model: str = "llava") -> ModelResult:
    """Call local Ollama."""
    try:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        
        if image_path:
            with open(image_path, "rb") as f:
                payload["images"] = [base64.b64encode(f.read()).decode()]
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{OLLAMA_URL}/api/generate",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=120)
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return ModelResult(
                        success=True,
                        content=data.get("response", ""),
                        provider="ollama",
                        tier=Tier.FREE,
                        cost=0.0,
                        quality_score=0.0,  # Will be set by judge
                        raw_response=data
                    )
                else:
                    return ModelResult(
                        success=False,
                        content="",
                        provider="ollama",
                        tier=Tier.FREE,
                        cost=0.0,
                        quality_score=0.0,
                        error=f"HTTP {resp.status}"
                    )
    except Exception as e:
        return ModelResult(
            success=False, content="", provider="ollama",
            tier=Tier.FREE, cost=0.0, quality_score=0.0, error=str(e)
        )


async def call_groq(prompt: str, image_path: str = None, model: str = "llava-v1.5-7b-4096-preview") -> ModelResult:
    """Call Groq API."""
    if not GROQ_API_KEY:
        return ModelResult(
            success=False, content="", provider="groq",
            tier=Tier.CHEAP, cost=0.0, quality_score=0.0, error="No API key"
        )
    
    try:
        messages = []
        
        if image_path:
            with open(image_path, "rb") as f:
                image_b64 = base64.b64encode(f.read()).decode()
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
                ]
            })
        else:
            messages.append({"role": "user", "content": prompt})
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": messages,
                    "max_tokens": 2000
                },
                timeout=aiohttp.ClientTimeout(total=60)
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return ModelResult(
                        success=True,
                        content=data["choices"][0]["message"]["content"],
                        provider="groq",
                        tier=Tier.CHEAP,
                        cost=0.0,  # Free tier
                        quality_score=0.0,
                        raw_response=data
                    )
                else:
                    return ModelResult(
                        success=False, content="", provider="groq",
                        tier=Tier.CHEAP, cost=0.0, quality_score=0.0,
                        error=f"HTTP {resp.status}"
                    )
    except Exception as e:
        return ModelResult(
            success=False, content="", provider="groq",
            tier=Tier.CHEAP, cost=0.0, quality_score=0.0, error=str(e)
        )


async def call_deepseek(prompt: str, image_path: str = None) -> ModelResult:
    """Call DeepSeek API."""
    if not DEEPSEEK_API_KEY:
        return ModelResult(
            success=False, content="", provider="deepseek",
            tier=Tier.CHEAP, cost=0.0, quality_score=0.0, error="No API key"
        )
    
    try:
        content = [{"type": "text", "text": prompt}]
        
        if image_path:
            with open(image_path, "rb") as f:
                image_b64 = base64.b64encode(f.read()).decode()
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}
            })
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": content}],
                    "max_tokens": 2000
                },
                timeout=aiohttp.ClientTimeout(total=60)
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    # Estimate cost: ~$0.001 per call
                    return ModelResult(
                        success=True,
                        content=data["choices"][0]["message"]["content"],
                        provider="deepseek",
                        tier=Tier.CHEAP,
                        cost=0.001,
                        quality_score=0.0,
                        raw_response=data
                    )
                else:
                    return ModelResult(
                        success=False, content="", provider="deepseek",
                        tier=Tier.CHEAP, cost=0.0, quality_score=0.0,
                        error=f"HTTP {resp.status}"
                    )
    except Exception as e:
        return ModelResult(
            success=False, content="", provider="deepseek",
            tier=Tier.CHEAP, cost=0.0, quality_score=0.0, error=str(e)
        )


async def call_gemini(prompt: str, image_path: str = None) -> ModelResult:
    """Call Gemini API."""
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        
        content = [prompt]
        if image_path:
            with open(image_path, "rb") as f:
                content.append({"mime_type": "image/jpeg", "data": f.read()})
        
        response = model.generate_content(content)
        
        return ModelResult(
            success=True,
            content=response.text,
            provider="gemini",
            tier=Tier.PREMIUM,
            cost=0.01,  # Estimate
            quality_score=0.0,
            raw_response=response
        )
    except Exception as e:
        return ModelResult(
            success=False, content="", provider="gemini",
            tier=Tier.PREMIUM, cost=0.0, quality_score=0.0, error=str(e)
        )


# ============================================================================
# INTELLIGENT ROUTER
# ============================================================================

class IntelligentRouter:
    """
    Routes requests through model tiers with quality gates.
    
    Cascade:
    1. FREE: Ollama (local) - always try first
    2. CHEAP: Groq (free tier), DeepSeek ($0.001) - if free fails
    3. PREMIUM: Gemini, Claude - only if cheap fails quality check
    """
    
    def __init__(self, min_quality: float = 0.6):
        self.judge = QualityJudge(min_score=min_quality)
        self.stats = {
            "total_calls": 0,
            "tier_usage": {Tier.FREE: 0, Tier.CHEAP: 0, Tier.PREMIUM: 0},
            "total_cost": 0.0,
            "escalations": 0
        }
    
    async def process(
        self,
        prompt: str,
        image_path: str = None,
        expected_format: str = "json",
        force_tier: Tier = None
    ) -> ModelResult:
        """
        Process request through the cascade.
        
        Args:
            prompt: The prompt/question
            image_path: Optional image for vision tasks
            expected_format: "json" or "text"
            force_tier: Force a specific tier (skip cascade)
        
        Returns:
            Best result at lowest cost
        """
        self.stats["total_calls"] += 1
        
        # Define cascade
        cascade = [
            (Tier.FREE, [call_ollama]),
            (Tier.CHEAP, [call_groq, call_deepseek]),
            (Tier.PREMIUM, [call_gemini])
        ]
        
        # If forcing tier, filter cascade
        if force_tier:
            cascade = [(t, providers) for t, providers in cascade if t == force_tier]
        
        best_result = None
        
        for tier, providers in cascade:
            for provider_fn in providers:
                # Call provider
                result = await provider_fn(prompt, image_path)
                
                if not result.success:
                    print(f"  ❌ {result.provider}: {result.error}")
                    continue
                
                # Judge quality
                quality = self.judge.evaluate(result, expected_format)
                result.quality_score = quality.score
                
                print(f"  {'✅' if quality.passed else '⚠️'} {result.provider}: "
                      f"score={quality.score:.2f} {quality.reasons}")
                
                # Update stats
                self.stats["tier_usage"][tier] += 1
                self.stats["total_cost"] += result.cost
                
                if quality.passed:
                    # Good enough, return it
                    return result
                else:
                    # Keep as fallback
                    if not best_result or result.quality_score > best_result.quality_score:
                        best_result = result
                    self.stats["escalations"] += 1
        
        # If nothing passed, return best attempt
        return best_result or ModelResult(
            success=False, content="All providers failed",
            provider="none", tier=Tier.PREMIUM, cost=0, quality_score=0
        )
    
    def get_stats(self) -> Dict:
        """Get usage statistics."""
        return {
            **self.stats,
            "tier_usage": {t.name: v for t, v in self.stats["tier_usage"].items()}
        }


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

# Global router instance
_router = None

def get_router(min_quality: float = 0.6) -> IntelligentRouter:
    """Get or create global router."""
    global _router
    if _router is None:
        _router = IntelligentRouter(min_quality=min_quality)
    return _router


async def smart_analyze(prompt: str, image_path: str = None) -> str:
    """Quick helper for smart analysis."""
    router = get_router()
    result = await router.process(prompt, image_path)
    return result.content


# ============================================================================
# CLI
# ============================================================================

if __name__ == "__main__":
    import sys
    
    async def test():
        router = IntelligentRouter()
        
        prompt = "Describe this image in detail. What equipment is shown? What text is visible?"
        image = sys.argv[1] if len(sys.argv) > 1 else None
        
        print(f"🧠 Testing Intelligent Router")
        print(f"   Image: {image or 'None'}")
        print(f"   Prompt: {prompt[:50]}...")
        print()
        
        result = await router.process(prompt, image)
        
        print(f"\n📊 Result:")
        print(f"   Provider: {result.provider}")
        print(f"   Tier: {result.tier.name}")
        print(f"   Cost: ${result.cost:.4f}")
        print(f"   Quality: {result.quality_score:.2f}")
        print(f"\n📝 Content:\n{result.content[:500]}...")
        print(f"\n📈 Stats: {router.get_stats()}")
    
    asyncio.run(test())
