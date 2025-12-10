#!/usr/bin/env python3
"""
Script to generate Sphinx documentation from Python code and docstrings.

This script:
1. Automatically runs sphinx-apidoc to generate API documentation stubs
2. Builds the HTML documentation using sphinx-build

Usage:
    python generate_docs.py [clean]
    
    If 'clean' is provided, it will clean the build directory first.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent
SRC_DIR = PROJECT_ROOT / "src"
DOCS_DIR = SCRIPT_DIR
API_DIR = DOCS_DIR / "api"
BUILD_DIR = DOCS_DIR / "_build"
MODULE_DIR = SRC_DIR / "phopyqttimelineplotter"


def run_command(cmd, description):
    """Run a shell command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}\n")
    
    result = subprocess.run(cmd, cwd=DOCS_DIR, check=False)
    if result.returncode != 0:
        print(f"\n❌ Error: {description} failed with exit code {result.returncode}")
        sys.exit(1)
    print(f"✅ {description} completed successfully\n")


def clean_build():
    """Clean the build directory and API directory."""
    print("Cleaning build directories...")
    for dir_path in [BUILD_DIR, API_DIR]:
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"  Removed: {dir_path}")
    print("✅ Clean completed\n")


def generate_api_docs():
    """Generate API documentation stubs using sphinx-apidoc."""
    # Ensure API directory exists
    API_DIR.mkdir(exist_ok=True)
    
    # Run sphinx-apidoc
    cmd = [
        sys.executable, "-m", "sphinx.ext.apidoc",
        "--implicit-namespaces",
        "-f",  # Force overwrite
        "-o", str(API_DIR),
        str(MODULE_DIR)
    ]
    
    run_command(cmd, "Generating API documentation stubs (sphinx-apidoc)")


def build_html_docs():
    """Build HTML documentation using sphinx-build."""
    cmd = [
        sys.executable, "-m", "sphinx",
        "-b", "html",
        str(DOCS_DIR),
        str(BUILD_DIR / "html")
    ]
    
    run_command(cmd, "Building HTML documentation (sphinx-build)")


def main():
    """Main function."""
    # Check if clean was requested
    if len(sys.argv) > 1 and sys.argv[1].lower() == "clean":
        clean_build()
    
    # Check if module directory exists
    if not MODULE_DIR.exists():
        print(f"❌ Error: Module directory not found: {MODULE_DIR}")
        sys.exit(1)
    
    # Generate API docs (sphinx-apidoc is also run in conf.py, but this ensures it's done)
    # Note: conf.py also runs apidoc, so this is optional but ensures it's done first
    if not API_DIR.exists() or len(list(API_DIR.glob("*.rst"))) == 0:
        generate_api_docs()
    
    # Build HTML documentation
    build_html_docs()
    
    print(f"\n{'='*60}")
    print("✅ Documentation generation completed!")
    print(f"{'='*60}")
    print(f"\n📖 Open the documentation in your browser:")
    print(f"   file://{BUILD_DIR / 'html' / 'index.html'}")
    print(f"\n   Or navigate to: {BUILD_DIR / 'html' / 'index.html'}\n")


if __name__ == "__main__":
    main()

