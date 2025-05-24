#!/usr/bin/env python3
"""
Audio Generation Library - Simple Usage Examples

This demonstrates how to use the audio_api library for text-to-speech generation.
"""

import asyncio
from dotenv import load_dotenv

from audio_api import AudioRequest, VoiceModel, Language, SpeakerMode, TTSService

# Load environment variables
load_dotenv()


async def simple_example():
    """Simple example of generating audio from text."""
    print("🎵 Simple Audio Generation Example")
    print("=" * 40)

    # Create a TTS service instance
    tts = TTSService()

    # Create an audio request
    request = AudioRequest(
        text="Hello! This is a simple example of the audio generation library.",
        model=VoiceModel.GEMINI_TTS,
        language=Language.ENGLISH,
        speaker_mode=SpeakerMode.SINGLE,
        output_filename="simple_example.wav",
    )

    # Generate audio
    result = await tts.generate_audio(request)

    if result.success:
        print("✅ Audio generated successfully!")
        print(f"📁 File saved to: {result.file_path}")
    else:
        print(f"❌ Failed to generate audio: {result.error}")


async def multi_language_example():
    """Example showing multiple language support with new expanded languages."""
    print("\n🌍 Multi-Language Example (24 Languages Supported)")
    print("=" * 50)

    tts = TTSService()

    # Showcase diverse languages from different regions
    languages = [
        (Language.ENGLISH_US, "Hello, this is English from the United States."),
        (Language.SPANISH_US, "Hola, esto es español de Estados Unidos."),
        (Language.FRENCH_FRANCE, "Bonjour, c'est du français de France."),
        (Language.HINDI_INDIA, "नमस्ते, यह भारत से हिंदी है।"),
        (Language.JAPANESE_JAPAN, "こんにちは、これは日本からの日本語です。"),
        (Language.ARABIC_EGYPTIAN, "مرحبا، هذه عربية من مصر."),
        (Language.DUTCH_NETHERLANDS, "Hallo, dit is Nederlands uit Nederland."),
        (Language.KOREAN_KOREA, "안녕하세요, 이것은 한국의 한국어입니다."),
    ]

    print(f"🎵 Generating audio in {len(languages)} different languages...")

    for i, (lang, text) in enumerate(languages):
        print(f"\n🔄 [{i+1}/{len(languages)}] Generating {lang.name} audio...")

        request = AudioRequest(
            text=text,
            language=lang,
            output_filename=f"multilang_{lang.value.replace('-', '_')}.wav",
        )

        result = await tts.generate_audio(request)

        if result.success:
            print(f"✅ {lang.name}: {result.file_path}")
        else:
            print(f"❌ {lang.name}: {result.error}")

    print(
        f"\n📊 All 24 supported languages: {', '.join([lang.value for lang in Language])}"
    )


async def custom_voice_example():
    """Example with custom voice configuration."""
    print("\n🎭 Custom Voice Example")
    print("=" * 40)

    from audio_api import VoiceConfig, AudioFormat, VoiceName

    tts = TTSService()

    # Custom voice configuration
    voice_config = VoiceConfig(
        voice_name=VoiceName.AOEDE,  # Different voice
        speed=1.2,  # Slightly faster
        pitch=1.1,  # Slightly higher pitch
    )

    # Custom audio format
    audio_format = AudioFormat(
        sample_rate=24000,  # 24kHz as requested
        bit_depth=16,  # 16-bit
        channels=1,  # Mono
    )

    request = AudioRequest(
        text="This audio uses a custom voice configuration with different speed and pitch settings.",
        voice_config=voice_config,
        audio_format=audio_format,
        output_filename="custom_voice_example.wav",
    )

    result = await tts.generate_audio(request)

    if result.success:
        print(f"✅ Custom voice audio generated: {result.file_path}")
        print(
            f"🎵 Format: {audio_format.sample_rate}Hz, {audio_format.bit_depth}-bit, {audio_format.channels} channel"
        )
    else:
        print(f"❌ Failed: {result.error}")


async def batch_processing_example():
    """Example showing how to process multiple texts."""
    print("\n📦 Batch Processing Example")
    print("=" * 40)

    tts = TTSService()

    texts = [
        "This is the first audio file.",
        "This is the second audio file.",
        "This is the third audio file.",
    ]

    print(f"🔄 Processing {len(texts)} audio files...")

    results = []
    for i, text in enumerate(texts):
        request = AudioRequest(text=text, output_filename=f"batch_audio_{i+1}.wav")

        result = await tts.generate_audio(request)
        results.append(result)

        if result.success:
            print(f"✅ File {i+1}: {result.file_path}")
        else:
            print(f"❌ File {i+1}: {result.error}")

    successful = sum(1 for r in results if r.success)
    print(
        f"\n📊 Batch complete: {successful}/{len(texts)} files generated successfully"
    )


def main():
    """Main function to run examples."""
    print("🚀 Audio Generation Library Examples")
    print("=" * 50)

    # Check if API key is set
    import os

    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY not found in environment variables")
        print("Please set your Gemini API key in the .env file")
        return

    print("🔑 API key found, running examples...\n")

    # Run all examples
    asyncio.run(simple_example())
    asyncio.run(multi_language_example())
    asyncio.run(custom_voice_example())
    asyncio.run(batch_processing_example())

    print("\n🎉 All examples completed!")
    print("\n💡 Usage in your code:")
    print(
        """
from audio_api import AudioRequest, TTSService, Language

async def generate_audio():
    tts = TTSService()
    request = AudioRequest(
        text="Your text here",
        language=Language.ENGLISH,
        output_filename="output.wav"
    )
    result = await tts.generate_audio(request)
    return result.file_path if result.success else None
    """
    )


if __name__ == "__main__":
    main()
