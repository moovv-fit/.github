# CI/CD & Ephemeral Spot Runner Playbook

> **Scope**: Platform-wide testing patterns, on-demand suite execution, and ephemeral AWS Spot runner operations for AI agents and developers.

---

## ⚡ Core Invariants

1. **Zero Quota Waste (macOS Preservation)**:
   - Free/hosted GitHub Actions minutes are strictly reserved for macOS iOS builds (`runs-on: macos-15`) in `repos/apps/mobile`.
   - All Linux workloads (CI, SAST, unit tests, integration tests, E2E) MUST use self-hosted ephemeral Spot instances:
     - General Linux compute: `runs-on: [self-hosted, spot-compute]`
     - Web UI/Playwright compute: `runs-on: [self-hosted, spot-web]`
2. **Ephemeral Spot Runners**:
   - Provisioned JIT via the AWS Lambda dispatcher stack (`moovv-fit-spot-runner-dispatcher`) in `ap-south-1`.
   - Multi-region Golden AMIs pre-baked with Node 22, pnpm, Docker, Python 3.12, Semgrep, Flutter, and Maestro:
     - `us-east-2`: `ami-0840c9f13119c6201`
     - `us-east-1`: `ami-0dd7c5e44cb54532f`
     - `us-west-2`: `ami-0e9ca90dd60332cdb`
     - `eu-west-1`: `ami-081dfdc01223cfeec`
     - `ap-south-1`: `ami-0f38dc9a9dbfad965`
   - Instances boot in ~12 seconds and terminate (`shutdown -h now`) immediately after job execution.
3. **No Duplicate CI on Merge (Rule 1)**:
   - Merging a PR into `main` must NEVER trigger duplicate CI test runs.
   - Pushes to `main` run only Release-Please and environment CD (`deploy.yml`).

---

## 🧪 Running Tests Without Deployments or PRs

AI agents and developers do NOT need to deploy environments or open PRs to execute test suites.

### 1. On-Demand Cloud E2E Test Suite (Ephemeral Spot Runner)
Targets existing persistent staging environment (`api-staging.moovv.fit`) with zero deployment overhead:
```bash
# Backend E2E Smoke suite:
gh workflow run e2e.yml --repo moovv-fit/moovv-fit-backend-node \
  -f environment=staging \
  -f suite=smoke

# Backend Full E2E suite (with automatic test data cleanup):
gh workflow run e2e.yml --repo moovv-fit/moovv-fit-backend-node \
  -f environment=staging \
  -f suite=full

# Mobile Maestro Web E2E (Headless Chrome on spot runner):
gh workflow run maestro-e2e.yml --repo moovv-fit/moovv-fit-mobile --ref main
```

### 2. On-Demand Unit, Integration & SAST Suites (Ephemeral Spot Runner)
Run an entire submodule test suite on `main` or any feature branch on a spot runner:
```bash
# Backend (Prisma, Biome, Vitest Unit & Integration, Semgrep SAST, CDK Synth)
gh workflow run ci.yml --repo moovv-fit/moovv-fit-backend-node --ref main

# Web (Biome, TypeScript, Vitest Unit, Production Build, Bundle Size)
gh workflow run ci.yml --repo moovv-fit/moovv-fit-web --ref main

# Mobile (Flutter Unit & Widget Tests)
gh workflow run ci.yml --repo moovv-fit/moovv-fit-mobile --ref main

# Infra (CDK Synth, Biome, TypeScript)
gh workflow run ci.yml --repo moovv-fit/moovv-fit-infra --ref main
```

### 3. Local Test Execution (Dev Machine / Container)
Run suites directly without cloud resources:
```bash
# Backend unit & integration tests (in-memory / mock DB):
cd repos/backend/node && pnpm test:unit && pnpm test:integration

# Web unit tests & type check:
cd repos/apps/web && pnpm test && pnpm type-check

# Mobile unit & widget tests:
cd repos/apps/mobile
cp .env.example .env && cp .env.example .env.staging && cp .env.example .env.production
flutter test

# Multi-Persona E2E Simulator (Local UI + Engine against Staging APIs):
cd repos/platform/simulator
pnpm install && pnpm build:ui && pnpm simulate
# UI available at http://localhost:3000
```

---

## 🔍 Inspecting & Analyzing Test Results

```bash
# View latest run status for a repo:
gh run list --repo moovv-fit/moovv-fit-backend-node --limit 1

# Inspect step-by-step progress and annotations:
gh run view <RUN_ID> --repo moovv-fit/moovv-fit-backend-node

# View failed logs only:
gh run view <RUN_ID> --repo moovv-fit/moovv-fit-backend-node --log-failed
```
* **GitHub Summary**: Detailed Markdown summary in `$GITHUB_STEP_SUMMARY`.
* **JUnit Reports**: Populated under the GitHub Checks tab.
* **Artifacts**: S3 sync for failed HTML reports (`s3://moovv-fit-release-assets/ci/e2e-reports/`).
