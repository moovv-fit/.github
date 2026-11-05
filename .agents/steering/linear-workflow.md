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
3. **Default to Rich Cards & Checklists**: Never post bare, one-line descriptions or raw local file paths (`repos/...`) that non-technical founders cannot read. Every ticket must be a self-contained, beautifully formatted proposal with context, options tables, and interactive review checklists.
4. **Tag Team Members Directly**: Tag relevant stakeholders so issues ping their native Linear inbox:
   - **Pawan Deshmukh (Clinical & Product Lead)**: `https://linear.app/moovv-fit/profiles/p`
   - **Rahul Jain (Growth & Commercial Strategy)**: `https://linear.app/moovv-fit/profiles/r`
   - **Ujwal Parker (Engineering & Architecture)**: `https://linear.app/moovv-fit/profiles/u`
5. **Capture on the fly**: When new work, deferred ideas, or edge cases emerge in chat, log them to Linear immediately.
6. **Reconcile at completion**: Close completed work and record follow-ups as explicit backlog items.

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

### Pattern 4: Interactive Review Previews & CDN Hosting Standard
For any issue requiring executive, clinical, or growth sign-off (e.g. copy, funnel flows, pricing, interactive widgets):
1. **Never build multi-tab or bloated umbrella pages**: Create a **single-purpose, zero-tab simulator** dedicated strictly to that ticket's review scope.
2. **Repository Location**: Commit the source file under `docs/previews/<ticket-id>-<slug>.html` within the affected repository. This provides full **Git version history**, commit diffs, and pull request tracking.
3. **CDN Hosting Location**:
   - Upload to: `s3://moovv-fit-content-staging/previews/<ticket-id>-<slug>.html`
   - Access URL: `https://content.staging.moovv.fit/previews/<ticket-id>-<slug>.html`
   - **Isolation Guarantee**: Stored outside `web/landing` and `web/*` so it is never deleted by landing/web `aws s3 sync ... --delete` deployment pipelines.
4. **Object Versioning & Historical Revisions**:
   - **S3 Bucket Versioning**: `moovv-fit-content-staging` and `moovv-fit-content-production` have S3 Object Versioning **Enabled**. Every upload automatically preserves historical versions with unique `VersionId`s.
   - **Versioned URL Convention (Optional for major revisions)**: For immutable point-in-time review snapshots across design rounds, upload as `.../previews/<ticket-id>-<slug>-v<N>.html` while maintaining the root `<ticket-id>-<slug>.html` as the floating latest.
   - **CDN Invalidation**: When updating the floating latest, run `aws cloudfront create-invalidation --distribution-id E2N6CYC2PTUSQY --paths "/previews/*"` to ensure edge cache freshness.
5. **Linear Linking**: Embed the preview prominently at the top of the Linear issue description:
   ```markdown
   > 🌐 **Live Interactive Preview:** [https://content.staging.moovv.fit/previews/<ticket-id>-<slug>.html](https://content.staging.moovv.fit/previews/<ticket-id>-<slug>.html)
   ```

---

## 📋 Mandatory Rich Card Template for Issue Descriptions

Every Linear ticket created or detailed by an agent must follow this rich schema:

```markdown
## 🎯 Overview & Context
[1-2 sentences summarizing the business/product problem, referencing parent PDR/initiative]

> 🌐 **Live Interactive Preview:** [https://content.staging.moovv.fit/previews/<ticket-id>-<slug>.html](https://content.staging.moovv.fit/previews/<ticket-id>-<slug>.html)

---

## 📝 Specifications / Options / Architecture
[Visual comparison tables for copy/pricing, mermaid diagrams, or API schemas]

---

## ✅ Sign-Off & Approval Checklist
- [ ] https://linear.app/moovv-fit/profiles/p **(Clinical / Product Review):** [Specific clinical confirmation or disclaimer check]
- [ ] https://linear.app/moovv-fit/profiles/r **(Commercial / Growth Review):** [Specific decision point or option selection]
- [ ] https://linear.app/moovv-fit/profiles/u **(Architecture / DevOps Review):** [Implementation approval]

---

+++ [Full Technical Details]
### Invariants & Edge Cases
- [Key technical / regulatory invariants]

### Full Spec Document
[Clickable HTTPS link to GitHub spec file in the repository]
+++
```

