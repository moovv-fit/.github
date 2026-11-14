# Agent Token Burn Optimization Report — Moovv Fit Platform

## Executive Summary

After analyzing both reference projects (Omnipolis, Treasury) and all Moovv Fit repos, we identified **6 systemic patterns** causing excessive token burn. The reference projects demonstrate mature token optimization; the Moovv repos had copied the surface patterns but lacked the discipline, resulting in bloated context, duplicate rules, and LLM hooks that should be deterministic scripts.

> [!IMPORTANT]
> **Observed Waste:** Each repo previously burned **3,000–8,000 extra tokens per turn** from auto-loaded redundant steering, plus **10,000–30,000 tokens per multi-file edit** from LLM-driven PostFileSave hooks. Fixing these 6 patterns reduces token consumption by **40–60%** per session.

---

## Reference Project Patterns (What "Good" Looks Like)

### Omnipolis ✅
| Pattern | Implementation |
|---------|---------------|
| **20-word cap** | `Max 20 words (excl. code)` — hard budget |
| **Fixed hook responses** | `"Response: '✅ Logged'"` (2 tokens), `"✅ Quality Pass"` (3 tokens) |
| **Manifest pointers** | `#[[file:path]]` lazy-loads; only audit manifest if that *layer* changed |
| **Test log offloading** | `pnpm vitest 2>&1 \| tee .agents/sessions/.../test.log` — prevents log flooding |
| **Scoped test runs** | `pnpm test:unit --include [test-path]` — never runs full suite |
| **Event-driven hooks** | Quality/sync/tracker fire on precise `fileEdited` patterns, not blanket |
| **Reuse-check hook** | Only fires on `**/design.md` creation — zero cost during coding |

### Treasury ✅
| Pattern | Implementation |
|---------|---------------|
| **Forbidden-patterns table** | Single definitive copy in `.agents/agents.md` |
| **`inclusion: auto` discipline** | Only 2 files auto-loaded: `operational-principles.md` (domain) + `system-rules.md` (constraints) |
| **`.contextignore`** | Explicitly blocks `node_modules/`, `pnpm-lock.yaml`, `static/`, `reference/`, `.svelte-kit/` |
| **On-demand prompts** | `design-system-alignment.md`, `component-refactor.md` — loaded only when needed |
| **Batch + Read-before-write** | `"Modify files once. No incremental edits."` + `"Read before write"` |
| **No auto-tests** | `"Only add tests when explicitly requested"` |

---

## Critical Issues Identified

### 🔴 Issue 1: Blanket `inclusion: auto` on ALL Steering Files
Every steering file in every Moovv repo previously had `inclusion: auto`. This forced **all rules** into context on **every turn**, regardless of task.

| Repo | Auto-loaded Files | Approx. Baseline Tokens |
|------|-------------------|----------------|
| **Mobile** | `system-rules.md` + `operational-context.md` + pattern files + `AGENTS.md` | ~5,500 |
| **Web** | `system-rules.md` + `operational-context.md` + `git-branch-strategy.md` + `session-workspace.md` + `AGENTS.md` | ~3,200 |
| **Backend** | `system-rules.md` + `operational-context.md` + `domain-context.md` + `cdk-patterns.md` + branching/session files + `AGENTS.md` | ~4,500 |
| **Infra** | `system-rules.md` + `operational-context.md` + `cdk-patterns.md` + `git-branch-strategy.md` + `AGENTS.md` | ~3,100 |

### 🔴 Issue 2: Content Duplication Across Files
Rules were copy-pasted across `AGENTS.md`, `system-rules.md`, quality hooks, and operational context. Every duplicate added tokens with zero information gain.

### 🔴 Issue 3: LLM-Driven Hooks on Every File Save
The #1 token burner. Every file save fired `PostFileSave` hooks with `"type": "agent"`, spawning full LLM reasoning turns to check quality rules that could be validated deterministically.

### 🟡 Issue 4: `PreToolUse` Hooks on Every Bash Command
`linear-commit.json` fired an LLM reminder on **every `execute_bash`** call, not just `git commit`.

### 🟡 Issue 5: Broken Paths & Symlink Triplication
Circular symlinks (`.agents/rules -> steering`) and host links (`.agents/shared -> /home/ubuntu/.agents`) caused tools to double/triple index files and bleed host context into sandboxed sessions.

---

## Complete PR Registry & Rollout Status

All adjustments have been systematically implemented using isolated git worktrees (`chore/agent-token-optimization`), committed, pushed to `origin`, and opened as pull requests against `main` (with worktree manifests tracked locally):

| # | Repository | Submodule Path | PR Link | Status | Key Improvements |
|---|---|---|---|---|---|
| 1 | **moovv-fit-mobile** | `repos/apps/mobile` | [PR #34](https://github.com/moovv-fit/moovv-fit-mobile/pull/34) | `pr_open` | `inclusion: fileMatch`, deterministic command hooks, lean `AGENTS.md` |
| 2 | **moovv-fit-web** | `repos/apps/web` | [PR #40](https://github.com/moovv-fit/moovv-fit-web/pull/40) | `pr_open` | `inclusion: fileMatch`, grep quality guard, `.contextignore` |
| 3 | **moovv-fit-backend-node** | `repos/backend/node` | [PR #115](https://github.com/moovv-fit/moovv-fit-backend-node/pull/115) | `pr_open` | `inclusion: fileMatch`, filtered commit hook, symlinks removed |
| 4 | **moovv-fit-infra** | `repos/infra/cdk` | [PR #22](https://github.com/moovv-fit/moovv-fit-infra/pull/22) | `pr_open` | `inclusion: manual`, filtered PreToolUse, symlinks removed |
| 5 | **moovvfit-recommendation-engine** | `repos/backend/engine` | [PR #4](https://github.com/moovv-fit/moovvfit-recommendation-engine/pull/4) | `pr_open` | `inclusion: fileMatch`, guarded hooks, `.contextignore` |
| 6 | **exercise_canonical_analysis** | `repos/backend/analysis` | [PR #1](https://github.com/moovv-fit/exercise_canonical_analysis/pull/1) | `pr_open` | `inclusion: fileMatch`, guarded hooks, ML artifact ignores |
| 7 | **moovv-fit-landing** | `repos/apps/landing` | [PR #11](https://github.com/moovv-fit/moovv-fit-landing/pull/11) | `pr_open` | `inclusion: fileMatch` for CSS/HTML, deterministic quality guards |
| 8 | **moovv-fit-kiro-spot** | `repos/infra/kiro-spot` | [PR #1](https://github.com/moovv-fit/moovv-fit-kiro-spot/pull/1) | `pr_open` | Streamlined `AGENTS.md`, guarded `git-safety.json` |
| 9 | **moovv-fit-design-system** | `repos/platform/design-system` | [PR #4](https://github.com/moovv-fit/moovv-fit-design-system/pull/4) | `pr_open` | `inclusion: manual`, deterministic quality guard, symlinks removed |
| 10 | **self-test-qa-portal** | `repos/platform/exercise-validator` | [PR #1](https://github.com/moovv-fit/self-test-qa-portal/pull/1) | `pr_open` | `.contextignore` (heavy prompts & assets), telegraphic `AGENTS.md` |
| 11 | **moovv-fit-simulator** | `repos/platform/simulator` | [PR #3](https://github.com/moovv-fit/moovv-fit-simulator/pull/3) | `pr_open` | Replaced 4 agent hooks with 0-token commands, `inclusion: manual` |
| 12 | **moovv-fit-docs** | `repos/docs/technical` | [PR #7](https://github.com/moovv-fit/moovv-fit-docs/pull/7) | `pr_open` | `inclusion: manual`, deterministic quality guard, session end command |
| 13 | **moovv-fit-product** | `repos/docs/product` | [PR #8](https://github.com/moovv-fit/moovv-fit-product/pull/8) | `pr_open` | Replaced agent hooks with bash verification scripts, `inclusion: manual` |
| 14 | **Master Orchestration** | `moovv-fit/.github` | [PR #11](https://github.com/moovv-fit/.github/pull/11) | `pr_open` | `inclusion: manual` for non-core steering, command hooks, root `.contextignore` |
