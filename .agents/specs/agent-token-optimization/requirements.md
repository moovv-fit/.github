# Requirements: Agent Token Burn Optimization

## 1. Objective
Establish an ecosystem-wide engineering and configuration standard across all 14 repositories to prevent AI coding agents from burning excessive tokens during routine development and review workflows.

## 2. Functional Requirements
1. **Selective Inclusion Rules**:
   - Only fundamental invariant constraints may use `inclusion: auto`.
   - Domain logic and framework-specific patterns must use `inclusion: fileMatch` targeted to relevant paths.
   - Reference operational runbooks and branching guides must use `inclusion: manual`.
2. **Deterministic Quality Enforcement**:
   - Zero `type: agent` hooks triggered on routine events (`PostFileSave`, `Stop`).
   - All file-save checks must run as `type: command` executing grep or local linters in under 50ms.
3. **PreToolUse Scoping**:
   - Tool-use hooks must filter arguments and execute checks only when destructive or relevant commands (e.g. `git commit`, `git push --force`) are triggered.
4. **Context Ignore Lists**:
   - Every repository must have a `.contextignore` file blocking build outputs, dependencies, lockfiles, and worktrees from agent directory crawlers.
5. **Redundant Symlink Removal**:
   - Eliminate circular `.agents/rules -> steering` symlinks and global `.agents/shared -> ~/.agents` symlinks.
6. **Telegraphic Persona Lead**:
   - `AGENTS.md` must enforce max 20 words for status updates, use standard status prefixes, and reference deep context rather than duplicating text.
