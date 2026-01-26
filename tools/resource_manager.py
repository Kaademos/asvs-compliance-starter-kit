#!/usr/bin/env python3
"""
ASVS Resource Manager - Downloads and manages resources from GitHub.

This module handles downloading templates and reference files from the
GitHub repository when the CLI is installed via pip without the full repo.
"""

import hashlib
import json
import os
import sys
import tempfile
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional, Dict, List, Any

# GitHub repository configuration
GITHUB_REPO = "Kaademos/asvs-compliance-starter-kit"
GITHUB_RAW_BASE = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main"
GITHUB_REPO_URL = f"https://github.com/{GITHUB_REPO}"

# Default cache directory for downloaded resources
DEFAULT_CACHE_DIR = Path.home() / ".asvs-compliance" / "resources"

# Resource manifest - defines all downloadable resources
RESOURCE_MANIFEST = {
    "templates": {
        "description": "Decision templates for security documentation",
        "base_path": "00-Documentation-Standards/Decision-Templates",
        "files": [
            "V6-Authentication-Strategy.md",
            "V7-Session-Management.md",
            "V8-Authorization-Rules.md",
            "V11-Cryptography-Strategy.md",
            "V14-Data-Classification.md",
            "V16-Security-Logging-Strategy.md",
        ],
    },
    "core_reference": {
        "description": "ASVS core reference files (JSON/CSV)",
        "base_path": "01-ASVS-Core-Reference",
        "files": [
            "ASVS-5.0-en.json",
            "ASVS-L1-Baseline.json",
            "ASVS-L1-Baseline.csv",
            "ASVS-L2-Standard.json",
            "ASVS-L2-Standard.csv",
        ],
    },
    "functional_requirements": {
        "description": "Functional requirements by level",
        "base_path": "01-ASVS-Core-Reference/Functional-Requirements",
        "files": [
            "ASVS-Functional-Requirements-L1.json",
            "ASVS-Functional-Requirements-L2.json",
            "ASVS-Functional-Requirements-L3.json",
        ],
    },
    "patterns": {
        "description": "Implementation patterns",
        "base_path": "02-Implementation-Guidance/Patterns",
        "files": [
            "Anti-CSRF-Implementation.md",
            "Input-Validation.md",
            "Secure-Access-Control-IDOR.md",
            "Secure-File-Uploads.md",
            "Security-Logging-and-Monitoring.md",
        ],
    },
}


class ResourceDownloadError(Exception):
    """Raised when resource download fails."""
    pass


class ResourceManager:
    """Manages downloading and caching of ASVS resources from GitHub."""

    def __init__(self, cache_dir: Optional[Path] = None):
        """
        Initialize the resource manager.

        Args:
            cache_dir: Directory to cache downloaded resources.
                      Defaults to ~/.asvs-compliance/resources
        """
        self.cache_dir = cache_dir or DEFAULT_CACHE_DIR
        self._manifest_cache: Optional[Dict] = None

    def get_cache_path(self, resource_type: str, filename: str) -> Path:
        """Get the cached path for a resource file."""
        manifest = RESOURCE_MANIFEST.get(resource_type)
        if not manifest:
            raise ValueError(f"Unknown resource type: {resource_type}")
        return self.cache_dir / manifest["base_path"] / filename

    def is_resource_cached(self, resource_type: str, filename: str) -> bool:
        """Check if a resource file is already cached."""
        return self.get_cache_path(resource_type, filename).exists()

    def are_resources_available(self, resource_type: str) -> bool:
        """Check if all resources of a type are cached."""
        manifest = RESOURCE_MANIFEST.get(resource_type)
        if not manifest:
            return False
        return all(
            self.is_resource_cached(resource_type, f)
            for f in manifest["files"]
        )

    def get_resource_url(self, resource_type: str, filename: str) -> str:
        """Get the GitHub raw URL for a resource file."""
        manifest = RESOURCE_MANIFEST.get(resource_type)
        if not manifest:
            raise ValueError(f"Unknown resource type: {resource_type}")
        return f"{GITHUB_RAW_BASE}/{manifest['base_path']}/{filename}"

    def download_file(self, url: str, dest_path: Path, timeout: int = 30) -> bool:
        """
        Download a file from URL to destination path.

        Args:
            url: URL to download from
            dest_path: Destination path for the file
            timeout: Request timeout in seconds

        Returns:
            True if download successful, False otherwise
        """
        try:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            request = urllib.request.Request(
                url,
                headers={"User-Agent": "ASVS-Compliance-CLI"}
            )
            
            with urllib.request.urlopen(request, timeout=timeout) as response:
                content = response.read()
                dest_path.write_bytes(content)
            
            return True
            
        except urllib.error.URLError:
            return False
        except urllib.error.HTTPError:
            return False
        except OSError:
            return False

    def download_resource(
        self,
        resource_type: str,
        filename: str,
        force: bool = False
    ) -> tuple[bool, str]:
        """
        Download a single resource file.

        Args:
            resource_type: Type of resource (templates, core_reference, etc.)
            filename: Name of the file to download
            force: If True, re-download even if cached

        Returns:
            Tuple of (success, message)
        """
        if not force and self.is_resource_cached(resource_type, filename):
            return True, f"Already cached: {filename}"

        url = self.get_resource_url(resource_type, filename)
        dest_path = self.get_cache_path(resource_type, filename)

        if self.download_file(url, dest_path):
            return True, f"Downloaded: {filename}"
        else:
            return False, f"Failed to download: {filename}"

    def download_resource_type(
        self,
        resource_type: str,
        progress_callback: Optional[callable] = None,
        force: bool = False
    ) -> tuple[int, int, List[str]]:
        """
        Download all files for a resource type.

        Args:
            resource_type: Type of resource to download
            progress_callback: Optional callback(filename, success, message)
            force: If True, re-download even if cached

        Returns:
            Tuple of (success_count, total_count, error_messages)
        """
        manifest = RESOURCE_MANIFEST.get(resource_type)
        if not manifest:
            raise ValueError(f"Unknown resource type: {resource_type}")

        success_count = 0
        errors = []

        for filename in manifest["files"]:
            success, message = self.download_resource(resource_type, filename, force)
            
            if progress_callback:
                progress_callback(filename, success, message)
            
            if success:
                success_count += 1
            else:
                errors.append(message)

        return success_count, len(manifest["files"]), errors

    def download_all_resources(
        self,
        progress_callback: Optional[callable] = None,
        force: bool = False
    ) -> Dict[str, tuple[int, int, List[str]]]:
        """
        Download all resource types.

        Args:
            progress_callback: Optional callback(resource_type, filename, success, message)
            force: If True, re-download even if cached

        Returns:
            Dict mapping resource_type to (success_count, total_count, errors)
        """
        results = {}
        
        for resource_type in RESOURCE_MANIFEST:
            def type_callback(filename, success, message):
                if progress_callback:
                    progress_callback(resource_type, filename, success, message)
            
            results[resource_type] = self.download_resource_type(
                resource_type, type_callback, force
            )

        return results

    def get_templates_path(self) -> Path:
        """Get the path to cached templates directory."""
        return self.cache_dir / RESOURCE_MANIFEST["templates"]["base_path"]

    def get_core_reference_path(self) -> Path:
        """Get the path to cached core reference directory."""
        return self.cache_dir / RESOURCE_MANIFEST["core_reference"]["base_path"]

    def clear_cache(self) -> bool:
        """Clear all cached resources."""
        try:
            import shutil
            if self.cache_dir.exists():
                shutil.rmtree(self.cache_dir)
            return True
        except OSError:
            return False


def prompt_download_permission(resource_types: Optional[List[str]] = None) -> bool:
    """
    Prompt the user for permission to download resources.

    Args:
        resource_types: Optional list of specific resource types to download.
                       If None, downloads all resources.

    Returns:
        True if user grants permission, False otherwise
    """
    print("\n" + "=" * 60)
    print("ASVS Compliance Starter Kit - Resource Download Required")
    print("=" * 60)
    print()
    print("The ASVS CLI requires additional resources to function fully.")
    print("These include templates, reference files, and documentation.")
    print()
    print("Resources will be downloaded from:")
    print(f"  {GITHUB_REPO_URL}")
    print()
    print("And cached locally at:")
    print(f"  {DEFAULT_CACHE_DIR}")
    print()
    
    if resource_types:
        print("Resources to download:")
        for rt in resource_types:
            manifest = RESOURCE_MANIFEST.get(rt)
            if manifest:
                print(f"  - {manifest['description']} ({len(manifest['files'])} files)")
    else:
        print("Resources to download:")
        for rt, manifest in RESOURCE_MANIFEST.items():
            print(f"  - {manifest['description']} ({len(manifest['files'])} files)")
    
    print()
    
    try:
        response = input("Do you want to download these resources? [Y/n]: ").strip().lower()
        return response in ("", "y", "yes")
    except (EOFError, KeyboardInterrupt):
        print()
        return False


def show_manual_instructions():
    """Display instructions for manual setup when user declines download."""
    print()
    print("=" * 60)
    print("Manual Setup Instructions")
    print("=" * 60)
    print()
    print("To use the ASVS CLI with full functionality, please clone")
    print("the repository and run the CLI from within the repo:")
    print()
    print(f"  git clone {GITHUB_REPO_URL}.git")
    print("  cd asvs-compliance-starter-kit")
    print("  pip install -e .")
    print("  asvs init --interactive")
    print()
    print("Alternatively, visit the repository for more information:")
    print(f"  {GITHUB_REPO_URL}")
    print()


def ensure_resources(
    resource_types: Optional[List[str]] = None,
    interactive: bool = True,
    quiet: bool = False
) -> tuple[bool, Optional[Path]]:
    """
    Ensure required resources are available, downloading if necessary.

    Args:
        resource_types: List of resource types to ensure. If None, ensures all.
        interactive: If True, prompt user before downloading.
        quiet: If True, suppress progress output.

    Returns:
        Tuple of (success, cache_path). cache_path is None if resources unavailable.
    """
    manager = ResourceManager()
    
    types_to_check = resource_types or list(RESOURCE_MANIFEST.keys())
    
    missing_types = [
        rt for rt in types_to_check
        if not manager.are_resources_available(rt)
    ]
    
    if not missing_types:
        return True, manager.cache_dir
    
    if interactive:
        if not prompt_download_permission(missing_types):
            show_manual_instructions()
            return False, None
    
    if not quiet:
        print()
        print("Downloading resources...")
        print()
    
    all_success = True
    
    for resource_type in missing_types:
        manifest = RESOURCE_MANIFEST.get(resource_type)
        if not quiet:
            print(f"  {manifest['description']}:")
        
        def progress(filename, success, message):
            if not quiet:
                status = "OK" if success else "FAILED"
                print(f"    [{status}] {filename}")
        
        success, total, errors = manager.download_resource_type(
            resource_type, progress
        )
        
        if success < total:
            all_success = False
            if not quiet:
                for error in errors:
                    print(f"    Error: {error}")
    
    if not quiet:
        print()
        if all_success:
            print("All resources downloaded successfully.")
        else:
            print("Some resources failed to download.")
            print("The CLI may have limited functionality.")
    
    return all_success, manager.cache_dir


def get_resource_path(resource_type: str) -> Optional[Path]:
    """
    Get the path to a resource type, checking local repo first then cache.

    Args:
        resource_type: Type of resource (templates, core_reference, etc.)

    Returns:
        Path to the resource directory, or None if not available.
    """
    manifest = RESOURCE_MANIFEST.get(resource_type)
    if not manifest:
        return None
    
    script_dir = Path(__file__).parent.parent
    local_path = script_dir / manifest["base_path"]
    if local_path.exists():
        return local_path
    
    manager = ResourceManager()
    cached_path = manager.cache_dir / manifest["base_path"]
    if cached_path.exists():
        return cached_path
    
    return None


def main():
    """CLI entry point for resource management."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="ASVS Resource Manager - Download and manage CLI resources"
    )
    parser.add_argument(
        "--download",
        action="store_true",
        help="Download all resources"
    )
    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Clear cached resources"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show resource cache status"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-download even if cached"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress progress output"
    )
    
    args = parser.parse_args()
    
    manager = ResourceManager()
    
    if args.clear_cache:
        if manager.clear_cache():
            print("Cache cleared successfully.")
        else:
            print("Failed to clear cache.")
        return 0
    
    if args.status:
        print(f"Cache directory: {manager.cache_dir}")
        print()
        for rt, manifest in RESOURCE_MANIFEST.items():
            available = manager.are_resources_available(rt)
            status = "Available" if available else "Missing"
            print(f"  {manifest['description']}: {status}")
        return 0
    
    if args.download:
        success, _ = ensure_resources(
            interactive=False,
            quiet=args.quiet
        )
        return 0 if success else 1
    
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
