# Autonomous Improvements Log

Tracking autonomous code improvements made by the Automaton.

---

## 2026-01-31

### 11:26 UTC — Fixed Bare Exception in API Server

**File:** `projects/shoptalk/src/api/server.py`
**Line:** 241
**Issue:** Bare `except:` clause hiding potential errors
**Fix:** Replaced with specific exception types: `WebSocketDisconnect, ConnectionError, RuntimeError`
**Impact:** Better error visibility, follows Python best practices

**Before:**
```python
except:
    websocket_clients.remove(client)
```

**After:**
```python
except (WebSocketDisconnect, ConnectionError, RuntimeError) as e:
    logger.debug(f"Removing disconnected client: {e}")
    websocket_clients.remove(client)
```

---

### 11:49 UTC — Fixed Bare Exceptions in Ollama Serve

**File:** `projects/shoptalk/llm/serve/ollama_serve.py`
**Issues Fixed:** 2
**Changes:**
- `check_ollama()`: Added `requests.RequestException, ConnectionError, TimeoutError`
- `list_models()`: Added `requests.RequestException, json.JSONDecodeError, KeyError`

### 11:49 UTC — Fixed Bare Exceptions in TTS

**File:** `projects/shoptalk/src/voice/tts.py`
**Issues Fixed:** 3
**Changes:**
- `_detect_backend()` edge-tts check: Added `subprocess.SubprocessError, FileNotFoundError, OSError`
- `_detect_backend()` piper check: Added same
- `_espeak()` ffmpeg conversion: Added same

---

## Known Technical Debt (Remaining)

| File | Issue | Priority |
|------|-------|----------|
| `src/voice/tts.py` | 1 bare except clause remaining | Low |
| `cli.py` | 1 bare except clause | Low |
| `autoconnect/service.py` | 2 bare except clauses | Medium |
| `autoconnect/scanner.py` | 2 bare except clauses | Low |

---

*Auto-updated by Autonomous Code Improver*

## 2026-01-31 13:22 UTC - Code Quality Fix

**File:** projects/shoptalk/cli.py
**Issue:** Bare except clause
**Fix:** Changed to specific exceptions (json.JSONDecodeError, IOError, OSError)
**Impact:** Better error visibility, follows Python best practices

