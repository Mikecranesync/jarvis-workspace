# CLAUDE.md - ShowUI Computer Use Demo

## Project Goal
Get the ShowUI visual computer control demo running on Windows. This is a Gradio app that uses vision models to control the computer via screenshots.

## Current Status
- Gradio/HuggingFace dependency conflicts being resolved
- Model: ShowUI (visual grounding for computer use)
- Running on Windows with Python venv

## Key Constraints
1. **Windows environment** - Use PowerShell/cmd syntax, not bash
2. **Limited disk space** - Don't download huge models unnecessarily
3. **Local first** - Try `share=False` before `share=True` (Gradio)
4. **Dependency hell** - Pin versions explicitly when conflicts arise

## Common Issues & Fixes

### Gradio + HuggingFace conflicts
```
# If version conflicts:
pip install gradio==4.44.1 huggingface_hub<1.0
```

### Model not loading (low memory)
- Check if model downloaded: `~/.cache/huggingface/`
- ShowUI needs ~4-8GB VRAM for inference
- Try CPU mode if GPU issues: `device="cpu"`

### share=True hangs
- Gradio's share server can be slow
- Test locally first with `share=False`
- Access via `http://localhost:7860`

## Architecture
```
app.py
├── Gradio UI (screenshot display + controls)
├── ShowUI model (visual grounding)
└── pyautogui (mouse/keyboard control)
```

## When Stuck
1. Check Python process memory (should be >1GB when model loaded)
2. Check for port conflicts: `netstat -an | findstr 7860`
3. Try minimal test: just load model, no UI
4. Check CUDA: `python -c "import torch; print(torch.cuda.is_available())"`

## Success Criteria
- Gradio UI launches at localhost:7860
- Can take screenshot
- Model interprets "click the X button" type commands
- Actually moves mouse/clicks

## Don't
- Don't use share=True until local works
- Don't upgrade all packages blindly
- Don't ignore Windows vs Linux path differences
