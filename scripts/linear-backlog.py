#!/usr/bin/env python3
"""
Moovv Fit — Cross-Repo Linear Backlog CLI
Summarizes, filters, and syncs backlog issues across all repositories.

Usage:
  ./scripts/linear-backlog.py                  # Full cross-repo summary in terminal
  ./scripts/linear-backlog.py -r mobile        # Filter by repo (e.g. mobile, backend, web, landing)
  ./scripts/linear-backlog.py -p urgent        # Filter by priority (urgent, high, medium, low)
  ./scripts/linear-backlog.py --sync           # Re-generate master BACKLOG.md snapshot
"""

import sys
import os
import argparse
import subprocess
import json
from datetime import datetime, timezone

REPO_METADATA = {
    "mobile": {
        "title": "Mobile (iOS & Android)",
        "path": "repos/apps/mobile",
        "icon": "📱",
        "desc": "Flutter rehabilitation app, assessment engine, routine player, and pain tracking."
    },
    "backend": {
        "title": "Backend Core API & Database",
        "path": "repos/backend/node",
        "icon": "⚙️",
        "desc": "Node/TypeScript Lambda API, Prisma ORM, Cognito auth, and clinical data models."
    },
    "web": {
        "title": "Web Portals (Clinic OS & Admin)",
        "path": "repos/apps/web",
        "icon": "🌐",
        "desc": "React 19 clinical portal, appointment booking, patient queue, and chat."
    },
    "landing": {
        "title": "Landing & Patient Acquisition",
        "path": "repos/apps/landing",
        "icon": "🚀",
        "desc": "Static marketing sites, physician lead funnels, and store/PWA onboarding."
    },
    "simulator": {
        "title": "Autonomous Simulator & Test Harness",
        "path": "repos/platform/simulator",
        "icon": "🧪",
        "desc": "E2E multi-persona automated test harness, websocket synthetic testing."
    },
    "design-system": {
        "title": "Design System Tokens & UI",
        "path": "repos/platform/design-system",
        "icon": "🎨",
        "desc": "Svelte 5 / Tailwind v4 canonical components and tokens."
    },
    "docs": {
        "title": "Documentation Portals",
        "path": "repos/docs/technical",
        "icon": "📚",
        "desc": "Partner developer documentation and clinical specifications."
    },
    "cross-repo / platform": {
        "title": "Platform Infrastructure & Cross-Repo",
        "path": "repos/infra/cdk",
        "icon": "☁️",
        "desc": "Shared CDK stacks, CloudFront routing, DNS, auth pools, and cross-cutting platform epics."
    }
}

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

def generate_markdown(issues, output_path):
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    by_repo = {}
    for issue in issues:
        lbl_nodes = issue.get("labels", {}).get("nodes", [])
        repo_labels = [l["name"].replace("repo:", "") for l in lbl_nodes if l["name"].startswith("repo:")]
        repo_key = repo_labels[0] if repo_labels else "cross-repo / platform"
        if repo_key in ("infra", "cdk"):
            repo_key = "cross-repo / platform"
        elif repo_key == "engine":
            repo_key = "backend"

        prio_label = issue.get("priorityLabel", "None")
        by_repo.setdefault(repo_key, []).append({
            "id": issue["identifier"],
            "title": issue["title"],
            "url": issue["url"],
            "priority": prio_label,
            "team": issue.get("team", {}).get("key", "")
        })

    total_issues = sum(len(v) for v in by_repo.values())

    lines = []
    lines.append("# 📋 Moovv Fit — Master Cross-Repo Backlog")
    lines.append("")
    lines.append(f"> **Canonical Backlog Mirror** synchronized with Linear (`moovv-fit` workspace).  ")
    lines.append(f"> **Last Synced:** `{now_utc}` • **Total Open Backlog Issues:** `{total_issues}`  ")
    lines.append("> *To refresh this document automatically, run: `./scripts/linear-backlog.py --sync`*")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 🎯 Habit-Building Guide: Managing & Exploring the Backlog")
    lines.append("")
    lines.append("To stay on top of the backlog without UI friction, use **Option 1** (terminal CLI) or **Option 4** (conversational pairing with the agent):")
    lines.append("")
    lines.append("### ⚡ Option 1: Backlog CLI Explorer (`./scripts/linear-backlog.py`)")
    lines.append("Run directly from anywhere in the repository:")
    lines.append("```bash")
    lines.append("# 1. Quick cross-repo overview in your terminal")
    lines.append("./scripts/linear-backlog.py")
    lines.append("")
    lines.append("# 2. Filter by specific repository domain")
    lines.append("./scripts/linear-backlog.py -r mobile      # iOS / Android app backlog")
    lines.append("./scripts/linear-backlog.py -r backend     # Node / Lambda / DB backlog")
    lines.append("./scripts/linear-backlog.py -r web         # Clinic OS & Physio Portal backlog")
    lines.append("./scripts/linear-backlog.py -r landing     # Landing page & funnel backlog")
    lines.append("")
    lines.append("# 3. Filter by urgency across all repos")
    lines.append("./scripts/linear-backlog.py -p urgent      # Only Urgent tickets")
    lines.append("./scripts/linear-backlog.py -p high        # High priority tickets")
    lines.append("")
    lines.append("# 4. Deep-dive into any specific ticket")
    lines.append("linear issue view CORE-113")
    lines.append("")
    lines.append("# 5. Refresh this static BACKLOG.md snapshot")
    lines.append("./scripts/linear-backlog.py --sync")
    lines.append("```")
    lines.append("")
    lines.append("### 💬 Option 4: Conversational Prompts with the Agent")
    lines.append("When pair-programming with Antigravity or Kiro, you don't need to leave chat:")
    lines.append("- **Querying**:")
    lines.append("  - *\"Show me the mobile backlog\"*")
    lines.append("  - *\"What urgent tasks are pending in backend?\"*")
    lines.append("  - *\"What landing page items do we have?\"*")
    lines.append("- **Capturing on the Fly**:")
    lines.append("  - *\"Backlog this: [idea or task description]\"* → The agent calls `linear issue create --state Backlog` immediately and reports the new ticket ID.")
    lines.append("- **Periodic Snapshot Updates**:")
    lines.append("  - *\"Update the master BACKLOG.md snapshot\"* → The agent runs the sync command and updates this file.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 📊 Backlog Summary by Repository")
    lines.append("")
    lines.append("| Domain | Submodule Path | Issues | Primary Focus |")
    lines.append("|---|---|:---:|---|")

    # Order keys logically
    key_order = ["mobile", "backend", "web", "landing", "simulator", "design-system", "docs", "cross-repo / platform"]
    for k in key_order:
        if k in by_repo:
            meta = REPO_METADATA.get(k, {"title": k, "path": "-", "icon": "📦", "desc": "-"})
            lines.append(f"| **{meta['icon']} {meta['title']}** | [`{meta['path']}`]({meta['path']}) | **{len(by_repo[k])}** | {meta['desc']} |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 📦 Detailed Backlog Breakdown")
    lines.append("")

    for k in key_order:
        if k not in by_repo:
            continue
        meta = REPO_METADATA.get(k, {"title": k.upper(), "path": "-", "icon": "📦", "desc": "-"})
        r_issues = by_repo[k]

        lines.append(f"### {meta['icon']} {meta['title']} ({len(r_issues)} issues)")
        lines.append(f"**Path:** [`{meta['path']}`]({meta['path']})  ")
        lines.append(f"*{meta['desc']}*")
        lines.append("")
        lines.append("| ID | Priority | Title | Team |")
        lines.append("|---|:---:|---|:---:|")

        # Sort urgent first, then high, then medium, then low/none
        prio_weight = {"Urgent": 1, "High": 2, "Medium": 3, "Low": 4, "None": 5}
        sorted_issues = sorted(r_issues, key=lambda x: prio_weight.get(x["priority"], 99))

        for iss in sorted_issues:
            prio_badge = f"`{iss['priority']}`" if iss['priority'] != "None" else "`-`"
            lines.append(f"| [{iss['id']}]({iss['url']}) | {prio_badge} | {iss['title']} | `{iss['team']}` |")
        lines.append("")

    lines.append("---")
    lines.append(f"*Generated automatically via `scripts/linear-backlog.py --sync` on {now_utc}.*")
    lines.append("")

    content = "\n".join(lines)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Successfully wrote backlog snapshot to {output_path} ({total_issues} issues synced).")

def main():
    parser = argparse.ArgumentParser(description="Cross-repo Linear Backlog Explorer & Synchronizer")
    parser.add_argument("-r", "--repo", help="Filter by repo name (e.g. backend, mobile, web, landing, infra)")
    parser.add_argument("-p", "--priority", help="Filter by priority (urgent, high, medium, low)")
    parser.add_argument("-l", "--limit", type=int, default=10, help="Max issues to display per repo in terminal (default: 10)")
    parser.add_argument("--sync", action="store_true", help="Synchronize and write master BACKLOG.md snapshot at repository root")
    parser.add_argument("--out", default="BACKLOG.md", help="Output file path for --sync (default: BACKLOG.md)")
    args = parser.parse_args()

    issues = fetch_backlog()
    if not issues:
        print("No backlog issues found.")
        return

    if args.sync:
        generate_markdown(issues, args.out)
        return

    by_repo = {}
    for issue in issues:
        prio_label = issue.get("priorityLabel", "None")
        if args.priority and args.priority.lower() not in prio_label.lower():
            continue

        lbl_nodes = issue.get("labels", {}).get("nodes", [])
        repo_labels = [l["name"].replace("repo:", "") for l in lbl_nodes if l["name"].startswith("repo:")]
        repo = repo_labels[0] if repo_labels else "cross-repo / platform"
        if repo in ("infra", "cdk"):
            repo = "cross-repo / platform"
        elif repo == "engine":
            repo = "backend"

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
    print("  • Filter by repo:            ./scripts/linear-backlog.py -r <repo>")
    print("  • Sync BACKLOG.md snapshot:  ./scripts/linear-backlog.py --sync\n")

if __name__ == "__main__":
    main()
