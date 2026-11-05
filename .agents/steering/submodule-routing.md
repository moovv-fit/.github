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
| Recommendation Engine | `repos/backend/engine` | `cd repos/backend/engine` |
| Canonical Analysis & Embeddings | `repos/backend/analysis` | `cd repos/backend/analysis` |
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
| `backend/node` | TypeScript | Node 22 / Lambda / Prisma / CDK | pnpm |
| `backend/engine` | Python 3.12 | Flask / Lambda | pip |
| `backend/analysis` | Python 3.12 | sentence-transformers / PostgreSQL | pip |
| `apps/mobile` | Dart | Flutter 3.x / Riverpod / Go Router | flutter pub |
| `apps/web` | TypeScript | React 19 / Vite / Tailwind v4 | pnpm |
| `apps/landing` | JavaScript / HTML / CSS | Vanilla JS / CloudFront | - |
| `infra/cdk` | TypeScript | AWS CDK v2 | pnpm |
| `platform/design-system` | TypeScript | Svelte 5 (Runes) / Tailwind v4 | pnpm |
| `platform/simulator` | TypeScript | Node 22 / Zod / undici / ws | pnpm |
| `docs/technical` | TypeScript | SvelteKit 2 / Svelte 5 / Tailwind v4 | pnpm |
| `docs/product` | Markdown | PDRs / Clinical Invariants | - |

## Submodule AGENTS.md Locations

Each submodule has its own agent configuration:

```
repos/backend/node/AGENTS.md                          # Core API patterns
repos/backend/engine/AGENTS.md                        # Recommendation engine patterns
repos/backend/analysis/AGENTS.md                      # Canonical curation & embeddings
repos/apps/mobile/AGENTS.md                           # Mobile Flutter patterns
repos/apps/web/AGENTS.md                              # Web React 19 patterns
repos/apps/landing/AGENTS.md                          # Landing HTML5 patterns
repos/infra/cdk/AGENTS.md                             # Infra CDK patterns
repos/platform/design-system/AGENTS.md                 # Design system Svelte 5 patterns
repos/platform/simulator/AGENTS.md                    # Simulator E2E patterns
repos/docs/technical/AGENTS.md                        # Technical documentation patterns
repos/docs/product/AGENTS.md                          # Product context & clinical invariants
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
