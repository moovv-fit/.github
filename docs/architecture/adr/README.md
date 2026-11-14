# Architecture Decision Records

Platform-level architecture decisions for the Moovv Fit ecosystem.

For repo-specific ADRs, see the `docs/architecture/adr/` directory in each submodule.

## Index

| ADR | Title | Status |
|-----|-------|--------|
| [ADR-001](./ADR-001-SUBMODULE-ARCHITECTURE.md) | Submodule Architecture for Moovv Platform | ✅ Current |
| [ADR-002](./ADR-002-SPOT-RUNNER-FIFO-PROTECTION.md) | Spot Runner FIFO Protection via Run-Specific Labels | ✅ Current |
| [ADR-003](./ADR-003-AWS-COST-OPTIMIZATION-AND-INFRASTRUCTURE-CONSOLIDATION.md) | AWS Cost Optimization, Secrets Elimination, and RDS Right-Sizing | ✅ Current |
| [ADR-004](./ADR-004-VIDEO-ASSESSMENT-ARCHITECTURE.md) | Video Assessment Architecture | ✅ Current |
| [ADR-005](./ADR-005-AGENT-TOKEN-OPTIMIZATION-AND-STEERING-STANDARDS.md) | Agent Token Burn Optimization and Steering Standards | ✅ Current |

## Template

When creating new ADRs, use this structure:

```markdown
# ADR-XXX: Title

**Status**: 🚧 Proposed | ✅ Current | ⛔ Superseded  
**Last Updated**: YYYY-MM-DD

## Context
What is the issue that we're seeing that is motivating this decision?

## Decision
What is the change that we're proposing?

## Consequences
What becomes easier or more difficult because of this change?

## References
Links to related docs, code, or other ADRs.
```
