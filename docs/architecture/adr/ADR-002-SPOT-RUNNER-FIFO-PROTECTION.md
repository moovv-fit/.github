# ADR-002: Spot Runner FIFO Protection via Run-Specific Labels

**Status**: ✅ Current  
**Date**: 2026-11-09

## Context

The Moovv platform uses ephemeral AWS EC2 Spot instances as self-hosted GitHub Actions runners. When a `workflow_job.queued` webhook fires, an AWS Lambda dispatcher launches a Spot instance that registers with GitHub using labels like `[self-hosted, spot-compute]`.

### The Problem: Runner Theft

GitHub Actions uses FIFO (First-In-First-Out) scheduling for self-hosted runners. When a runner registers with generic labels, GitHub assigns it to the **oldest queued job** matching those labels—regardless of which job triggered the Spot instance.

**Timeline of a Runner Theft Incident:**
```
09:32:51  Job A queued (older) - requests [self-hosted, spot-compute]
09:43:38  Job B queued (newer) - requests [self-hosted, spot-compute]
09:43:40  Lambda launches Spot instance for Job B
09:44:49  Runner registers as spot-us-east-2-<job-b-id>
09:44:50  GitHub assigns runner to Job A (FIFO) ← THEFT
09:48:29  Job A completes, runner terminates (--once)
09:48:30+ Job B remains orphaned - no runner ever assigned
```

The webhook fires only once per job queue event. When the stolen runner terminates, Job B has no mechanism to request another runner.

## Decision

Add a **run-specific label** to all CI workflow `runs-on` declarations:

```yaml
# Before (vulnerable)
runs-on: [self-hosted, spot-compute]

# After (protected)
runs-on: [self-hosted, spot-compute, "run-${{ github.run_id }}"]
```

### Why `github.run_id`?

| Variable | Available at `runs-on` | Available in Webhook | Verdict |
|----------|------------------------|----------------------|---------|
| `github.run_id` | ✅ Yes | ✅ Yes (`workflow_job.run_id`) | **Use this** |
| `github.job` | ✅ Yes (YAML key) | ✅ Yes | Optional refinement |
| `workflow_job.id` | ❌ No (created on queue) | ✅ Yes | Cannot use |

`github.run_id` is the workflow run identifier, available both:
1. At workflow YAML evaluation time (for `runs-on`)
2. In the `workflow_job.queued` webhook payload (for the dispatcher)

This creates 1:1 binding between a workflow run and its dedicated runner.

### Dispatcher Changes

The Lambda dispatcher (`repos/infra/cdk/cdk/src/github-spot-runner/dispatcher.ts`) was updated to:
1. Detect `run-\d+` pattern in incoming labels
2. Log success (✅) when run-specific label is present
3. Log warning (⚠️) when generic labels are used, noting vulnerability

No cleanup Lambda is needed—GitHub's JIT (Just-In-Time) runner token expires after 5 minutes, automatically cleaning up registrations for runners that never connect.

## Consequences

### Positive

- **No more orphaned jobs**: Each runner is dedicated to its triggering run
- **Backward compatible**: Workflows without the label still work (with logged warning)
- **No additional infrastructure**: JIT token expiry handles cleanup
- **Observable**: Dispatcher logs clearly indicate protection status

### Negative

- **All CI workflows require update**: Must add the label to every `runs-on` block
- **Slightly longer labels**: Minor visual noise in workflow YAML

### Repositories Updated

| Repository | CI Workflow | Status |
|------------|-------------|--------|
| `moovv-fit-backend-node` | `.github/workflows/ci.yml` | ✅ |
| `moovv-fit-web` | `.github/workflows/ci.yml` | ✅ |
| `moovv-fit-mobile` | `.github/workflows/ci.yml` | ✅ |
| `moovv-fit-simulator` | `.github/workflows/ci.yml` | ✅ |
| `moovv-fit-infra` | `.github/workflows/ci.yml`, `deploy.yml`, `release-please.yml` | ✅ |
| `moovv-fit-kiro-spot` | `.github/workflows/ci.yml` | ✅ |

## References

- `#[[file:.kiro/steering/ci-cd-spot-runner-playbook.md]]` — CI/CD operational playbook
- `#[[file:repos/infra/cdk/cdk/src/github-spot-runner/dispatcher.ts]]` — Lambda dispatcher implementation
- GitHub Actions Runner documentation: [Self-hosted runners](https://docs.github.com/en/actions/hosting-your-own-runners)
