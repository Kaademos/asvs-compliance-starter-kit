#!/usr/bin/env python3
"""
ASVS Project Initialization - Bootstrap security documentation templates.

This module initializes a new ASVS compliance project by copying templates
and creating the necessary structure for security documentation.
"""

import argparse
import sys
from pathlib import Path

from tools.resource_manager import (
    ensure_resources,
    get_resource_path,
    GITHUB_REPO_URL,
)


def get_templates_directory() -> Path | None:
    """
    Get the templates directory, checking local repo first then cache.

    Returns:
        Path to templates directory, or None if unavailable.
    """
    script_dir = Path(__file__).parent.parent
    local_templates = script_dir / "00-Documentation-Standards" / "Decision-Templates"
    if local_templates.exists():
        return local_templates

    return get_resource_path("templates")


def interactive_init():
    """Run the interactive project initialization wizard."""
    print("ASVS Compliance Starter Kit - Init Wizard")
    print("=" * 43)

    project_name = input("Project Name: ").strip()
    if not project_name:
        print("Project name required.")
        return 1

    print("\nSelect ASVS Assurance Level:")
    print("1) Level 1 (Basic - Automated)")
    print("2) Level 2 (Standard - Sensitive Data)")
    print("3) Level 3 (Critical - Defense in Depth)")
    level_choice = input("Choice [2]: ").strip() or "2"

    output_dir = input("\nOutput directory for docs [./docs]: ").strip() or "./docs"
    output_path = Path(output_dir)

    print(f"\nInitializing {project_name} at {output_path} (Level {level_choice})...")
    output_path.mkdir(parents=True, exist_ok=True)

    templates_dir = get_templates_directory()

    if templates_dir is None:
        print("  Templates not found locally.")
        success, cache_path = ensure_resources(
            resource_types=["templates"],
            interactive=True,
            quiet=False
        )

        if not success:
            print("\n  Unable to access templates.")
            print(f"  Visit {GITHUB_REPO_URL} to clone the repository.")
            return 1

        templates_dir = get_resource_path("templates")

    if templates_dir and templates_dir.exists():
        template_count = 0
        for item in templates_dir.glob("*.md"):
            dest = output_path / item.name
            if not dest.exists():
                content = item.read_text(encoding="utf-8")
                content = content.replace("[Project Name]", project_name)
                dest.write_text(content, encoding="utf-8")
                print(f"  + Created {item.name}")
                template_count += 1
            else:
                print(f"  ! Skipped {item.name} (Exists)")

        if template_count == 0:
            print("  No new templates created (all already exist)")
    else:
        print("  Warning: Templates unavailable. Documentation not created.")
        print(f"  Visit {GITHUB_REPO_URL} for manual setup.")

    evidence_path = Path("evidence.yml")
    if not evidence_path.exists():
        evidence_content = f"""# Evidence Manifest for {project_name}
# Map your code files to ASVS requirements here.

requirements:
  # Example: Verify HTTP Security Headers are installed
  V14.4:
    checks:
      - type: file_exists
        path: "package.json"
      # - type: content_match
      #   path: "package.json"
      #   pattern: "helmet"
"""
        evidence_path.write_text(evidence_content, encoding="utf-8")
        print("  + Created evidence.yml")

    print("\nInitialization complete!")
    print(f"Next step: Review documents in {output_dir}")
    print(f"Then run: asvs verify --docs-path {output_dir} --level {level_choice}")

    return 0


def main(args=None):
    """Main entry point for project initialization."""
    parser = argparse.ArgumentParser(description="Initialize a new ASVS project")
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    parsed = parser.parse_args(args)

    if parsed.interactive:
        return interactive_init()
    else:
        print("Run with --interactive to start the wizard.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
