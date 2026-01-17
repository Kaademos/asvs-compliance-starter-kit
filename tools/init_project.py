import argparse
import sys
from pathlib import Path
import shutil

TEMPLATES_DIR = Path(__file__).parent.parent / "00-Documentation-Standards" / "Decision-Templates"

def interactive_init():
    print("🛡️  ASVS Compliance Starter Kit - Init Wizard")
    print("===========================================")
    
    project_name = input("Project Name: ").strip()
    
    print("\nSelect ASVS Assurance Level:")
    print("1) Level 1 (Basic - Automated)")
    print("2) Level 2 (Standard - Sensitive Data)")
    print("3) Level 3 (Critical - Defense in Depth)")
    level_choice = input("Choice [2]: ").strip() or "2"
    
    output_dir = input("\nOutput directory for docs [./docs]: ").strip() or "./docs"
    output_path = Path(output_dir)
    
    # Create logic
    print(f"\nInitializing {project_name} at {output_path} (Level {level_choice})...")
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Copy templates
    # In a real impl, we might filter based on level, but for now copying all is safer for start
    if TEMPLATES_DIR.exists():
        for item in TEMPLATES_DIR.glob("*.md"):
            dest = output_path / item.name
            if not dest.exists():
                content = item.read_text(encoding="utf-8")
                # Simple templating
                content = content.replace("[Project Name]", project_name)
                dest.write_text(content, encoding="utf-8")
                print(f"  + Created {item.name}")
            else:
                print(f"  ! Skipped {item.name} (Exists)")
    
    # Generate evidence.yml stub
    evidence_path = Path("evidence.yml")
    if not evidence_path.exists():
        evidence_content = f"""# Evidence Manifest for {project_name}
requirements:
  V14.4:
    checks:
      - type: file_exists
        path: "package.json"
"""
        evidence_path.write_text(evidence_content)
        print("  + Created evidence.yml")

    print("\n✅ Initialization complete!")
    print(f"Next step: Review documents in {output_dir}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interactive", action="store_true")
    args = parser.parse_args()
    
    if args.interactive:
        interactive_init()
    else:
        print("Use --interactive to start the wizard.")

if __name__ == "__main__":
    main()