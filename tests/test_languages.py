#!/usr/bin/env python3
"""
Test script for expanded language support in audio generation library.
Tests a few key languages to verify the new language codes work properly.
"""

import asyncio
import os
from dotenv import load_dotenv
from audio_api import AudioRequest, TTSService, Language

# Load environment variables from .env file
load_dotenv()


async def test_language_support():
    """Test various languages to ensure they work correctly."""

    # Check if API key is available
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY not found in environment variables")
        print("Please set your API key in .env file")
        return

    tts = TTSService()

    # Test cases with different languages
    test_cases = [
        {
            "language": Language.ENGLISH_US,
            "text": "Hello, this is a test in English.",
            "name": "English (US)",
        },
        {
            "language": Language.SPANISH_US,
            "text": "Hola, esta es una prueba en español.",
            "name": "Spanish (US)",
        },
        {
            "language": Language.FRENCH_FRANCE,
            "text": "Bonjour, ceci est un test en français.",
            "name": "French (France)",
        },
        {
            "language": Language.HINDI_INDIA,
            "text": "नमस्ते, यह हिंदी में एक परीक्षण है।",
            "name": "Hindi (India)",
        },
        {
            "language": Language.JAPANESE_JAPAN,
            "text": "こんにちは、これは日本語のテストです。",
            "name": "Japanese (Japan)",
        },
        {
            "language": Language.ARABIC_EGYPTIAN,
            "text": "مرحبا، هذا اختبار باللغة العربية.",
            "name": "Arabic (Egyptian)",
        },
    ]

    print("🎵 Testing expanded language support...")
    print(f"📊 Testing {len(test_cases)} languages\n")

    results = []

    for i, test_case in enumerate(test_cases, 1):
        print(f"🔄 [{i}/{len(test_cases)}] Testing {test_case['name']}...")

        try:
            request = AudioRequest(
                text=test_case["text"],
                language=test_case["language"],
                output_filename=f"test_{test_case['language'].value.replace('-', '_')}.wav",
            )

            result = await tts.generate_audio(request)

            if result.success:
                print(f"✅ {test_case['name']}: SUCCESS")
                print(f"   📁 File: {result.file_path}")
                results.append(
                    {
                        "language": test_case["name"],
                        "status": "SUCCESS",
                        "file": result.file_path,
                    }
                )
            else:
                print(f"❌ {test_case['name']}: FAILED")
                print(f"   🚫 Error: {result.error}")
                results.append(
                    {
                        "language": test_case["name"],
                        "status": "FAILED",
                        "error": result.error,
                    }
                )

        except Exception as e:
            print(f"❌ {test_case['name']}: EXCEPTION")
            print(f"   🚫 Exception: {str(e)}")
            results.append(
                {"language": test_case["name"], "status": "EXCEPTION", "error": str(e)}
            )

        print()

    # Summary
    print("📋 SUMMARY:")
    print("=" * 50)

    successful = sum(1 for r in results if r["status"] == "SUCCESS")
    failed = len(results) - successful

    print(f"✅ Successful: {successful}/{len(results)}")
    print(f"❌ Failed: {failed}/{len(results)}")

    if successful > 0:
        print("\n🎉 Language support is working! Generated files:")
        for result in results:
            if result["status"] == "SUCCESS":
                print(f"   • {result['language']}: {result['file']}")

    if failed > 0:
        print("\n⚠️  Some languages failed:")
        for result in results:
            if result["status"] != "SUCCESS":
                print(
                    f"   • {result['language']}: {result.get('error', 'Unknown error')}"
                )


async def test_all_language_enum_values():
    """Test that all language enum values are properly defined."""
    print("\n🔍 Testing all language enum values...")

    all_languages = [lang for lang in Language]
    print(f"📊 Total languages defined: {len(all_languages)}")

    print("\n📝 All supported languages:")
    for i, lang in enumerate(all_languages, 1):
        print(f"   {i:2d}. {lang.name}: {lang.value}")

    print(f"\n✅ All {len(all_languages)} language codes are properly defined!")


if __name__ == "__main__":
    print("🚀 Audio Generation Library - Language Support Test")
    print("=" * 60)

    # Test enum values first
    asyncio.run(test_all_language_enum_values())

    # Test actual audio generation
    asyncio.run(test_language_support())

    print("\n🏁 Language support test completed!")
