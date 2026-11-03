---
inclusion: auto
name: Submodule Routing
description: "Quick reference for navigating to the right submodule for any task."
---

# Submodule Routing Guide

## Quick Lookup

### "I need to work on..."

| Need | Go to | Command |
|------|-------|---------|
| Backend API | `repos/backend/node` | `cd repos/backend/node` |
| Mobile app | `repos/apps/mobile` | `cd repos/apps/mobile` |
| Web dashboard | `repos/apps/web` | `cd repos/apps/web` |
| Landing page | `repos/apps/landing` | `cd repos/apps/landing` |
| AWS infrastructure | `repos/infra/cdk` | `cd repos/infra/cdk` |
| UI components | `repos/platform/design-system` | `cd repos/platform/design-system` |
| E2E testing | `repos/platform/simulator` | `cd repos/platform/simulator` |
| Technical docs | `repos/docs/technical` | `cd repos/docs/technical` |
| Product specs | `repos/docs/product` | `cd repos/docs/product` |

## Tech Stack by Repo

| Repo | Language | Framework | Package Manager |
|------|----------|-----------|-----------------|
| `backend/node` | TypeScript | Lambda/CDK | pnpm |
| `apps/mobile` | TypeScript | React Native/Expo | pnpm |
| `apps/web` | TypeScript | Next.js | pnpm |
| `apps/landing` | TypeScript | Astro | pnpm |
| `infra/cdk` | TypeScript | CDK | pnpm |
| `platform/design-system` | TypeScript | Svelte | pnpm |
| `platform/simulator` | TypeScript | - | pnpm |
| `docs/technical` | Markdown | - | - |
| `docs/product` | Markdown | - | - |

## Submodule AGENTS.md Locations

Each submodule has its own agent configuration:

```
repos/backend/node/AGENTS.md          # Backend patterns
repos/apps/mobile/AGENTS.md           # Mobile patterns
repos/apps/web/AGENTS.md              # Web patterns
repos/apps/landing/AGENTS.md          # Landing patterns
repos/infra/cdk/AGENTS.md             # Infra patterns
repos/platform/design-system/AGENTS.md # Design system patterns
repos/platform/simulator/AGENTS.md    # Simulator patterns
```

## Common Operations

### Update all submodules
```bash
git submodule update --remote --merge
```

### Check submodule status
```bash
git submodule status
```

### Work in a submodule
```bash
cd repos/backend/node
git checkout -b feature/my-feature
# ... make changes ...
git add -A && git commit -m "feat: my changes"
git push origin feature/my-feature
```

### Update parent after submodule changes
```bash
cd /mnt/workspace/src/moovv-fit
git add repos/backend/node
git commit -m "chore: update backend submodule"
```
