# Audio Generation Library

A simple, powerful Python library for text-to-speech generation using Google Gemini TTS. Generate high-quality WAV audio files (24kHz, 16-bit PCM) with support for multiple languages and async processing.

## Features

- 🎵 **High-Quality Audio**: WAV output (24kHz, 16-bit PCM)
- 🌍 **Multi-language Support**: 24 languages supported with proper BCP-47 codes
- 🎭 **Voice Customization**: 30 voice options with speed and pitch control
- 👥 **Multi-Speaker TTS**: Support for conversations between 2 speakers with different voices
- � **Async Processing**: Non-blocking audio generation
- 📦 **Simple API**: Easy-to-use Python library
- 🚀 **Fast**: Efficient processing with Google Gemini TTS

## Installation

1. **Install dependencies**:
   ```bash
   uv sync
   # or
   pip install -r requirements.txt
   ```

2. **Set up your API key**:
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

## Quick Start

```python
import asyncio
from audio_api import AudioRequest, TTSService, Language

async def generate_audio():
    # Create TTS service
    tts = TTSService()
    
    # Create request
    request = AudioRequest(
        text="Hello, this is a test of the audio generation library!",
        language=Language.ENGLISH,
        output_filename="hello.wav"
    )
    
    # Generate audio
    result = await tts.generate_audio(request)
    
    if result.success:
        print(f"Audio saved to: {result.file_path}")
    else:
        print(f"Error: {result.error}")

# Run the example
asyncio.run(generate_audio())
```

## Usage Examples

### Basic Usage

```python
from audio_api import AudioRequest, TTSService

async def simple_example():
    tts = TTSService()
    
    request = AudioRequest(
        text="Your text here",
        output_filename="output.wav"
    )
    
    result = await tts.generate_audio(request)
    return result.file_path if result.success else None
```

### Multi-Language Support (24 Languages)

```python
from audio_api import AudioRequest, TTSService, Language

async def multi_language():
    tts = TTSService()
    
    # Examples from the 24 supported languages
    languages = [
        (Language.ENGLISH_US, "Hello, world!"),
        (Language.SPANISH_US, "¡Hola, mundo!"),
        (Language.FRENCH_FRANCE, "Bonjour, le monde!"),
        (Language.HINDI_INDIA, "नमस्ते दुनिया!"),
        (Language.JAPANESE_JAPAN, "こんにちは世界！"),
        (Language.ARABIC_EGYPTIAN, "مرحبا بالعالم!"),
    ]
    
    for lang, text in languages:
        request = AudioRequest(
            text=text,
            language=lang,
            output_filename=f"hello_{lang.value.replace('-', '_')}.wav"
        )
        
        result = await tts.generate_audio(request)
        print(f"{lang.name}: {result.file_path}")
```

### Custom Voice Configuration

```python
from audio_api import AudioRequest, TTSService, VoiceName, VoiceConfig, AudioFormat

async def custom_voice():
    tts = TTSService()
    
    # Custom voice settings with specific voice
    voice_config = VoiceConfig(
        voice_name=VoiceName.SULAFAR,  # Warm voice
        speed=1.2,                     # 0.1 to 3.0
        pitch=1.1                      # 0.1 to 2.0
    )
    
    # Custom audio format
    audio_format = AudioFormat(
        sample_rate=24000,   # 24kHz
        bit_depth=16,        # 16-bit
        channels=1           # Mono
    )
    
    request = AudioRequest(
        text="This uses a warm, friendly voice",
        voice_config=voice_config,
        audio_format=audio_format,
        output_filename="custom.wav"
    )
    
    result = await tts.generate_audio(request)
    return result
```

### Voice Characteristics Examples

```python
from audio_api import AudioRequest, TTSService, VoiceName

async def voice_examples():
    tts = TTSService()
    
    # Different voice characteristics
    voice_examples = [
        (VoiceName.KORE, "This is the default firm voice"),
        (VoiceName.ZEPHYR, "This is a bright, energetic voice"),
        (VoiceName.PUCK, "This is an upbeat, cheerful voice"),
        (VoiceName.ACHERNAR, "This is a soft, gentle voice"),
        (VoiceName.GACRUX, "This is a mature, experienced voice"),
        (VoiceName.SULAFAR, "This is a warm, friendly voice"),
    ]
    
    for voice, text in voice_examples:
        request = AudioRequest(
            text=text,
            voice_config={"voice_name": voice},
            output_filename=f"example_{voice.value.lower()}.wav"
        )
        
        result = await tts.generate_audio(request)
        print(f"{voice.value}: {result.file_path}")
```

### Batch Processing

```python
async def batch_processing():
    tts = TTSService()
    
    texts = [
        "First audio file",
        "Second audio file", 
        "Third audio file"
    ]
    
    results = []
    for i, text in enumerate(texts):
        request = AudioRequest(
            text=text,
            output_filename=f"batch_{i+1}.wav"
        )
        
        result = await tts.generate_audio(request)
        results.append(result)
    
    return results
```

### Multi-Speaker TTS Examples

```python
from audio_api import (
    AudioRequest,
    TTSService,
    Language,
    VoiceName,
    SpeakerMode,
    MultiSpeakerConfig,
    SpeakerConfig,
)

async def multi_speaker_example():
    tts = TTSService()

    # Example 1: Professional Conversation
    speaker1_prof = SpeakerConfig(name="Speaker1", voice_name=VoiceName.KORE)  # Firm voice
    speaker2_prof = SpeakerConfig(name="Speaker2", voice_name=VoiceName.CHARON) # Informative voice
    
    multi_config_prof = MultiSpeakerConfig(
        speakers=[speaker1_prof, speaker2_prof]
    )

    request_prof = AudioRequest(
        text=(
            "Speaker1: Good morning, team. Let's discuss the quarterly results. "
            "Speaker2: Agreed. I have the reports ready for review."
        ),
        language=Language.ENGLISH_US,
        speaker_mode=SpeakerMode.MULTI,
        multi_speaker_config=multi_config_prof,
        output_filename="professional_conversation.wav",
    )
    result_prof = await tts.generate_audio(request_prof)
    if result_prof.success:
        print(f"Professional conversation saved to: {result_prof.file_path}")

    # Example 2: Casual Chat with Emotional Direction
    speaker1_cas = SpeakerConfig(name="Alex", voice_name=VoiceName.PUCK) # Upbeat voice
    speaker2_cas = SpeakerConfig(name="Jordan", voice_name=VoiceName.AOEDE) # Breezy voice
    
    multi_config_cas = MultiSpeakerConfig(
        speakers=[speaker1_cas, speaker2_cas]
    )

    request_cas = AudioRequest(
        text=(
            "Alex: Hey Jordan! Did you see that amazing goal last night? (excited) "
            "Jordan: Oh yeah, it was incredible! I was on the edge of my seat. (enthusiastic)"
        ),
        language=Language.ENGLISH_US,
        speaker_mode=SpeakerMode.MULTI,
        multi_speaker_config=multi_config_cas,
        output_filename="casual_chat.wav",
    )
    result_cas = await tts.generate_audio(request_cas)
    if result_cas.success:
        print(f"Casual chat saved to: {result_cas.file_path}")

```

## API Reference

### AudioRequest

Main class for creating audio generation requests.

```python
AudioRequest(
    text: str,                          # Text to convert to speech
    model: VoiceModel = GEMINI_TTS,     # TTS model (currently only Gemini)
    speaker_mode: SpeakerMode = SINGLE, # Single or multiple speakers
    language: Language = ENGLISH,       # Target language
    voice_config: VoiceConfig = None,   # Voice customization
    audio_format: AudioFormat = None,   # Audio output format
    output_filename: str = None         # Custom filename
)
```

### TTSService

Service class for audio generation.

```python
tts = TTSService()
result = await tts.generate_audio(request)
```

### Supported Languages (24 Total)

All languages supported by Google Gemini TTS with proper BCP-47 language codes:

**Core Languages:**
- `Language.ARABIC_EGYPTIAN` - Arabic (Egyptian) - ar-EG
- `Language.ENGLISH_US` - English (US) - en-US
- `Language.GERMAN_GERMANY` - German (Germany) - de-DE
- `Language.SPANISH_US` - Spanish (US) - es-US
- `Language.FRENCH_FRANCE` - French (France) - fr-FR
- `Language.HINDI_INDIA` - Hindi (India) - hi-IN
- `Language.INDONESIAN_INDONESIA` - Indonesian (Indonesia) - id-ID
- `Language.ITALIAN_ITALY` - Italian (Italy) - it-IT
- `Language.JAPANESE_JAPAN` - Japanese (Japan) - ja-JP
- `Language.KOREAN_KOREA` - Korean (Korea) - ko-KR
- `Language.PORTUGUESE_BRAZIL` - Portuguese (Brazil) - pt-BR
- `Language.RUSSIAN_RUSSIA` - Russian (Russia) - ru-RU

**Additional Languages:**
- `Language.DUTCH_NETHERLANDS` - Dutch (Netherlands) - nl-NL
- `Language.POLISH_POLAND` - Polish (Poland) - pl-PL
- `Language.THAI_THAILAND` - Thai (Thailand) - th-TH
- `Language.TURKISH_TURKEY` - Turkish (Turkey) - tr-TR
- `Language.VIETNAMESE_VIETNAM` - Vietnamese (Vietnam) - vi-VN
- `Language.ROMANIAN_ROMANIA` - Romanian (Romania) - ro-RO
- `Language.UKRAINIAN_UKRAINE` - Ukrainian (Ukraine) - uk-UA
- `Language.BENGALI_BANGLADESH` - Bengali (Bangladesh) - bn-BD
- `Language.ENGLISH_INDIA_HINDI_BUNDLE` - English (India) & Hindi - en-IN
- `Language.MARATHI_INDIA` - Marathi (India) - mr-IN
- `Language.TAMIL_INDIA` - Tamil (India) - ta-IN
- `Language.TELUGU_INDIA` - Telugu (India) - te-IN

**Backward Compatibility:**
- `Language.ENGLISH` - English (maps to en-US)
- `Language.SPANISH` - Spanish (maps to es-US)
- `Language.FRENCH` - French (maps to fr-FR)
- `Language.GERMAN` - German (maps to de-DE)
- `Language.ITALIAN` - Italian (maps to it-IT)
- `Language.PORTUGUESE` - Portuguese (maps to pt-BR)
- `Language.RUSSIAN` - Russian (maps to ru-RU)
- `Language.JAPANESE` - Japanese (maps to ja-JP)
- `Language.KOREAN` - Korean (maps to ko-KR)
- `Language.CHINESE` - Chinese (legacy code)

**Note**: Gemini TTS automatically detects the input language, but explicit language codes ensure proper pronunciation and regional variants.

### Available Voices (30 Total)

The library supports 30 different voice options, each with unique characteristics:

**Bright Voices:**
- `VoiceName.ZEPHYR` - Bright
- `VoiceName.AUTONOE` - Bright

**Upbeat Voices:**
- `VoiceName.PUCK` - Upbeat
- `VoiceName.LAOMEDEIA` - Upbeat

**Informative Voices:**
- `VoiceName.CHARON` - Informative
- `VoiceName.RASALGETHI` - Informative

**Firm Voices:**
- `VoiceName.KORE` - Firm (default)
- `VoiceName.ORUS` - Firm
- `VoiceName.ALNILAM` - Firm

**Excitable Voices:**
- `VoiceName.FENRIR` - Excitable

**Youthful Voices:**
- `VoiceName.LEDA` - Youthful

**Breezy Voices:**
- `VoiceName.AOEDE` - Breezy

**Easy-going Voices:**
- `VoiceName.CALLIRHOE` - Easy-going
- `VoiceName.UMBRIEL` - Easy-going

**Breathy Voices:**
- `VoiceName.ENCELADUS` - Breathy

**Clear Voices:**
- `VoiceName.IAPETUS` - Clear
- `VoiceName.ERINOME` - Clear

**Smooth Voices:**
- `VoiceName.ALGIEBA` - Smooth
- `VoiceName.DESPINA` - Smooth

**Gravelly Voices:**
- `VoiceName.ALGENIB` - Gravelly

**Soft Voices:**
- `VoiceName.ACHERNAR` - Soft

**Even Voices:**
- `VoiceName.SCHEDAR` - Even

**Mature Voices:**
- `VoiceName.GACRUX` - Mature

**Friendly Voices:**
- `VoiceName.ACHIRD` - Friendly

**Casual Voices:**
- `VoiceName.ZUBENELGENUBI` - Casual

**Forward Voices:**
- `VoiceName.PULCHERRIMA` - Forward

**Gentle Voices:**
- `VoiceName.VINDEMIATRIX` - Gentle

**Lively Voices:**
- `VoiceName.SADACHBIA` - Lively

**Knowledgeable Voices:**
- `VoiceName.SADALTAGER` - Knowledgeable

**Warm Voices:**
- `VoiceName.SULAFAR` - Warm

**Usage:**
```python
from audio_api import VoiceName

# Use any voice by importing the enum
request = AudioRequest(
    text="Your text here",
    voice_config={"voice_name": VoiceName.SULAFAR}  # Warm voice
)
```

**Note:** All voice options can be previewed in AI Studio before use.

## Audio Format

All audio files are generated with the following specifications:
- **Sample Rate**: 24kHz (24,000 Hz)
- **Bit Depth**: 16-bit
- **Channels**: 1 (Mono)
- **Format**: WAV (PCM)

## Testing

Run the test script to verify everything works:

```bash
python test_example.py
```

Test all 24 supported languages:

```bash
python test_languages.py
```

Test voice options and characteristics:

```bash
python test_voice_options.py
```

Test multi-speaker TTS functionality:

```bash
python test_multi_speaker.py
```

Run the examples:

```bash
python main.py
```

## 📚 Documentation

For comprehensive documentation, examples, and tutorials, visit the [`docs/`](docs/) directory:

- **[Quick Start Guide](docs/quick-start.md)** - Get up and running in minutes
- **[Voice Options Guide](docs/examples/voice-options.md)** - Complete guide to all 30 voices
- **[Multi-Language Guide](docs/examples/multi-language.md)** - Using all 24 supported languages
- **[Basic Usage Examples](docs/examples/basic-usage.md)** - Fundamental usage patterns
- **[Configuration Guide](docs/configuration.md)** - Setup and optimization
- **[Voice Assistant Tutorial](docs/tutorials/voice-assistant.md)** - Build a complete voice assistant
- **[API Reference](docs/api/)** - Detailed API documentation

### Quick Links
- [All 30 Voice Options](docs/api/voice-names.md)
- [Configuration Setup](docs/configuration.md)
- [Example Code](docs/examples/)

## Async Processing (Optional)

The library supports both in-memory and Redis-based queuing:

### In-Memory Queue (Default - Recommended)

```python
from audio_api import QueueService

# Default: Uses internal memory (no external dependencies)
queue = QueueService()  # use_redis=False by default
task_id = await queue.enqueue_single_task(request)

# Check results
result = await queue.get_task_result(task_id)
```

### Redis Queue (Advanced)

For persistent queues and multi-process scaling:

```python
from audio_api import QueueService, WorkerManager

# Redis-based queue (requires Redis)
queue = QueueService(use_redis=True, redis_url="redis://localhost:6379/0")

# Start workers (in separate process/container)
worker_manager = WorkerManager(num_workers=3)
await worker_manager.start_workers()

# Queue tasks
task_id = await queue.enqueue_single_task(request)

# Check results
result = await queue.get_task_result(task_id)
```

### Queue Comparison

| Feature | In-Memory | Redis |
|---------|-----------|-------|
| Setup | Zero dependencies | Requires Redis |
| Persistence | No | Yes |
| Multi-process | No | Yes |
| Use Case | Simple/moderate volume | High volume/production |

## Error Handling

```python
result = await tts.generate_audio(request)

if result.success:
    print(f"Success: {result.file_path}")
    print(f"Message: {result.message}")
else:
    print(f"Error: {result.error}")
    print(f"Message: {result.message}")
```

## Requirements

- Python 3.12+
- Google Gemini API key
- Redis (optional, for async processing)

## Environment Variables

```env
GEMINI_API_KEY=your_gemini_api_key_here
REDIS_URL=redis://localhost:6379/0  # Optional
NUM_WORKERS=3                       # Optional
```

## Project Structure

```
audio_api/
├── models/          # Data models (AudioRequest, AudioResponse, etc.)
├── services/        # Core services (TTSService, QueueService, etc.)
└── __init__.py      # Main library exports

main.py              # Usage examples
test_example.py      # Test script
```

## License

This project is licensed under the MIT License.