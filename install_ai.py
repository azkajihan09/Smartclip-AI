#!/usr/bin/env python3
"""
AI Dependencies Installer untuk Smartclip AI
Install semua AI libraries yang dibutuhkan
"""

import subprocess
import sys
import importlib.util
import time

def print_banner():
    """Print installation banner"""
    print("=" * 60)
    print("    SMARTCLIP AI - AI DEPENDENCIES INSTALLER")
    print("=" * 60)
    print("🤖 Installing AI libraries for advanced features...")
    print()

def check_package(package_name):
    """Check if package is already installed"""
    spec = importlib.util.find_spec(package_name)
    return spec is not None

def install_package(package_name, display_name=None, extra_args=None):
    """Install single package with error handling"""
    if display_name is None:
        display_name = package_name
        
    # Check if already installed
    base_package = package_name.split('[')[0].split('=')[0]
    if check_package(base_package.replace('-', '_')):
        print(f"✅ {display_name} - Already installed")
        return True
        
    try:
        print(f"📦 Installing {display_name}...")
        
        # Build command
        cmd = [sys.executable, "-m", "pip", "install", package_name]
        if extra_args:
            cmd.extend(extra_args)
            
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=300  # 5 minute timeout per package
        )
        
        print(f"✅ {display_name} - Installed successfully")
        return True
        
    except subprocess.TimeoutExpired:
        print(f"⏱️ {display_name} - Installation timeout (5 minutes)")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ {display_name} - Installation failed")
        print(f"   Error: {e.stderr.strip()}")
        return False
    except Exception as e:
        print(f"❌ {display_name} - Unexpected error: {str(e)}")
        return False

def install_pytorch():
    """Install PyTorch dengan CPU version untuk compatibility"""
    print("🔥 Installing PyTorch (CPU version)...")
    
    # Check if torch already installed
    if check_package('torch'):
        print("✅ PyTorch - Already installed")
        return True
    
    try:
        # Install PyTorch CPU version (lebih ringan)
        cmd = [
            sys.executable, "-m", "pip", "install",
            "torch", "torchvision", "torchaudio",
            "--index-url", "https://download.pytorch.org/whl/cpu"
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=600  # 10 minutes for PyTorch
        )
        
        print("✅ PyTorch - Installed successfully")
        return True
        
    except subprocess.TimeoutExpired:
        print("⏱️ PyTorch - Installation timeout")
        return False
    except subprocess.CalledProcessError as e:
        print("❌ PyTorch - Installation failed")
        print(f"   Error: {e.stderr.strip()}")
        return False

def install_ai_packages():
    """Install essential AI packages"""
    print("\n🧠 Installing AI/ML packages...")
    print("-" * 40)
    
    packages = [
        # Core AI packages
        ("openai-whisper", "OpenAI Whisper (Speech Recognition)"),
        ("transformers", "Hugging Face Transformers"),
        
        # Audio processing
        ("librosa", "Librosa (Audio Analysis)"),
        ("speechbrain", "SpeechBrain (Voice Processing)"),
        
        # Computer Vision
        ("opencv-python", "OpenCV (Computer Vision)"),
        ("face-recognition", "Face Recognition"),
        
        # Scientific computing  
        ("scikit-learn", "Scikit-learn (Machine Learning)"),
        ("scipy", "SciPy (Scientific Computing)"),
        
        # Data processing
        ("pandas", "Pandas (Data Analysis)"),
        ("matplotlib", "Matplotlib (Plotting)")
    ]
    
    successful = 0
    total = len(packages)
    
    for package, name in packages:
        if install_package(package, name):
            successful += 1
        time.sleep(1)  # Small delay between installations
        print()
    
    print(f"📊 AI Packages: {successful}/{total} installed successfully")
    return successful

def install_speaker_diarization():
    """Install speaker diarization packages"""
    print("\n🎙️ Installing Speaker Diarization...")
    print("-" * 40)
    
    packages = [
        ("pyannote.audio", "PyAnnote Audio (Speaker Diarization)"),
        ("asteroid", "Asteroid (Audio Source Separation)"),
        ("torch-audio", "PyTorch Audio")
    ]
    
    successful = 0
    for package, name in packages:
        try:
            if install_package(package, name):
                successful += 1
        except:
            print(f"⚠️ {name} - Skipping due to compatibility issues")
        time.sleep(1)
        print()
    
    print(f"📊 Speaker Diarization: {successful}/{len(packages)} packages installed")
    return successful

def test_ai_installation():
    """Test AI package imports"""
    print("\n🧪 Testing AI package imports...")
    print("-" * 40)
    
    test_packages = [
        ("torch", "PyTorch"),
        ("whisper", "OpenAI Whisper"), 
        ("transformers", "Transformers"),
        ("cv2", "OpenCV"),
        ("face_recognition", "Face Recognition"),
        ("librosa", "Librosa"),
        ("sklearn", "Scikit-learn"),
        ("scipy", "SciPy"),
        ("pandas", "Pandas"),
        ("matplotlib", "Matplotlib")
    ]
    
    working = 0
    total = len(test_packages)
    
    for module, name in test_packages:
        try:
            __import__(module)
            print(f"✅ {name} - Import successful")
            working += 1
        except ImportError as e:
            print(f"❌ {name} - Import failed: {str(e)[:50]}...")
        except Exception as e:
            print(f"⚠️ {name} - Import error: {str(e)[:50]}...")
    
    print(f"\n📊 AI Import Test: {working}/{total} packages working")
    
    if working >= 6:
        print("🎉 Enough AI packages working for advanced features!")
        return True
    else:
        print("⚠️ Limited AI functionality - some features may not work")
        return False

def show_next_steps():
    """Show what to do after installation"""
    print("\n" + "=" * 60)
    print("           INSTALLATION COMPLETE!")
    print("=" * 60)
    
    print("\n🚀 Ready to use AI features:")
    print("   • 🎯 Auto-detect best moments")
    print("   • 👤 Smart face tracking") 
    print("   • 🎙️ Speaker identification")
    print("   • 📝 Automatic subtitles")
    print("   • 🔖 Watermark addition")
    print("   • 📺 Podcast mode (split screen)")
    
    print("\n📋 Next steps:")
    print("   1. Run: python main.py")
    print("   2. Input YouTube URL")
    print("   3. Select AI processing options")
    print("   4. Start processing!")
    
    print("\n💡 Tips:")
    print("   • First run will download AI models (~1-2GB)")
    print("   • Processing speed depends on video length")
    print("   • Use GPU if available for faster processing")
    
    print("\n🌟 Enjoy AI-powered video processing!")

def main():
    """Main installer function"""
    print_banner()
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required!")
        print(f"   Current version: {sys.version}")
        input("Press Enter to exit...")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    print()
    
    # Upgrade pip
    print("🔄 Upgrading pip...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      capture_output=True, check=True)
        print("✅ Pip upgraded")
    except:
        print("⚠️ Could not upgrade pip - continuing anyway")
    print()
    
    # Install components step by step
    total_success = 0
    
    # Install PyTorch
    if install_pytorch():
        total_success += 3  # Count as 3 packages
    
    # Install AI packages
    ai_success = install_ai_packages()
    total_success += ai_success
    
    # Install speaker diarization (optional)
    speaker_success = install_speaker_diarization()
    total_success += speaker_success
    
    # Test installation
    ai_working = test_ai_installation()
    
    # Show results
    print("\n" + "=" * 60)
    print("           INSTALLATION SUMMARY")
    print("=" * 60)
    print(f"📦 Packages installed: ~{total_success}")
    print(f"✅ AI packages working: {ai_working}")
    
    if ai_working >= 6:
        print("🎉 AI installation successful!")
        show_next_steps()
    else:
        print("⚠️ Limited AI installation")
        print("   Some advanced features may not work")
        print("   You can still use basic video processing")
        print("\n💡 Try running: python main_lite.py")
    
    print("\n📚 Need help?")
    print("   • Check README.md for troubleshooting")
    print("   • Manual install commands in TESTING.md")
    
    input("\nPress Enter to exit...")
    return ai_working >= 6

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)