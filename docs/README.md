# Audio Generation Library Documentation

Welcome to the comprehensive documentation for the Audio Generation Library. This documentation provides detailed examples, guides, and reference materials to help you get the most out of the library.

## 📚 Documentation Structure

### Getting Started
- [Quick Start Guide](quick-start.md) - Get up and running in minutes
- [Installation Guide](installation.md) - Detailed installation instructions
- [Configuration](configuration.md) - Environment setup and API keys

### Usage Examples
- [Basic Usage](examples/basic-usage.md) - Simple audio generation examples
- [Voice Options](examples/voice-options.md) - Complete guide to all 30 voices
- [Multi-Language Support](examples/multi-language.md) - Using all 24 supported languages
- [Custom Voice Configuration](examples/custom-voice.md) - Advanced voice customization
- [Batch Processing](examples/batch-processing.md) - Processing multiple audio files
- [Async Processing](examples/async-processing.md) - Queue-based processing

### Advanced Features
- [Queue System](advanced/queue-system.md) - In-memory vs Redis queues
- [Worker Management](advanced/worker-management.md) - Scaling with multiple workers
- [Error Handling](advanced/error-handling.md) - Robust error management
- [Performance Optimization](advanced/performance.md) - Tips for optimal performance

### API Reference
- [AudioRequest](api/audio-request.md) - Complete AudioRequest documentation
- [TTSService](api/tts-service.md) - TTS service methods and options
- [Voice Names](api/voice-names.md) - All available voices with characteristics
- [Languages](api/languages.md) - Supported languages and codes
- [Response Objects](api/responses.md) - Understanding response objects

### Tutorials
- [Building a Voice Assistant](tutorials/voice-assistant.md) - Step-by-step tutorial
- [Creating Audio Books](tutorials/audio-books.md) - Long-form content generation
- [Multi-Language Content](tutorials/multi-language-content.md) - International applications

### Best Practices
- [Code Organization](best-practices/code-organization.md) - Structuring your projects
- [Performance Tips](best-practices/performance.md) - Optimizing audio generation
- [Security](best-practices/security.md) - API key management and security

## 🚀 Quick Navigation

### Most Common Use Cases
1. **Simple Text-to-Speech**: [Basic Usage](examples/basic-usage.md)
2. **Different Voices**: [Voice Options](examples/voice-options.md)
3. **Multiple Languages**: [Multi-Language](examples/multi-language.md)
4. **Batch Processing**: [Batch Processing](examples/batch-processing.md)

### Need Help?
- Check the [FAQ](faq.md) for common questions
- Review [Troubleshooting](troubleshooting.md) for common issues
- See [Examples](examples/) for code samples

## 📋 Quick Reference

### Essential Imports
```python
from audio_api import (
    AudioRequest, 
    TTSService, 
    VoiceName, 
    Language,
    VoiceConfig,
    AudioFormat
)
```

### Basic Pattern
```python
import asyncio

async def generate_audio():
    tts = TTSService()
    request = AudioRequest(text="Your text here")
    result = await tts.generate_audio(request)
    return result.file_path if result.success else None

# Run
asyncio.run(generate_audio())
```

---

*This documentation is automatically updated with each library release.*