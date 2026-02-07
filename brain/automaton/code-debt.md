# Code Debt Log

*Auto-scanned by Automaton*

## Bare Except Clauses (Anti-pattern)
These should be converted to specific exception types:

| File | Status |
|------|--------|
| `projects/Rivet-PRO/bot_launcher.py` | Needs fix |
| `projects/Rivet-PRO/start_bot.py` | Needs fix |
| `projects/Rivet-PRO/test_llm_judge.py` | Needs fix |
| `projects/Rivet-PRO/test_single_manual.py` | Needs fix |
| `projects/Rivet-PRO/test_url_validator.py` | Needs fix |

## TODOs/FIXMEs

### Siemens KB Sources (Phase 3)
- `rivet/prompts/sme/siemens.py:178` - Add Siemens KB sources
- `rivet/prompts/sme/siemens.py:185` - Add Siemens KB sources

### Research Improvements
- `rivet/tools/response_gap_filler.py:301` - Query actual KB for known manufacturers
- `rivet/workflows/research.py:267` - Implement fuzzy query matching

### Stripe Integration (Round 8?)
- `rivet/integrations/stripe.py:74` - Integrate harvest block from Harvester
- `rivet/integrations/stripe.py:189` - Integrate harvest block from Harvester
- `rivet/integrations/stripe.py:246` - Update user tier in database
- `rivet/integrations/stripe.py:247` - Send welcome email
- `rivet/integrations/stripe.py:248` - Grant access to features
- `rivet/integrations/stripe.py:258` - Update user status in database

*Last scanned: 2026-02-06 14:36 UTC*

## 2026-02-07 05:09 UTC - Bare Except Scan
Found 5 bare `except:` clauses (Python anti-pattern):
- `.github/workflows/flag-review-reminder.yml` (line in Python block)
- `test_single_manual.py`
- `ycb/rendering/manim_engine.py`
- `scripts/ralph/ralph_local.py` (2 occurrences)

**Recommendation:** Replace with specific exceptions (e.g., `except Exception as e:`)
**Priority:** Low - not blocking, but should fix for code quality
