# Basic Usage Examples

This guide covers the fundamental usage patterns of the Audio Generation Library. Perfect for getting started with simple text-to-speech generation.

## 🎵 Simple Text-to-Speech

### Minimal Example

```python
import asyncio
from audio_api import AudioRequest, TTSService

async def simple_tts():
    # Create the service
    tts = TTSService()
    
    # Create a basic request
    request = AudioRequest(text="Hello, this is a simple text-to-speech example.")
    
    # Generate audio
    result = await tts.generate_audio(request)
    
    # Check result
    if result.success:
        print(f"✅ Audio saved to: {result.file_path}")
        print(f"⏱️  Duration: {result.duration:.2f} seconds")
    else:
        print(f"❌ Error: {result.error}")

# Run it
asyncio.run(simple_tts())
```

### With Custom Filename

```python
async def custom_filename():
    tts = TTSService()
    
    request = AudioRequest(
        text="This audio file has a custom name.",
        output_filename="my_custom_audio.wav"
    )
    
    result = await tts.generate_audio(request)
    if result.success:
        print(f"✅ Saved as: {result.file_path}")

asyncio.run(custom_filename())
```

## 🎛️ Basic Voice Customization

### Using Different Voices

```python
from audio_api import AudioRequest, TTSService, VoiceName

async def different_voices():
    tts = TTSService()
    
    # Default voice (Kore - Firm)
    request1 = AudioRequest(
        text="This is the default firm voice.",
        output_filename="default_voice.wav"
    )
    
    # Warm voice
    request2 = AudioRequest(
        text="This is a warm, friendly voice.",
        voice_config={"voice_name": VoiceName.SULAFAR},
        output_filename="warm_voice.wav"
    )
    
    # Bright voice
    request3 = AudioRequest(
        text="This is a bright, energetic voice.",
        voice_config={"voice_name": VoiceName.ZEPHYR},
        output_filename="bright_voice.wav"
    )
    
    # Generate all three
    for request in [request1, request2, request3]:
        result = await tts.generate_audio(request)
        if result.success:
            print(f"✅ Generated: {result.file_path}")

asyncio.run(different_voices())
```

### Adjusting Speed and Pitch

```python
async def speed_and_pitch():
    tts = TTSService()
    
    # Slow and low
    slow_request = AudioRequest(
        text="This is spoken slowly with a lower pitch.",
        voice_config={
            "voice_name": VoiceName.KORE,
            "speed": 0.7,  # Slower
            "pitch": 0.8   # Lower
        },
        output_filename="slow_low.wav"
    )
    
    # Fast and high
    fast_request = AudioRequest(
        text="This is spoken quickly with a higher pitch.",
        voice_config={
            "voice_name": VoiceName.PUCK,
            "speed": 1.5,  # Faster
            "pitch": 1.3   # Higher
        },
        output_filename="fast_high.wav"
    )
    
    for request in [slow_request, fast_request]:
        result = await tts.generate_audio(request)
        if result.success:
            print(f"✅ Generated: {result.file_path}")

asyncio.run(speed_and_pitch())
```

## 🌍 Basic Multi-Language

### Simple Language Examples

```python
from audio_api import AudioRequest, TTSService, Language

async def basic_languages():
    tts = TTSService()
    
    # English
    english = AudioRequest(
        text="Hello, welcome to our service!",
        language=Language.ENGLISH_US,
        output_filename="welcome_english.wav"
    )
    
    # Spanish
    spanish = AudioRequest(
        text="¡Hola, bienvenido a nuestro servicio!",
        language=Language.SPANISH_US,
        output_filename="welcome_spanish.wav"
    )
    
    # French
    french = AudioRequest(
        text="Bonjour, bienvenue dans notre service!",
        language=Language.FRENCH_FRANCE,
        output_filename="welcome_french.wav"
    )
    
    for request in [english, spanish, french]:
        result = await tts.generate_audio(request)
        if result.success:
            print(f"✅ Generated: {result.file_path}")

asyncio.run(basic_languages())
```

## 📝 Working with Different Text Types

### Short Messages

```python
async def short_messages():
    tts = TTSService()
    
    messages = [
        "Hello!",
        "Thank you.",
        "Please wait.",
        "Your order is ready.",
        "Have a great day!"
    ]
    
    for i, message in enumerate(messages, 1):
        request = AudioRequest(
            text=message,
            output_filename=f"message_{i:02d}.wav"
        )
        
        result = await tts.generate_audio(request)
        if result.success:
            print(f"✅ Message {i}: {result.file_path}")

asyncio.run(short_messages())
```

### Longer Content

```python
async def longer_content():
    tts = TTSService()
    
    long_text = """
    Welcome to our comprehensive audio generation service. 
    We provide high-quality text-to-speech conversion using 
    advanced artificial intelligence technology. Our system 
    supports multiple languages and voice options to meet 
    your diverse needs. Whether you're creating educational 
    content, business presentations, or personal projects, 
    we're here to help you bring your text to life with 
    natural-sounding speech.
    """
    
    request = AudioRequest(
        text=long_text.strip(),
        voice_config={"voice_name": VoiceName.CHARON},  # Informative voice
        output_filename="long_content.wav"
    )
    
    result = await tts.generate_audio(request)
    if result.success:
        print(f"✅ Long content: {result.file_path}")
        print(f"⏱️  Duration: {result.duration:.2f} seconds")

asyncio.run(longer_content())
```

### Numbers and Special Characters

```python
async def numbers_and_special():
    tts = TTSService()
    
    examples = [
        "The price is $29.99 plus tax.",
        "Call us at 1-800-555-0123.",
        "Visit our website at www.example.com.",
        "The meeting is at 3:30 PM on March 15th, 2024.",
        "Use code SAVE20 for 20% off your order.",
    ]
    
    for i, text in enumerate(examples, 1):
        request = AudioRequest(
            text=text,
            output_filename=f"special_{i:02d}.wav"
        )
        
        result = await tts.generate_audio(request)
        if result.success:
            print(f"✅ Special text {i}: {result.file_path}")

asyncio.run(numbers_and_special())
```

## 🔄 Error Handling Basics

### Simple Error Handling

```python
async def basic_error_handling():
    tts = TTSService()
    
    # This might fail if API key is missing
    request = AudioRequest(text="Test message")
    
    result = await tts.generate_audio(request)
    
    if result.success:
        print(f"✅ Success: {result.file_path}")
        print(f"📝 Message: {result.message}")
        if result.duration:
            print(f"⏱️  Duration: {result.duration:.2f}s")
    else:
        print(f"❌ Failed: {result.error}")
        print(f"📝 Message: {result.message}")

asyncio.run(basic_error_handling())
```

### Handling Multiple Requests

```python
async def multiple_requests_with_errors():
    tts = TTSService()
    
    requests = [
        AudioRequest(text="First message", output_filename="msg1.wav"),
        AudioRequest(text="Second message", output_filename="msg2.wav"),
        AudioRequest(text="Third message", output_filename="msg3.wav"),
    ]
    
    successful = 0
    failed = 0
    
    for i, request in enumerate(requests, 1):
        result = await tts.generate_audio(request)
        
        if result.success:
            print(f"✅ Request {i}: {result.file_path}")
            successful += 1
        else:
            print(f"❌ Request {i} failed: {result.error}")
            failed += 1
    
    print(f"\n📊 Summary: {successful} successful, {failed} failed")

asyncio.run(multiple_requests_with_errors())
```

## 📁 File Management

### Organizing Output Files

```python
import os
from datetime import datetime

async def organized_output():
    tts = TTSService()
    
    # Create timestamp for organization
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Different categories
    categories = {
        "greetings": [
            "Hello and welcome!",
            "Good morning!",
            "Thank you for visiting!"
        ],
        "announcements": [
            "Attention please.",
            "Important update.",
            "System maintenance scheduled."
        ],
        "farewells": [
            "Goodbye!",
            "See you later!",
            "Have a wonderful day!"
        ]
    }
    
    for category, messages in categories.items():
        for i, message in enumerate(messages, 1):
            filename = f"{timestamp}_{category}_{i:02d}.wav"
            
            request = AudioRequest(
                text=message,
                output_filename=filename
            )
            
            result = await tts.generate_audio(request)
            if result.success:
                print(f"✅ {category.title()} {i}: {result.file_path}")

asyncio.run(organized_output())
```

### Checking File Properties

```python
import os

async def file_properties():
    tts = TTSService()
    
    request = AudioRequest(
        text="This is a test file to check properties.",
        output_filename="test_properties.wav"
    )
    
    result = await tts.generate_audio(request)
    
    if result.success:
        file_path = result.file_path
        file_size = os.path.getsize(file_path)
        
        print(f"✅ File created: {file_path}")
        print(f"📁 File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
        print(f"⏱️  Duration: {result.duration:.2f} seconds")
        print(f"📊 Quality: 24kHz, 16-bit, Mono WAV")

asyncio.run(file_properties())
```

## 🎯 Common Use Cases

### Notification Messages

```python
async def notification_messages():
    tts = TTSService()
    
    notifications = [
        ("info", "You have a new message.", VoiceName.CHARON),
        ("success", "Operation completed successfully!", VoiceName.PUCK),
        ("warning", "Please check your input.", VoiceName.KORE),
        ("error", "An error occurred. Please try again.", VoiceName.ACHERNAR),
    ]
    
    for msg_type, text, voice in notifications:
        request = AudioRequest(
            text=text,
            voice_config={"voice_name": voice},
            output_filename=f"notification_{msg_type}.wav"
        )
        
        result = await tts.generate_audio(request)
        if result.success:
            print(f"✅ {msg_type.title()} notification: {result.file_path}")

asyncio.run(notification_messages())
```

### Menu Options

```python
async def menu_options():
    tts = TTSService()
    
    menu_items = [
        "Press 1 for customer service.",
        "Press 2 for technical support.",
        "Press 3 for billing inquiries.",
        "Press 4 to speak with a manager.",
        "Press 0 to repeat this menu.",
    ]
    
    # Generate menu intro
    intro = AudioRequest(
        text="Welcome to our customer service line. Please select from the following options:",
        voice_config={"voice_name": VoiceName.SULAFAR},
        output_filename="menu_intro.wav"
    )
    
    result = await tts.generate_audio(intro)
    if result.success:
        print(f"✅ Menu intro: {result.file_path}")
    
    # Generate each option
    for i, option in enumerate(menu_items, 1):
        request = AudioRequest(
            text=option,
            voice_config={"voice_name": VoiceName.CHARON},
            output_filename=f"menu_option_{i}.wav"
        )
        
        result = await tts.generate_audio(request)
        if result.success:
            print(f"✅ Option {i}: {result.file_path}")

asyncio.run(menu_options())
```

### Educational Content

```python
async def educational_content():
    tts = TTSService()
    
    lessons = [
        ("intro", "Welcome to today's lesson on renewable energy."),
        ("definition", "Renewable energy comes from natural sources that replenish themselves."),
        ("examples", "Examples include solar power, wind energy, and hydroelectric power."),
        ("benefits", "These energy sources are clean, sustainable, and environmentally friendly."),
        ("conclusion", "Thank you for learning about renewable energy with us today."),
    ]
    
    for section, content in lessons:
        request = AudioRequest(
            text=content,
            voice_config={"voice_name": VoiceName.CHARON},  # Informative voice
            output_filename=f"lesson_{section}.wav"
        )
        
        result = await tts.generate_audio(request)
        if result.success:
            print(f"✅ Lesson {section}: {result.file_path}")

asyncio.run(educational_content())
```

## 💡 Tips for Basic Usage

### Best Practices

1. **Always Check Results**: Use `if result.success:` before accessing file paths
2. **Use Descriptive Filenames**: Make it easy to identify your audio files
3. **Choose Appropriate Voices**: Match voice characteristics to content type
4. **Handle Errors Gracefully**: Provide fallbacks for failed generations
5. **Organize Your Files**: Use consistent naming conventions

### Common Patterns

```python
# Standard pattern for single audio generation
async def standard_pattern():
    tts = TTSService()
    
    request = AudioRequest(
        text="Your text here",
        voice_config={"voice_name": VoiceName.KORE},
        output_filename="your_file.wav"
    )
    
    result = await tts.generate_audio(request)
    
    if result.success:
        print(f"✅ Success: {result.file_path}")
        return result.file_path
    else:
        print(f"❌ Error: {result.error}")
        return None

# Pattern for multiple files
async def batch_pattern():
    tts = TTSService()
    
    texts = ["First text", "Second text", "Third text"]
    results = []
    
    for i, text in enumerate(texts, 1):
        request = AudioRequest(
            text=text,
            output_filename=f"batch_{i:03d}.wav"
        )
        
        result = await tts.generate_audio(request)
        results.append(result)
        
        if result.success:
            print(f"✅ Generated {i}/{len(texts)}: {result.file_path}")
        else:
            print(f"❌ Failed {i}/{len(texts)}: {result.error}")
    
    return results
```

## 🎭 Multi-Speaker Conversations

### Basic Multi-Speaker Setup

```python
from audio_api import (
    AudioRequest, TTSService, SpeakerMode,
    MultiSpeakerConfig, SpeakerConfig, VoiceName
)

async def multi_speaker_conversation():
    tts = TTSService()
    
    # Configure two speakers
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
    
    # Create conversation
    conversation = """TTS the following conversation between Alice and Bob:
Alice: Good morning! How are you today?
Bob: I'm doing well, thank you. How about you?
Alice: I'm excited about our new project!
Bob: That's great to hear. Let's discuss the details."""
    
    request = AudioRequest(
        text=conversation,
        speaker_mode=SpeakerMode.MULTIPLE,
        multi_speaker_config=multi_speaker_config,
        output_filename="conversation.wav"
    )
    
    result = await tts.generate_audio(request)
    if result.success:
        print(f"✅ Conversation: {result.file_path}")

asyncio.run(multi_speaker_conversation())
```

### Multi-Speaker with Emotions

```python
async def emotional_conversation():
    tts = TTSService()
    
    # Use contrasting voice characteristics
    multi_speaker_config = MultiSpeakerConfig(
        speakers=[
            SpeakerConfig(
                speaker_name="Emma",
                voice_name=VoiceName.PUCK     # Upbeat
            ),
            SpeakerConfig(
                speaker_name="David",
                voice_name=VoiceName.GACRUX   # Mature
            )
        ]
    )
    
    # Add emotional direction
    emotional_text = """Make Emma sound excited and David sound calm:

Emma: Oh wow! This is incredible news!
David: Yes, it's certainly a positive development we should consider carefully.
Emma: I can't wait to get started on this!
David: Let's plan our approach thoughtfully."""
    
    request = AudioRequest(
        text=emotional_text,
        speaker_mode=SpeakerMode.MULTIPLE,
        multi_speaker_config=multi_speaker_config,
        output_filename="emotional_chat.wav"
    )
    
    result = await tts.generate_audio(request)
    if result.success:
        print(f"✅ Emotional conversation: {result.file_path}")

asyncio.run(emotional_conversation())
```

### Professional vs Casual Conversations

```python
async def different_contexts():
    tts = TTSService()
    
    # Professional meeting
    professional_config = MultiSpeakerConfig(
        speakers=[
            SpeakerConfig(speaker_name="Manager", voice_name=VoiceName.KORE),      # Firm
            SpeakerConfig(speaker_name="Employee", voice_name=VoiceName.CHARON)    # Informative
        ]
    )
    
    professional_text = """TTS the following business meeting:
Manager: Let's review the quarterly results.
Employee: I'm pleased to report we exceeded targets by 15%.
Manager: Excellent work. What were the key success factors?
Employee: Team dedication and process improvements made the difference."""
    
    # Casual chat
    casual_config = MultiSpeakerConfig(
        speakers=[
            SpeakerConfig(speaker_name="Sam", voice_name=VoiceName.AOEDE),         # Breezy
            SpeakerConfig(speaker_name="Jordan", voice_name=VoiceName.CALLIRHOE)   # Easy-going
        ]
    )
    
    casual_text = """TTS the following casual conversation:
Sam: Hey! Want to grab coffee later?
Jordan: That sounds great! I could use a break.
Sam: Perfect! There's this new café downtown.
Jordan: Awesome! I love trying new places."""
    
    # Generate both
    for config, text, filename in [
        (professional_config, professional_text, "professional_meeting.wav"),
        (casual_config, casual_text, "casual_chat.wav")
    ]:
        request = AudioRequest(
            text=text,
            speaker_mode=SpeakerMode.MULTIPLE,
            multi_speaker_config=config,
            output_filename=filename
        )
        
        result = await tts.generate_audio(request)
        if result.success:
            print(f"✅ Generated: {result.file_path}")

asyncio.run(different_contexts())
```

## 🎛️ Enhanced Voice Controls

### Speed and Pitch with Natural Language

```python
async def voice_style_controls():
    tts = TTSService()
    
    # Speed and pitch are now controlled via natural language prompts
    request = AudioRequest(
        text="This message will be spoken with custom style controls.",
        voice_config={
            "voice_name": VoiceName.SULAFAR,
            "speed": 1.3,  # Converts to "speak a bit faster"
            "pitch": 1.2   # Converts to "with a slightly higher pitch"
        },
        output_filename="styled_speech.wav"
    )
    
    result = await tts.generate_audio(request)
    if result.success:
        print(f"✅ Styled speech: {result.file_path}")

asyncio.run(voice_style_controls())
```

This covers all the basic usage patterns you'll need to get started with the Audio Generation Library, including the new multi-speaker functionality. Once you're comfortable with these examples, you can explore more advanced features like batch processing and async queues!