#!/usr/bin/env python3
"""
Absorb a completed spec into a Product Decision Record (PDR).

This script:
1. Creates a PDR draft in repos/docs/product/docs/product/pdr/
2. Creates a Linear issue for review assigned to @p
3. Deletes the spec after PDR is created

Usage: python3 scripts/absorb-spec-to-pdr.py <spec-name> [--pdr-domain <domain>]

Example:
    python3 scripts/absorb-spec-to-pdr.py free-content-backend --pdr-domain subscriptions-billing
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Configuration
MASTER_ROOT = Path("/mnt/workspace/src/moovv-fit")
MASTER_SPECS = MASTER_ROOT / ".agents" / "specs"
PDR_ROOT = MASTER_ROOT / "repos" / "docs" / "product" / "docs" / "product" / "pdr"

# PDR domain mapping
PDR_DOMAINS = {
    "clinical": "clinical-exercise-engine",
    "billing": "subscriptions-billing",
    "auth": "auth-patient-identity",
    "partner": "partner-video-sdk",
    "clinic": "tele-rehab-clinic-os",
}


def get_next_pdr_number(domain_path: Path) -> int:
    """Find the next available PDR number in the domain."""
    max_num = 0
    if domain_path.exists():
        for pdr_file in domain_path.glob("PDR-*.md"):
            match = re.match(r"PDR-(\d+)", pdr_file.name)
            if match:
                num = int(match.group(1))
                max_num = max(max_num, num)
    return max_num + 1


def extract_spec_summary(spec_path: Path) -> dict:
    """Extract key information from spec files."""
    summary = {
        "title": "",
        "context": "",
        "decisions": [],
        "linear_issue": "",
    }
    
    # Try to read requirements.md for context
    requirements_file = spec_path / "requirements.md"
    if requirements_file.exists():
        content = requirements_file.read_text()
        
        # Extract title from first H1
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if title_match:
            summary["title"] = title_match.group(1).strip()
        
        # Extract Linear issue
        linear_match = re.search(r"\[(CORE|CLINIC)-\d+\]", content)
        if linear_match:
            summary["linear_issue"] = linear_match.group(0).strip("[]")
        
        # Extract overview/context section
        overview_match = re.search(r"##\s+Overview\s*\n([\s\S]*?)(?=\n##|\Z)", content)
        if overview_match:
            summary["context"] = overview_match.group(1).strip()[:500]
    
    # Try to read design.md for decisions
    design_file = spec_path / "design.md"
    if design_file.exists():
        content = design_file.read_text()
        
        # Extract decision sections (H3 headings often contain decisions)
        decisions = re.findall(r"###\s+(.+?)\n", content)
        summary["decisions"] = decisions[:5]  # First 5 decisions
    
    return summary


def create_pdr_draft(spec_name: str, spec_path: Path, pdr_domain: str) -> Path:
    """Create a PDR draft from the spec."""
    domain_path = PDR_ROOT / pdr_domain
    domain_path.mkdir(parents=True, exist_ok=True)
    
    pdr_num = get_next_pdr_number(domain_path)
    
    # Extract spec info
    spec_info = extract_spec_summary(spec_path)
    
    # Generate PDR title from spec name
    title = spec_info["title"] or spec_name.replace("-", " ").title()
    kebab_title = spec_name.upper()
    
    pdr_filename = f"PDR-{pdr_num:03d}-{kebab_title}.md"
    pdr_path = domain_path / pdr_filename
    
    # Generate PDR content
    pdr_content = f"""# PDR-{pdr_num:03d}: {title}

**Status**: 📋 Draft  
**Date**: {datetime.now().strftime('%Y-%m-%d')}  
**Spec**: {spec_name} (Linear: {spec_info['linear_issue'] or 'TBD'})

## Context

{spec_info['context'] or 'TODO: Describe the problem and what drove this decision.'}

## Decision

TODO: Extract key decisions from the spec design.md:

{chr(10).join(f'- {d}' for d in spec_info['decisions']) if spec_info['decisions'] else '- Key decision 1\n- Key decision 2'}

### Key Rules & Invariants

TODO: List business rules, state machines, and invariants.

### API Contracts (if applicable)

TODO: Document external-facing API changes.

## Consequences

### Positive

- TODO

### Negative

- TODO

## Implementation Notes

This PDR was absorbed from spec `{spec_name}`.
See implementation PRs linked to Linear issue {spec_info['linear_issue'] or 'TBD'}.

## References

- Spec: `.agents/specs/{spec_name}/` (now deleted)
- Linear: {spec_info['linear_issue'] or 'TBD'}
"""
    
    pdr_path.write_text(pdr_content)
    return pdr_path


def create_linear_issue(pdr_path: Path, spec_name: str) -> str:
    """Create a Linear issue for PDR review."""
    title = f"Review PDR: {spec_name}"
    description = f"""PDR draft created from completed spec `{spec_name}`.

**PDR Location**: `{pdr_path.relative_to(MASTER_ROOT)}`

**Reviewer Tasks**:
1. Review and refine the PDR content
2. Ensure all key decisions are captured
3. Verify invariants match implementation
4. Approve or request changes

**After Approval**:
- Update PDR status to ✅ Approved
- Close this issue
"""
    
    try:
        result = subprocess.run(
            [
                "linear", "issue", "create",
                "--title", title,
                "--description", description,
                "--assignee", "@p",
                "--label", "pdr-review",
                "--priority", "2",
            ],
            capture_output=True,
            text=True,
            cwd=str(MASTER_ROOT),
        )
        if result.returncode == 0:
            # Extract issue ID from output
            match = re.search(r"(CORE|CLINIC)-\d+", result.stdout)
            return match.group(0) if match else "Created (ID in Linear)"
        else:
            print(f"  ⚠️  Linear issue creation failed: {result.stderr}", file=sys.stderr)
            return "Manual creation needed"
    except FileNotFoundError:
        print("  ⚠️  Linear CLI not found, skipping issue creation", file=sys.stderr)
        return "Linear CLI not available"


def delete_spec(spec_name: str, spec_path: Path):
    """Delete the spec from submodule and remove symlink from master."""
    # Remove master symlink
    master_link = MASTER_SPECS / spec_name
    if master_link.is_symlink():
        master_link.unlink()
        print(f"  🗑️  Removed symlink: {spec_name}")
    
    # Delete actual spec directory
    if spec_path.exists() and spec_path.is_dir():
        shutil.rmtree(spec_path)
        print(f"  🗑️  Deleted spec: {spec_path.relative_to(MASTER_ROOT)}")


def main():
    parser = argparse.ArgumentParser(description="Absorb a completed spec into a PDR")
    parser.add_argument("spec_name", help="Name of the spec to absorb (e.g., free-content-backend)")
    parser.add_argument(
        "--pdr-domain",
        choices=list(PDR_DOMAINS.values()),
        help="PDR domain directory",
    )
    parser.add_argument(
        "--no-delete",
        action="store_true",
        help="Don't delete the spec after PDR creation (for testing)",
    )
    parser.add_argument(
        "--no-linear",
        action="store_true",
        help="Don't create Linear issue",
    )
    
    args = parser.parse_args()
    
    # Find spec
    spec_link = MASTER_SPECS / args.spec_name
    if not spec_link.exists():
        print(f"❌ Spec not found: {args.spec_name}", file=sys.stderr)
        print(f"   Available specs: {', '.join(s.name for s in MASTER_SPECS.iterdir() if s.is_symlink())}")
        return 1
    
    spec_path = spec_link.resolve()
    if not spec_path.exists():
        print(f"❌ Spec target not found: {spec_path}", file=sys.stderr)
        return 1
    
    print(f"📄 Absorbing spec: {args.spec_name}")
    print(f"   Source: {spec_path.relative_to(MASTER_ROOT)}")
    
    # Determine PDR domain
    pdr_domain = args.pdr_domain
    if not pdr_domain:
        # Try to infer from spec name
        if "billing" in args.spec_name or "payment" in args.spec_name or "content" in args.spec_name:
            pdr_domain = "subscriptions-billing"
        elif "auth" in args.spec_name:
            pdr_domain = "auth-patient-identity"
        elif "clinic" in args.spec_name or "triage" in args.spec_name:
            pdr_domain = "tele-rehab-clinic-os"
        elif "partner" in args.spec_name or "sdk" in args.spec_name:
            pdr_domain = "partner-video-sdk"
        else:
            pdr_domain = "clinical-exercise-engine"  # Default
        print(f"   Inferred PDR domain: {pdr_domain}")
    
    # Create PDR draft
    print(f"\n📝 Creating PDR draft...")
    pdr_path = create_pdr_draft(args.spec_name, spec_path, pdr_domain)
    print(f"   Created: {pdr_path.relative_to(MASTER_ROOT)}")
    
    # Create Linear issue
    if not args.no_linear:
        print(f"\n🎫 Creating Linear issue...")
        issue_id = create_linear_issue(pdr_path, args.spec_name)
        print(f"   Issue: {issue_id}")
    
    # Delete spec
    if not args.no_delete:
        print(f"\n🗑️  Cleaning up spec...")
        delete_spec(args.spec_name, spec_path)
    else:
        print(f"\n⏭️  Skipping spec deletion (--no-delete)")
    
    print(f"\n✅ PDR absorption complete!")
    print(f"   Next: Review and approve PDR at {pdr_path.relative_to(MASTER_ROOT)}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
