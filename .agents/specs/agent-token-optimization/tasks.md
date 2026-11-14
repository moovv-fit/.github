# Implementation Tasks: Agent Token Burn Optimization

## Phase 1: Core Critical Repositories
- [x] `repos/apps/mobile`: Switch patterns to `fileMatch`, convert quality-guard to command, streamline `AGENTS.md`, add `.contextignore` (PR #34)
- [x] `repos/apps/web`: Switch patterns to `fileMatch`, convert quality-guard to command, streamline `AGENTS.md`, add `.contextignore` (PR #40)
- [x] `repos/backend/node`: Convert domain/cdk steering to `fileMatch`, convert quality-guard to command, filter linear-commit, add `.contextignore` (PR #115)
- [x] `repos/infra/cdk`: Convert operational steering to `manual`, convert quality-guard to command, remove symlinks, add `.contextignore` (PR #22)

## Phase 2: Backend Engines & Analysis
- [x] `repos/backend/engine`: Convert domain steering to `fileMatch`, filter linear-commit/git-safety, add `.contextignore` (PR #4)
- [x] `repos/backend/analysis`: Convert domain steering to `fileMatch`, filter hooks, add `.contextignore` (PR #1)

## Phase 3: Applications & Platform Repos
- [x] `repos/apps/landing`: Convert css/html steering to `fileMatch`, convert quality guards to commands, add `.contextignore` (PR #11)
- [x] `repos/infra/kiro-spot`: Guard git-safety hook, streamline `AGENTS.md`, add `.contextignore` (PR #1)
- [x] `repos/platform/design-system`: Convert operational steering to `manual`, convert quality-guard to command, add `.contextignore` (PR #4)
- [x] `repos/platform/exercise-validator`: Add `.contextignore` for heavy prompt/asset files, streamline `AGENTS.md`, ignore worktrees (PR #1)
- [x] `repos/platform/simulator`: Convert steering to `manual`, replace 4 agent hooks with commands, add `.contextignore` (PR #3)

## Phase 4: Documentation Portals & Master Orchestration
- [x] `repos/docs/technical`: Convert domain/operational steering to `manual`, convert quality-guard/session-end to commands, add `.contextignore` (PR #7)
- [x] `repos/docs/product`: Convert PDR steering to `manual`, convert invariant-guard to bash script, convert manifest-sync, add `.contextignore` (PR #8)
- [x] Master repo (`moovv-fit`): Convert non-essential steering to `manual`, convert hooks to commands, remove `.agents/rules`, add root `.contextignore` (PR #11)

## Phase 5: Architecture Decisions & Reporting
- [x] Author ADR-005 in `docs/architecture/adr/ADR-005-AGENT-TOKEN-OPTIMIZATION-AND-STEERING-STANDARDS.md`
- [x] Update `docs/architecture/adr/README.md`
- [x] Publish comprehensive report in `docs/architecture/reports/agent-token-burn-optimization-report.md`
- [x] Record spec in `.agents/specs/agent-token-optimization/`
