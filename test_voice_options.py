#!/usr/bin/env python3
"""
Test script to demonstrate all 30 voice options available in the audio generation library.
"""

import asyncio
import os
from audio_api import AudioRequest, TTSService, VoiceName, Language


async def test_voice_options():
    """Test a selection of voice options to demonstrate functionality."""
    
    # Initialize TTS service
    tts = TTSService()
    
    # Test text
    test_text = "Hello, this is a test of the voice generation system."
    
    # Test a variety of voice characteristics
    test_voices = [
        (VoiceName.KORE, "Firm (default)"),
        (VoiceName.ZEPHYR, "Bright"),
        (VoiceName.PUCK, "Upbeat"),
        (VoiceName.CHARON, "Informative"),
        (VoiceName.AOEDE, "Breezy"),
        (VoiceName.FENRIR, "Excitable"),
        (VoiceName.ACHERNAR, "Soft"),
        (VoiceName.GACRUX, "Mature"),
        (VoiceName.SULAFAR, "Warm"),
        (VoiceName.VINDEMIATRIX, "Gentle"),
    ]
    
    print("🎵 Testing Voice Options")
    print("=" * 50)
    
    for voice, description in test_voices:
        print(f"\n🎤 Testing {voice.value} ({description})")
        
        # Create request with specific voice
        request = AudioRequest(
            text=test_text,
            language=Language.ENGLISH,
            voice_config={
                "voice_name": voice,
                "speed": 1.0,
                "pitch": 1.0
            },
            output_filename=f"voice_test_{voice.value.lower()}"
        )
        
        # Generate audio
        result = await tts.generate_audio(request)
        
        if result.success:
            print(f"   ✅ Generated: {result.file_path}")
            if result.duration:
                print(f"   ⏱️  Duration: {result.duration:.2f}s")
        else:
            print(f"   ❌ Failed: {result.error}")
    
    print(f"\n📋 All Available Voices ({len(VoiceName)} total):")
    print("=" * 50)
    
    # Group voices by characteristic
    voice_groups = {
        "Bright": [VoiceName.ZEPHYR, VoiceName.AUTONOE],
        "Upbeat": [VoiceName.PUCK, VoiceName.LAOMEDEIA],
        "Informative": [VoiceName.CHARON, VoiceName.RASALGETHI],
        "Firm": [VoiceName.KORE, VoiceName.ORUS, VoiceName.ALNILAM],
        "Excitable": [VoiceName.FENRIR],
        "Youthful": [VoiceName.LEDA],
        "Breezy": [VoiceName.AOEDE],
        "Easy-going": [VoiceName.CALLIRHOE, VoiceName.UMBRIEL],
        "Breathy": [VoiceName.ENCELADUS],
        "Clear": [VoiceName.IAPETUS, VoiceName.ERINOME],
        "Smooth": [VoiceName.ALGIEBA, VoiceName.DESPINA],
        "Gravelly": [VoiceName.ALGENIB],
        "Soft": [VoiceName.ACHERNAR],
        "Even": [VoiceName.SCHEDAR],
        "Mature": [VoiceName.GACRUX],
        "Friendly": [VoiceName.ACHIRD],
        "Casual": [VoiceName.ZUBENELGENUBI],
        "Forward": [VoiceName.PULCHERRIMA],
        "Gentle": [VoiceName.VINDEMIATRIX],
        "Lively": [VoiceName.SADACHBIA],
        "Knowledgeable": [VoiceName.SADALTAGER],
        "Warm": [VoiceName.SULAFAR],
    }
    
    for characteristic, voices in voice_groups.items():
        voice_names = ", ".join([v.value for v in voices])
        print(f"   {characteristic:15}: {voice_names}")


async def demonstrate_voice_usage():
    """Demonstrate how to use different voices in code."""
    
    print("\n💻 Code Usage Examples")
    print("=" * 50)
    
    examples = [
        """
# Basic usage with default voice (Kore - Firm)
from audio_api import AudioRequest, TTSService

request = AudioRequest(text="Hello world")
tts = TTSService()
result = await tts.generate_audio(request)
        """,
        """
# Using a specific voice
from audio_api import AudioRequest, TTSService, VoiceName

request = AudioRequest(
    text="This is a warm, friendly voice",
    voice_config={
        "voice_name": VoiceName.SULAFAR,  # Warm voice
        "speed": 1.2,
        "pitch": 1.1
    }
)
        """,
        """
# All available voice characteristics:
# Bright: Zephyr, Autonoe
# Upbeat: Puck, Laomedeia  
# Informative: Charon, Rasalgethi
# Firm: Kore (default), Orus, Alnilam
# Excitable: Fenrir
# Youthful: Leda
# Breezy: Aoede
# Easy-going: Callirhoe, Umbriel
# Breathy: Enceladus
# Clear: Iapetus, Erinome
# Smooth: Algieba, Despina
# Gravelly: Algenib
# Soft: Achernar
# Even: Schedar
# Mature: Gacrux
# Friendly: Achird
# Casual: Zubenelgenubi
# Forward: Pulcherrima
# Gentle: Vindemiatrix
# Lively: Sadachbia
# Knowledgeable: Sadaltager
# Warm: Sulafar
        """
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\nExample {i}:")
        print(example.strip())


async def main():
    """Main test function."""
    
    # Check if API key is available
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY not found in environment variables")
        print("   Please set your API key in .env file or environment")
        return
    
    print("🎵 Audio Generation Library - Voice Options Test")
    print("=" * 60)
    
    try:
        await test_voice_options()
        await demonstrate_voice_usage()
        
        print(f"\n✅ Voice options test completed!")
        print(f"   📁 Audio files saved in: output/")
        print(f"   🎧 You can listen to the generated audio files to hear the differences")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())