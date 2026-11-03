# Contributing to Moovv Fit

This is the master orchestration repository containing all Moovv Fit repos as submodules.

## Repository Structure

Each submodule is an independent git repository with its own:
- Branches and commit history
- CI/CD pipelines
- Code owners and review process

The master repo tracks which commit each submodule points to.

## Working with Submodules

### Initial Clone

```bash
git clone --recurse-submodules git@github.com:moovv-fit/moovv-fit.git
```

Or if you already cloned without submodules:

```bash
git submodule update --init --recursive
```

### Update All Submodules

```bash
git submodule update --remote --merge
```

### Working in a Submodule

```bash
# Navigate to submodule
cd repos/backend/node

# Create feature branch
git checkout -b feature/my-feature

# Make changes, commit, push
git add -A
git commit -m "feat: my changes"
git push origin feature/my-feature

# Create PR in the submodule's repo
```

### Updating the Master Repo

After submodule changes are merged:

```bash
# From master repo root
cd /path/to/moovv-fit

# Update submodule pointer
git add repos/backend/node
git commit -m "chore: update backend submodule"
git push
```

## Cross-Repo Changes

When a change spans multiple repositories:

1. **Plan** — Document which repos are affected
2. **Branch** — Create feature branches in each affected submodule
3. **Implement** — Make changes in each submodule
4. **PR** — Create PRs in each submodule repo, linking them together
5. **Merge** — Merge submodule PRs first
6. **Update Master** — Update master repo to point to new commits

### Example: API + Mobile Feature

```bash
# 1. Backend changes
cd repos/backend/node
git checkout -b feature/exercise-history
# ... make changes ...
git commit -m "feat(api): add exercise-history endpoint"
git push origin feature/exercise-history
# Create PR in moovv-fit-backend-node

# 2. Mobile changes  
cd ../apps/mobile
git checkout -b feature/exercise-history
# ... make changes ...
git commit -m "feat(history): add exercise history screen"
git push origin feature/exercise-history
# Create PR in moovv-fit-mobile (link to backend PR)

# 3. After both PRs merged, update master
cd ../../..
git add repos/backend/node repos/apps/mobile
git commit -m "feat: exercise history feature"
git push
```

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): description

feat:     New feature
fix:      Bug fix
docs:     Documentation
chore:    Maintenance
refactor: Code refactoring
test:     Tests
ci:       CI/CD changes
```

## Code Review

- Submodule changes are reviewed in their respective repos
- Master repo updates (submodule pointer changes) require review
- Cross-repo changes should reference related PRs

## Questions?

Check the [AGENTS.md](./AGENTS.md) for AI agent configuration or reach out to the team.
