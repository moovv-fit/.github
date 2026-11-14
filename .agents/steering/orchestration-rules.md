---
inclusion: auto
name: Orchestration Rules
description: "Cross-repo coordination patterns, task routing, platform-level decisions."
---

# Orchestration Rules

## 🎯 Master Repo Purpose

This is the **orchestration hub** for the Moovv Fit platform. When working here:

1. **Route tasks** to appropriate submodules
2. **Coordinate** cross-repo changes
3. **Maintain** platform-level documentation and ADRs
4. **Don't duplicate** submodule-specific logic

## 🔀 Task Routing

| Task Type | Route To | Example |
|-----------|----------|---------|
| API changes | `repos/backend/node` | New endpoint, DB migration |
| Mobile features | `repos/apps/mobile` | Screen, component, navigation |
| Web dashboard | `repos/apps/web` | Page, feature, styling |
| Landing/marketing | `repos/apps/landing` | Copy, layout, SEO |
| CDK constructs | `repos/infra/cdk` | New stack, shared resource |
| UI components | `repos/platform/design-system` | Button, modal, form |
| E2E tests | `repos/platform/simulator` | Test scenario, fixture |
| Technical docs | `repos/docs/technical` | API docs, runbooks |
| Product specs | `repos/docs/product` | PRDs, feature specs |

## 📝 Cross-Repo Changes

When a change spans multiple repos:

1. **Plan first**: Document which repos are affected
2. **Parallel work**: Make changes in each submodule
3. **Atomic commits**: Each submodule gets its own commit tagged with its specific Linear issue
4. **Update parent**: Commit submodule pointer updates together
5. **Link PRs**: Reference related PRs across repos
6. **Linear Sync**: Close finished issues and record follow-ups in Backlog via the `linear` CLI

### Example: New API + Mobile Feature

```
1. repos/backend/node: Add new endpoint
   → Commit: "feat(api): add exercise-history endpoint"
   
2. repos/apps/mobile: Consume new endpoint
   → Commit: "feat(history): add exercise history screen"
   
3. Master repo: Update both submodule pointers
   → Commit: "feat: exercise history feature (backend + mobile)"
```

## 🚫 Don't Do Here

| Anti-pattern | Why | Instead |
|--------------|-----|---------|
| Write app code | Wrong scope | Work in submodule |
| Duplicate steering | Maintenance burden | Reference submodule steering |
| Hijack unrelated Linear issues | Muddles project tracking & changelogs | Mint a new issue with `linear issue create` or commit cleanly |
| Store secrets | Security risk | Use AWS SSM / Secrets Manager |
| Ignore available skills / ad-hoc guessing | Inconsistent quality, regressions | Consult matching skill in `.agents/skills/` or `.agents/shared/skills/` |
| Manual AWS console / mock keys | Security risk & broken audit trail | Authenticate with SSO profile `moovv-fit-ujwal-admin` |
| Heavy builds | Slow, unnecessary | Build in submodules |

## ☁️ AWS Authentication Standard

All AWS cloud operations across all submodules (CDK deployments, S3 sync, SSM parameter lookups, Spot runner bakes) MUST target:
- **Profile**: `moovv-fit-ujwal-admin` (or `moovv-fit-worker` for headless CI scripts)
- **Region**: `ap-south-1` (Mumbai)
- **Account**: `855246887543`
- **Headless Devbox Login**: `aws sso login --profile moovv-fit-ujwal-admin --use-device-code`
- Detailed playbook: `aws-and-cloud-credentials.md` and `.agents/skills/aws-sso-helper/SKILL.md`.

## 🧰 Skill-First Protocol & Available Skills

Agents are equipped with specialized skills residing at the repo root (`.agents/skills/`) and the shared devbox pool (`.agents/shared/skills/` or `~/.agents/skills/`).

### Invariant: Skill-First Activation
Before writing code, debugging complex regressions, branching for parallel work, or marking tasks complete, agents **MUST check available skills and activate the appropriate `SKILL.md`**.

### Core Skills Directory

| Domain | Skill | Location | Trigger / When to Activate |
| :--- | :--- | :--- | :--- |
| **AWS & SSO** | `aws-sso-helper` | `.agents/skills/aws-sso-helper/` | Expired AWS tokens, AWS CLI errors, headless device login, credential export |
| **Root-Cause Analysis** | `systematic-debugging` | `.agents/skills/systematic-debugging/` | Unclear test failures, flaky CI, obscure runtime exceptions before patching |
| **Verification Gate** | `verification-before-completion` | `.agents/skills/verification-before-completion/` | MANDATORY before declaring tasks done, submitting PRs, or closing Linear tickets |
| **Branch & Isolation** | `using-git-worktrees` | `.agents/skills/using-git-worktrees/` | Parallel agent tasks, feature branches, protecting main workspace |
| **PR & Commits** | `git-flow` | `.agents/skills/git-flow/` | Conventional commits, Linear issue linking in PRs, gh CLI operations |
| **Serverless Backend** | `aws-lambda` | `.agents/skills/aws-lambda/` | Lambda cold starts, event payloads, handler optimization, CloudWatch debugging |
| **Product & Clinical** | `moovv-fit-product` | `repos/docs/product/...` | Validating clinical invariants, prescription flows, compliance, PDR specs |
| **Design Tokens & UI** | `moovv-design-system` | `repos/platform/design-system/...` | Svelte 5 runes, bits-ui primitives, Tailwind v4 design tokens |
| **Browser E2E** | `playwright-e2e` | `.agents/shared/skills/` | Authoring, debugging, or running web E2E specs |
| **Database** | `postgres-best-practices` | `.agents/shared/skills/` | Schema migrations, Prisma queries, index optimization |

### How to Activate Skills
1. **Antigravity / Native Agents**: Read `.agents/skills/<name>/SKILL.md` directly.
2. **Kiro / Markdown Cross-Links**: `#[[file:.agents/skills/{name}/SKILL.md]]` or `#[[file:.agents/shared/skills/{name}/SKILL.md]]`.
3. **Execution**: Follow the step-by-step phases in the skill's instructions — do not skip baseline verification or completion checklists.

## ✅ Do Here

| Pattern | Example |
|---------|---------|
| Platform ADRs | Cross-cutting architecture decisions |
| Migration scripts | `scripts/migrate-kiro-sessions.sh`, `scripts/migrate-antigravity-sessions.py` |
| Submodule coordination | Updating multiple repos together |
| Org profile | `profile/README.md` |

## 📎 References

- `#[[file:AGENTS.md]]`
- `#[[file:docs/architecture/adr/ADR-001-SUBMODULE-ARCHITECTURE.md]]`
