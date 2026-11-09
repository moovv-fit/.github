# CI/CD & Ephemeral Spot Runner Playbook

> **Scope**: Platform-wide testing patterns, on-demand suite execution, and ephemeral AWS Spot runner operations for AI agents and developers.

---

## ⚡ Core Invariants

1. **Zero Quota Waste (macOS Preservation)**:
   - Free/hosted GitHub Actions minutes are strictly reserved for macOS iOS builds (`runs-on: macos-15`) in `repos/apps/mobile`.
   - All Linux workloads (CI, SAST, unit tests, integration tests, E2E) MUST use self-hosted ephemeral Spot instances:
     - General Linux compute: `runs-on: [self-hosted, spot-compute, "run-${{ github.run_id }}"]`
     - Web UI/Playwright compute: `runs-on: [self-hosted, spot-web, "run-${{ github.run_id }}"]`
2. **FIFO Runner Theft Prevention (Run-Specific Labels)**:
   - GitHub's FIFO scheduler assigns runners to the oldest queued job matching the requested labels.
   - Without run-specific labels, a runner launched for Job B can be "stolen" by older Job A, leaving Job B orphaned.
   - **Solution**: All CI workflows MUST include `"run-${{ github.run_id }}"` in `runs-on` labels.
   - The dispatcher Lambda logs presence of run-specific labels (✅ protected vs ⚠️ vulnerable).
   - JIT token expiry (5 minutes) handles cleanup of orphaned runner registrations.
3. **Ephemeral Spot Runners**:
   - Provisioned JIT via the AWS Lambda dispatcher stack (`moovv-fit-github-spot-runner`) in `ap-south-1`.
   - Multi-region Golden AMIs pre-baked with Node 22, pnpm, Docker, Python 3.12, Semgrep, Flutter, Kiro CLI, gh CLI, and Linear CLI.
   - **AMI IDs managed via SSM Parameter Store** (single source of truth):
     - SSM Path: `/moovv-fit/spot-runner/ami/{region}`
     - The bake script (`scripts/bake_runner_ami.py`) updates SSM after successful bakes.
     - Lambda dispatcher reads from SSM with 1-hour caching.
     - No code deployment needed when AMIs rotate.
   - Instances boot in ~12 seconds and terminate (`shutdown -h now`) immediately after job execution.
4. **No Duplicate CI on Merge (Rule 1)**:
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

---

## 🛡️ Sentry CI/CD & Production Observability

1. **Organization-Level Configuration**:
   - `SENTRY_AUTH_TOKEN`: Injected into GitHub Org secrets across all `moovv-fit` repositories.
   - `SENTRY_ORG`: `moovv-fit` configured as org-level variable.
2. **Automated Source Maps (Web)**:
   - During `pnpm build`, `@sentry/vite-plugin` automatically uploads source maps to Sentry for the corresponding portal (`moovv-fit-physio-pwa`, `moovv-fit-clinic-pwa`, `moovv-fit-admin-pwa`).
   - `sourcemaps.filesToDeleteAfterUpload` deletes `.map` files before S3 sync so they are never exposed publicly.
3. **Debug Symbol Uploads (Mobile)**:
   - `deploy-android`: Uploads ProGuard obfuscation mapping files to `moovv-fit-patient-mobile-android`.
   - `deploy-ios`: Uploads dSYM archives to `moovv-fit-patient-mobile-ios`.
4. **Release & Deployment Tracking**:
   - Every deploy to Staging or Production registers a release and deployment marker via `@sentry/cli`.
   - Stack traces correlate with git commits, identifying "Suspect Commits" automatically.
   - Backend API: `moovv-fit-backend-node` (DSN in SSM Parameter `/moovv-fit/shared/sentry/backend-node-dsn`).
