# ShowUI Computer Use - Travel Laptop

## Access
- **Public URL:** https://a5f0c2094e874e1cee.gradio.live
- **Local URL:** http://127.0.0.1:7860
- **Expires:** ~Feb 10, 2026

## Capabilities
- Visual computer control via natural language
- ShowUI model (free, local) - visual grounding
- Screen capture and analysis
- Mouse/keyboard automation via pyautogui

## Usage
1. Open the public URL in browser
2. Select Planner model (needs API key) or use ShowUI only
3. Type natural language commands like "click the Chrome icon"
4. ShowUI identifies UI elements, executes actions

## From VPS
```bash
# Test accessibility
curl -s "https://a5f0c2094e874e1cee.gradio.live" | head -3

# Could potentially use Gradio API for programmatic control
# See: https://www.gradio.app/docs/gradio/client
```

## Notes
- Travel laptop must be on and running app.py
- Share link regenerates if app restarts
- Windows-specific setup (venv/Scripts/activate)
