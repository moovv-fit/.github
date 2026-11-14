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
│   │   ├── cdk/            → moovv-fit-infra (CDK constructs)
│   │   └── kiro-spot/      → moovv-fit-kiro-spot (Spot orchestration)
│   ├── platform/
│   │   ├── design-system/  → moovv-fit-design-system (Svelte)
│   │   ├── exercise-validator/ → self-test-qa-portal (Node/Express)
│   │   └── simulator/      → moovv-fit-simulator
│   └── docs/
│       ├── technical/      → moovv-fit-docs
│       └── product/        → moovv-fit-product
├── profile/                # GitHub org profile (README.md)
├── scripts/                # Cross-repo tooling
├── BACKLOG.md              # Canonical cross-repo backlog mirror (Linear sync)
└── docs/architecture/adr/  # Platform-level ADRs
```

## 🤖 Agent Behavior

### Orchestration Mode
When working from this master repo, the agent acts as an **orchestrator**:
- Routes tasks to appropriate submodule repos
- Coordinates cross-repo changes
- Maintains platform-level documentation
- Manages Linear issue tracking autonomously via the `linear` CLI (on-the-fly backlog capture, pre-commit ticket minting, and retrospective status sync)

### Submodule Mode
When working in a submodule (e.g., `repos/backend/node`), the agent follows that repo's `AGENTS.md` and steering files.

## 📁 Submodule Quick Reference

| Domain | Path | Stack | Purpose |
|--------|------|-------|---------|
| **Backend (Core API)** | `repos/backend/node` | Node 22 / TypeScript / Lambda / Prisma / CDK | Main API, auth, business logic |
| **Backend (Engine)** | `repos/backend/engine` | Python 3.12 / Flask / Lambda | Clinical exercise recommendation service |
| **Backend (Analysis)** | `repos/backend/analysis` | Python 3.12 / sentence-transformers / PostgreSQL | Semantic embeddings & curation pipeline |
| **Mobile** | `repos/apps/mobile` | Flutter 3.x / Dart / Riverpod / Go Router | iOS/Android rehabilitation application |
| **Web** | `repos/apps/web` | React 19 / Vite / Tailwind v4 / Zustand / React Query | Clinical (`/physio`, `/clinic`) & Admin portals |
| **Landing** | `repos/apps/landing` | HTML5 / CSS3 / Vanilla JS / CloudFront | Marketing sites & patient lead acquisition |
| **Infra (CDK)** | `repos/infra/cdk` | AWS CDK v2 / TypeScript / Docker Compose | Shared cloud infrastructure & telemetry |
| **Infra (Kiro Spot)** | `repos/infra/kiro-spot` | Bash / AWS CLI / EC2 Spot | On-demand spot instance orchestration for CI/codegen |
| **Design** | `repos/platform/design-system` | Svelte 5 (Runes) / Tailwind v4 / bits-ui | Canonical design tokens & UI library |
| **Exercise Validator** | `repos/platform/exercise-validator` | Node 22 / Express | Stakeholder validation portal for exercise content |
| **Simulator** | `repos/platform/simulator` | Node 22 / TypeScript / Zod / undici / ws | Autonomous multi-persona E2E test harness |
| **Docs (Technical)** | `repos/docs/technical` | SvelteKit 2 / Svelte 5 / Tailwind v4 / CDK | Partner developer documentation portal |
| **Docs (Product)** | `repos/docs/product` | Markdown / PDRs / Clinical Invariants | Product source of truth & compliance specs |

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

## ☁️ AWS Authentication & SSO Profile

All cloud infrastructure, SSM parameters, and S3 assets across the platform use AWS Account `855246887543` in `ap-south-1` (Mumbai) with IAM Identity Center in `us-east-1`.

| Context | SSO Profile | Role | Usage |
| :--- | :--- | :--- | :--- |
| **Interactive / Agent Dev** | `moovv-fit-ujwal-admin` | `AdministratorAccess` | CDK diff/synth/deploy, S3 releases, SSM lookups, manual Spot launches |
| **Automation / Worker** | `moovv-fit-worker` | `AdministratorAccess` | Ephemeral CI/CD runners, automated AMIs, background scripts |

```bash
# Headless re-auth (always use device code on remote devboxes):
aws sso login --profile moovv-fit-ujwal-admin --use-device-code

# Verify active session:
aws sts get-caller-identity --profile moovv-fit-ujwal-admin

# Default profile in terminal:
export AWS_PROFILE=moovv-fit-ujwal-admin
```
> **Guideline:** When AWS CLI credentials expire or fail, activate the `aws-sso-helper` skill immediately. Do not manually manipulate `.aws/credentials`.

## 🧰 Available Skills & Skill-First Protocol

Agents must adhere to the **Skill-First Principle**: before modifying code, debugging complex regressions, branching, or finishing tasks, check the available skills catalog and load the matching `SKILL.md`.

### Core Skills Catalog

| Domain | Skill Name | Path | When to Activate |
| :--- | :--- | :--- | :--- |
| **AWS & SSO** | `aws-sso-helper` | `.agents/skills/aws-sso-helper/` | Expired tokens, AWS CLI errors, headless device login, credential export |
| **Root-Cause Analysis** | `systematic-debugging` | `.agents/skills/systematic-debugging/` | Flaky tests, elusive runtime crashes, or regression isolation |
| **Verification Gate** | `verification-before-completion` | `.agents/skills/verification-before-completion/` | MANDATORY before declaring tasks complete or opening PRs |
| **Workspace Isolation** | `using-git-worktrees` | `.agents/skills/using-git-worktrees/` | Parallel agent work, preventing branch clashes on shared devbox |
| **Git & PR Workflows** | `git-flow` | `.agents/skills/git-flow/` | Commit message conventions, Linear issue tags, PR lifecycle |
| **Product & Clinical** | `moovv-fit-product` | `repos/docs/product/...` | Verifying clinical invariants, prescription rules, PDR specs |
| **Design Tokens & UI** | `moovv-design-system` | `repos/platform/design-system/...` | Svelte 5 runes, bits-ui primitives, Tailwind v4 tokens |
| **Serverless Lambda** | `aws-lambda` | `.agents/shared/skills/` | Lambda cold starts, event payloads, handler optimization |
| **Browser E2E** | `playwright-e2e` | `.agents/shared/skills/` | Authoring, debugging, or running web E2E specs |

### Activation Methods
- **Antigravity / Gemini**: Direct file read of `.agents/skills/<name>/SKILL.md`.
- **Kiro / Markdown Anchors**: `#[[file:.agents/skills/{name}/SKILL.md]]` or `#[[file:.agents/shared/skills/{name}/SKILL.md]]`.

## 📎 Steering (auto-loaded)

| File | Purpose |
|------|---------|
| `orchestration-rules.md` | Cross-repo coordination patterns, skill-first protocol & anti-patterns |
| `aws-and-cloud-credentials.md` | AWS SSO profiles, authentication, region targeting & token recovery |
| `submodule-routing.md` | Task routing to submodules |
| `linear-workflow.md` | Linear issue tracking & agent CLI workflow |
| `ci-cd-spot-runner-playbook.md` | Ephemeral Spot runner CI/CD & on-demand test execution |

## 📚 ADRs
Platform-level architecture decisions live in `docs/architecture/adr/`.
Repo-specific ADRs live in each submodule.

## 🔗 References
- `#[[file:docs/architecture/adr/ADR-001-SUBMODULE-ARCHITECTURE.md]]`
