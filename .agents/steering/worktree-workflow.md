---
inclusion: auto
name: Worktree Workflow
description: "Mandatory worktree-based development workflow for all feature work across Moovv Fit submodules."
---

# Worktree Workflow

## Core Principle

**Never work directly on `main`.** All feature development MUST use git worktrees to isolate work and prevent context clashes between concurrent agent sessions or developers.

---

## 1. Worktree Creation Convention

### Directory Structure
```
{repo}/
├── .worktrees/                     # Worktree root (gitignored)
│   ├── manifest.json               # Worktree tracking manifest
│   ├── feat-CORE-123-add-login/    # Worktree directory
│   ├── fix-CLINIC-456-auth-bug/    # Another worktree
│   └── chore-CORE-789-refactor/    # Another worktree
└── ... (main branch files)
```

### Naming Convention
- Branch: `{type}/{LINEAR-ISSUE}-{slug}` (e.g., `feat/CORE-123-add-login`)
- Worktree path: `.worktrees/{type}-{LINEAR-ISSUE}-{slug}` (slashes become dashes)

### Creation Command
```bash
# From repo root (on main)
git worktree add .worktrees/feat-CORE-123-add-login -b feat/CORE-123-add-login

# Update manifest after creation
# (Agent or script updates .worktrees/manifest.json)
```

---

## 2. Manifest Specification

### Dual Manifest Architecture

Worktree tracking uses **both** a central manifest and per-repo manifests:

1. **Central Manifest** (`/mnt/workspace/src/moovv-fit/.worktrees/manifest.json`) — Master orchestration repo tracks all worktrees across all submodules
2. **Per-Repo Manifests** (`{repo}/.worktrees/manifest.json`) — Each submodule maintains its own manifest for local agent context

### Central Manifest Schema

```json
{
  "version": "1.0",
  "lastUpdated": "2026-11-13T10:00:00Z",
  "repos": {
    "repos/backend/node": {
      "worktrees": [
        {
          "branch": "feat/CORE-123-add-login",
          "linearIssue": "CORE-123",
          "spec": "login-flow",
          "createdAt": "2026-11-13T10:00:00Z",
          "path": ".worktrees/feat-CORE-123-add-login",
          "prNumber": 42,
          "prStatus": "open",
          "merged": false
        }
      ]
    },
    "repos/apps/web": {
      "worktrees": []
    }
  }
}
```

### Per-Repo Manifest Schema

Each repo maintains `.worktrees/manifest.json` for local agent context:

```json
{
  "version": "1.0",
  "worktrees": [
    {
      "branch": "feat/CORE-123-add-login",
      "linearIssue": "CORE-123",
      "spec": "login-flow",
      "createdAt": "2026-11-13T10:00:00Z",
      "path": ".worktrees/feat-CORE-123-add-login",
      "prNumber": null,
      "prStatus": "none",
      "merged": false
    },
    {
      "branch": "fix/CLINIC-456-auth-bug",
      "linearIssue": "CLINIC-456",
      "spec": null,
      "createdAt": "2026-11-12T14:30:00Z",
      "path": ".worktrees/fix-CLINIC-456-auth-bug",
      "prNumber": 42,
      "prStatus": "open",
      "merged": false
    }
  ]
}
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `branch` | string | Full branch name (e.g., `feat/CORE-123-add-login`) |
| `linearIssue` | string | Linear issue ID (e.g., `CORE-123`, `CLINIC-456`) |
| `spec` | string\|null | Kiro spec name if applicable |
| `createdAt` | ISO 8601 | Worktree creation timestamp |
| `path` | string | Relative path to worktree directory |
| `prNumber` | number\|null | GitHub PR number once opened |
| `prStatus` | enum | `none`, `draft`, `open`, `approved`, `merged`, `closed` |
| `merged` | boolean | Whether the branch has been merged to main |

### Manifest Update Triggers

| Event | Action |
|-------|--------|
| Worktree created | Add entry with `prStatus: "none"` |
| PR opened | Update `prNumber` and `prStatus: "open"` or `"draft"` |
| PR approved | Update `prStatus: "approved"` |
| PR merged | Update `prStatus: "merged"`, `merged: true` |
| PR closed (unmerged) | Update `prStatus: "closed"` |
| Worktree removed | Remove entry from manifest |

---

## 3. Agent Workflow

### Starting Work on a Feature

```bash
# 1. Ensure main is up to date
git checkout main
git pull origin main

# 2. Create or find Linear issue
linear issue create --team CORE --title "[Backend] Add login endpoint" --state "In Progress"
# → Returns CORE-123

# 3. Create worktree
git worktree add .worktrees/feat-CORE-123-add-login -b feat/CORE-123-add-login

# 4. Enter worktree
cd .worktrees/feat-CORE-123-add-login

# 5. Update manifest (agent responsibility)
# Add entry to .worktrees/manifest.json in repo root
```

### Committing Work
See `commit-conventions.md` for commit message format. All commits must reference the Linear issue.

### Creating PR

```bash
# From worktree directory
git push -u origin feat/CORE-123-add-login
gh pr create --title "feat(CORE-123): Add login endpoint" --body "Closes CORE-123"

# Update manifest with PR number
```

### Cleanup After Merge

```bash
# From repo root (main)
git worktree remove .worktrees/feat-CORE-123-add-login
git branch -d feat/CORE-123-add-login

# Update manifest - remove entry
```

---

## 4. Integration with Linear Workflow

This workflow integrates with the existing Linear workflow from `linear-workflow.md`:

1. **Pre-Commit Issue Minting:** If no Linear issue exists, create one before the first commit
2. **Status Sync:** Update Linear issue status when PR status changes
3. **Session Wrap-Up:** Close Linear issues when PRs merge

---

## 5. Protected Branch Enforcement

Direct push to `main` is blocked by `.husky/pre-push` (or `.githooks/pre-push`) hooks in all repos. This enforces the worktree workflow:

- Pushing to `main` directly → ❌ Blocked
- Pushing feature branch → ✅ Allowed
- Bypassing (emergency): `git push --no-verify`

---

## 6. Gitignore Requirement

Every repo must have `.worktrees/` in its `.gitignore`:

```gitignore
# Worktrees
.worktrees/
```

This prevents worktree contents from being committed while allowing `manifest.json` to be tracked if desired.

---

## References

- `linear-workflow.md` — Linear issue tracking integration
- `commit-conventions.md` — Commit message format
- `submodule-routing.md` — Submodule task routing
