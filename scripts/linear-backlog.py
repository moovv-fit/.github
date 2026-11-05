#!/usr/bin/env python3
"""
Moovv Fit — Cross-Repo Linear Backlog CLI
Summarizes or filters backlog issues across all repositories.

Usage:
  ./scripts/linear-backlog.py                  # Full cross-repo summary
  ./scripts/linear-backlog.py -r mobile        # Filter by repo (e.g. mobile, backend, web, landing)
  ./scripts/linear-backlog.py -p urgent        # Filter by priority (urgent, high, medium, low)
"""

import sys
import argparse
import subprocess
import json

def fetch_backlog():
    cmd = [
        "linear", "issue", "query",
        "--all-teams",
        "-s", "backlog",
        "--limit", "100",
        "--json"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error executing linear CLI: {res.stderr}", file=sys.stderr)
        sys.exit(1)
    try:
        data = json.loads(res.stdout)
        return data.get("nodes", [])
    except Exception as e:
        print(f"Failed to parse linear JSON: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Cross-repo Linear Backlog Explorer")
    parser.add_argument("-r", "--repo", help="Filter by repo name (e.g. backend, mobile, web, landing, infra)")
    parser.add_argument("-p", "--priority", help="Filter by priority (urgent, high, medium, low)")
    parser.add_argument("-l", "--limit", type=int, default=10, help="Max issues to display per repo (default: 10)")
    args = parser.parse_args()

    issues = fetch_backlog()
    if not issues:
        print("No backlog issues found.")
        return

    by_repo = {}
    for issue in issues:
        prio_label = issue.get("priorityLabel", "None")
        if args.priority and args.priority.lower() not in prio_label.lower():
            continue

        lbl_nodes = issue.get("labels", {}).get("nodes", [])
        repo_labels = [l["name"].replace("repo:", "") for l in lbl_nodes if l["name"].startswith("repo:")]
        repo = repo_labels[0] if repo_labels else "cross-repo / platform"

        if args.repo and args.repo.lower() not in repo.lower():
            continue

        by_repo.setdefault(repo, []).append((
            issue["identifier"],
            issue["title"],
            prio_label,
            issue.get("team", {}).get("key", "")
        ))

    total_matched = sum(len(v) for v in by_repo.values())
    print(f"\n📋 Moovv Fit Backlog ({total_matched} issues total across {len(by_repo)} categories)\n" + "=" * 70)

    for r, r_issues in sorted(by_repo.items()):
        print(f"\n📦 {r.upper()} ({len(r_issues)} issues)")
        print("-" * 50)
        for ident, title, prio, team in r_issues[:args.limit]:
            prio_badge = f"[{prio}]" if prio != "None" else ""
            print(f"  • {ident} {prio_badge:<9} {title}")
        if len(r_issues) > args.limit:
            print(f"    ... +{len(r_issues) - args.limit} more (use -l {len(r_issues)} to show all)")

    print("\n" + "=" * 70)
    print("💡 Tips:")
    print("  • View details of an issue:  linear issue view <ID>")
    print("  • Open in browser:           https://linear.app/moovv-fit")
    print("  • Filter by repo:            ./scripts/linear-backlog.py -r <repo>\n")

if __name__ == "__main__":
    main()
