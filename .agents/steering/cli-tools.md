---
inclusion: manual
name: CLI Tools
description: "Standard CLI tool configuration and usage patterns for AWS, Linear, and GitHub across Moovv Fit."
---

# CLI Tools

## AWS CLI

### SSO Profile Configuration

All AWS CLI commands use the `moovv-fit-ujwal-admin` SSO profile:

```bash
# Authenticate (opens browser for SSO)
aws sso login --profile moovv-fit-ujwal-admin

# Verify authentication
aws sts get-caller-identity --profile moovv-fit-ujwal-admin
```

### Using the Profile

Always specify the profile explicitly:

```bash
# ✅ Correct
aws s3 ls --profile moovv-fit-ujwal-admin
aws ssm get-parameter --name "/moovv-fit/shared/sentry/backend-node-dsn" --profile moovv-fit-ujwal-admin

# ❌ Avoid (relies on default profile)
aws s3 ls
```

### Environment Variable Alternative

For scripts or long sessions:

```bash
export AWS_PROFILE=moovv-fit-ujwal-admin
aws s3 ls  # Now uses the exported profile
```

---

## AWS Skills

For complex AWS operations, consider using available Kiro skills that provide built-in patterns and best practices:

| Skill | Keywords | Use For |
|-------|----------|---------|
| `amazon-aurora-postgresql` | aurora, postgresql, database, aws, rds | Database operations, queries, schema management, cluster creation |
| `aws-security-agent` | security scan, code review, sast, pentest | Security scanning, threat modeling, penetration testing |

Skills are activated automatically based on keywords in your request, or explicitly via `load_resource`. They encapsulate AWS patterns including SSO authentication, SSM parameter retrieval, and service-specific best practices.

---

## SSM Parameter Store

### Path Convention

SSM parameters follow this hierarchy:

```
/moovv-fit/{environment}/{service}/{key}
```

| Segment | Values | Examples |
|---------|--------|----------|
| `environment` | `shared`, `staging`, `production` | `/moovv-fit/shared/...` |
| `service` | Service or component name | `sentry`, `cognito`, `github` |
| `key` | Parameter name | `dsn`, `pool-id`, `client-id` |

### Common Parameters

| Parameter Path | Description |
|----------------|-------------|
| `/moovv-fit/shared/sentry/backend-node-dsn` | Sentry DSN for backend |
| `/moovv-fit/{env}/cognito/mobile/pool_id` | Cognito User Pool ID |
| `/moovv-fit/{env}/cognito/mobile/client_id` | Cognito App Client ID |
| `/moovv-fit/spot-runner/ami/{region}` | Golden AMI ID for Spot runners |

### Retrieving Parameters

```bash
# Plain text parameter
aws ssm get-parameter \
  --name "/moovv-fit/shared/sentry/backend-node-dsn" \
  --profile moovv-fit-ujwal-admin \
  --query "Parameter.Value" \
  --output text

# Encrypted parameter (SecureString)
aws ssm get-parameter \
  --name "/moovv-fit/production/cognito/mobile/pool_id" \
  --with-decryption \
  --profile moovv-fit-ujwal-admin \
  --query "Parameter.Value" \
  --output text
```

### Setting Parameters

```bash
# Plain text
aws ssm put-parameter \
  --name "/moovv-fit/staging/myservice/config" \
  --value "config-value" \
  --type String \
  --profile moovv-fit-ujwal-admin

# Encrypted (SecureString)
aws ssm put-parameter \
  --name "/moovv-fit/production/myservice/secret" \
  --value "secret-value" \
  --type SecureString \
  --profile moovv-fit-ujwal-admin
```

---

## Linear CLI

The `linear` CLI is pre-installed and authenticated as workspace admin (`moovv-fit`).

### Quick Reference

```bash
# Create issue
linear issue create \
  --team CORE \
  --title "[Backend] Add feature X" \
  --description "Details..." \
  --priority 2 \
  --state Backlog

# Update issue status
linear issue update CORE-123 --state "In Progress"
linear issue update CORE-123 --state Done

# View issue
linear issue view CORE-123

# List issues
linear issue list -t CORE --limit 10
linear issue list -t CLINIC --state "In Progress"
```

### Teams

| Team | ID | Prefix | Scope |
|------|-----|--------|-------|
| CORE | `5e29efad-4ed6-468d-a0e9-29f1e75b4f05` | `CORE-` | Platform, Backend, Mobile, Infra |
| CLINIC | `1770afb0-d1a0-44d6-958a-51ec8d2706c1` | `CLINIC-` | Clinic OS, Web Portals |

See `linear-workflow.md` for detailed patterns.

---

## GitHub CLI (`gh`)

### Authentication

```bash
# Check auth status
gh auth status

# Login if needed
gh auth login
```

### Fork Repository Defaults (IMPORTANT)

All submodules are forks with both `origin` (moovv-fit) and `upstream` (moovvfit) remotes. By default, `gh pr create` targets the **upstream** repo, which is usually not what we want.

**Fix:** Set the default repo to origin for each submodule:

```bash
# One-time setup per repo
gh repo set-default moovv-fit/moovv-fit-web
gh repo set-default moovv-fit/moovv-fit-mobile
gh repo set-default moovv-fit/moovv-fit-backend-node
# ... etc
```

This creates a `.git/.gh-resolved` file that persists the setting. All repos should have this configured:

| Submodule | Default Repo |
|-----------|--------------|
| `repos/apps/web` | `moovv-fit/moovv-fit-web` |
| `repos/apps/mobile` | `moovv-fit/moovv-fit-mobile` |
| `repos/apps/landing` | `moovv-fit/moovv-fit-landing` |
| `repos/backend/node` | `moovv-fit/moovv-fit-backend-node` |
| `repos/infra/cdk` | `moovv-fit/moovv-fit-infra` |
| `repos/platform/design-system` | `moovv-fit/moovv-fit-design-system` |
| `repos/platform/simulator` | `moovv-fit/moovv-fit-simulator` |
| `repos/docs/technical` | `moovv-fit/moovv-fit-docs` |
| `repos/docs/product` | `moovv-fit/moovv-fit-product` |

**Verify:** After cloning fresh, run this in each submodule:
```bash
gh repo set-default  # Shows current default
```

### Common Operations

```bash
# Create PR
gh pr create --title "feat(CORE-123): Add feature" --body "Description"

# View PR
gh pr view 42

# List PRs
gh pr list --state open

# Trigger workflow
gh workflow run deploy.yml --ref main -f environment=staging

# View workflow runs
gh run list --limit 5
gh run view <RUN_ID>
gh run view <RUN_ID> --log-failed
```

### Repository Context

Most `gh` commands auto-detect the repo from git remote. To be explicit:

```bash
gh pr list --repo moovv-fit/moovv-fit-backend-node
gh workflow run ci.yml --repo moovv-fit/moovv-fit-web --ref main
```

---

## Quick Reference Card

| Task | Command |
|------|---------|
| AWS SSO Login | `aws sso login --profile moovv-fit-ujwal-admin` |
| Get SSM Parameter | `aws ssm get-parameter --name "..." --with-decryption --profile moovv-fit-ujwal-admin` |
| Create Linear Issue | `linear issue create --team CORE --title "..." --state Backlog` |
| Update Linear Status | `linear issue update CORE-123 --state Done` |
| Create GitHub PR | `gh pr create --title "..." --body "..."` |
| Trigger CI Workflow | `gh workflow run ci.yml --ref main` |
| View Failed Logs | `gh run view <ID> --log-failed` |

---

## References

- `linear-workflow.md` — Detailed Linear patterns
- `ci-cd-spot-runner-playbook.md` — CI/CD and workflow dispatch
