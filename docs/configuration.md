# Configuration Guide

Complete guide to configuring the Audio Generation Library for optimal performance and security.

## 🔑 API Key Setup

### Getting Your Gemini API Key

1. **Visit Google AI Studio**: Go to [https://aistudio.google.com/](https://aistudio.google.com/)
2. **Sign in**: Use your Google account
3. **Get API Key**: Click "Get API Key" and create a new key
4. **Copy the Key**: Save it securely - you'll need it for configuration

### Setting Up Environment Variables

#### Method 1: Using .env File (Recommended)

1. **Copy the example file**:
   ```bash
   cp .env.example .env
   ```

2. **Edit the .env file**:
   ```env
   # Required: Your Gemini API key
   GEMINI_API_KEY=your_actual_api_key_here
   
   # Optional: Redis configuration (for advanced async processing)
   REDIS_URL=redis://localhost:6379/0
   
   # Optional: Worker configuration
   NUM_WORKERS=3
   ```

3. **Verify the setup**:
   ```python
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   
   api_key = os.getenv("GEMINI_API_KEY")
   if api_key:
       print("✅ API key loaded successfully")
   else:
       print("❌ API key not found")
   ```

#### Method 2: System Environment Variables

**Linux/macOS**:
```bash
export GEMINI_API_KEY="your_actual_api_key_here"
export REDIS_URL="redis://localhost:6379/0"  # Optional
export NUM_WORKERS="3"  # Optional
```

**Windows (Command Prompt)**:
```cmd
set GEMINI_API_KEY=your_actual_api_key_here
set REDIS_URL=redis://localhost:6379/0
set NUM_WORKERS=3
```

**Windows (PowerShell)**:
```powershell
$env:GEMINI_API_KEY="your_actual_api_key_here"
$env:REDIS_URL="redis://localhost:6379/0"
$env:NUM_WORKERS="3"
```

#### Method 3: Python Code (Not Recommended for Production)

```python
import os

# Only for testing - never commit API keys to code
os.environ["GEMINI_API_KEY"] = "your_api_key_here"
```

## 🎛️ Audio Configuration

### Default Audio Settings

The library uses these default settings for optimal quality:

```python
from audio_api import AudioFormat

# Default audio format
default_format = AudioFormat(
    sample_rate=24000,  # 24kHz - high quality
    bit_depth=16,       # 16-bit - good balance of quality and size
    channels=1          # Mono - standard for speech
)
```

### Custom Audio Configuration

```python
from audio_api import AudioRequest, AudioFormat

# Custom audio settings
custom_format = AudioFormat(
    sample_rate=24000,  # Keep at 24kHz for best quality
    bit_depth=16,       # Keep at 16-bit (don't change)
    channels=1          # Keep at 1 (mono) for speech
)

request = AudioRequest(
    text="Your text here",
    audio_format=custom_format
)
```

**⚠️ Important**: The Gemini TTS service requires specific audio format settings. Changing these values may cause errors:
- **Sample Rate**: Must be 24000 Hz
- **Bit Depth**: Must be 16-bit
- **Channels**: Must be 1 (mono)

## 🎭 Voice Configuration

### Default Voice Settings

```python
from audio_api import VoiceConfig, VoiceName

# Default voice configuration
default_voice = VoiceConfig(
    voice_name=VoiceName.KORE,  # Firm, professional voice
    speed=1.0,                  # Normal speed
    pitch=1.0                   # Normal pitch
)
```

### Custom Voice Configuration

```python
# Slow, deep voice for serious content
serious_voice = VoiceConfig(
    voice_name=VoiceName.GACRUX,  # Mature voice
    speed=0.8,                    # 20% slower
    pitch=0.9                     # 10% lower pitch
)

# Fast, high voice for energetic content
energetic_voice = VoiceConfig(
    voice_name=VoiceName.FENRIR,  # Excitable voice
    speed=1.3,                    # 30% faster
    pitch=1.2                     # 20% higher pitch
)

# Use in requests
request = AudioRequest(
    text="This is serious content",
    voice_config=serious_voice
)
```

### Voice Parameter Ranges

```python
# Valid ranges for voice parameters
VOICE_RANGES = {
    "speed": {
        "min": 0.1,    # Very slow
        "max": 3.0,    # Very fast
        "default": 1.0,
        "recommended": (0.8, 1.5)  # Good range for most content
    },
    "pitch": {
        "min": 0.1,    # Very low
        "max": 2.0,    # Very high
        "default": 1.0,
        "recommended": (0.9, 1.3)  # Natural sounding range
    }
}
```

## 📁 Output Configuration

### Default Output Settings

```python
# Default output directory
DEFAULT_OUTPUT_DIR = "output/"

# Default filename pattern
# If no filename specified, uses: "audio_{timestamp}_{hash}.wav"
```

### Custom Output Configuration

```python
from datetime import datetime
import os

# Custom output directory
custom_output_dir = "my_audio_files/"
os.makedirs(custom_output_dir, exist_ok=True)

# Custom filename with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
custom_filename = f"{timestamp}_my_audio.wav"

request = AudioRequest(
    text="Your text here",
    output_filename=custom_filename
)
```

### Organized File Structure

```python
async def organized_output_example():
    """Example of organizing output files by category."""
    
    categories = {
        "greetings": ["Hello!", "Welcome!", "Good morning!"],
        "notifications": ["New message", "Update available", "Task complete"],
        "errors": ["Error occurred", "Please try again", "Invalid input"]
    }
    
    for category, messages in categories.items():
        # Create category directory
        category_dir = f"output/{category}/"
        os.makedirs(category_dir, exist_ok=True)
        
        for i, message in enumerate(messages, 1):
            filename = f"{category_dir}{category}_{i:02d}.wav"
            
            request = AudioRequest(
                text=message,
                output_filename=filename
            )
            
            # Generate audio...
```

## 🔄 Async Processing Configuration

### In-Memory Queue (Default)

```python
from audio_api import QueueService

# Default configuration - no external dependencies
queue = QueueService()  # use_redis=False by default

# Optional configuration
queue = QueueService(
    use_redis=False,
    max_queue_size=1000,  # Maximum items in memory queue
    worker_timeout=300    # Worker timeout in seconds
)
```

### Redis Queue Configuration

```python
# Redis queue for production use
redis_queue = QueueService(
    use_redis=True,
    redis_url="redis://localhost:6379/0",
    redis_db=0,
    redis_password=None,  # If Redis requires authentication
    max_retries=3,
    retry_delay=1.0
)
```

### Worker Configuration

```python
from audio_api import WorkerManager

# Configure workers for high-volume processing
worker_manager = WorkerManager(
    num_workers=3,                    # Number of worker processes
    queue_service=redis_queue,        # Queue to process
    worker_timeout=300,               # Timeout per task
    max_tasks_per_worker=100,         # Restart workers after N tasks
    log_level="INFO"                  # Logging level
)
```

## 🌍 Language Configuration

### Default Language

```python
from audio_api import Language

# Default language is English (US)
DEFAULT_LANGUAGE = Language.ENGLISH_US
```

### Language Selection Strategy

```python
def select_language_by_content(text: str) -> Language:
    """Smart language selection based on content."""
    
    # Simple heuristics (you can make this more sophisticated)
    if any(char in text for char in "áéíóúñ¿¡"):
        return Language.SPANISH_US
    elif any(char in text for char in "àâäéèêëîïôöùûüÿç"):
        return Language.FRENCH_FRANCE
    elif any(char in text for char in "äöüß"):
        return Language.GERMAN_GERMANY
    elif any(char in text for char in "देवनागरी"):
        return Language.HINDI_INDIA
    else:
        return Language.ENGLISH_US

# Usage
text = "¡Hola mundo!"
language = select_language_by_content(text)
```

### Multi-Language Application Configuration

```python
# Configuration for multi-language applications
LANGUAGE_CONFIG = {
    "supported_languages": [
        Language.ENGLISH_US,
        Language.SPANISH_US,
        Language.FRENCH_FRANCE,
        Language.GERMAN_GERMANY,
        Language.HINDI_INDIA,
    ],
    "default_language": Language.ENGLISH_US,
    "fallback_language": Language.ENGLISH_US,
    "voice_mapping": {
        Language.ENGLISH_US: VoiceName.SULAFAR,
        Language.SPANISH_US: VoiceName.ACHIRD,
        Language.FRENCH_FRANCE: VoiceName.AOEDE,
        Language.GERMAN_GERMANY: VoiceName.KORE,
        Language.HINDI_INDIA: VoiceName.CHARON,
    }
}
```

## 🔒 Security Configuration

### API Key Security

```python
# ✅ Good practices
def load_api_key():
    """Securely load API key from environment."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    return api_key

# ❌ Bad practices - never do this
API_KEY = "your_actual_api_key_here"  # Never hardcode keys
```

### Environment-Specific Configuration

```python
import os

def get_config():
    """Get configuration based on environment."""
    env = os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        return {
            "redis_url": os.getenv("REDIS_URL"),
            "num_workers": int(os.getenv("NUM_WORKERS", "5")),
            "log_level": "WARNING",
            "max_queue_size": 10000,
        }
    elif env == "staging":
        return {
            "redis_url": os.getenv("REDIS_URL", "redis://localhost:6379/1"),
            "num_workers": int(os.getenv("NUM_WORKERS", "2")),
            "log_level": "INFO",
            "max_queue_size": 1000,
        }
    else:  # development
        return {
            "redis_url": None,  # Use in-memory queue
            "num_workers": 1,
            "log_level": "DEBUG",
            "max_queue_size": 100,
        }
```

## 📊 Performance Configuration

### Optimization Settings

```python
# Performance-optimized configuration
PERFORMANCE_CONFIG = {
    # Audio settings
    "audio_format": AudioFormat(
        sample_rate=24000,  # Don't change - required by Gemini
        bit_depth=16,       # Don't change - required by Gemini
        channels=1          # Don't change - required by Gemini
    ),
    
    # Voice settings for speed
    "fast_voice_config": VoiceConfig(
        voice_name=VoiceName.CHARON,  # Clear and efficient
        speed=1.2,                    # Slightly faster
        pitch=1.0                     # Normal pitch
    ),
    
    # Queue settings
    "queue_config": {
        "use_redis": True,            # For production
        "max_queue_size": 5000,       # Large queue
        "worker_timeout": 180,        # 3 minutes per task
        "max_retries": 2,             # Fewer retries for speed
    },
    
    # Worker settings
    "worker_config": {
        "num_workers": 5,             # More workers
        "max_tasks_per_worker": 50,   # Restart workers frequently
    }
}
```

### Memory Management

```python
# Memory-conscious configuration for large batches
MEMORY_CONFIG = {
    "batch_size": 10,                 # Process in smaller batches
    "max_queue_size": 100,            # Smaller queue
    "worker_memory_limit": "512MB",   # Limit worker memory
    "cleanup_interval": 50,           # Clean up every 50 tasks
}
```

## 🧪 Testing Configuration

### Test Environment Setup

```python
# Configuration for testing
TEST_CONFIG = {
    "api_key": os.getenv("GEMINI_API_KEY_TEST", os.getenv("GEMINI_API_KEY")),
    "output_dir": "test_output/",
    "use_redis": False,  # Always use in-memory for tests
    "log_level": "DEBUG",
    "test_voices": [VoiceName.KORE, VoiceName.SULAFAR, VoiceName.CHARON],
    "test_languages": [Language.ENGLISH_US, Language.SPANISH_US],
}
```

### Configuration Validation

```python
def validate_configuration():
    """Validate that all required configuration is present."""
    
    # Check API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is required")
    
    # Check Redis if using Redis queue
    if os.getenv("USE_REDIS", "false").lower() == "true":
        redis_url = os.getenv("REDIS_URL")
        if not redis_url:
            raise ValueError("REDIS_URL is required when USE_REDIS=true")
    
    # Check output directory
    output_dir = os.getenv("OUTPUT_DIR", "output/")
    os.makedirs(output_dir, exist_ok=True)
    
    print("✅ Configuration validation passed")

# Run validation
validate_configuration()
```

## 📋 Configuration Checklist

### Development Setup
- [ ] API key set in `.env` file
- [ ] Dependencies installed (`uv sync` or `pip install -r requirements.txt`)
- [ ] Output directory exists and is writable
- [ ] Test script runs successfully (`python test_example.py`)

### Production Setup
- [ ] API key set as environment variable (not in code)
- [ ] Redis server running (if using Redis queue)
- [ ] Worker processes configured
- [ ] Logging configured appropriately
- [ ] Output directory has sufficient disk space
- [ ] Monitoring and alerting set up

### Security Checklist
- [ ] API keys stored securely (environment variables)
- [ ] No API keys in source code
- [ ] `.env` file in `.gitignore`
- [ ] Production environment isolated
- [ ] Access controls in place

## 🔧 Troubleshooting Configuration

### Common Issues

**API Key Not Found**:
```python
# Check if API key is loaded
import os
print("API Key:", "✅ Set" if os.getenv("GEMINI_API_KEY") else "❌ Missing")
```

**Redis Connection Issues**:
```python
# Test Redis connection
import redis
try:
    r = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
    r.ping()
    print("✅ Redis connection successful")
except Exception as e:
    print(f"❌ Redis connection failed: {e}")
```

**Output Directory Issues**:
```python
# Check output directory
import os
output_dir = "output/"
if os.path.exists(output_dir) and os.access(output_dir, os.W_OK):
    print("✅ Output directory is writable")
else:
    print("❌ Output directory issue")
    os.makedirs(output_dir, exist_ok=True)
```

This comprehensive configuration guide covers all aspects of setting up and optimizing the Audio Generation Library for your specific needs.