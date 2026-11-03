# Moovv Fit — Master Orchestration Repo

## 🎯 Mission
Central orchestration hub for the Moovv Fit platform ecosystem. Manages cross-repo coordination, shared agent patterns, and platform-wide documentation.

**This is the GitHub organization profile repo** (`moovv-fit/.github`).

## 🏗️ Repository Structure

```
moovv-fit/
├── repos/
│   ├── apps/               # User-facing applications
│   │   ├── mobile/         → moovv-fit-mobile (React Native)
│   │   ├── web/            → moovv-fit-web (Next.js)
│   │   └── landing/        → moovv-fit-landing (Astro)
│   ├── backend/
│   │   └── node/           → moovv-fit-backend-node (Lambda/CDK)
│   ├── infra/
│   │   └── cdk/            → moovv-fit-infra (CDK constructs)
│   ├── platform/
│   │   ├── design-system/  → moovv-fit-design-system (Svelte)
│   │   └── simulator/      → moovv-fit-simulator
│   └── docs/
│       ├── technical/      → moovv-fit-docs
│       └── product/        → moovv-fit-product
├── profile/                # GitHub org profile (README.md)
├── scripts/                # Cross-repo tooling
└── docs/architecture/adr/  # Platform-level ADRs
```

## 🤖 Agent Behavior

### Orchestration Mode
When working from this master repo, the agent acts as an **orchestrator**:
- Routes tasks to appropriate submodule repos
- Coordinates cross-repo changes
- Maintains platform-level documentation

### Submodule Mode
When working in a submodule (e.g., `repos/backend/node`), the agent follows that repo's `AGENTS.md` and steering files.

## 📁 Submodule Quick Reference

| Domain | Path | Stack | Purpose |
|--------|------|-------|---------|
| **Backend** | `repos/backend/node` | Node/Lambda/CDK | API, business logic |
| **Mobile** | `repos/apps/mobile` | React Native/Expo | iOS/Android app |
| **Web** | `repos/apps/web` | Next.js | Web dashboard |
| **Landing** | `repos/apps/landing` | Astro | Marketing site |
| **Infra** | `repos/infra/cdk` | CDK | Shared constructs |
| **Design** | `repos/platform/design-system` | Svelte | UI components |
| **Simulator** | `repos/platform/simulator` | - | Test harness |
| **Docs** | `repos/docs/technical` | - | Technical docs |
| **Product** | `repos/docs/product` | - | Product specs |

## 🔀 Cross-Repo Operations

### Working with Submodules
```bash
# Update all submodules
git submodule update --remote --merge

# Work in a specific submodule
cd repos/backend/node
git checkout -b feature/my-feature
# ... make changes ...
git commit -m "feat: my changes"
git push origin feature/my-feature

# Update parent to track new commit
cd ../../../
git add repos/backend/node
git commit -m "chore: update backend submodule"
```

### Cross-Repo Changes
When a change spans multiple repos:
1. Make changes in each affected submodule
2. Commit and push each submodule
3. Update parent repo to track new commits
4. Create PRs in each repo referencing the parent PR

## 📎 Steering (auto-loaded)

| File | Purpose |
|------|---------|
| `orchestration-rules.md` | Cross-repo coordination patterns |
| `submodule-routing.md` | Task routing to submodules |

## 📚 ADRs
Platform-level architecture decisions live in `docs/architecture/adr/`.
Repo-specific ADRs live in each submodule.

## 🔗 References
- `#[[file:docs/architecture/adr/ADR-001-SUBMODULE-ARCHITECTURE.md]]`
- `#[[file:migration-manifest.json]]`
- `#[[file:scripts/migrate-antigravity-sessions.py]]`
- `#[[file:scripts/migrate-kiro-sessions.sh]]`
