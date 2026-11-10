---
name: git-flow
description: Git workflow conventions including commits, branches, PRs, releases, and GitHub CLI automation. Covers Conventional Commits, branching strategies, merge policies, and gh CLI operations.
inclusion: auto
---

# Git Flow & GitHub Workflows

## Commit Conventions

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

| Type | Purpose |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code change that neither fixes nor adds |
| `perf` | Performance improvement |
| `test` | Adding or updating tests |
| `chore` | Build, CI, dependencies |
| `revert` | Revert a previous commit |

### Examples

```bash
feat(auth): add OAuth2 login flow
fix(api): handle null response from payment gateway
docs: update README with setup instructions
chore(deps): bump axios from 1.4.0 to 1.5.0
feat!: drop support for Node 16  # Breaking change
```

### Scope

Optional, indicates the affected area: `auth`, `api`, `ui`, `db`, `ci`, etc.

### Breaking Changes

Mark with `!` after type or include `BREAKING CHANGE:` in footer:

```bash
feat(api)!: change response format for /users endpoint

BREAKING CHANGE: Response now returns { data: [...] } instead of array directly.
```

## Branching Strategy

### Branch Naming

```
<type>/<ticket>-<short-description>
```

| Prefix | Purpose |
|--------|---------|
| `feature/` | New features |
| `fix/` | Bug fixes |
| `hotfix/` | Urgent production fixes |
| `release/` | Release preparation |
| `chore/` | Maintenance tasks |
| `docs/` | Documentation updates |

### Examples

```bash
feature/AUTH-123-oauth-login
fix/BUG-456-null-pointer-checkout
hotfix/PROD-789-payment-timeout
release/v2.1.0
chore/upgrade-dependencies
```

### Branch Workflow

```
main (production)
  │
  ├── develop (integration)
  │     │
  │     ├── feature/AUTH-123-oauth
  │     │
  │     └── feature/UI-456-dashboard
  │
  └── hotfix/PROD-789-critical-fix
```

**Rules:**
- `main` — Always deployable, protected
- `develop` — Integration branch (optional, some teams use main directly)
- Feature branches — Created from develop/main, merged via PR
- Hotfix branches — Created from main, merged to both main and develop

## Pull Requests

### PR Title Format

Follow the same convention as commits:

```
feat(auth): add OAuth2 login flow
fix(api): handle null response from payment gateway
```

### PR Description Template

```markdown
## Summary
Brief description of what this PR does.

## Changes
- Added OAuth2 authentication flow
- Created login/logout endpoints
- Added session management

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing completed
- [ ] Edge cases verified

## Related
Closes #123
```

### PR Checklist

Before requesting review:
- [ ] Self-reviewed the diff
- [ ] Tests pass locally
- [ ] No console.logs or debugger statements
- [ ] No secrets or credentials committed
- [ ] Documentation updated if needed
- [ ] Meaningful commit messages
- [ ] Merge conflicts resolved

## Merge Strategies

| Strategy | When to Use |
|----------|-------------|
| **Squash** | Feature branches — clean history, one commit per feature |
| **Merge** | Release branches — preserve full history |
| **Rebase** | Small fixes — linear history, experienced users only |

### Recommended Default: Squash Merge

```bash
gh pr merge 123 --squash --delete-branch
```

## Safety Rules

### Never Do

```bash
# ❌ Force push to protected branches
git push --force origin main
git push --force origin master

# ❌ Commit secrets
git add .env
git add credentials.json
git add *.pem

# ❌ Reset shared history
git reset --hard HEAD~5 && git push --force

# ❌ Delete remote branches others depend on
git push origin --delete feature/shared-work
```

### Always Do

```bash
# ✅ Use force-with-lease instead of force
git push --force-with-lease origin feature/my-branch

# ✅ Check what you're committing
git diff --staged
git status

# ✅ Pull before push
git pull --rebase origin main

# ✅ Verify branch before destructive operations
git branch --show-current
```

## GitHub CLI (gh)

### Setup

```bash
# Authenticate
gh auth login

# Check status
gh auth status
```

### Pull Requests

```bash
# Create PR
gh pr create --title "feat: add feature" --body "Description"
gh pr create --draft  # Draft PR
gh pr create --fill   # Use commit messages

# List PRs
gh pr list
gh pr list --author "@me"
gh pr list --state open

# View/checkout PR
gh pr view 123
gh pr checkout 123
gh pr diff 123

# Review
gh pr review 123 --approve
gh pr review 123 --request-changes --body "Please fix X"

# Merge
gh pr merge 123 --squash --delete-branch

# Check status
gh pr checks 123
gh pr checks 123 --watch  # Wait for CI
```

### Issues

```bash
# Create issue
gh issue create --title "Bug: login fails" --label "bug"

# List/view
gh issue list --state open
gh issue view 123

# Manage
gh issue close 123
gh issue comment 123 --body "Fixed in #456"
```

### Workflows (GitHub Actions)

```bash
# List runs
gh run list
gh run list --workflow "CI"

# View/watch
gh run view 123456
gh run watch 123456

# Re-run
gh run rerun 123456
gh run rerun 123456 --failed

# Trigger workflow
gh workflow run deploy.yml -f environment=staging
```

### Releases

```bash
# Create release
gh release create v1.0.0 --generate-notes
gh release create v1.0.0 --title "Release 1.0.0" --notes "Changelog..."
gh release create v1.0.0 --draft
gh release create v1.0.0 ./dist/*.zip  # With assets

# List/view
gh release list
gh release view v1.0.0
gh release download v1.0.0
```

### Repository

```bash
# Clone
gh repo clone owner/repo

# Create
gh repo create my-project --public
gh repo create my-project --template owner/template

# Fork
gh repo fork owner/repo --clone
```

## Semantic Versioning

```
MAJOR.MINOR.PATCH
```

| Increment | When |
|-----------|------|
| **MAJOR** | Breaking changes |
| **MINOR** | New features, backward compatible |
| **PATCH** | Bug fixes, backward compatible |

### Examples

```
1.0.0 → 1.0.1  # Bug fix
1.0.1 → 1.1.0  # New feature
1.1.0 → 2.0.0  # Breaking change
```

### Pre-release Tags

```
2.0.0-alpha.1
2.0.0-beta.1
2.0.0-rc.1
```

## Common Workflows

### Feature Development

```bash
# 1. Create branch
git checkout main
git pull origin main
git checkout -b feature/AUTH-123-oauth

# 2. Develop with atomic commits
git add -p  # Stage interactively
git commit -m "feat(auth): add OAuth2 provider config"
git commit -m "feat(auth): implement login flow"
git commit -m "test(auth): add OAuth integration tests"

# 3. Push and create PR
git push -u origin feature/AUTH-123-oauth
gh pr create --fill

# 4. After review, merge
gh pr merge --squash --delete-branch
```

### Hotfix

```bash
# 1. Branch from main
git checkout main
git pull origin main
git checkout -b hotfix/PROD-789-payment-fix

# 2. Fix and test
git commit -m "fix(payment): handle timeout in gateway response"

# 3. Push and create urgent PR
git push -u origin hotfix/PROD-789-payment-fix
gh pr create --title "fix: handle payment timeout" --label "urgent"

# 4. Merge to main (and develop if using gitflow)
gh pr merge --merge  # Preserve commit for traceability
```

### Release

```bash
# 1. Create release branch (optional)
git checkout -b release/v2.1.0

# 2. Bump version, update changelog
# ... edit package.json, CHANGELOG.md ...
git commit -m "chore: bump version to 2.1.0"

# 3. Tag and push
git tag -a v2.1.0 -m "Release 2.1.0"
git push origin v2.1.0

# 4. Create GitHub release
gh release create v2.1.0 --generate-notes
```

## Git Hooks

### Pre-commit (lint-staged)

```json
// package.json
{
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md}": ["prettier --write"]
  }
}
```

### Commit Message (commitlint)

```javascript
// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'scope-enum': [2, 'always', ['auth', 'api', 'ui', 'db', 'ci']],
  },
};
```

### Setup with Husky

```bash
npm install -D husky lint-staged @commitlint/cli @commitlint/config-conventional
npx husky init
echo "npx lint-staged" > .husky/pre-commit
echo "npx commitlint --edit \$1" > .husky/commit-msg
```

## Useful Aliases

```bash
# ~/.gitconfig
[alias]
  co = checkout
  br = branch
  ci = commit
  st = status
  lg = log --oneline --graph --decorate -20
  undo = reset --soft HEAD~1
  amend = commit --amend --no-edit
  wip = commit -am "WIP"
  branches = branch -a --sort=-committerdate
  recent = for-each-ref --sort=-committerdate refs/heads/ --format='%(committerdate:short) %(refname:short)'
```
