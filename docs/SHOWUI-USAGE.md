# ShowUI Computer Use - Usage Guide

## Quick Start

### 1. Open the UI
Go to: **https://a5f0c2094e874e1cee.gradio.live**

### 2. Configure Models

**Planner Model** (chooses what to do):
- `claude-3-5-sonnet-20241022` → needs Anthropic API key
- `gpt-4o` → needs OpenAI API key  
- `qwen2-vl-2b (local)` → FREE, runs on laptop (slower)

**Actor Model** (finds UI elements):
- `ShowUI` → FREE, already downloaded ✅

### 3. Add API Key (if using Claude/GPT-4)
- In the Settings panel, paste your API key
- For Claude: use your Anthropic key
- For GPT-4: use your OpenAI key

### 4. Test Commands
Try these in the chat:
- "What do you see on the screen?"
- "Click the Start menu"
- "Open Chrome"
- "Type 'hello world' in the search box"

---

## API Usage (from VPS)

```python
from gradio_client import Client

client = Client("https://a5f0c2094e874e1cee.gradio.live")

# Set API key (required for Claude/GPT-4)
client.predict(
    api_key_value="sk-your-key-here",
    api_name="/update_api_key"
)

# Send command
result = client.predict(
    user_input="click the Chrome icon",
    api_name="/process_input"
)
print(result)
```

---

## Test Checklist

| Test | Command | Expected |
|------|---------|----------|
| Screen capture | "What do you see?" | Describes desktop |
| Mouse move | "Move mouse to center" | Mouse moves |
| Click | "Click the Start menu" | Start menu opens |
| Type | "Type hello" | Text appears |
| Multi-step | "Open Chrome and go to google.com" | Browser opens |

---

## Troubleshooting

**"upstream Gradio app has raised an exception"**
- Missing API key for planner model
- Try using local qwen2-vl-2b model (no key needed)

**Slow response**
- First run downloads models (~2-4GB)
- Local models slower than cloud APIs

**Share URL expired**
- Restart app.py on the laptop
- New URL will be generated
