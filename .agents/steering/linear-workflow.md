---
inclusion: auto
name: Linear Issue Tracking & Agent Workflow
description: "Guidelines and CLI automation patterns for tracking tasks, capturing on-the-fly backlog items, and synchronizing commits with Linear across all agents."
---

# Linear Issue Tracking & Agent Workflow

## 🎯 Philosophy: Agent as Linear Administrator

The user ideates and directs at high velocity ("thinking on the fly"). The agent's responsibility is to **eliminate issue tracking friction** by managing Linear autonomously via the CLI:
1. **Never stall flow**: Never ask the user to leave the conversation or click around in the Linear web UI to create tickets.
2. **Never hijack unrelated tickets**: Do not tag commits with an unrelated issue ID (e.g., re-using a CI/Docs ticket for UX or infra fixes) just to satisfy commit linters.
3. **Capture on the fly**: When new work, deferred ideas, or edge cases emerge in chat, log them to Linear immediately.
4. **Reconcile at completion**: Close completed work and record follow-ups as explicit backlog items.

---

## 🛠️ Linear CLI Quick Reference

The `linear` CLI is pre-installed and authenticated as workspace admin (`moovv-fit`).

### Workspace Teams
- `CORE`: Platform, Shared Infra, Backend, Mobile, Landing, Design System (`5e29efad-4ed6-468d-a0e9-29f1e75b4f05`)
- `CLINIC`: Clinic OS, Portals (`1770afb0-d1a0-44d6-958a-51ec8d2706c1`)

### Key Commands

```bash
# 1. Create a new issue (on-the-fly capture or new task)
linear issue create \
  --team CORE \
  --title "[Landing] Fix CTA baseline alignment" \
  --description "Details..." \
  --priority 2 \
  --state Backlog

# 2. Update issue status
linear issue update CORE-124 --state "In Progress"
linear issue update CORE-124 --state Done

# 3. View an issue
linear issue view CORE-124

# 4. Search / list issues
linear issue list -t CORE --limit 10
```

---

## 🤖 Operating Patterns for All Agents (Antigravity, Kiro, etc.)

### Pattern 1: On-the-Fly Quick Capture
Whenever the user says phrases like:
- *"Backlog this..."*
- *"Note this for later..."*
- *"Let's do this next week..."*
- *"We should also fix X later..."*

**Action:**
1. Call `linear issue create` immediately with `--state Backlog`.
2. Report the created issue ID (e.g. `CORE-126`) in a single line.
3. Keep the conversation focused on the current in-flight task without derailment.

### Pattern 2: Pre-Commit Issue Minting
Before committing code across any repo:
1. **Check if a matching Linear issue exists**:
   - If yes, reference it: `feat(scope): description (CORE-XXX)`.
   - If no matching issue exists for the scope:
     - Run `linear issue create --team <TEAM> --title "[Scope] Title" --state "In Progress"` to mint the true issue.
     - **NEVER** reuse an unrelated ticket just to satisfy a hook.

### Pattern 3: Session Wrap-Up & Follow-Up Sync
At the conclusion of a work stream or when significant progress was made:
1. Move the corresponding Linear issues to `Done` via `linear issue update <ID> --state Done`.
2. Add commit hashes and affected repositories in the issue comments/description.
3. If temporary bridges were introduced (e.g. feature flags, review bypasses, mock data), create a follow-up ticket in `Backlog` so it is never forgotten.
