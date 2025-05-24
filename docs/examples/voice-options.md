# Voice Options Guide

The Audio Generation Library supports 30 different voice options, each with unique characteristics. This guide shows you how to use them effectively.

## 🎭 All Available Voices

### Bright Voices
Perfect for energetic, uplifting content.

```python
from audio_api import AudioRequest, TTSService, VoiceName

# Bright and energetic
request = AudioRequest(
    text="Welcome to our exciting new product launch!",
    voice_config={"voice_name": VoiceName.ZEPHYR}  # Bright
)

# Bright and clear
request = AudioRequest(
    text="Today's weather forecast is sunny and bright!",
    voice_config={"voice_name": VoiceName.AUTONOE}  # Bright
)
```

### Upbeat Voices
Great for cheerful, positive content.

```python
# Cheerful and upbeat
request = AudioRequest(
    text="Congratulations on your achievement!",
    voice_config={"voice_name": VoiceName.PUCK}  # Upbeat
)

# Enthusiastic and upbeat
request = AudioRequest(
    text="Let's get started with today's fun activities!",
    voice_config={"voice_name": VoiceName.LAOMEDEIA}  # Upbeat
)
```

### Informative Voices
Ideal for educational and instructional content.

```python
# Clear and informative
request = AudioRequest(
    text="In this tutorial, we'll learn about machine learning basics.",
    voice_config={"voice_name": VoiceName.CHARON}  # Informative
)

# Professional and informative
request = AudioRequest(
    text="The quarterly report shows significant growth in all sectors.",
    voice_config={"voice_name": VoiceName.RASALGETHI}  # Informative
)
```

### Firm Voices
Perfect for authoritative, professional content.

```python
# Default firm voice
request = AudioRequest(
    text="Please follow the safety guidelines at all times.",
    voice_config={"voice_name": VoiceName.KORE}  # Firm (default)
)

# Strong and firm
request = AudioRequest(
    text="The deadline for submissions is tomorrow at 5 PM.",
    voice_config={"voice_name": VoiceName.ORUS}  # Firm
)

# Confident and firm
request = AudioRequest(
    text="We are committed to delivering excellence in every project.",
    voice_config={"voice_name": VoiceName.ALNILAM}  # Firm
)
```

### Warm and Friendly Voices
Great for welcoming, personal content.

```python
# Warm and welcoming
request = AudioRequest(
    text="Thank you for choosing our service. We're here to help!",
    voice_config={"voice_name": VoiceName.SULAFAR}  # Warm
)

# Friendly and approachable
request = AudioRequest(
    text="Hi there! How can I assist you today?",
    voice_config={"voice_name": VoiceName.ACHIRD}  # Friendly
)
```

### Gentle and Soft Voices
Perfect for calming, soothing content.

```python
# Soft and gentle
request = AudioRequest(
    text="Take a deep breath and relax. Everything will be okay.",
    voice_config={"voice_name": VoiceName.ACHERNAR}  # Soft
)

# Gentle and caring
request = AudioRequest(
    text="Remember to take care of yourself and get enough rest.",
    voice_config={"voice_name": VoiceName.VINDEMIATRIX}  # Gentle
)
```

## 🎯 Voice Selection Guide

### By Content Type

**Educational Content**
```python
# Use informative voices
voices = [VoiceName.CHARON, VoiceName.RASALGETHI]
```

**Marketing Content**
```python
# Use bright or upbeat voices
voices = [VoiceName.ZEPHYR, VoiceName.PUCK, VoiceName.LAOMEDEIA]
```

**Professional Announcements**
```python
# Use firm or even voices
voices = [VoiceName.KORE, VoiceName.ORUS, VoiceName.SCHEDAR]
```

**Customer Service**
```python
# Use warm or friendly voices
voices = [VoiceName.SULAFAR, VoiceName.ACHIRD, VoiceName.CALLIRHOE]
```

**Meditation/Relaxation**
```python
# Use soft or gentle voices
voices = [VoiceName.ACHERNAR, VoiceName.VINDEMIATRIX]
```

## 🎛️ Complete Voice Reference

### All 30 Voices with Characteristics

```python
import asyncio
from audio_api import AudioRequest, TTSService, VoiceName

async def demonstrate_all_voices():
    tts = TTSService()
    
    # Complete voice catalog
    voice_catalog = {
        # Bright Voices
        VoiceName.ZEPHYR: "Bright and energetic voice",
        VoiceName.AUTONOE: "Bright and clear voice",
        
        # Upbeat Voices
        VoiceName.PUCK: "Upbeat and cheerful voice",
        VoiceName.LAOMEDEIA: "Upbeat and enthusiastic voice",
        
        # Informative Voices
        VoiceName.CHARON: "Informative and educational voice",
        VoiceName.RASALGETHI: "Informative and professional voice",
        
        # Firm Voices
        VoiceName.KORE: "Firm and authoritative voice (default)",
        VoiceName.ORUS: "Firm and strong voice",
        VoiceName.ALNILAM: "Firm and confident voice",
        
        # Excitable Voices
        VoiceName.FENRIR: "Excitable and dynamic voice",
        
        # Youthful Voices
        VoiceName.LEDA: "Youthful and fresh voice",
        
        # Breezy Voices
        VoiceName.AOEDE: "Breezy and light voice",
        
        # Easy-going Voices
        VoiceName.CALLIRHOE: "Easy-going and relaxed voice",
        VoiceName.UMBRIEL: "Easy-going and casual voice",
        
        # Breathy Voices
        VoiceName.ENCELADUS: "Breathy and intimate voice",
        
        # Clear Voices
        VoiceName.IAPETUS: "Clear and crisp voice",
        VoiceName.ERINOME: "Clear and articulate voice",
        
        # Smooth Voices
        VoiceName.ALGIEBA: "Smooth and polished voice",
        VoiceName.DESPINA: "Smooth and flowing voice",
        
        # Gravelly Voices
        VoiceName.ALGENIB: "Gravelly and textured voice",
        
        # Soft Voices
        VoiceName.ACHERNAR: "Soft and gentle voice",
        
        # Even Voices
        VoiceName.SCHEDAR: "Even and balanced voice",
        
        # Mature Voices
        VoiceName.GACRUX: "Mature and experienced voice",
        
        # Friendly Voices
        VoiceName.ACHIRD: "Friendly and approachable voice",
        
        # Casual Voices
        VoiceName.ZUBENELGENUBI: "Casual and conversational voice",
        
        # Forward Voices
        VoiceName.PULCHERRIMA: "Forward and assertive voice",
        
        # Gentle Voices
        VoiceName.VINDEMIATRIX: "Gentle and caring voice",
        
        # Lively Voices
        VoiceName.SADACHBIA: "Lively and animated voice",
        
        # Knowledgeable Voices
        VoiceName.SADALTAGER: "Knowledgeable and wise voice",
        
        # Warm Voices
        VoiceName.SULAFAR: "Warm and welcoming voice",
    }
    
    # Generate sample for each voice
    for voice, description in voice_catalog.items():
        request = AudioRequest(
            text=f"Hello, this is {description}",
            voice_config={"voice_name": voice},
            output_filename=f"voice_demo_{voice.value.lower()}.wav"
        )
        
        result = await tts.generate_audio(request)
        if result.success:
            print(f"✅ {voice.value:15} - {description}")
        else:
            print(f"❌ {voice.value:15} - Failed: {result.error}")

# Run the demonstration
asyncio.run(demonstrate_all_voices())
```

## 🎨 Advanced Voice Customization

### Combining Voice with Speed and Pitch

```python
async def advanced_voice_config():
    tts = TTSService()
    
    # Slow, deep, authoritative voice
    request = AudioRequest(
        text="This is an important announcement.",
        voice_config={
            "voice_name": VoiceName.GACRUX,  # Mature
            "speed": 0.8,                    # Slower
            "pitch": 0.9                     # Lower pitch
        }
    )
    
    # Fast, high, energetic voice
    request = AudioRequest(
        text="Exciting news! Limited time offer!",
        voice_config={
            "voice_name": VoiceName.FENRIR,  # Excitable
            "speed": 1.4,                    # Faster
            "pitch": 1.3                     # Higher pitch
        }
    )
```

### Voice Pairing Recommendations

```python
# Content-specific voice recommendations
voice_recommendations = {
    "podcast_intro": VoiceName.SULAFAR,      # Warm
    "tutorial": VoiceName.CHARON,            # Informative
    "advertisement": VoiceName.ZEPHYR,       # Bright
    "audiobook": VoiceName.SCHEDAR,          # Even
    "meditation": VoiceName.ACHERNAR,        # Soft
    "news": VoiceName.RASALGETHI,            # Informative
    "children_story": VoiceName.LEDA,        # Youthful
    "business_presentation": VoiceName.KORE,  # Firm
    "customer_service": VoiceName.ACHIRD,    # Friendly
    "sports_commentary": VoiceName.FENRIR,   # Excitable
}
```

## 🎵 Testing Voice Options

Use the provided test script to hear all voices:

```bash
python test_voice_options.py
```

This will generate sample audio files for different voice characteristics, allowing you to hear the differences and choose the best voice for your needs.

## 💡 Pro Tips

1. **Match Voice to Content**: Choose voices that complement your content's tone and purpose
2. **Test Before Production**: Generate samples with different voices to find the perfect match
3. **Consider Your Audience**: Younger audiences might prefer upbeat voices, while professional content benefits from firm or informative voices
4. **Combine with Speed/Pitch**: Fine-tune the voice further with speed and pitch adjustments
5. **Consistency**: Use the same voice throughout a project for consistency

## 🔄 Voice Switching Example

```python
async def dynamic_voice_content():
    """Example showing different voices for different parts of content."""
    tts = TTSService()
    
    # Introduction - Warm and welcoming
    intro = AudioRequest(
        text="Welcome to our audio guide!",
        voice_config={"voice_name": VoiceName.SULAFAR},
        output_filename="01_intro.wav"
    )
    
    # Main content - Clear and informative
    content = AudioRequest(
        text="In this section, we'll cover the key concepts.",
        voice_config={"voice_name": VoiceName.CHARON},
        output_filename="02_content.wav"
    )
    
    # Conclusion - Bright and positive
    conclusion = AudioRequest(
        text="Thank you for listening! We hope this was helpful.",
        voice_config={"voice_name": VoiceName.ZEPHYR},
        output_filename="03_conclusion.wav"
    )
    
    # Generate all parts
    for request in [intro, content, conclusion]:
        result = await tts.generate_audio(request)
        if result.success:
            print(f"✅ Generated: {result.file_path}")

asyncio.run(dynamic_voice_content())
```

This approach allows you to create more engaging content by using different voices for different purposes within the same project.