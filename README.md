# Moovv Fit Platform

Central orchestration repository for the Moovv Fit ecosystem.

## Overview

[Moovv](https://moovv.fit) is an AI-driven healthtech platform for digital MSK and mobility care.

This repository serves as:
- **GitHub organization profile** (`profile/README.md`)
- **Submodule orchestration hub** for all Moovv repositories
- **Platform-level documentation** and architecture decisions

## Repository Structure

```
repos/
├── apps/                   # User-facing applications
│   ├── mobile/             # Flutter (iOS/Android) app
│   ├── web/                # React 19 / Vite portals (/physio, /clinic, /admin)
│   └── landing/            # HTML5 / CSS3 marketing site
├── backend/
│   ├── node/               # Primary Node/Lambda API (Prisma/Sequelize/CDK)
│   ├── engine/             # Python 3.12 Flask recommendation engine
│   └── analysis/           # Python 3.12 semantic matching & embeddings
├── infra/
│   └── cdk/                # Shared AWS CDK v2 constructs
├── platform/
│   ├── design-system/      # Svelte 5 component library & design tokens
│   └── simulator/          # Autonomous multi-persona E2E test harness
└── docs/
    ├── technical/          # Partner SDK technical docs (SvelteKit)
    └── product/            # Product specifications & clinical invariants
```

## Getting Started

### Clone with Submodules

```bash
git clone --recurse-submodules git@github.com:moovv-fit/moovv-fit.git
cd moovv-fit
```

### Update Submodules

```bash
git submodule update --remote --merge
```

### Work in a Submodule

```bash
cd repos/backend/node
git checkout -b feature/my-feature
# ... make changes ...
git commit -m "feat: my changes"
git push origin feature/my-feature
```

## Documentation

- [ADR-001: Submodule Architecture](docs/architecture/adr/ADR-001-SUBMODULE-ARCHITECTURE.md)
- [Agent Configuration](AGENTS.md)

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend (Node API) | Node.js 22, TypeScript, Lambda, Prisma, Sequelize, CDK |
| Backend (Engines) | Python 3.12, Flask, sentence-transformers, PostgreSQL |
| Mobile | Flutter 3.x, Dart, Riverpod, Go Router, Freezed |
| Web | React 19, TypeScript, Vite, Tailwind CSS v4, Zustand |
| Landing | HTML5, CSS3, Vanilla JS, CloudFront |
| Design System | Svelte 5 (Runes), Tailwind CSS v4, bits-ui |
| Simulator | Node.js 22, TypeScript, Zod, undici, ws |
| Documentation | SvelteKit 2, Svelte 5, AWS CDK |
| Infrastructure | AWS CDK v2, TypeScript, Docker Compose |

## License

Proprietary — © Moovv Fit
