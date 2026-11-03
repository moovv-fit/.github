#!/bin/bash
#
# migrate-kiro-sessions.sh
# Migrates Kiro session data when a workspace path changes
#
# Usage:
#   ./migrate-kiro-sessions.sh <old_path> <new_path> [--dry-run]
#   ./migrate-kiro-sessions.sh --from-manifest [--dry-run]
#
# Examples:
#   ./migrate-kiro-sessions.sh /mnt/workspace/src/moovv-fit-mobile /mnt/workspace/src/moovv-fit/repos/apps/mobile
#   ./migrate-kiro-sessions.sh --from-manifest --dry-run
#

set -e

KIRO_DIR="${KIRO_DIR:-$HOME/.kiro}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFEST_FILE="$SCRIPT_DIR/../migration-manifest.json"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

DRY_RUN=false

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Compute SHA256 hash (first 16 hex chars) of a path - same as Kiro uses
compute_hash() {
    local path="$1"
    echo -n "$path" | sha256sum | cut -c1-16
}

# Migrate sessions for a single path change
migrate_single() {
    local old_path="$1"
    local new_path="$2"
    
    local old_hash=$(compute_hash "$old_path")
    local new_hash=$(compute_hash "$new_path")
    
    log_info "Migrating: $old_path -> $new_path"
    log_info "  Old hash: $old_hash"
    log_info "  New hash: $new_hash"
    
    if [ "$old_hash" == "$new_hash" ]; then
        log_warn "  Hashes are identical, nothing to migrate"
        return 0
    fi
    
    # Check if old session data exists
    if [ ! -d "$KIRO_DIR/sessions/$old_hash" ]; then
        log_warn "  No sessions found for old path (hash: $old_hash)"
        return 0
    fi
    
    # Check if new hash already has data (would be overwritten)
    if [ -d "$KIRO_DIR/sessions/$new_hash" ]; then
        log_warn "  Sessions already exist for new path. Merging..."
    fi
    
    if [ "$DRY_RUN" = true ]; then
        log_info "  [DRY-RUN] Would perform the following:"
        log_info "    - Rename sessions/$old_hash -> sessions/$new_hash"
        log_info "    - Rename workspace-roots/$old_hash -> workspace-roots/$new_hash"
        log_info "    - Rename session-index/$old_hash.jsonl -> session-index/$new_hash.jsonl"
        log_info "    - Update paths in session files"
        return 0
    fi
    
    # Create backup
    log_info "  Creating backup..."
    mkdir -p "$KIRO_DIR/sessions/$old_hash/.backup"
    cp -r "$KIRO_DIR/sessions/$old_hash"/* "$KIRO_DIR/sessions/$old_hash/.backup/" 2>/dev/null || true
    
    # 1. Rename sessions directory
    if [ -d "$KIRO_DIR/sessions/$old_hash" ]; then
        log_info "  Moving sessions directory..."
        if [ -d "$KIRO_DIR/sessions/$new_hash" ]; then
            # Merge: move contents into existing
            cp -r "$KIRO_DIR/sessions/$old_hash"/* "$KIRO_DIR/sessions/$new_hash/" 2>/dev/null || true
            rm -rf "$KIRO_DIR/sessions/$old_hash"
        else
            mv "$KIRO_DIR/sessions/$old_hash" "$KIRO_DIR/sessions/$new_hash"
        fi
    fi
    
    # 2. Rename workspace-roots directory
    if [ -d "$KIRO_DIR/workspace-roots/$old_hash" ]; then
        log_info "  Moving workspace-roots directory..."
        if [ -d "$KIRO_DIR/workspace-roots/$new_hash" ]; then
            rm -rf "$KIRO_DIR/workspace-roots/$new_hash"
        fi
        mv "$KIRO_DIR/workspace-roots/$old_hash" "$KIRO_DIR/workspace-roots/$new_hash"
    fi
    
    # 3. Update .trust-migration.json with new root path
    local trust_file="$KIRO_DIR/workspace-roots/$new_hash/.trust-migration.json"
    if [ -f "$trust_file" ]; then
        log_info "  Updating .trust-migration.json..."
        # Use python for safe JSON manipulation
        python3 << PYEOF
import json
with open("$trust_file", "r") as f:
    data = json.load(f)
data["root"] = "$new_path"
with open("$trust_file", "w") as f:
    json.dump(data, f, indent=2)
PYEOF
    fi
    
    # 4. Rename and update session-index
    if [ -f "$KIRO_DIR/session-index/$old_hash.jsonl" ]; then
        log_info "  Updating session-index..."
        # Update sessionPath entries and rename file
        sed "s|$old_hash/|$new_hash/|g" "$KIRO_DIR/session-index/$old_hash.jsonl" > "$KIRO_DIR/session-index/$new_hash.jsonl"
        rm "$KIRO_DIR/session-index/$old_hash.jsonl"
    fi
    
    # 5. Update session.json files with new paths
    log_info "  Updating session.json files..."
    for session_dir in "$KIRO_DIR/sessions/$new_hash"/sess_*/; do
        if [ -d "$session_dir" ]; then
            local session_file="$session_dir/session.json"
            if [ -f "$session_file" ]; then
                # Update workspacePaths and rootPaths
                python3 << PYEOF
import json
import sys
try:
    with open("$session_file", "r") as f:
        data = json.load(f)
    
    modified = False
    
    # Update workspacePaths
    if "workspacePaths" in data:
        new_paths = []
        for p in data["workspacePaths"]:
            if p == "$old_path":
                new_paths.append("$new_path")
                modified = True
            else:
                new_paths.append(p)
        data["workspacePaths"] = new_paths
    
    # Update rootPaths
    if "rootPaths" in data:
        new_paths = []
        for p in data["rootPaths"]:
            if p == "$old_path":
                new_paths.append("$new_path")
                modified = True
            else:
                new_paths.append(p)
        data["rootPaths"] = new_paths
    
    if modified:
        with open("$session_file", "w") as f:
            json.dump(data, f, indent=2)
        print(f"  Updated: {sys.argv[0] if len(sys.argv) > 0 else 'session'}")
except Exception as e:
    print(f"  Warning: Could not update $session_file: {e}", file=sys.stderr)
PYEOF
            fi
        fi
    done
    
    log_info "  Migration complete for $old_path"
    return 0
}

# Migrate all repos from manifest
migrate_from_manifest() {
    if [ ! -f "$MANIFEST_FILE" ]; then
        log_error "Manifest file not found: $MANIFEST_FILE"
        exit 1
    fi
    
    log_info "Reading manifest from: $MANIFEST_FILE"
    
    # Parse manifest and migrate each repo
    local count=$(python3 -c "import json; print(len(json.load(open('$MANIFEST_FILE'))['repos']))")
    log_info "Found $count repos to migrate"
    
    python3 << 'PYEOF'
import json
import subprocess
import sys
import os

manifest_file = os.environ.get('MANIFEST_FILE', 'migration-manifest.json')
dry_run = os.environ.get('DRY_RUN', 'false') == 'true'
script_path = sys.argv[0] if len(sys.argv) > 0 else './migrate-kiro-sessions.sh'

with open(manifest_file, 'r') as f:
    manifest = json.load(f)

for repo in manifest['repos']:
    old_path = repo['oldPath']
    new_path = repo['newPath']
    name = repo['name']
    
    print(f"\n{'='*60}")
    print(f"Processing: {name}")
    print(f"{'='*60}")
PYEOF

    # Actually run migrations
    python3 -c "
import json
manifest = json.load(open('$MANIFEST_FILE'))
for repo in manifest['repos']:
    print(repo['oldPath'] + '|' + repo['newPath'])
" | while IFS='|' read -r old_path new_path; do
        migrate_single "$old_path" "$new_path"
    done
    
    # Update manifest status
    if [ "$DRY_RUN" = false ]; then
        log_info "Updating manifest status..."
        python3 << PYEOF
import json
with open("$MANIFEST_FILE", "r") as f:
    manifest = json.load(f)
for repo in manifest["repos"]:
    repo["sessionMigrationStatus"] = "migrated"
with open("$MANIFEST_FILE", "w") as f:
    json.dump(manifest, f, indent=2)
PYEOF
    fi
    
    log_info "All migrations complete!"
}

# Parse arguments
if [ $# -eq 0 ]; then
    echo "Usage:"
    echo "  $0 <old_path> <new_path> [--dry-run]"
    echo "  $0 --from-manifest [--dry-run]"
    exit 1
fi

# Check for --dry-run flag
for arg in "$@"; do
    if [ "$arg" == "--dry-run" ]; then
        DRY_RUN=true
        log_warn "DRY-RUN MODE - No changes will be made"
    fi
done

if [ "$1" == "--from-manifest" ]; then
    export MANIFEST_FILE DRY_RUN
    migrate_from_manifest
else
    if [ $# -lt 2 ]; then
        log_error "Must provide both old_path and new_path"
        exit 1
    fi
    migrate_single "$1" "$2"
fi
