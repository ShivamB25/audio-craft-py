#!/usr/bin/env python3
"""
Audio Generation Library - Test Script

Simple test to verify the library works correctly.
"""

import asyncio
import os
from dotenv import load_dotenv

from audio_api import AudioRequest, VoiceModel, Language, SpeakerMode, TTSService

# Load environment variables
load_dotenv()


async def test_library():
    """Test the audio generation library."""
    print("🧪 Testing Audio Generation Library")
    print("=" * 40)

    # Check environment
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        print("❌ GEMINI_API_KEY not found in environment")
        return False

    print("✅ Environment check passed")

    # Test basic functionality
    try:
        tts = TTSService()

        request = AudioRequest(
            text="This is a test of the audio generation library.",
            model=VoiceModel.GEMINI_TTS,
            language=Language.ENGLISH,
            speaker_mode=SpeakerMode.SINGLE,
            output_filename="library_test.wav",
        )

        print("🔄 Generating test audio...")
        result = await tts.generate_audio(request)

        if result.success:
            print(f"✅ Test passed! Audio saved to: {result.file_path}")

            # Check file exists and has content
            if os.path.exists(result.file_path):
                file_size = os.path.getsize(result.file_path)
                print(f"📊 File size: {file_size:,} bytes")
                return True
            else:
                print("❌ Audio file was not created")
                return False
        else:
            print(f"❌ Test failed: {result.error}")
            return False

    except Exception as e:
        print(f"💥 Exception during test: {str(e)}")
        return False


async def main():
    """Main test function."""
    success = await test_library()

    if success:
        print("\n🎉 Library test completed successfully!")
        print("📁 Check the 'output' directory for generated audio files")
    else:
        print("\n❌ Library test failed")
        print("🔧 Please check your GEMINI_API_KEY and try again")

    return success


if __name__ == "__main__":
    result = asyncio.run(main())
    exit(0 if result else 1)
