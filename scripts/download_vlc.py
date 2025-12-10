#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Download and extract VLC 3.0.8 64-bit portable to external/vlc-portable.

This script downloads VLC from VideoLAN's official repository and extracts
it to the project's external/vlc-portable directory.
"""

import os
import sys
import zipfile
import shutil
from pathlib import Path
from urllib.request import urlretrieve
from urllib.error import URLError


VLC_VERSION = "3.0.8"
VLC_URL = f"https://download.videolan.org/pub/videolan/vlc/{VLC_VERSION}/win64/vlc-{VLC_VERSION}-win64.zip"
VLC_DLL_NAME = "libvlc.dll"


def get_project_root():
    """Get the project root directory."""
    # This script is in scripts/, so project root is parent
    script_dir = Path(__file__).parent.resolve()
    project_root = script_dir.parent
    return project_root


def get_vlc_portable_path():
    """Get the path where portable VLC should be installed."""
    project_root = get_project_root()
    return project_root / "external" / "vlc-portable"


def vlc_already_installed():
    """Check if VLC is already installed in the portable location."""
    vlc_path = get_vlc_portable_path()
    dll_path = vlc_path / VLC_DLL_NAME
    return dll_path.exists()


def download_vlc(progress_callback=None):
    """
    Download VLC portable ZIP file.
    
    Args:
        progress_callback: Optional callback function for download progress
        
    Returns:
        Path to downloaded ZIP file
    """
    project_root = get_project_root()
    download_dir = project_root / "external"
    download_dir.mkdir(parents=True, exist_ok=True)
    
    zip_filename = f"vlc-{VLC_VERSION}-win64.zip"
    zip_path = download_dir / zip_filename
    
    # Remove existing ZIP if present
    if zip_path.exists():
        print(f"Removing existing download: {zip_path}")
        zip_path.unlink()
    
    print(f"Downloading VLC {VLC_VERSION} from {VLC_URL}")
    print(f"Destination: {zip_path}")
    
    try:
        if progress_callback:
            urlretrieve(VLC_URL, zip_path, reporthook=progress_callback)
        else:
            urlretrieve(VLC_URL, zip_path)
        print("Download completed successfully.")
        return zip_path
    except URLError as e:
        print(f"ERROR: Failed to download VLC: {e}")
        print(f"Please check your internet connection and try again.")
        print(f"Alternatively, manually download from: {VLC_URL}")
        raise


def extract_vlc(zip_path):
    """
    Extract VLC ZIP file to external/vlc-portable.
    
    Args:
        zip_path: Path to the VLC ZIP file
    """
    vlc_path = get_vlc_portable_path()
    
    # Remove existing installation if present
    if vlc_path.exists():
        print(f"Removing existing VLC installation: {vlc_path}")
        shutil.rmtree(vlc_path)
    
    vlc_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Extracting VLC to: {vlc_path}")
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Extract all files
            zip_ref.extractall(vlc_path.parent)
            
            # The ZIP contains a folder like "vlc-3.0.8", we need to move contents up
            extracted_folders = [f for f in vlc_path.parent.iterdir() 
                               if f.is_dir() and f.name.startswith('vlc-')]
            
            if extracted_folders:
                extracted_folder = extracted_folders[0]
                # Move contents from extracted folder to vlc-portable
                vlc_path.mkdir(parents=True, exist_ok=True)
                for item in extracted_folder.iterdir():
                    dest = vlc_path / item.name
                    if item.is_dir():
                        shutil.copytree(item, dest, dirs_exist_ok=True)
                    else:
                        shutil.copy2(item, dest)
                
                # Remove the intermediate folder
                shutil.rmtree(extracted_folder)
        
        print("Extraction completed successfully.")
        
        # Verify installation
        dll_path = vlc_path / VLC_DLL_NAME
        if not dll_path.exists():
            raise FileNotFoundError(f"VLC DLL not found at expected location: {dll_path}")
        
        print(f"VLC {VLC_VERSION} installed successfully at: {vlc_path}")
        print(f"VLC DLL found at: {dll_path}")
        
    except zipfile.BadZipFile:
        print(f"ERROR: Invalid ZIP file: {zip_path}")
        raise
    except Exception as e:
        print(f"ERROR: Failed to extract VLC: {e}")
        raise


def cleanup_download(zip_path):
    """Remove the downloaded ZIP file after extraction."""
    if zip_path.exists():
        print(f"Cleaning up download file: {zip_path}")
        zip_path.unlink()


def download_progress_hook(count, block_size, total_size):
    """Display download progress."""
    downloaded = count * block_size
    percent = min(100, (downloaded * 100) / total_size) if total_size > 0 else 0
    sys.stdout.write(f"\rProgress: {percent:.1f}% ({downloaded / (1024*1024):.1f} MB)")
    sys.stdout.flush()


def main():
    """Main function to download and install VLC."""
    print("=" * 60)
    print(f"VLC {VLC_VERSION} Portable Installation")
    print("=" * 60)
    
    # Check if already installed
    if vlc_already_installed():
        print(f"VLC {VLC_VERSION} is already installed at: {get_vlc_portable_path()}")
        response = input("Do you want to reinstall? (y/N): ").strip().lower()
        if response != 'y':
            print("Installation cancelled.")
            return
        print()
    
    try:
        # Download
        zip_path = download_vlc(progress_callback=download_progress_hook)
        print()  # New line after progress
        
        # Extract
        extract_vlc(zip_path)
        
        # Cleanup
        cleanup_download(zip_path)
        
        print()
        print("=" * 60)
        print("Installation completed successfully!")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nERROR: Installation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

