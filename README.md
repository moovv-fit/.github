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
│   ├── mobile/             # React Native/Expo app
│   ├── web/                # Next.js dashboard
│   └── landing/            # Astro marketing site
├── backend/
│   └── node/               # Lambda/CDK API
├── infra/
│   └── cdk/                # Shared CDK constructs
├── platform/
│   ├── design-system/      # Svelte component library
│   └── simulator/          # E2E test harness
└── docs/
    ├── technical/          # Technical documentation
    └── product/            # Product specifications
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
| Backend | Node.js, TypeScript, Lambda, CDK |
| Mobile | React Native, Expo |
| Web | Next.js |
| Landing | Astro |
| Design System | Svelte |
| Infrastructure | AWS CDK |

## License

Proprietary — © Moovv Fit
