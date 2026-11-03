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
3. **Atomic commits**: Each submodule gets its own commit
4. **Update parent**: Commit submodule pointer updates together
5. **Link PRs**: Reference related PRs across repos

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
| Store secrets | Security risk | Use AWS SSM / Secrets Manager |
| Heavy builds | Slow, unnecessary | Build in submodules |

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
- `#[[file:migration-manifest.json]]`
- `#[[file:scripts/migrate-antigravity-sessions.py]]`
- `#[[file:scripts/migrate-kiro-sessions.sh]]`
