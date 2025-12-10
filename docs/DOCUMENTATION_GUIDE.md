# Documentation Generation Guide

This guide explains how to automatically generate documentation from your Python code, docstrings, and type hints.

## Overview

The project uses [Sphinx](https://www.sphinx-doc.org/) to automatically generate documentation from:
- **Python docstrings** (Google/NumPy style supported via Napoleon extension)
- **Type hints** (automatically extracted and displayed)
- **Module structure** (automatically discovered via `sphinx-apidoc`)

## Prerequisites

Install the documentation dependencies:

```bash
# Using pip
pip install -e ".[docs]"

# Or install directly
pip install sphinx>=3.2.1 myst-parser[linkify]
```

### Optional: Enhanced Type Hint Support

For better type hint formatting in the documentation, you can install the `sphinx-autodoc-typehints` extension:

```bash
pip install sphinx-autodoc-typehints
```

Then uncomment the relevant lines in `docs/conf.py` to enable it.

## Generating Documentation

### Method 1: Using the Python Script (Recommended)

The easiest way to generate documentation is using the provided script:

```bash
# Generate documentation
python docs/generate_docs.py

# Clean and regenerate (removes old build files)
python docs/generate_docs.py clean
```

This script will:
1. Automatically run `sphinx-apidoc` to generate API documentation stubs
2. Build the HTML documentation
3. Show you where to find the generated docs

### Method 2: Using Make (Linux/Mac/Git Bash)

If you have `make` installed:

```bash
cd docs

# Generate HTML documentation
make html

# Clean build directory
make clean

# View all available options
make help
```

### Method 3: Using Sphinx Directly

You can also run Sphinx commands directly:

```bash
cd docs

# Generate API documentation stubs
sphinx-apidoc --implicit-namespaces -f -o api ../src/phopyqttimelineplotter

# Build HTML documentation
sphinx-build -b html . _build/html
```

## Viewing the Documentation

After building, open the generated HTML documentation:

```
docs/_build/html/index.html
```

You can open this file in any web browser.

## Configuration

Documentation generation is configured in `docs/conf.py`. Key settings include:

### Type Hints Display

- `autodoc_typehints = "description"` - Shows type hints in the description
- `autodoc_typehints_description_target = "documented"` - Only show hints for documented items
- `typehints_fully_qualified = False` - Use short names instead of fully qualified names

### What Gets Documented

- `autodoc_default_options` - Controls which members are documented
  - `members: True` - Document all members
  - `undoc-members: False` - Skip undocumented members
  - `show-inheritance: True` - Show class inheritance
  - `special-members: "__init__"` - Document `__init__` methods

## Writing Good Documentation

### Docstrings

Use Google-style or NumPy-style docstrings (both are supported via Napoleon):

**Google Style:**
```python
def parse_video_folder(cls, folder_path: Path, video_extensions: List[str] = ['.mp4', '.avi']) -> pd.DataFrame:
    """Parse a folder containing video files.
    
    Args:
        folder_path: Path to the folder containing videos
        video_extensions: List of video file extensions to look for
        
    Returns:
        DataFrame containing video file information
        
    Raises:
        FileNotFoundError: If the folder doesn't exist
    """
    pass
```

**NumPy Style:**
```python
def parse_video_folder(cls, folder_path: Path, video_extensions: List[str] = ['.mp4', '.avi']) -> pd.DataFrame:
    """Parse a folder containing video files.
    
    Parameters
    ----------
    folder_path : Path
        Path to the folder containing videos
    video_extensions : List[str], optional
        List of video file extensions to look for, by default ['.mp4', '.avi']
        
    Returns
    -------
    pd.DataFrame
        DataFrame containing video file information
        
    Raises
    ------
    FileNotFoundError
        If the folder doesn't exist
    """
    pass
```

### Type Hints

Type hints are automatically extracted and displayed. Make sure to use proper type annotations:

```python
from typing import List, Optional, Dict
from pathlib import Path
import pandas as pd

def process_data(
    file_path: Path,
    options: Optional[Dict[str, str]] = None,
    columns: List[str] = None
) -> pd.DataFrame:
    """Process data from a file."""
    pass
```

## Automatic API Documentation

The `sphinx-apidoc` command (run automatically in `conf.py`) scans your Python package and generates `.rst` files for each module. These are then processed by Sphinx to create the final documentation.

The generated API documentation includes:
- Module documentation
- Class documentation with inheritance
- Function/method signatures with type hints
- Docstrings formatted nicely

## Troubleshooting

### Documentation not updating

If changes to your code aren't reflected in the docs:

1. Clean the build directory: `python docs/generate_docs.py clean`
2. Regenerate: `python docs/generate_docs.py`

### Missing modules

If a module isn't being documented:

1. Check that it's in `src/phopyqttimelineplotter/`
2. Ensure it has an `__init__.py` file (for packages)
3. Check `exclude_patterns` in `conf.py` isn't excluding it

### Type hints not showing

- Ensure you're using Python 3.9+ (type hints are more reliable)
- Check that `sphinx.ext.typehints` is in the `extensions` list
- Verify `autodoc_typehints` is set to `"description"` or `"signature"`

### Import errors during build

If you get import errors when building docs, add problematic packages to `autodoc_mock_imports` in `conf.py`:

```python
autodoc_mock_imports = ["some_problematic_package"]
```

## Continuous Integration

For automated documentation builds (e.g., on ReadTheDocs), the `conf.py` file automatically runs `sphinx-apidoc` before building, so no manual steps are needed.

## Additional Resources

- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [Napoleon Extension](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html)
- [Autodoc Extension](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html)
- [Type Hints Extension](https://github.com/agronholm/sphinx-autodoc-typehints)

