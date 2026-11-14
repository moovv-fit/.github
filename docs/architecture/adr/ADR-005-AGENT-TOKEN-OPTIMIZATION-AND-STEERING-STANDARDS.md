# ADR-005: Agent Token Burn Optimization and Steering Standards

**Status**: ✅ Current  
**Last Updated**: 2026-11-14

## Context

Across the Moovv Fit multi-repo ecosystem, AI coding agents (Kiro, Antigravity, Claude Code) were exhibiting unsustainable token consumption during routine development sessions. Key domains—especially `repos/apps/mobile`, `repos/apps/web`, `repos/backend/node`, and `repos/infra/cdk`—frequently exhausted token quotas and context windows.

A comparative architecture review against reference repositories (`omnipolis` and `treasury`) identified five critical drivers of token waste:

1. **Unconditional Steering Loading (`inclusion: auto`)**: Every steering file was loaded on every single conversational turn, injecting 3,000–5,000 static tokens regardless of task relevance (e.g. loading mobile deployment guides when fixing a button style).
2. **LLM Evaluation Hooks (`type: agent`)**: Editor hooks (`quality-guard.json`, `invariant-guard.json`, `test-tracker.json`, `sync.json`) spawned full conversational LLM passes on every file save and on session stop. Saving 10 files in a session burned 50,000–100,000 tokens in secondary background agent calls.
3. **Unfiltered PreToolUse Hooks**: Hooks such as `linear-commit.json` listened to `execute_bash` without filtering for `git commit`, executing on every `ls`, `grep`, or `cat`.
4. **Context Crawler Inefficiency & Symlink Loops**: Lack of `.contextignore` caused workspace crawlers to traverse `node_modules`, lockfiles (`pnpm-lock.yaml`, `package-lock.json`), build directories, and virtual environments. Redundant symlinks (`.agents/rules -> steering` and `.agents/shared -> /home/ubuntu/.agents`) caused duplicate file indexing and external context leakage.
5. **Verbose `AGENTS.md` and Rule Duplication**: Detailed forbidden patterns tables and workflow guides were repeated across both `AGENTS.md` and multiple steering files.

## Decision

Establish a platform-wide standard for agent steering, hooks, and context management across all 14 repositories:

### 1. Selective Steering Inclusion
- **`inclusion: auto`**: Reserved strictly for universal, hard invariant files (`system-rules.md`, `product-invariants.md`, `submodule-routing.md`).
- **`inclusion: fileMatch`**: Applied to domain- and framework-specific patterns (e.g. `domain-context.md`, `css-patterns.md`, `component-patterns.md`, `cdk-patterns.md`) so they only load when matching files are edited.
- **`inclusion: manual`**: Applied to reference documentation, operational runbooks, branch strategies, and session workspace rules.

### 2. Zero-Token Deterministic Command Hooks
- All `type: agent` hooks are prohibited for routine file-save and post-action gates.
- Replace with `type: command` hooks executing fast, deterministic bash/grep checks or local verification scripts (e.g., scanning for `: any`, `console.log`, forbidden AST tokens, or invoking existing validator scripts like `./scripts/verify-product-integrity.sh`).
- Hook execution latency reduced from 3–8s (LLM call) to <15ms (local shell command).

### 3. Filtered PreToolUse Gates
- Shell tool use hooks must inspect the command string before executing logic (e.g. checking `echo "$AGY_TOOL_ARGS" | grep -qE "git\s+commit"`).
- Destructive git commands are blocked or guarded via local deterministic scripts (`git-safety.py` / bash one-liners).

### 4. Canonical Directory Structure & Exclusion Rules
- Add a `.contextignore` file to every repository ignoring `node_modules`, build artifacts (`dist`, `build`, `.svelte-kit`, `.dart_tool`), lockfiles, and `.worktrees/`.
- Remove circular symlinks (`.agents/rules -> steering`) and non-standard host symlinks (`.agents/shared -> /home/ubuntu/.agents`).
- Keep `.agents/steering/` as the single canonical directory for agent steering rules.

### 5. Telegraphic & Pointer-Based AGENTS.md
- Maintain lean `AGENTS.md` files: telegraphic style, 20-word response limits, status prefixes (`✅`, `🚧`, `❌`, `❓`), and pointer links to deep context rather than embedded duplicated tables.

## Implementation & Rollout

This architecture was rolled out across all 14 repositories via isolated git worktrees (`chore/agent-token-optimization`), committed, and submitted as pull requests against `main`:

| Submodule | Target Repo | PR |
|---|---|---|
| `repos/apps/mobile` | `moovv-fit-mobile` | [#34](https://github.com/moovv-fit/moovv-fit-mobile/pull/34) |
| `repos/apps/web` | `moovv-fit-web` | [#40](https://github.com/moovv-fit/moovv-fit-web/pull/40) |
| `repos/backend/node` | `moovv-fit-backend-node` | [#115](https://github.com/moovv-fit/moovv-fit-backend-node/pull/115) |
| `repos/infra/cdk` | `moovv-fit-infra` | [#22](https://github.com/moovv-fit/moovv-fit-infra/pull/22) |
| `repos/backend/engine` | `moovvfit-recommendation-engine` | [#4](https://github.com/moovv-fit/moovvfit-recommendation-engine/pull/4) |
| `repos/backend/analysis` | `exercise_canonical_analysis` | [#1](https://github.com/moovv-fit/exercise_canonical_analysis/pull/1) |
| `repos/apps/landing` | `moovv-fit-landing` | [#11](https://github.com/moovv-fit/moovv-fit-landing/pull/11) |
| `repos/infra/kiro-spot` | `moovv-fit-kiro-spot` | [#1](https://github.com/moovv-fit/moovv-fit-kiro-spot/pull/1) |
| `repos/platform/design-system` | `moovv-fit-design-system` | [#4](https://github.com/moovv-fit/moovv-fit-design-system/pull/4) |
| `repos/platform/exercise-validator` | `self-test-qa-portal` | [#1](https://github.com/moovv-fit/self-test-qa-portal/pull/1) |
| `repos/platform/simulator` | `moovv-fit-simulator` | [#3](https://github.com/moovv-fit/moovv-fit-simulator/pull/3) |
| `repos/docs/technical` | `moovv-fit-docs` | [#7](https://github.com/moovv-fit/moovv-fit-docs/pull/7) |
| `repos/docs/product` | `moovv-fit-product` | [#8](https://github.com/moovv-fit/moovv-fit-product/pull/8) |
| Master Orchestration | `moovv-fit/.github` | [#11](https://github.com/moovv-fit/.github/pull/11) |

## Consequences

### Positive
- **60%–75% Baseline Turn Reduction**: Baseline token payload per turn reduced from ~4,500 tokens to ~1,200 tokens across all repos.
- **Zero LLM Hook Waste**: Completely eliminates 5,000–20,000 secondary tokens burned per editing session by switching to deterministic commands.
- **Faster Agent Turnarounds**: Sub-millisecond hook execution removes multi-second agent pauses after every file modification.
- **Accurate Tool Traversal**: `.contextignore` prevents accidental indexing of multi-megabyte lockfiles and third-party vendor directories.

### Negative / Trade-offs
- Manual steering documents (`inclusion: manual`) must be explicitly referenced or opened when needed for operational or branching tasks.
- Command-based quality hooks use regex patterns (e.g. `grep`) rather than semantic LLM reasoning, requiring well-defined syntax checks.

## References
- Comprehensive Analysis Report: `docs/architecture/reports/agent-token-burn-optimization-report.md`
- Submodule Architecture: `ADR-001-SUBMODULE-ARCHITECTURE.md`
- Reference implementations: `omnipolis` and `treasury`
