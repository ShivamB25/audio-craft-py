# Memory Bank - Audio Generation Library

## Project Overview

**Current State**: Production-ready Python TTS library built around Google's Gemini TTS API

### Core Features
- **24 supported languages** with proper BCP-47 codes (en-US, es-US, fr-FR, etc.)
- **30 voice options** with lowercase API-compliant names (kore, zephyr, puck, etc.)
- **Multi-speaker support** (up to 2 speakers with different voices)
- **Dual queue system** (in-memory default, Redis optional)
- **Model selection** (GEMINI_TTS_PRO and GEMINI_TTS_FLASH)

### Architecture
- **Package structure**: `audio_api/models/`, `audio_api/services/`
- **Type-safe** with Pydantic validation
- **Async-first** design
- **Zero dependencies by default** with optional Redis for scaling

### Audio Specifications (Critical Requirements)
- **Format**: WAV (PCM)
- **Sample Rate**: 24kHz
- **Bit Depth**: 16-bit
- **Channels**: 1 (Mono)

## Recent Critical Fixes (Phase 8)

### Voice Name API Alignment
- **Problem**: Voice names didn't match Gemini API requirements
- **Solution**: All voice names now lowercase and API-compliant
- **Key Changes**:
  - "Sulafar" → "sulafat" (API uses 't' at end)
  - "Callirhoe" → "callirrhoe" (API uses double 'r')
  - All voices now lowercase (e.g., "Kore" → "kore")
- **Files Updated**: All models, tests, and documentation
- **Result**: Eliminates 400 INVALID_ARGUMENT voice name errors

## Voice Options (30 Total)

### Voice Categories
- **Bright**: zephyr, autonoe
- **Upbeat**: puck, laomedeia
- **Informative**: charon, rasalgethi
- **Firm**: kore (default), orus, alnilam
- **Warm**: sulafat
- **Easy-going**: callirrhoe, umbriel
- **Gentle**: vindemiatrix
- **Soft**: achernar
- **Mature**: gacrux
- **[21 more voices available]**

## Language Support (24 Total)

### Core Languages
- English (US): en-US
- Spanish (US): es-US
- French (France): fr-FR
- German (Germany): de-DE
- Hindi (India): hi-IN
- Japanese (Japan): ja-JP
- Arabic (Egyptian): ar-EG
- **[17 more languages available]**

## Usage Patterns

### Simple Usage
```python
from audio_api import AudioRequest, TTSService

tts = TTSService()
request = AudioRequest(text="Hello world")
result = await tts.generate_audio(request)
```

### Multi-Speaker
```python
from audio_api import SpeakerMode, MultiSpeakerConfig, SpeakerConfig, VoiceName

config = MultiSpeakerConfig(speakers=[
    SpeakerConfig(speaker_name="Alice", voice_name=VoiceName.KORE),
    SpeakerConfig(speaker_name="Bob", voice_name=VoiceName.CHARON)
])

request = AudioRequest(
    text="Alice: Hello! Bob: Hi there!",
    speaker_mode=SpeakerMode.MULTIPLE,
    multi_speaker_config=config
)
```

## Testing

### Test Files
- `tests/test_example.py` - Basic functionality
- `tests/test_languages.py` - All 24 languages
- `tests/test_voice_options.py` - Voice characteristics
- `tests/test_multi_speaker.py` - Multi-speaker conversations
- `main.py` - Comprehensive examples

### Quick Test Commands
```bash
python setup.py                    # Setup
python tests/test_example.py       # Basic test
python run_all_tests.py           # Full test suite
```

## Common Issues & Solutions

### Voice Name Errors
- **Issue**: 400 INVALID_ARGUMENT for voice names
- **Solution**: Use VoiceName enum, ensure lowercase API names

### Import Errors
- **Issue**: ModuleNotFoundError
- **Solution**: Proper package installation with `uv sync`

### API Key Issues
- **Issue**: Authentication errors
- **Solution**: Set GEMINI_API_KEY in .env file

## Development Notes

### Critical Dependencies
- **google-genai**: >=1.16.1 (TTS support)
- **pydantic**: Data validation
- **python-dotenv**: Environment management

### File Structure
```
audio_api/
├── models/audio_request.py    # Core models and enums
├── services/tts_service.py    # TTS processing
└── services/queue_service.py  # Queue management
```

### Design Philosophy
- Simple by default, powerful when needed
- Progressive enhancement (Redis optional)
- Type-safe with comprehensive validation
- 95% Gemini TTS API feature coverage

---

**Last Updated**: Phase 8 - Voice name corrections applied
**Status**: Production ready, all tests passing