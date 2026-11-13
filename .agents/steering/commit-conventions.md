---
inclusion: auto
name: Commit Conventions
description: "Standardized commit message format with Linear issue references for all Moovv Fit repositories."
---

# Commit Conventions

## Commit Title Format

```
type(LINEAR-ISSUE): description
```

### Examples

```
feat(CORE-123): add login endpoint with OTP verification
fix(CLINIC-456): resolve auth token refresh race condition
docs(CORE-789): update API documentation for v2 endpoints
refactor(CORE-101): extract payment service into separate module
test(CLINIC-202): add integration tests for telehealth flow
chore(CORE-303): update dependencies to latest versions
ci(CORE-404): add Maestro E2E tests to release pipeline
style(CLINIC-505): fix lint warnings in physio portal
```

---

## Type Reference

| Type | Description | When to Use |
|------|-------------|-------------|
| `feat` | New feature | Adding new functionality |
| `fix` | Bug fix | Fixing broken behavior |
| `docs` | Documentation | README, ADRs, inline docs, comments |
| `style` | Code style | Formatting, linting (no logic change) |
| `refactor` | Refactoring | Code restructure (no behavior change) |
| `test` | Tests | Adding or updating tests |
| `chore` | Maintenance | Dependencies, configs, tooling |
| `ci` | CI/CD | Workflow files, deployment scripts |

---

## Linear Issue Requirement

**All commits MUST reference a Linear issue.** This is enforced by the `linear-issue-check.json` hook.

### Finding or Creating Issues

```bash
# Search for existing issue
linear issue list -t CORE --limit 10

# Create new issue if none exists
linear issue create \
  --team CORE \
  --title "[Backend] Add login endpoint" \
  --state "In Progress"
```

### Team Prefixes

| Prefix | Team | Scope |
|--------|------|-------|
| `CORE-` | Platform Core | Backend, Mobile, Landing, Design System, Infra |
| `CLINIC-` | Clinic OS | Web Portals (Physio, Clinic, Admin) |

---

## Commit Body Guidelines

For complex changes, add a body after a blank line:

```
feat(CORE-123): add login endpoint with OTP verification

- Implement Cognito custom auth flow
- Add rate limiting (5 attempts per 15 min)
- Include WhatsApp OTP channel fallback

Closes CORE-123
```

### Body Best Practices

1. **Bullet points** for multiple changes
2. **Present tense** ("add" not "added")
3. **No period** at end of title
4. **72 character** line wrap in body
5. **Reference closing** with `Closes LINEAR-XXX` or `Fixes LINEAR-XXX`

---

## Anti-Patterns

### ❌ Avoid

```
# Missing issue reference
feat: add login endpoint

# Wrong format (issue in wrong position)
feat: add login endpoint (CORE-123)

# Vague description
fix(CORE-123): fix bug

# Too long (> 72 chars)
feat(CORE-123): add comprehensive login endpoint with OTP verification and WhatsApp fallback

# Wrong type
feat(CORE-123): fix typo in README  # Should be 'docs'

# Borrowing unrelated issue
feat(CORE-999): add payment flow  # CORE-999 is for docs, not payment
```

### ✅ Correct

```
feat(CORE-123): add login endpoint with OTP verification
fix(CLINIC-456): resolve auth token refresh race condition
docs(CORE-789): update API documentation
```

---

## Scope Specificity (Optional)

For large repos, add scope after the type:

```
feat(CORE-123/auth): add OTP verification
fix(CLINIC-456/telehealth): resolve video reconnect
refactor(CORE-789/payments): extract Razorpay adapter
```

---

## Breaking Changes

Indicate breaking changes with `!` after type:

```
feat(CORE-123)!: change auth response schema

BREAKING CHANGE: The /auth/login response now returns
`accessToken` instead of `token`. All clients must update.
```

---

## Automated Enforcement

The `linear-issue-check.json` hook validates:

1. Commit message starts with valid type
2. Linear issue ID is present in parentheses
3. Issue ID matches `CORE-XXX` or `CLINIC-XXX` pattern
4. Description is present after colon

### Bypassing (Emergency Only)

```bash
git commit --no-verify -m "emergency: hotfix production crash"
```

Use sparingly. Create Linear issue retroactively.

---

## References

- `linear-workflow.md` — Linear CLI commands and patterns
- `worktree-workflow.md` — Branch naming conventions
