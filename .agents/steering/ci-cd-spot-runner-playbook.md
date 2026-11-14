# CI/CD & Ephemeral Spot Runner Playbook

> **Scope**: Platform-wide testing patterns, on-demand suite execution, and ephemeral AWS Spot runner operations for AI agents and developers.

---

## ⚡ Core Invariants

1. **Zero Quota Waste (macOS Preservation)**:
   - Free/hosted GitHub Actions minutes are strictly reserved for macOS iOS builds (`runs-on: macos-15`) in `repos/apps/mobile`.
   - All Linux workloads (CI, SAST, unit tests, integration tests, E2E) MUST use self-hosted ephemeral instances:
     - General Linux compute: `runs-on: [self-hosted, spot-compute, "run-${{ github.run_id }}"]`
     - Web UI/Playwright compute: `runs-on: [self-hosted, spot-web, "run-${{ github.run_id }}"]`
     - **Critical deploys (CDK)**: `runs-on: [self-hosted, ondemand-compute, "run-${{ github.run_id }}"]`
2. **FIFO Runner Theft Prevention (Run-Specific Labels)**:
   - GitHub's FIFO scheduler assigns runners to the oldest queued job matching the requested labels.
   - Without run-specific labels, a runner launched for Job B can be "stolen" by older Job A, leaving Job B orphaned.
   - **Solution**: All CI workflows MUST include `"run-${{ github.run_id }}"` in `runs-on` labels.
   - The dispatcher Lambda logs presence of run-specific labels (✅ protected vs ⚠️ vulnerable).
   - JIT token expiry (5 minutes) handles cleanup of orphaned runner registrations.
3. **Ephemeral Spot Runners**:
   - Provisioned JIT via the AWS Lambda dispatcher stack (`moovv-fit-github-spot-runner`) in `ap-south-1`.
   - Multi-region Golden AMIs pre-baked with Node 26, pnpm, Docker, Python 3.12, Semgrep, Flutter 3.50, Kiro CLI, gh CLI, and Linear CLI.
   - **AMI IDs managed via SSM Parameter Store** (single source of truth):
     - SSM Path: `/moovv-fit/spot-runner/ami/{region}`
     - The bake script (`scripts/bake_runner_ami.py`) updates SSM after successful bakes.
     - Lambda dispatcher reads from SSM with 1-hour caching.
     - No code deployment needed when AMIs rotate.
   - Instances boot in ~12 seconds and terminate (`shutdown -h now`) immediately after job execution.
   - **On-Demand vs Spot Selection**:
     - `spot-compute`, `spot-web`: Spot instances (~70-80% cost savings, may be reclaimed)
     - `ondemand-compute`: On-demand instances (full price, no reclamation risk)
     - Use `ondemand-compute` for long-running critical jobs (CDK deploys 15-20 min) where reclamation would block releases
   - **Runner Reuse for Sequential Jobs** (CORE-233):
     - `spot-reuse`, `ondemand-reuse`: Persistent runners that stay alive between sequential jobs in the same workflow
     - Requires `chain-${{ github.repository_id }}-${{ github.run_id }}` label for uniqueness
     - Rolling idle timeout (10 min) resets after each job completes
     - Hard stop (spot: 2hr, on-demand: 1hr) prevents cost overruns
4. **No Duplicate CI on Merge (Rule 1)**:
   - Merging a PR into `main` must NEVER trigger duplicate CI test runs.
   - Pushes to `main` run the release pipeline (`release-pipeline.yml` for mobile, `deploy.yml` for other repos).

---

## 🏷️ Runner Label Reference (CORE-232, CORE-233)

### Label Matrix

| Label | Instance Lifecycle | Market Type | Use Case |
|-------|-------------------|-------------|----------|
| `spot-compute` | Ephemeral (JIT) | Spot | CI, unit tests, short stateless jobs |
| `spot-web` | Ephemeral (JIT) | Spot | Playwright E2E, web builds |
| `ondemand-compute` | Ephemeral (JIT) | On-demand | Long CDK deploys (15-20 min) |
| `spot-reuse` | Persistent (idle TTL) | Spot | Sequential jobs, warm cache, tolerates reclaim |
| `ondemand-reuse` | Persistent (idle TTL) | On-demand | Sequential deploys, warm cache, guaranteed completion |

### Ephemeral Runners (Default)
Single-use runners that terminate immediately after one job:

```yaml
# Standard CI job
ci:
  runs-on: [self-hosted, spot-compute, "run-${{ github.run_id }}"]

# Long-running deploy (no reclaim risk)
deploy:
  runs-on: [self-hosted, ondemand-compute, "run-${{ github.run_id }}"]
```

### Reuse Runners (Sequential Jobs)
Persistent runners for sequential jobs in the same workflow run:

```yaml
# Deploy staging, then reuse warm runner for production
deploy-staging:
  runs-on: [self-hosted, ondemand-reuse, "chain-${{ github.repository_id }}-${{ github.run_id }}"]

deploy-production:
  needs: deploy-staging
  runs-on: [self-hosted, ondemand-reuse, "chain-${{ github.repository_id }}-${{ github.run_id }}"]
```

**Benefits of reuse:**
- pnpm cache already warm (~50s → ~5s)
- CDK context and assets cached
- Docker layers cached
- No duplicate boot overhead

**Chain ID requirement:**
- Format: `chain-{repository_id}-{run_id}`
- Ensures uniqueness per workflow run per repository
- Dispatcher validates: `*-reuse` requires `chain-*`, and vice versa

### Timeout Behavior (Reuse Runners)

| Runner Type | Idle Timeout | Hard Stop |
|-------------|--------------|-----------|
| `spot-reuse` | 10 min rolling | 2 hours |
| `ondemand-reuse` | 10 min rolling | 1 hour |

- **Idle timeout**: Resets after each job completes. Runner terminates if idle for 10 min with no job.
- **Hard stop**: Absolute max lifetime regardless of activity (on-demand is shorter due to ~3x cost).

---

## 📱 Mobile Release Pipeline

The mobile repo (`moovv-fit/moovv-fit-mobile`) uses a progressive validation pipeline on merge to `main`:

```
merge to main → release-please (tag) → web deploy → Maestro E2E → Firebase deploy
                                                                        │
                                                           (manual) → Store upload
```

| Stage | Runner | Duration | Gate |
|-------|--------|----------|------|
| Release-Please | `spot-compute` | ~30s | Auto |
| Web Deploy | `spot-compute` | ~2-3 min | Auto |
| Maestro E2E | `spot-web` | ~5 min | **Blocking** |
| Firebase Android | `spot-compute` | ~8 min | Auto |
| Firebase iOS | `macos-15` | ~15 min | Auto |
| Store Upload | Manual dispatch | ~5 min | **Manual** |

### Manual Store Submission (After Firebase QA)
```bash
# Android → Play Store
gh workflow run deploy.yml --repo moovv-fit/moovv-fit-mobile --ref main \
  -f environment=production \
  -f platform=android \
  -f upload_to_store=true \
  -f distribution_channel=store

# iOS → App Store Connect
gh workflow run deploy.yml --repo moovv-fit/moovv-fit-mobile --ref main \
  -f environment=production \
  -f platform=ios \
  -f upload_to_store=true \
  -f distribution_channel=store
```

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
  ```bash
  # Inspect failed artifacts from S3 (requires active SSO session):
  aws s3 ls s3://moovv-fit-release-assets/ci/e2e-reports/ --profile moovv-fit-ujwal-admin
  ```

### AWS Cloud Credentials & Profile
When managing Spot runner AMIs, dispatcher Lambdas, or querying SSM parameters:
- **SSO Profile**: `moovv-fit-ujwal-admin` (interactive) or `moovv-fit-worker` (CI/Spot)
- **Region**: `ap-south-1`
- **Re-authenticate**: `aws sso login --profile moovv-fit-ujwal-admin --use-device-code` (see `aws-and-cloud-credentials.md`)

---

## 🤖 Agent Hooks on Spot Runners

Kiro agent sessions on ephemeral spot runners set `KIRO_SPOT=1` to distinguish CI/codegen contexts from interactive developer sessions.

### Hook Type Guidelines

| Hook Purpose | Type | Spot Behavior |
|--------------|------|---------------|
| Prompt injection (reminders, context) | `agent` | Fires in both modes (acceptable) |
| Actual work (linting, external tools) | `command` | Guard with `KIRO_SPOT` check |

**Why this matters:**
- `agent`-type hooks inject prompts into model context directly
- `command`-type hooks with `echo` only work on triggers that forward stdout (`SessionStart`, `UserPromptSubmit`, `PreTaskExec`, `PreCompact`, `PostCompact`)
- Triggers like `PostFileSave`, `Stop`, `PostToolUse` do NOT forward stdout — `echo`-based prompt injection silently fails

### Command Hook Pattern

For hooks that do actual work (file I/O, external API calls), skip on spot runners:

```json
{
  "version": "v1",
  "hooks": [{
    "name": "Quality Guard",
    "trigger": "PostFileSave",
    "matcher": "\\.(ts|tsx)$",
    "action": {
      "type": "command",
      "command": "[ \"$KIRO_SPOT\" = \"1\" ] && exit 0; /mnt/workspace/tooling/bin/agent-router route-steering"
    }
  }]
}
```

### Agent Hook Pattern

For hooks that inject prompts/reminders, use `agent` type (fires in both modes):

```json
{
  "version": "v1",
  "hooks": [{
    "name": "Session End Reminder",
    "trigger": "Stop",
    "action": {
      "type": "agent",
      "prompt": "Before ending, ensure all changes are committed with proper Linear issue references."
    }
  }]
}
```

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
