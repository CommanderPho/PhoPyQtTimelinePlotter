"""
VLC Setup Utilities

This module provides utilities for managing the portable VLC installation
and configuring the application to use it.
"""

import os
import sys
from pathlib import Path


VLC_VERSION = "3.0.8"
VLC_DLL_NAME = "libvlc.dll"


def get_project_root():
    """
    Get the project root directory.
    
    This function calculates the project root relative to this module's location.
    vlc_setup.py is at: src/phopyqttimelineplotter/lib/vlc_setup.py
    Project root is: ../../.. relative to this file (lib -> phopyqttimelineplotter -> src -> root)
    """
    # Get the directory containing this file
    lib_dir = Path(__file__).parent.resolve()
    # Navigate to project root: lib -> phopyqttimelineplotter -> src -> project_root
    project_root = lib_dir.parent.parent.parent
    return project_root


def get_vlc_portable_path():
    """Get the path where portable VLC should be installed."""
    project_root = get_project_root()
    return project_root / "external" / "vlc-portable"


def get_vlc_dll_path():
    """Get the path to libvlc.dll in the portable installation."""
    vlc_path = get_vlc_portable_path()
    return vlc_path / VLC_DLL_NAME


def get_vlc_plugin_path():
    """Get the path to the plugins directory in the portable installation."""
    vlc_path = get_vlc_portable_path()
    return vlc_path / "plugins"


def vlc_portable_exists():
    """
    Check if portable VLC installation exists and is valid.
    
    Returns:
        bool: True if portable VLC is installed, False otherwise
    """
    dll_path = get_vlc_dll_path()
    return dll_path.exists() and dll_path.is_file()


def configure_vlc_environment():
    """
    Configure environment variables to use portable VLC if it exists.
    
    This sets PYTHON_VLC_LIB_PATH and PYTHON_VLC_MODULE_PATH environment
    variables if portable VLC is found. These variables are checked by
    the vlc.py module before falling back to system VLC.
    
    Returns:
        bool: True if portable VLC was configured, False otherwise
    """
    if not vlc_portable_exists():
        return False
    
    dll_path = get_vlc_dll_path()
    plugin_path = get_vlc_plugin_path()
    
    # Set environment variables (these are checked first in vlc.py's find_lib())
    os.environ['PYTHON_VLC_LIB_PATH'] = str(dll_path)
    if plugin_path.exists():
        os.environ['PYTHON_VLC_MODULE_PATH'] = str(plugin_path)
    
    return True


def ensure_vlc_available(auto_download=False):
    """
    Ensure VLC is available, optionally downloading if missing.
    
    Args:
        auto_download: If True, automatically download VLC if not found.
                      If False, only configure environment if VLC exists.
    
    Returns:
        bool: True if VLC is available, False otherwise
    """
    if vlc_portable_exists():
        configure_vlc_environment()
        return True
    
    if auto_download:
        try:
            # Import here to avoid circular dependencies
            import subprocess
            script_path = get_project_root() / "scripts" / "download_vlc.py"
            
            if script_path.exists():
                print(f"VLC not found. Downloading VLC {VLC_VERSION}...")
                result = subprocess.run(
                    [sys.executable, str(script_path)],
                    check=False
                )
                if result.returncode == 0 and vlc_portable_exists():
                    configure_vlc_environment()
                    return True
                else:
                    print("Failed to download VLC automatically.")
                    return False
            else:
                print(f"Download script not found at: {script_path}")
                return False
        except Exception as e:
            print(f"Error during automatic VLC download: {e}")
            return False
    else:
        return False


def get_vlc_info():
    """
    Get information about the VLC installation.
    
    Returns:
        dict: Dictionary with VLC installation information
    """
    info = {
        'portable_exists': vlc_portable_exists(),
        'version': VLC_VERSION,
        'dll_path': None,
        'plugin_path': None,
    }
    
    if info['portable_exists']:
        info['dll_path'] = str(get_vlc_dll_path())
        plugin_path = get_vlc_plugin_path()
        if plugin_path.exists():
            info['plugin_path'] = str(plugin_path)
    
    return info

