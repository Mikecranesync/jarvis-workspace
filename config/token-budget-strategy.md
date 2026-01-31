# Token Budget Strategy

**Auto-managed by Jarvis based on context usage**

## Tiers

| Context % | Mode | Behavior |
|-----------|------|----------|
| <50% | Full | Voice OK, detailed responses, explore freely |
| 50-70% | Efficient | Batch ops, shorter responses, text-only |
| 70-80% | Conservative | Essential work only, minimal output |
| >80% | Pause | Stop work, wait for new session |

## Current: 60% → Efficient Mode

**Active rules:**
- Batch file writes together
- Skip voice unless user-facing
- Shorter status updates
- Focus on completing current vision steps

## Model Selection (Future)

When available:
- Routine writing → Sonnet/Haiku
- Code generation → Sonnet
- Complex decisions → Opus
- Approvals → Opus
