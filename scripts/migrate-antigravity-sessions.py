#!/usr/bin/env python3
"""
migrate-antigravity-sessions.py
Migrates Antigravity conversation sessions in ~/.gemini/antigravity/conversation_summaries.db
when repos are consolidated into submodules under a master repository.

Usage:
  python3 scripts/migrate-antigravity-sessions.py [--dry-run] [--target-project-id <id>]
"""

import argparse
import json
import os
import shutil
import sqlite3
import sys

GEMINI_DIR = os.path.expanduser("~/.gemini")
ANTIGRAVITY_DIR = os.path.join(GEMINI_DIR, "antigravity")
DB_PATH = os.path.join(ANTIGRAVITY_DIR, "conversation_summaries.db")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MANIFEST_PATH = os.path.join(SCRIPT_DIR, "..", "migration-manifest.json")
PROJECTS_DIR = os.path.join(GEMINI_DIR, "config", "projects")

def get_current_project_info():
    """Finds current project ID for /mnt/workspace/src/moovv-fit."""
    current_workspace_path = "/mnt/workspace/src/moovv-fit"
    if not os.path.exists(PROJECTS_DIR):
        return None, "moovv-fit"
    
    for fname in os.listdir(PROJECTS_DIR):
        if fname.endswith(".json"):
            fpath = os.path.join(PROJECTS_DIR, fname)
            try:
                with open(fpath, "r") as f:
                    data = json.load(f)
                resources = data.get("projectResources", {}).get("resources", [])
                for res in resources:
                    uri = res.get("folderUri") or res.get("gitFolder", {}).get("folderUri", "")
                    if current_workspace_path in uri:
                        return data.get("id"), data.get("name", "moovv-fit")
            except Exception:
                continue
    return "7bd47f1a-f76e-4b87-b0e6-b85d1e6acce4", "moovv-fit"

def main():
    parser = argparse.ArgumentParser(description="Migrate Antigravity conversation history")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without modifying DB")
    parser.add_argument("--target-project-id", help="Override target project ID (default auto-detected)")
    parser.add_argument("--manifest", default=MANIFEST_PATH, help="Path to migration-manifest.json")
    args = parser.parse_args()

    if not os.path.exists(DB_PATH):
        print(f"[ERROR] Database not found at: {DB_PATH}", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.manifest):
        print(f"[ERROR] Manifest not found at: {args.manifest}", file=sys.stderr)
        sys.exit(1)

    with open(args.manifest, "r") as f:
        manifest = json.load(f)

    # Build mapping from old URI to new submodule URI
    old_to_new = {}
    for repo in manifest.get("repos", []):
        old_uri = f"file://{repo['oldPath']}"
        new_uri = f"file://{repo['newPath']}"
        old_to_new[old_uri] = {
            "name": repo["name"],
            "old_uri": old_uri,
            "new_uri": new_uri
        }

    target_pid, target_name = get_current_project_info()
    if args.target_project_id:
        target_pid = args.target_project_id

    master_workspace_uri = "file:///mnt/workspace/src/moovv-fit"

    print("=" * 70)
    print(f"Target Master Project ID:   {target_pid}")
    print(f"Target Master Project Name: {target_name}")
    print(f"Target Master Workspace:    {master_workspace_uri}")
    print(f"Mode:                       {'DRY-RUN' if args.dry_run else 'LIVE MIGRATION'}")
    print("=" * 70)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT conversation_id, title, workspace_uris, project_id FROM conversation_summaries")
    rows = cursor.fetchall()

    matches = []
    for cid, title, uris_raw, pid in rows:
        try:
            uris = json.loads(uris_raw) if uris_raw.startswith("[") else [uris_raw]
        except Exception:
            uris = [uris_raw]

        for u in uris:
            if u in old_to_new:
                matches.append({
                    "cid": cid,
                    "title": title or "(Untitled)",
                    "old_uri": u,
                    "submodule_uri": old_to_new[u]["new_uri"],
                    "repo_name": old_to_new[u]["name"],
                    "old_pid": pid
                })
                break

    if not matches:
        print("[INFO] No conversations found requiring migration.")
        return

    print(f"\nFound {len(matches)} conversations to re-index:\n")
    for m in matches:
        print(f" • [{m['cid'][:8]}...] {m['title'][:35]:35} | {m['repo_name']} -> {target_name}")

    if args.dry_run:
        print("\n[DRY-RUN] No changes made. Run without --dry-run to apply updates.")
        return

    # Backup database
    backup_path = f"{DB_PATH}.bak"
    print(f"\nCreating backup: {backup_path}")
    shutil.copy2(DB_PATH, backup_path)

    updated_count = 0
    for m in matches:
        cid = m["cid"]
        # Include both master workspace and submodule URI so it matches in either view
        new_uris_json = json.dumps([master_workspace_uri, m["submodule_uri"]])
        
        cursor.execute("""
            UPDATE conversation_summaries 
            SET project_id = ?, workspace_uris = ?
            WHERE conversation_id = ?
        """, (target_pid, new_uris_json, cid))

        # Update FTS table if exists
        try:
            cursor.execute("""
                UPDATE conversations_fts
                SET workspace = ?, project = ?
                WHERE conversation_id = ?
            """, (target_name, target_name, cid))
        except sqlite3.OperationalError:
            pass

        updated_count += 1

    conn.commit()
    conn.close()
    print(f"\n[SUCCESS] Successfully re-indexed {updated_count} conversations under project {target_pid} ({target_name}).")
    print("Reload or restart the Antigravity IDE / app to see your chat history in the UI.")

if __name__ == "__main__":
    main()

