#!/usr/bin/env python3
"""
ShopTalk Ollama Integration
Serve ShopTalk LLM locally using Ollama for edge deployment.
"""

import json
import requests
from pathlib import Path
from typing import Optional, Dict, Generator

# Ollama API endpoint
OLLAMA_API = "http://localhost:11434"

# System prompts
SYSTEM_PROMPTS = {
    "en": """You are ShopTalk, an expert industrial equipment diagnostic AI.
Analyze sensor data, diagnose problems, and recommend maintenance actions.
Be direct. Prioritize safety. Give specific action steps.""",
    
    "es": """Eres ShopTalk, un experto en diagnóstico de equipos industriales.
Analiza datos de sensores, diagnostica problemas y recomienda acciones de mantenimiento.
Sé directo. Prioriza la seguridad. Da pasos de acción específicos."""
}

# Recommended models for edge deployment
RECOMMENDED_MODELS = {
    "phi3:mini": "Best balance of size and capability (3.8B)",
    "qwen2:1.5b": "Smaller, good multilingual support (1.5B)",
    "qwen2:0.5b": "Ultra-small for constrained devices (0.5B)",
    "tinyllama": "Very fast, basic capability (1.1B)"
}


def check_ollama() -> bool:
    """Check if Ollama is running."""
    try:
        resp = requests.get(f"{OLLAMA_API}/api/tags", timeout=5)
        return resp.status_code == 200
    except (requests.RequestException, ConnectionError, TimeoutError):
        return False


def list_models() -> list:
    """List available Ollama models."""
    try:
        resp = requests.get(f"{OLLAMA_API}/api/tags", timeout=10)
        if resp.status_code == 200:
            return [m["name"] for m in resp.json().get("models", [])]
    except (requests.RequestException, json.JSONDecodeError, KeyError):
        pass
    return []


def pull_model(model_name: str) -> bool:
    """Pull a model from Ollama registry."""
    print(f"Pulling model: {model_name}")
    try:
        resp = requests.post(
            f"{OLLAMA_API}/api/pull",
            json={"name": model_name},
            stream=True,
            timeout=600
        )
        for line in resp.iter_lines():
            if line:
                data = json.loads(line)
                if "status" in data:
                    print(f"  {data['status']}")
        return True
    except Exception as e:
        print(f"Error pulling model: {e}")
        return False


def chat(model: str, prompt: str, language: str = "en", 
         stream: bool = False) -> str:
    """Send a chat message to Ollama."""
    system = SYSTEM_PROMPTS.get(language, SYSTEM_PROMPTS["en"])
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "stream": stream,
        "options": {
            "temperature": 0.3,
            "top_p": 0.9
        }
    }
    
    try:
        if stream:
            return _chat_stream(payload)
        else:
            resp = requests.post(
                f"{OLLAMA_API}/api/chat",
                json=payload,
                timeout=120
            )
            if resp.status_code == 200:
                return resp.json()["message"]["content"]
            else:
                return f"Error: {resp.status_code}"
    except Exception as e:
        return f"Error: {e}"


def _chat_stream(payload: Dict) -> Generator[str, None, None]:
    """Stream chat response."""
    try:
        resp = requests.post(
            f"{OLLAMA_API}/api/chat",
            json=payload,
            stream=True,
            timeout=120
        )
        for line in resp.iter_lines():
            if line:
                data = json.loads(line)
                if "message" in data:
                    yield data["message"].get("content", "")
    except Exception as e:
        yield f"Error: {e}"


def diagnose(model: str, equipment: str, readings: Dict, 
             language: str = "en") -> str:
    """Run a diagnosis on equipment readings."""
    readings_str = ", ".join([f"{k}: {v}" for k, v in readings.items()])
    
    prompt = f"""Equipment: {equipment}
Current readings: {readings_str}

Analyze these readings and provide:
1. Diagnosis (what's the issue, if any)
2. Severity (normal/warning/critical)
3. Recommended actions"""
    
    return chat(model, prompt, language)


class ShopTalkLLM:
    """High-level interface for ShopTalk LLM."""
    
    def __init__(self, model: str = "phi3:mini", language: str = "en"):
        self.model = model
        self.language = language
        
        if not check_ollama():
            raise RuntimeError("Ollama not running. Start with: ollama serve")
        
        models = list_models()
        if model not in models:
            print(f"Model {model} not found. Pulling...")
            pull_model(model)
    
    def diagnose(self, equipment: str, readings: Dict) -> str:
        """Diagnose equipment issue."""
        return diagnose(self.model, equipment, readings, self.language)
    
    def chat(self, prompt: str) -> str:
        """General chat."""
        return chat(self.model, prompt, self.language)
    
    def set_language(self, language: str):
        """Change language."""
        self.language = language


def install_ollama():
    """Print Ollama installation instructions."""
    print("""
Ollama Installation:

Linux/macOS:
  curl -fsSL https://ollama.com/install.sh | sh

Then start the server:
  ollama serve

Pull a model:
  ollama pull phi3:mini

Recommended models for ShopTalk:
""")
    for model, desc in RECOMMENDED_MODELS.items():
        print(f"  {model}: {desc}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="ShopTalk Ollama Integration")
    parser.add_argument("--check", action="store_true", help="Check Ollama status")
    parser.add_argument("--list", action="store_true", help="List models")
    parser.add_argument("--pull", type=str, help="Pull a model")
    parser.add_argument("--chat", type=str, help="Chat prompt")
    parser.add_argument("--model", default="phi3:mini", help="Model to use")
    parser.add_argument("--lang", default="en", help="Language (en/es)")
    parser.add_argument("--install", action="store_true", help="Show install instructions")
    args = parser.parse_args()
    
    if args.install:
        install_ollama()
    elif args.check:
        status = "✅ Running" if check_ollama() else "❌ Not running"
        print(f"Ollama status: {status}")
    elif args.list:
        models = list_models()
        if models:
            print("Available models:")
            for m in models:
                print(f"  - {m}")
        else:
            print("No models found or Ollama not running")
    elif args.pull:
        pull_model(args.pull)
    elif args.chat:
        if not check_ollama():
            print("Ollama not running. Start with: ollama serve")
        else:
            response = chat(args.model, args.chat, args.lang)
            print(response)
    else:
        parser.print_help()
