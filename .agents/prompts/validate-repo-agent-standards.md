# Cross-Repo Agent Standards & Validation Checklist

## Context & Purpose

This prompt provides a standardized checklist for AI agents working in any Moovv Fit repository (within the domain-based monorepo at `/mnt/workspace/src/moovv-fit/repos/`). 

Run this validation whenever starting a new task or auditing a repository to ensure full alignment across Linear task tracking, Release Please automation, SSM secrets/config resolution, and repository hygiene.

---

## 1. Linear CLI Integration Validation

Every Moovv repository must be linked to the `CORE` Linear team to allow agents to discover, update, and track issues autonomously without manual team flags.

- [ ] **Check `.linear.toml` exists at repository root:**
  ```toml
  # .linear.toml
  team_id = "CORE"
  workspace = "moovv-fit"
  issue_sort = "priority"
  ```
- [ ] **Validate CLI connectivity:**
  ```bash
  /mnt/workspace/tooling/bin/linear issue query --limit 3
  ```
  *Expected:* Lists recent issues from team `CORE` without prompting for a team key.
- [ ] **Validate repository routing label:**
  Ensure current work uses your repository's label:
  - `repo:infra` (moovv-fit-infra / cdk)
  - `repo:backend` (moovv-fit-backend-node)
  - `repo:mobile` (moovv-fit-mobile)
  - `repo:web` (moovv-fit-web)
  - `repo:landing` (moovv-fit-landing)
  - `repo:docs` (moovv-fit-docs)
  - `repo:product` (moovv-fit-product)
  - `repo:design-system` (moovv-fit-design-system)
  - `repo:simulator` (moovv-fit-simulator)
  - `repo:engine` (moovv-fit-recommendation-engine / canonical)

---

## 2. Cross-Repo Dependency & Task Coordination

To prevent cross-repo drift and avoid manual user coordination:

- [ ] **Parent / Child Issue Structure:**
  - Cross-repo initiatives (e.g. auth migrations, API changes) must have a Parent Issue in Linear.
  - Each participating repo has its own sub-issue tagged with `repo:<domain>`.
- [ ] **Check Blockers Before Execution:**
  ```bash
  linear issue view <ISSUE_ID>
  ```
  Verify all `blockedBy` issues are in `Done` or `Completed` before executing downstream changes.
- [ ] **Session Scratchpad Pattern:**
  - Keep `TODO.md` strictly as a local session buffer for active micro-tasks.
  - Reference the Linear issue key at the top (`Ref: CORE-XXX`).
  - Clear `TODO.md` upon issue completion.

---

## 3. Release Please Clean Root Validation

All repositories must maintain clean root directories by locating Release Please configuration inside `.github/`.

- [ ] **Verify configuration location:**
  - Config: `.github/release-please-config.json`
  - Manifest: `.github/.release-please-manifest.json`
  - Ensure NO `release-please*` files remain in repository root.
- [ ] **Verify workflow arguments in `.github/workflows/release-please.yml`:**
  ```yaml
  - uses: googleapis/release-please-action@v4 # or v5
    with:
      token: ${{ ... }}
      config-file: .github/release-please-config.json
      manifest-file: .github/.release-please-manifest.json
  ```

---

## 4. SSM Parameter Store Integration (Zero-Hardcoding)

Environment variables and shared cloud outputs must resolve dynamically from AWS SSM Parameter Store instead of manual GitHub Environment variables.

- [ ] **Infra SSM Parameters (Single Source of Truth):**
  - Staging Pool A: `/moovv-fit/staging/cognito/mobile/pool_id` (`ap-south-1_9Y0NmMzBP`)
  - Staging Client ID: `/moovv-fit/staging/cognito/mobile/client_id` (`6rgskm5annec21iblldua9d7ka`)
  - Production Pool A: `/moovv-fit/production/cognito/mobile/pool_id` (`ap-south-1_KOMPFSGiz`)
  - Production Client ID: `/moovv-fit/production/cognito/mobile/client_id` (`6qqcpdv9q4rkeg2pmq55ao7lat`)
- [ ] **Backend (`node`):**
  - Validated that `MultiPoolVerifier` resolves `COGNITO_MOBILE_POOL_ID_NEW` and `COGNITO_CLIENT_ID` via SSM.
- [ ] **Mobile (`mobile`):**
  - Validated that CI/CD build scripts (`deploy.yml`) fetch Pool ID and Client ID via `aws ssm get-parameter`.

---

## 5. Verification Commands

Run these quick checks to certify the repository:

```bash
# 1. Verify Linear integration
/mnt/workspace/tooling/bin/linear issue query --limit 1

# 2. Verify clean root (no release-please in root)
ls -la release-please* .release-please* 2>/dev/null || echo "✅ Root clean"

# 3. Verify types and lint
pnpm check && pnpm type-check # or flutter analyze / npm test depending on repo
```

