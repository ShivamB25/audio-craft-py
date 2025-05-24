#!/usr/bin/env python3
"""
Test script to demonstrate multi-speaker TTS functionality.
"""

import asyncio
import os
from audio_api import (
    AudioRequest, 
    TTSService, 
    VoiceName, 
    Language, 
    SpeakerMode,
    SpeakerConfig,
    MultiSpeakerConfig
)


async def test_single_speaker():
    """Test single speaker with style controls."""
    print("🎵 Testing Single Speaker TTS")
    print("=" * 40)
    
    tts = TTSService()
    
    # Test with speed and pitch controls
    request = AudioRequest(
        text="Hello! This is a test of single speaker TTS with style controls.",
        speaker_mode=SpeakerMode.SINGLE,
        voice_config={
            "voice_name": VoiceName.SULAFAR,
            "speed": 1.2,  # Slightly faster
            "pitch": 1.1   # Slightly higher
        },
        output_filename="single_speaker_styled.wav"
    )
    
    result = await tts.generate_audio(request)
    if result.success:
        print(f"✅ Single speaker with style: {result.file_path}")
    else:
        print(f"❌ Failed: {result.error}")


async def test_multi_speaker():
    """Test multi-speaker TTS functionality."""
    print("\n🎭 Testing Multi-Speaker TTS")
    print("=" * 40)
    
    tts = TTSService()
    
    # Create multi-speaker configuration
    multi_speaker_config = MultiSpeakerConfig(
        speakers=[
            SpeakerConfig(
                speaker_name="Alice",
                voice_name=VoiceName.SULAFAR  # Warm voice
            ),
            SpeakerConfig(
                speaker_name="Bob", 
                voice_name=VoiceName.KORE     # Firm voice
            )
        ]
    )
    
    # Multi-speaker conversation
    conversation_text = """TTS the following conversation between Alice and Bob:
Alice: Good morning Bob! How are you feeling today?
Bob: I'm doing well, thank you Alice. How about you?
Alice: I'm excited about our new project! It's going to be amazing.
Bob: I agree. Let's make sure we deliver excellent results."""
    
    request = AudioRequest(
        text=conversation_text,
        speaker_mode=SpeakerMode.MULTIPLE,
        multi_speaker_config=multi_speaker_config,
        language=Language.ENGLISH_US,
        output_filename="multi_speaker_conversation.wav"
    )
    
    result = await tts.generate_audio(request)
    if result.success:
        print(f"✅ Multi-speaker conversation: {result.file_path}")
    else:
        print(f"❌ Failed: {result.error}")


async def test_multi_speaker_with_emotions():
    """Test multi-speaker with emotional styles."""
    print("\n🎭 Testing Multi-Speaker with Emotions")
    print("=" * 45)
    
    tts = TTSService()
    
    # Create configuration with contrasting voices
    multi_speaker_config = MultiSpeakerConfig(
        speakers=[
            SpeakerConfig(
                speaker_name="Emma",
                voice_name=VoiceName.PUCK  # Upbeat voice
            ),
            SpeakerConfig(
                speaker_name="David",
                voice_name=VoiceName.GACRUX  # Mature voice
            )
        ]
    )
    
    # Emotional conversation
    emotional_text = """Make Emma sound excited and happy, and David sound calm and wise:

Emma: Oh wow! Did you hear the amazing news about our project?
David: Yes, I did. It's certainly a positive development that we should approach thoughtfully.
Emma: I can't believe how well everything is working out! This is incredible!
David: Indeed, it's important to celebrate our successes while maintaining our focus on quality."""
    
    request = AudioRequest(
        text=emotional_text,
        speaker_mode=SpeakerMode.MULTIPLE,
        multi_speaker_config=multi_speaker_config,
        output_filename="emotional_conversation.wav"
    )
    
    result = await tts.generate_audio(request)
    if result.success:
        print(f"✅ Emotional conversation: {result.file_path}")
    else:
        print(f"❌ Failed: {result.error}")


async def test_different_voice_combinations():
    """Test different voice combinations for multi-speaker."""
    print("\n🎨 Testing Different Voice Combinations")
    print("=" * 45)
    
    tts = TTSService()
    
    # Test different voice pairings
    voice_combinations = [
        {
            "name": "Professional Meeting",
            "speakers": [
                SpeakerConfig(speaker_name="Manager", voice_name=VoiceName.KORE),      # Firm
                SpeakerConfig(speaker_name="Employee", voice_name=VoiceName.ACHIRD)    # Friendly
            ],
            "text": """TTS the following professional conversation:
Manager: Let's review the quarterly results and discuss our next steps.
Employee: Absolutely! I'm pleased to report that we exceeded our targets by 15%.
Manager: Excellent work. What factors contributed to this success?
Employee: Our team's dedication and the new process improvements made a significant difference."""
        },
        {
            "name": "Casual Chat",
            "speakers": [
                SpeakerConfig(speaker_name="Sam", voice_name=VoiceName.AOEDE),         # Breezy
                SpeakerConfig(speaker_name="Jordan", voice_name=VoiceName.CALLIRHOE)   # Easy-going
            ],
            "text": """TTS the following casual conversation:
Sam: Hey Jordan! Want to grab some coffee later?
Jordan: That sounds great! I could use a break from work.
Sam: Perfect! There's this new café downtown that everyone's talking about.
Jordan: Awesome! I love trying new places. What time works for you?"""
        }
    ]
    
    for combo in voice_combinations:
        print(f"\n🎯 Testing: {combo['name']}")
        
        multi_speaker_config = MultiSpeakerConfig(speakers=combo['speakers'])
        
        request = AudioRequest(
            text=combo['text'],
            speaker_mode=SpeakerMode.MULTIPLE,
            multi_speaker_config=multi_speaker_config,
            output_filename=f"combo_{combo['name'].lower().replace(' ', '_')}.wav"
        )
        
        result = await tts.generate_audio(request)
        if result.success:
            print(f"   ✅ Generated: {result.file_path}")
        else:
            print(f"   ❌ Failed: {result.error}")


async def demonstrate_usage_patterns():
    """Demonstrate different usage patterns."""
    print("\n💡 Usage Pattern Examples")
    print("=" * 30)
    
    examples = [
        """
# Single Speaker with Style
from audio_api import AudioRequest, TTSService, VoiceName, SpeakerMode

request = AudioRequest(
    text="Welcome to our service!",
    speaker_mode=SpeakerMode.SINGLE,
    voice_config={
        "voice_name": VoiceName.SULAFAR,
        "speed": 1.1,  # Slightly faster
        "pitch": 1.0   # Normal pitch
    }
)
        """,
        """
# Multi-Speaker Conversation
from audio_api import (
    AudioRequest, SpeakerMode, MultiSpeakerConfig, 
    SpeakerConfig, VoiceName
)

multi_speaker_config = MultiSpeakerConfig(
    speakers=[
        SpeakerConfig(speaker_name="Host", voice_name=VoiceName.CHARON),
        SpeakerConfig(speaker_name="Guest", voice_name=VoiceName.SULAFAR)
    ]
)

request = AudioRequest(
    text="Host: Welcome to our podcast! Guest: Thank you for having me!",
    speaker_mode=SpeakerMode.MULTIPLE,
    multi_speaker_config=multi_speaker_config
)
        """,
        """
# Emotional Multi-Speaker
conversation = '''Make Speaker1 sound tired and Speaker2 sound excited:

Speaker1: So... what's on the agenda today?
Speaker2: You're never going to guess what happened!'''

request = AudioRequest(
    text=conversation,
    speaker_mode=SpeakerMode.MULTIPLE,
    multi_speaker_config=MultiSpeakerConfig(
        speakers=[
            SpeakerConfig(speaker_name="Speaker1", voice_name=VoiceName.ENCELADUS),  # Breathy
            SpeakerConfig(speaker_name="Speaker2", voice_name=VoiceName.FENRIR)      # Excitable
        ]
    )
)
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
    
    print("🎵 Multi-Speaker TTS Test Suite")
    print("=" * 50)
    
    try:
        # Test single speaker with style
        await test_single_speaker()
        
        # Test basic multi-speaker
        await test_multi_speaker()
        
        # Test multi-speaker with emotions
        await test_multi_speaker_with_emotions()
        
        # Test different voice combinations
        await test_different_voice_combinations()
        
        # Show usage examples
        await demonstrate_usage_patterns()
        
        print(f"\n✅ Multi-speaker TTS tests completed!")
        print(f"   📁 Audio files saved in: output/")
        print(f"   🎧 Listen to the files to hear the different speakers and styles")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())