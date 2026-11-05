# ADR-001: Submodule Architecture for Moovv Platform

**Status**: ✅ Current  
**Last Updated**: 2026-11-03

## Context

The Moovv Fit platform consists of 9 repositories spanning backend, mobile, web, infrastructure, and documentation. Managing these as independent repos created challenges:

- **Context switching**: Opening each repo separately fragmented AI agent context
- **Cross-repo visibility**: Difficult to understand dependencies and make coordinated changes
- **Session sprawl**: Kiro chat sessions scattered across workspaces
- **Onboarding friction**: New developers needed to clone 9+ repos manually

## Decision

Consolidate all Moovv repositories under a single **master orchestration repo** (`moovv-fit`) using git submodules, organized by domain:

```
repos/
├── apps/           # User-facing applications
│   ├── mobile/     # Flutter iOS/Android app
│   ├── web/        # React 19 / Vite portals
│   └── landing/    # HTML5 / CSS3 marketing site
├── backend/        # Server-side services
│   ├── node/       # Primary Lambda API (Node 22 / Prisma / CDK)
│   ├── moovvfit-recommendation-engine/ # Python recommendation engine
│   └── exercise-canonical-analysis/    # Python semantic embeddings
├── infra/          # Infrastructure
│   └── cdk/        # Shared CDK constructs
├── platform/       # Shared platform components
│   ├── design-system/  # Svelte 5 component library
│   └── simulator/      # E2E test harness
└── docs/           # Documentation
    ├── technical/  # Technical developer docs (SvelteKit)
    └── product/    # Product specifications & clinical invariants
```

### Submodule Registration (Not Clone)

Repos were **physically moved** into the master repo structure, then registered as submodules. This preserves:
- All uncommitted changes
- Unpushed commits
- Local branches
- Git history

### Session Migration

Session migration tools ensure historical chat sessions appear when opening repos from new paths:
- **Kiro Sessions**: `scripts/migrate-kiro-sessions.sh` updates Kiro workspace hashes, session paths, and index files in `~/.kiro/`.
- **Antigravity Sessions**: `scripts/migrate-antigravity-sessions.py` updates the conversation summaries database (`~/.gemini/antigravity/conversation_summaries.db`) and FTS tables, re-linking historical conversations to the master workspace project ID (`moovv-fit`) and new submodule URIs.

## Consequences

### Positive

- **Single workspace**: Clone one repo, get entire platform
- **Domain organization**: Clear grouping by function (apps, backend, infra, etc.)
- **Preserved autonomy**: Each submodule keeps its own `.kiro/`, `.agents/`, AGENTS.md
- **AI agent continuity**: Session history follows repos to new locations
- **Cross-repo context**: Master repo can coordinate multi-repo changes

### Negative

- **Submodule complexity**: Git submodules have learning curve
- **Two-step commits**: Changes in submodules require commit in sub + parent
- **Potential stale pointers**: Parent may point to old submodule commits

### Mitigations

| Risk | Mitigation |
|------|------------|
| Stale submodule pointers | CI check that submodules are on recent commits |
| Submodule confusion | Documentation in AGENTS.md and this ADR |
| Session migration failures | Backup created before migration; script is idempotent |

## Implementation Details

### Kiro Session Hash Algorithm

Kiro uses SHA256(path)[0:16] to map workspaces to session storage:
```bash
echo -n "/mnt/workspace/src/moovv-fit/repos/backend/node" | sha256sum | cut -c1-16
```

Migration script updates:
1. `~/.kiro/sessions/<hash>/` — session data directories
2. `~/.kiro/workspace-roots/<hash>/` — workspace metadata
3. `~/.kiro/session-index/<hash>.jsonl` — session lookup index
4. `session.json` files — `workspacePaths` and `rootPaths` arrays

### Antigravity Session Migration Architecture

Antigravity stores conversation state and metadata in SQLite databases:
- **Conversation State**: `~/.gemini/antigravity/conversations/<uuid>.db`
- **Session Index**: `~/.gemini/antigravity/conversation_summaries.db`
- **Project Definitions**: `~/.gemini/config/projects/<project_id>.json`

The UI queries `conversation_summaries.db` matching the active `project_id` and `workspace_uris`.
The migration script (`scripts/migrate-antigravity-sessions.py`):
1. Creates a backup of `conversation_summaries.db`.
2. Matches sessions by `oldPath` defined in `migration-manifest.json`.
3. Updates `project_id` to the master repo's project ID (`7bd47f1a-f76e-4b87-b0e6-b85d1e6acce4`).
4. Updates `workspace_uris` to include both the master workspace URI and the new submodule URI.
5. Updates the full-text search table `conversations_fts` so searches find sessions under `moovv-fit`.

### Submodule Commands

```bash
# Clone with all submodules
git clone --recurse-submodules git@github.com:moovv-fit/moovv-fit.git

# Update all submodules to latest remote
git submodule update --remote --merge

# Work in submodule
cd repos/backend/node
git checkout -b feature/x
# ... work ...
git commit && git push

# Update parent
cd ../../..
git add repos/backend/node
git commit -m "chore: update backend to include feature/x"
```

## References

- `#[[file:AGENTS.md]]` — Master repo agent configuration
- `#[[file:migration-manifest.json]]` — Repo migration tracking
- `#[[file:scripts/migrate-kiro-sessions.sh]]` — Kiro session migration script
- `#[[file:scripts/migrate-antigravity-sessions.py]]` — Antigravity session migration script
