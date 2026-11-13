#!/usr/bin/env python3
"""
Sync spec symlinks from submodules to master .agents/specs/ directory.

This script:
1. Scans all submodule .agents/specs/ directories
2. Creates symlinks in master .agents/specs/ with {feature}-{domain} naming
3. Updates _index.md manifest

Run: python3 scripts/sync-spec-symlinks.py
Hook: SessionStart (spec-sync)
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime

# Configuration
MASTER_ROOT = Path("/mnt/workspace/src/moovv-fit")
MASTER_SPECS = MASTER_ROOT / ".agents" / "specs"
ROADMAP_FILE = MASTER_ROOT / "docs" / "SPEC-ROADMAP.md"

# Submodule spec locations with domain identifiers
SUBMODULES = {
    "backend": MASTER_ROOT / "repos" / "backend" / "node" / ".agents" / "specs",
    "mobile": MASTER_ROOT / "repos" / "apps" / "mobile" / ".agents" / "specs",
    "web": MASTER_ROOT / "repos" / "apps" / "web" / ".agents" / "specs",
    "infra": MASTER_ROOT / "repos" / "infra" / "cdk" / ".agents" / "specs",
    "simulator": MASTER_ROOT / "repos" / "platform" / "simulator" / ".agents" / "specs",
}

# Domain suffix mapping for naming convention
DOMAIN_SUFFIX = {
    "backend": "",  # e.g., free-content-backend stays as-is
    "mobile": "-mobile" if not "mobile" else "",  # append -mobile only if not already in name
    "web": "-web",
    "infra": "-infra",
    "simulator": "-simulator",
}


def get_spec_name(spec_dir: Path, domain: str) -> str:
    """
    Convert spec directory name to {feature}-{domain} format.
    
    Examples:
        free-content-backend (backend) -> free-content-backend
        marketing-infra (mobile) -> marketing-infra-mobile
        free-content-mobile (mobile) -> free-content-mobile
    """
    name = spec_dir.name
    
    # If name already ends with domain identifier, use as-is
    if name.endswith(f"-{domain}"):
        return name
    
    # If it's a backend spec with -backend suffix, use as-is
    if domain == "backend" and name.endswith("-backend"):
        return name
    
    # Append domain suffix
    if domain == "backend":
        return name  # Backend specs keep original names
    elif domain in name:
        return name  # Already has domain in name
    else:
        return f"{name}-{domain}"


def create_relative_symlink(target: Path, link: Path) -> bool:
    """Create a relative symlink from link to target."""
    try:
        # Calculate relative path from link location to target
        rel_target = os.path.relpath(target, link.parent)
        
        # Remove existing symlink if present
        if link.is_symlink():
            link.unlink()
        elif link.exists():
            print(f"  ⚠️  Skipping {link.name}: not a symlink", file=sys.stderr)
            return False
        
        link.symlink_to(rel_target)
        return True
    except Exception as e:
        print(f"  ❌ Error creating symlink {link}: {e}", file=sys.stderr)
        return False


def scan_specs() -> dict:
    """Scan all submodules for specs and return mapping."""
    specs = {}
    
    for domain, specs_dir in SUBMODULES.items():
        if not specs_dir.exists():
            continue
            
        for item in specs_dir.iterdir():
            # Skip hidden files, gitkeep, and non-directories
            if item.name.startswith(".") or item.name.startswith("_"):
                continue
            if not item.is_dir():
                continue
            
            spec_name = get_spec_name(item, domain)
            specs[spec_name] = {
                "path": item,
                "domain": domain,
                "original_name": item.name,
            }
    
    return specs


def sync_symlinks(specs: dict) -> tuple[int, int]:
    """Create/update symlinks in master specs directory."""
    created = 0
    updated = 0
    
    # Ensure master specs directory exists
    MASTER_SPECS.mkdir(parents=True, exist_ok=True)
    
    # Get current symlinks
    current_links = {
        item.name: item
        for item in MASTER_SPECS.iterdir()
        if item.is_symlink()
    }
    
    for spec_name, spec_info in specs.items():
        link_path = MASTER_SPECS / spec_name
        target_path = spec_info["path"]
        
        if spec_name in current_links:
            # Check if symlink points to correct target
            existing_link = current_links[spec_name]
            if existing_link.resolve() == target_path.resolve():
                continue  # Already correct
            else:
                if create_relative_symlink(target_path, link_path):
                    updated += 1
                    print(f"  🔄 Updated: {spec_name}")
        else:
            if create_relative_symlink(target_path, link_path):
                created += 1
                print(f"  ➕ Created: {spec_name}")
    
    # Report orphaned symlinks (pointing to deleted specs)
    spec_names = set(specs.keys())
    for link_name, link_path in current_links.items():
        if link_name not in spec_names and not link_name.startswith("_"):
            if not link_path.resolve().exists():
                print(f"  ⚠️  Orphaned symlink: {link_name} (target deleted)")
    
    return created, updated


def main():
    print("📁 Syncing spec symlinks to master .agents/specs/")
    print()
    
    # Scan all submodules
    specs = scan_specs()
    print(f"Found {len(specs)} specs across submodules:")
    for domain in SUBMODULES.keys():
        domain_specs = [s for s, i in specs.items() if i["domain"] == domain]
        if domain_specs:
            print(f"  {domain}: {len(domain_specs)} specs")
    print()
    
    # Sync symlinks
    created, updated = sync_symlinks(specs)
    
    print()
    if created or updated:
        print(f"✅ Sync complete: {created} created, {updated} updated")
    else:
        print("✅ All symlinks up to date")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
