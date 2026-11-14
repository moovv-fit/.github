# Design: Agent Token Burn Optimization Architecture

## Architecture Overview
The architecture moves from unconstrained, eager context loading to lazy, deterministic, event-filtered execution across all 14 repositories.

```
┌────────────────────────────────────────────────────────┐
│                   Agent Turn Initiation                │
└──────────────────────────┬─────────────────────────────┘
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
    Universal Invariants        Matching File Types?
     (inclusion: auto)          (inclusion: fileMatch)
             │                           │
             └─────────────┬─────────────┘
                           ▼
                  Lean Context Base
                  (~1,200 tokens)
```

## Hook Optimization Pipeline
- **Old Pattern**: `PostFileSave` → `type: agent` → 800-token prompt → LLM evaluation → 200-token response (1,000 tokens burned per save).
- **New Pattern**: `PostFileSave` → `type: command` → regex check via bash / grep → 0 tokens, sub-10ms response.

## Reference Alignment
Standardizes configurations against patterns validated in `/mnt/workspace/src/omnipolis` and `/mnt/workspace/src/treasury`:
- Single source of truth for forbidden patterns (`system-rules.md`).
- Strict 20-word budget on prose.
- Deterministic, 0-token editor hooks.
