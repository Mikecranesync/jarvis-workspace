# Computer Use OOTB - Laptop Setup Plan

**Goal:** Install computer_use_ootb on Windows laptops so VPS/Jarvis can control them remotely via Gradio web interface.

**Architecture:**
- Laptop runs `computer_use_ootb` (Gradio server)
- Creates public URL like `https://xxxxx.gradio.live`
- VPS browses to that URL to send commands
- Claude/GPT-4o controls the laptop GUI

---

## FOR CLAUDE CLI ON LAPTOP - EXECUTE THIS

### Step 1: Prerequisites Check
```powershell
# Check Python version (need 3.10+)
python --version

# Check if git is installed
git --version

# Check if conda/miniconda is installed (recommended but optional)
conda --version
```

### Step 2: Clone Repository
```powershell
cd C:\
git clone https://github.com/showlab/computer_use_ootb.git
cd computer_use_ootb
```

### Step 3: Install Dependencies
```powershell
# Option A: With pip (simpler)
pip install -r requirements.txt

# Option B: With conda (cleaner)
conda create -n ootb python=3.12 -y
conda activate ootb
pip install -r requirements.txt
```

### Step 4: Set API Key (choose one)
```powershell
# For Claude (recommended)
$env:ANTHROPIC_API_KEY="sk-ant-xxxxx"

# Or for GPT-4o
$env:OPENAI_API_KEY="sk-xxxxx"

# Or for Qwen (cheaper)
$env:QWEN_API_KEY="sk-xxxxx"
```

### Step 5: Start the Server
```powershell
cd C:\computer_use_ootb
python app.py
```

**Expected Output:**
```
Running on local URL: http://127.0.0.1:7860
Running on public URL: https://xxxxxxxxxx.gradio.live
```

### Step 6: Make It Permanent (Auto-Start on Login)

Create startup script:
```powershell
# Create startup VBS script (runs hidden)
$vbsContent = @"
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c cd C:\computer_use_ootb && python app.py", 0, False
"@

$startupPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
Set-Content -Path "$startupPath\ComputerUseOOTB.vbs" -Value $vbsContent

Write-Host "Auto-start configured!" -ForegroundColor Green
```

### Step 7: Persist API Key
```powershell
# Set as system environment variable (persists across reboots)
[System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-xxxxx", "User")

# Verify
[System.Environment]::GetEnvironmentVariable("ANTHROPIC_API_KEY", "User")
```

### Step 8: Report Back to VPS
After successful setup, report the Gradio URL to VPS:
```powershell
# The public URL from app.py output - copy it!
# Example: https://abc123def456.gradio.live
```

---

## VERIFICATION CHECKLIST

- [ ] Python 3.10+ installed
- [ ] Repository cloned to C:\computer_use_ootb
- [ ] Dependencies installed (no errors)
- [ ] API key set (ANTHROPIC_API_KEY or OPENAI_API_KEY)
- [ ] Server starts without errors
- [ ] Public URL generated (gradio.live)
- [ ] Startup script created in Startup folder
- [ ] API key persisted to environment

---

## TROUBLESHOOTING

**"No module named X"**
```powershell
pip install X
```

**Port 7860 already in use**
```powershell
netstat -ano | findstr 7860
taskkill /PID <pid> /F
```

**Gradio public URL not generated**
- Check firewall isn't blocking
- Try: `python app.py --share`

**Server crashes on screenshot**
- Install: `pip install mss pillow`

---

## LAPTOP-SPECIFIC CONFIG

### PLC Laptop (100.72.2.99)
- Username: hharp
- Has: Factory I/O, TIA Portal, RSLinx
- GPU: Quadro P620 (can run local models)

### Travel Laptop (100.83.251.23)
- Username: mike
- Mobile workstation

---

## NEXT STEP FOR VPS

Once laptop reports gradio.live URL, VPS stores it:
```bash
echo "PLC_LAPTOP_OOTB=https://xxxxx.gradio.live" >> /opt/jarvis/laptop-urls.env
```

Then VPS can control laptop via browser automation or direct Gradio API calls.
