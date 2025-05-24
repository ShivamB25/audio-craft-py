# 🎵 Audio Craft

**Professional text-to-speech library for Python** - Generate high-quality audio with Google Gemini TTS

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Features

🎯 **Professional Quality** - 24kHz, 16-bit WAV audio  
🌍 **24 Languages** - Full international support with BCP-47 codes  
🎭 **30 Voice Options** - From bright & upbeat to warm & gentle  
👥 **Multi-Speaker** - Create conversations with different voices  
⚡ **Async Ready** - Non-blocking audio generation  
🚀 **Simple API** - Get started in 3 lines of code  

---

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
uv sync

# Set up API key
cp .env.example .env
# Add your GEMINI_API_KEY to .env
```

### Basic Usage

```python
import asyncio
from audio_api import AudioRequest, TTSService

async def main():
    tts = TTSService()
    request = AudioRequest(text="Hello, world!")
    result = await tts.generate_audio(request)
    print(f"Audio saved: {result.file_path}")

asyncio.run(main())
```

That's it! Your audio file is ready in the `output/` directory.

---

## 🎭 Voice Examples

```python
from audio_api import AudioRequest, TTSService, VoiceName

# Professional & authoritative
request = AudioRequest(
    text="Welcome to our quarterly meeting",
    voice_config={"voice_name": VoiceName.KORE}  # Firm
)

# Warm & friendly
request = AudioRequest(
    text="Thanks for calling! How can I help?",
    voice_config={"voice_name": VoiceName.SULAFAT}  # Warm
)

# Energetic & upbeat
request = AudioRequest(
    text="Congratulations on your achievement!",
    voice_config={"voice_name": VoiceName.PUCK}  # Upbeat
)
```

**Voice Categories**: Bright, Upbeat, Informative, Firm, Warm, Gentle, Soft, Mature, Friendly, and more!

---

## 🌍 Multi-Language Support

```python
from audio_api import Language

# 24 languages supported
languages = [
    (Language.ENGLISH_US, "Hello, world!"),
    (Language.SPANISH_US, "¡Hola, mundo!"),
    (Language.FRENCH_FRANCE, "Bonjour, le monde!"),
    (Language.HINDI_INDIA, "नमस्ते दुनिया!"),
    (Language.JAPANESE_JAPAN, "こんにちは世界！"),
    (Language.ARABIC_EGYPTIAN, "مرحبا بالعالم!")
]

for lang, text in languages:
    request = AudioRequest(text=text, language=lang)
    result = await tts.generate_audio(request)
```

---

## 👥 Multi-Speaker Conversations

```python
from audio_api import SpeakerMode, MultiSpeakerConfig, SpeakerConfig

# Create speakers with different voices
config = MultiSpeakerConfig(speakers=[
    SpeakerConfig(speaker_name="Alice", voice_name=VoiceName.KORE),
    SpeakerConfig(speaker_name="Bob", voice_name=VoiceName.CHARON)
])

request = AudioRequest(
    text="Alice: Good morning! Bob: Hello, ready for the meeting?",
    speaker_mode=SpeakerMode.MULTIPLE,
    multi_speaker_config=config
)
```

Perfect for podcasts, dialogues, and interactive content!

---

## 🎛️ Advanced Features

### Custom Voice Settings
```python
from audio_api import VoiceConfig

voice_config = VoiceConfig(
    voice_name=VoiceName.AOEDE,  # Breezy voice
    speed=1.2,                   # 20% faster
    pitch=1.1                    # Slightly higher
)
```

### Batch Processing
```python
texts = ["First message", "Second message", "Third message"]

for i, text in enumerate(texts):
    request = AudioRequest(text=text, output_filename=f"batch_{i}.wav")
    result = await tts.generate_audio(request)
```

### Queue Processing (Optional)
```python
from audio_api import QueueService

# In-memory queue (default)
queue = QueueService()
task_id = await queue.enqueue_single_task(request)
result = await queue.get_task_result(task_id)

# Redis queue (for production)
queue = QueueService(use_redis=True)
```

---

## 📚 Documentation

| Guide | Description |
|-------|-------------|
| [📖 Quick Start](docs/quick-start.md) | Get running in 5 minutes |
| [🎭 Voice Guide](docs/examples/voice-options.md) | All 30 voices with examples |
| [🌍 Languages](docs/examples/multi-language.md) | Complete language reference |
| [⚙️ Configuration](docs/configuration.md) | Setup and optimization |
| [🤖 Voice Assistant](docs/tutorials/voice-assistant.md) | Build a complete assistant |

---

## 🧪 Testing

```bash
# Quick test
python tests/test_example.py

# Test all features
python run_all_tests.py

# Run examples
python main.py
```

---

## 📋 Requirements

- **Python 3.12+**
- **Google Gemini API key** ([Get one here](https://ai.google.dev/))
- **Redis** (optional, for production queuing)

---

## 🔧 Environment Setup

```env
# Required
GEMINI_API_KEY=your_api_key_here

# Optional
REDIS_URL=redis://localhost:6379/0
NUM_WORKERS=3
```

---

## 🎵 Audio Specifications

- **Format**: WAV (PCM)
- **Sample Rate**: 24kHz
- **Bit Depth**: 16-bit
- **Channels**: Mono
- **Quality**: Professional broadcast standard

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Run tests: `python run_all_tests.py`
4. Submit a pull request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🌟 Why Audio Craft?

✅ **Production Ready** - Used in real applications  
✅ **Type Safe** - Full Pydantic validation  
✅ **Well Tested** - Comprehensive test suite  
✅ **Great Docs** - Clear examples and guides  
✅ **Active Support** - Regular updates and fixes  

**Perfect for**: Voice assistants, audiobooks, podcasts, e-learning, accessibility tools, and any application needing high-quality speech synthesis.

---

<div align="center">

**[⭐ Star this repo](https://github.com/yourusername/audio-craft-py)** if it helped you!

Made with ❤️ for developers who care about audio quality

</div>