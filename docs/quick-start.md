# Quick Start Guide

Get up and running with the Audio Generation Library in just a few minutes!

## 🚀 Installation

1. **Clone or download the library**
2. **Install dependencies**:
   ```bash
   uv sync
   # or
   pip install -r requirements.txt
   ```

3. **Set up your API key**:
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

## 🎵 Your First Audio File

Create a simple Python script:

```python
import asyncio
from audio_api import AudioRequest, TTSService

async def my_first_audio():
    # Create the TTS service
    tts = TTSService()
    
    # Create a request
    request = AudioRequest(
        text="Hello! This is my first generated audio file.",
        output_filename="my_first_audio.wav"
    )
    
    # Generate the audio
    result = await tts.generate_audio(request)
    
    if result.success:
        print(f"✅ Audio saved to: {result.file_path}")
        print(f"⏱️  Duration: {result.duration:.2f} seconds")
    else:
        print(f"❌ Error: {result.error}")

# Run it!
asyncio.run(my_first_audio())
```

Save this as `my_first_audio.py` and run:
```bash
python my_first_audio.py
```

## 🎭 Try Different Voices

```python
import asyncio
from audio_api import AudioRequest, TTSService, VoiceName

async def try_voices():
    tts = TTSService()
    
    # Try different voice characteristics
    voices_to_try = [
        (VoiceName.KORE, "This is the default firm voice"),
        (VoiceName.SULAFAR, "This is a warm, friendly voice"),
        (VoiceName.ZEPHYR, "This is a bright, energetic voice"),
        (VoiceName.ACHERNAR, "This is a soft, gentle voice"),
    ]
    
    for voice, text in voices_to_try:
        request = AudioRequest(
            text=text,
            voice_config={"voice_name": voice},
            output_filename=f"voice_{voice.value.lower()}.wav"
        )
        
        result = await tts.generate_audio(request)
        if result.success:
            print(f"✅ {voice.value}: {result.file_path}")

asyncio.run(try_voices())
```

## 🌍 Multiple Languages

```python
import asyncio
from audio_api import AudioRequest, TTSService, Language

async def multilingual():
    tts = TTSService()
    
    # Different languages
    languages = [
        (Language.ENGLISH_US, "Hello, world!"),
        (Language.SPANISH_US, "¡Hola, mundo!"),
        (Language.FRENCH_FRANCE, "Bonjour, le monde!"),
        (Language.HINDI_INDIA, "नमस्ते दुनिया!"),
    ]
    
    for lang, text in languages:
        request = AudioRequest(
            text=text,
            language=lang,
            output_filename=f"hello_{lang.value.replace('-', '_')}.wav"
        )
        
        result = await tts.generate_audio(request)
        if result.success:
            print(f"✅ {lang.name}: {result.file_path}")

asyncio.run(multilingual())
```

## 🎛️ Custom Voice Settings

```python
import asyncio
from audio_api import AudioRequest, TTSService, VoiceName

async def custom_voice():
    tts = TTSService()
    
    request = AudioRequest(
        text="This audio has custom speed and pitch settings",
        voice_config={
            "voice_name": VoiceName.AOEDE,  # Breezy voice
            "speed": 1.3,                   # Faster speech
            "pitch": 1.2                    # Higher pitch
        },
        output_filename="custom_voice.wav"
    )
    
    result = await tts.generate_audio(request)
    if result.success:
        print(f"✅ Custom voice audio: {result.file_path}")

asyncio.run(custom_voice())
```

## 📁 Output Files

All audio files are saved to the `output/` directory with these specifications:
- **Format**: WAV (PCM)
- **Sample Rate**: 24kHz
- **Bit Depth**: 16-bit
- **Channels**: Mono

## 🔧 Common Issues

### API Key Not Found
```
❌ GEMINI_API_KEY not found in environment variables
```
**Solution**: Make sure you've created a `.env` file with your API key:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

### Import Errors
```
❌ ModuleNotFoundError: No module named 'audio_api'
```
**Solution**: Make sure you're running from the project directory and dependencies are installed:
```bash
uv sync  # or pip install -r requirements.txt
```

## 🎯 Next Steps

Now that you have the basics working:

1. **Explore Voice Options**: Check out [Voice Options Guide](examples/voice-options.md) for all 30 voices
2. **Try More Languages**: See [Multi-Language Guide](examples/multi-language.md) for all 24 languages
3. **Batch Processing**: Learn [Batch Processing](examples/batch-processing.md) for multiple files
4. **Advanced Features**: Explore [Async Processing](examples/async-processing.md) for high-volume use

## 💡 Pro Tips

- **File Naming**: Use descriptive filenames to organize your audio files
- **Voice Selection**: Match voice characteristics to your content (warm for friendly content, informative for educational content)
- **Language Codes**: Use specific language codes (e.g., `Language.ENGLISH_US`) for better pronunciation
- **Error Handling**: Always check `result.success` before using the file path

Happy audio generation! 🎵