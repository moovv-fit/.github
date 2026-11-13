---
inclusion: auto
name: Commit Conventions
description: "Standardized commit message format with Linear issue references for all Moovv Fit repositories."
---

# Commit Conventions

## Commit Title Format

```
type(scope): description (LINEAR-ISSUE) [SPEC-ID]
```

- **type**: The category of change (feat, fix, docs, etc.)
- **scope**: The domain or component affected (mobility, auth, telehealth, etc.)
- **description**: What the commit does (imperative mood, lowercase)
- **LINEAR-ISSUE**: Required Linear issue reference in parentheses
- **SPEC-ID**: Optional spec reference in brackets (when working from a Kiro spec)

### Examples

```
feat(mobility): add kinetic chain validation (CORE-145) [SPEC-006]
fix(auth): resolve token refresh race condition (CLINIC-456)
docs(api): update v2 endpoint documentation (CORE-789)
refactor(payments): extract Razorpay adapter (CORE-101) [SPEC-012]
test(telehealth): add integration tests for video reconnect (CLINIC-202)
chore(deps): update dependencies to latest versions (CORE-303)
ci(release): add Maestro E2E tests to pipeline (CORE-404)
style(physio-portal): fix lint warnings (CLINIC-505)
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

## Scope Reference

Use a meaningful scope that describes the domain or component:

| Scope | Description | Examples |
|-------|-------------|----------|
| `mobility` | Exercise/mobility features | kinetic chain, ROM |
| `auth` | Authentication/authorization | login, OTP, tokens |
| `telehealth` | Video/remote features | calls, scheduling |
| `payments` | Payment processing | Razorpay, subscriptions |
| `api` | API endpoints | routes, handlers |
| `physio-portal` | Physio web portal | physio UI |
| `clinic-portal` | Clinic web portal | clinic UI |
| `admin-portal` | Admin web portal | admin UI |
| `deps` | Dependencies | package updates |
| `release` | Release pipeline | CI/CD |

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
feat(auth): add login endpoint

# Missing scope
feat: add login endpoint (CORE-123)

# Vague description
fix(auth): fix bug (CORE-123)

# Too long (> 72 chars title)
feat(mobility): add comprehensive kinetic chain validation with ROM analysis and feedback (CORE-145)

# Wrong type
feat(docs): fix typo in README (CORE-999)  # Should be 'docs' type

# Borrowing unrelated issue
feat(payments): add Razorpay flow (CORE-999)  # CORE-999 is for docs, not payments
```

### ✅ Correct

```
feat(mobility): add kinetic chain validation (CORE-145) [SPEC-006]
fix(auth): resolve token refresh race condition (CLINIC-456)
docs(api): update API documentation (CORE-789)
refactor(payments): extract Razorpay adapter (CORE-101) [SPEC-012]
```

---

## Skills Encouragement

When working with AWS resources, consider using available Kiro skills that provide built-in patterns and best practices:

- **amazon-aurora-postgresql** — For Aurora PostgreSQL database operations (queries, schema management, cluster creation). Keywords: aurora, postgresql, database, aws, rds
- **aws-security-agent** — For security scanning, threat modeling, and penetration testing. Keywords: security scan, code review, sast, pentest

Skills are activated automatically based on keywords in your request, or explicitly via `load_resource`.

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
