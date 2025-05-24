#!/usr/bin/env python3
"""
Setup script for the audio-api library.

This is a simple setup script that helps users get started quickly.
"""

import os
import sys
import subprocess


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 12):
        print("❌ Python 3.12 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")

    try:
        # Try uv first (faster)
        if subprocess.run(["uv", "--version"], capture_output=True).returncode == 0:
            print("   Using uv for faster installation...")
            subprocess.run(["uv", "sync"], check=True)
        else:
            print("   Using pip...")
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                check=True,
            )

        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def setup_environment():
    """Set up environment file."""
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            print("📝 Creating .env file from template...")
            with open(".env.example", "r") as src, open(".env", "w") as dst:
                dst.write(src.read())
        else:
            print("📝 Creating .env file...")
            with open(".env", "w") as f:
                f.write("GEMINI_API_KEY=your_gemini_api_key_here\n")
                f.write("REDIS_URL=redis://localhost:6379/0\n")
                f.write("NUM_WORKERS=3\n")

        print("⚠️  Please edit .env and add your GEMINI_API_KEY")
        return False
    else:
        print("✅ .env file already exists")
        return True


def run_test():
    """Run a simple test."""
    print("🧪 Running test...")

    try:
        result = subprocess.run(
            [sys.executable, "test_example.py"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            print("✅ Test passed!")
            return True
        else:
            print("❌ Test failed:")
            print(result.stdout)
            print(result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print("⏰ Test timed out (this might be normal if API key is not set)")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False


def main():
    """Main setup function."""
    print("🚀 Audio API Library Setup")
    print("=" * 40)

    # Check Python version
    if not check_python_version():
        sys.exit(1)

    # Install dependencies
    if not install_dependencies():
        sys.exit(1)

    # Setup environment
    env_ready = setup_environment()

    print("\n🎉 Setup completed!")
    print("\n📋 Next steps:")

    if not env_ready:
        print("   1. Edit .env file and add your GEMINI_API_KEY")
        print("   2. Run: python test_example.py")
        print("   3. Run: python main.py")
    else:
        print("   1. Run: python test_example.py")
        print("   2. Run: python main.py")

    print("\n💡 Usage in your code:")
    print(
        """
from audio_api import AudioRequest, TTSService

async def example():
    tts = TTSService()
    request = AudioRequest(text="Hello, world!")
    result = await tts.generate_audio(request)
    return result.file_path if result.success else None
    """
    )


if __name__ == "__main__":
    main()
