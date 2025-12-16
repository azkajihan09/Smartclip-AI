#!/usr/bin/env python3
"""
Simple Installer untuk Smartclip AI
Install basic dependencies yang dibutuhkan untuk menjalankan aplikasi
"""

import subprocess
import sys
import os
from pathlib import Path

def install_package(package_name):
    """Install single package dengan pip"""
    try:
        print(f"Installing {package_name}...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            package_name, "--quiet", "--user"
        ])
        print(f"✓ {package_name} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install {package_name}: {e}")
        return False

def main():
    print("=" * 50)
    print("SMARTCLIP AI - DEPENDENCY INSTALLER")
    print("=" * 50)
    print()
    
    # Basic dependencies yang wajib ada
    required_packages = [
        "customtkinter",
        "Pillow", 
        "numpy",
        "opencv-python",
        "yt-dlp",
        "moviepy",
        "tqdm",
        "psutil"
    ]
    
    print(f"Installing {len(required_packages)} required packages...")
    print()
    
    success_count = 0
    
    for package in required_packages:
        if install_package(package):
            success_count += 1
        print()
    
    print("=" * 50)
    print(f"Installation Summary: {success_count}/{len(required_packages)} packages installed")
    print("=" * 50)
    
    if success_count == len(required_packages):
        print("✓ All basic dependencies installed successfully!")
        print()
        print("NOTE: AI dependencies (torch, whisper, etc.) will be installed")
        print("automatically when first needed to save time and space.")
        print()
        print("To run Smartclip AI:")
        print("python main.py")
    else:
        print("⚠️ Some packages failed to install. You may need to:")
        print("1. Run as administrator/with elevated privileges")
        print("2. Update pip: python -m pip install --upgrade pip")
        print("3. Check your internet connection")
        print("4. Install packages manually")
    
    print()
    input("Press Enter to continue...")

if __name__ == "__main__":
    main()