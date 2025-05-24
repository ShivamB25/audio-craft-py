# Voice Names API Reference

Complete reference for all 30 available voice options in the Audio Generation Library.

## 🎭 VoiceName Enum

The `VoiceName` enum provides type-safe access to all available voices with their characteristics.

```python
from audio_api import VoiceName

# Access any voice
voice = VoiceName.SULAFAR  # Warm voice
print(voice.value)  # "Sulafar"
```

## 📋 Complete Voice Catalog

### Bright Voices
Energetic and uplifting, perfect for positive content.

| Voice | Enum Value | Characteristic | Best For |
|-------|------------|----------------|----------|
| Zephyr | `VoiceName.ZEPHYR` | Bright | Marketing, announcements, energetic content |
| Autonoe | `VoiceName.AUTONOE` | Bright | Presentations, upbeat messaging |

```python
# Usage example
request = AudioRequest(
    text="Exciting news! Our new product is here!",
    voice_config={"voice_name": VoiceName.ZEPHYR}
)
```

### Upbeat Voices
Cheerful and positive, great for friendly content.

| Voice | Enum Value | Characteristic | Best For |
|-------|------------|----------------|----------|
| Puck | `VoiceName.PUCK` | Upbeat | Celebrations, positive announcements |
| Laomedeia | `VoiceName.LAOMEDEIA` | Upbeat | Entertainment, cheerful messaging |

```python
# Usage example
request = AudioRequest(
    text="Congratulations on your achievement!",
    voice_config={"voice_name": VoiceName.PUCK}
)
```

### Informative Voices
Clear and educational, ideal for instructional content.

| Voice | Enum Value | Characteristic | Best For |
|-------|------------|----------------|----------|
| Charon | `VoiceName.CHARON` | Informative | Tutorials, educational content, explanations |
| Rasalgethi | `VoiceName.RASALGETHI` | Informative | Professional presentations, reports |

```python
# Usage example
request = AudioRequest(
    text="In this tutorial, we'll learn about machine learning basics.",
    voice_config={"voice_name": VoiceName.CHARON}
)
```

### Firm Voices
Authoritative and professional, perfect for business content.

| Voice | Enum Value | Characteristic | Best For |
|-------|------------|----------------|----------|
| Kore | `VoiceName.KORE` | Firm (Default) | Business announcements, professional content |
| Orus | `VoiceName.ORUS` | Firm | Authority statements, important notices |
| Alnilam | `VoiceName.ALNILAM` | Firm | Corporate communications, formal presentations |

```python
# Usage example (Kore is the default)
request = AudioRequest(
    text="Please follow the safety guidelines at all times.",
    voice_config={"voice_name": VoiceName.KORE}
)
```

### Excitable Voices
Dynamic and enthusiastic, great for high-energy content.

| Voice | Enum Value | Characteristic | Best For |
|-------|------------|----------------|----------|
| Fenrir | `VoiceName.FENRIR` | Excitable | Sports commentary, exciting announcements |

```python
# Usage example
request = AudioRequest(
    text="And the winner is... you!",
    voice_config={"voice_name": VoiceName.FENRIR}
)
```

### Youthful Voices
Fresh and young-sounding, perfect for modern content.

| Voice | Enum Value | Characteristic | Best For |
|-------|------------|----------------|----------|
| Leda | `VoiceName.LEDA` | Youthful | Youth-oriented content, modern messaging |

```python
# Usage example
request = AudioRequest(
    text="Check out our latest app features!",
    voice_config={"voice_name": VoiceName.LEDA}
)
```

### Breezy Voices
Light and airy, ideal for casual content.

| Voice | Enum Value | Characteristic | Best For |
|-------|------------|----------------|----------|
| Aoede | `VoiceName.AOEDE` | Breezy | Casual conversations, light content |

```python
# Usage example
request = AudioRequest(
    text="Just wanted to let you know about our weekend sale.",
    voice_config={"voice_name": VoiceName.AOEDE}
)
```

### Easy-going Voices
Relaxed and casual, perfect for informal content.

| Voice | Enum Value | Characteristic | Best For |
|-------|------------|----------------|----------|
| Callirhoe | `VoiceName.CALLIRHOE` | Easy-going | Casual messaging, friendly updates |
| Umbriel | `VoiceName.UMBRIEL` | Easy-going | Informal announcements, relaxed content |

```python
# Usage example
request = AudioRequest(
    text="Hey there! Just a quick update on your order.",
    voice_config={"voice_name": VoiceName.CALLIRHOE}
)
```

### Breathy Voices
Intimate and close, great for personal content.

| Voice | Enum Value | Characteristic | Best For |
|-------|------------|----------------|----------|
| Enceladus | `VoiceName.ENCELADUS` | Breathy | Personal messages, intimate content |

```python
# Usage example
request = AudioRequest(
    text="Thank you for being such a valued customer.",
    voice_config={"voice_name": VoiceName.ENCELADUS}
)
```

### Clear Voices
Crisp and articulate, excellent for important information.

| Voice | Enum Value | Characteristic | Best For |
|-------|------------|----------------|----------|
| Iapetus | `VoiceName.IAPETUS` | Clear | Important announcements, clear instructions |
| Erinome | `VoiceName.ERINOME` | Clear | Detailed explanations, precise information |

```python
# Usage example
request = AudioRequest(
    text="Please listen carefully to these important instructions.",
    voice_config={"voice_name": VoiceName.IAPETUS}
)
```

### Smooth Voices
Polished and flowing, perfect for professional content.

| Voice | Enum Value | Characteristic | Best For |
|-------|------------|----------------|----------|
| Algieba | `VoiceName.ALGIEBA` | Smooth | Professional presentations, polished content |
| Despina | `VoiceName.DESPINA` | Smooth | Elegant messaging, refined communications |

```python
# Usage example
request = AudioRequest(
    text="Welcome to our premium service experience.",
    voice_config={"voice_name": VoiceName.ALGIEBA}
)
```

### Gravelly Voices
Textured and distinctive, great for character.

| Voice | Enum Value | Characteristic | Best For |
|-------|------------|----------------|----------|
| Algenib | `VoiceName.ALGENIB` | Gravelly | Character voices, distinctive messaging |

```python
# Usage example
request = AudioRequest(
    text="This is a special message from our founder.",
    voice_config={"voice_name": VoiceName.ALGENIB}
)
```

### Soft Voices
Gentle and soothing, ideal for calming content.

| Voice | Enum Value | Characteristic | Best For |
|-------|------------|----------------|----------|
| Achernar | `VoiceName.ACHERNAR` | Soft | Meditation, calming messages, gentle content |

```python
# Usage example
request = AudioRequest(
    text="Take a deep breath and relax. Everything will be okay.",
    voice_config={"voice_name": VoiceName.ACHERNAR}
)
```

### Even Voices
Balanced and steady, perfect for consistent content.

| Voice | Enum Value | Characteristic | Best For |
|-------|------------|----------------|----------|
| Schedar | `VoiceName.SCHEDAR` | Even | Audiobooks, consistent narration, balanced content |

```python
# Usage example
request = AudioRequest(
    text="Chapter one: The beginning of our story.",
    voice_config={"voice_name": VoiceName.SCHEDAR}
)
```

### Mature Voices
Experienced and wise, great for authoritative content.

| Voice | Enum Value | Characteristic | Best For |
|-------|------------|----------------|----------|
| Gacrux | `VoiceName.GACRUX` | Mature | Expert commentary, wise advice, experienced perspectives |

```python
# Usage example
request = AudioRequest(
    text="Based on years of experience, I can tell you that...",
    voice_config={"voice_name": VoiceName.GACRUX}
)
```

### Friendly Voices
Approachable and warm, perfect for customer service.

| Voice | Enum Value | Characteristic | Best For |
|-------|------------|----------------|----------|
| Achird | `VoiceName.ACHIRD` | Friendly | Customer service, welcoming messages, helpful content |

```python
# Usage example
request = AudioRequest(
    text="Hi there! How can I help you today?",
    voice_config={"voice_name": VoiceName.ACHIRD}
)
```

### Casual Voices
Conversational and relaxed, great for informal communication.

| Voice | Enum Value | Characteristic | Best For |
|-------|------------|----------------|----------|
| Zubenelgenubi | `VoiceName.ZUBENELGENUBI` | Casual | Informal updates, conversational content |

```python
# Usage example
request = AudioRequest(
    text="So, here's what's happening with your order...",
    voice_config={"voice_name": VoiceName.ZUBENELGENUBI}
)
```

### Forward Voices
Assertive and direct, ideal for confident messaging.

| Voice | Enum Value | Characteristic | Best For |
|-------|------------|----------------|----------|
| Pulcherrima | `VoiceName.PULCHERRIMA` | Forward | Direct messaging, assertive communications |

```python
# Usage example
request = AudioRequest(
    text="We need to address this issue immediately.",
    voice_config={"voice_name": VoiceName.PULCHERRIMA}
)
```

### Gentle Voices
Caring and nurturing, perfect for supportive content.

| Voice | Enum Value | Characteristic | Best For |
|-------|------------|----------------|----------|
| Vindemiatrix | `VoiceName.VINDEMIATRIX` | Gentle | Supportive messages, caring communications |

```python
# Usage example
request = AudioRequest(
    text="Remember to take care of yourself and get enough rest.",
    voice_config={"voice_name": VoiceName.VINDEMIATRIX}
)
```

### Lively Voices
Animated and energetic, great for dynamic content.

| Voice | Enum Value | Characteristic | Best For |
|-------|------------|----------------|----------|
| Sadachbia | `VoiceName.SADACHBIA` | Lively | Dynamic presentations, animated content |

```python
# Usage example
request = AudioRequest(
    text="Let's dive into today's exciting agenda!",
    voice_config={"voice_name": VoiceName.SADACHBIA}
)
```

### Knowledgeable Voices
Wise and informed, perfect for educational content.

| Voice | Enum Value | Characteristic | Best For |
|-------|------------|----------------|----------|
| Sadaltager | `VoiceName.SADALTAGER` | Knowledgeable | Expert explanations, educational content, informed commentary |

```python
# Usage example
request = AudioRequest(
    text="Research shows that this approach is most effective because...",
    voice_config={"voice_name": VoiceName.SADALTAGER}
)
```

### Warm Voices
Welcoming and friendly, ideal for personal connection.

| Voice | Enum Value | Characteristic | Best For |
|-------|------------|----------------|----------|
| Sulafar | `VoiceName.SULAFAR` | Warm | Welcome messages, personal greetings, friendly content |

```python
# Usage example
request = AudioRequest(
    text="Welcome to our family! We're so glad you're here.",
    voice_config={"voice_name": VoiceName.SULAFAR}
)
```

## 🎯 Voice Selection Guide

### By Content Type

```python
# Content-specific recommendations
VOICE_RECOMMENDATIONS = {
    # Business & Professional
    "business_presentation": VoiceName.KORE,
    "corporate_announcement": VoiceName.ORUS,
    "professional_report": VoiceName.RASALGETHI,
    
    # Educational & Informative
    "tutorial": VoiceName.CHARON,
    "explanation": VoiceName.SADALTAGER,
    "audiobook": VoiceName.SCHEDAR,
    
    # Marketing & Sales
    "advertisement": VoiceName.ZEPHYR,
    "product_launch": VoiceName.PUCK,
    "promotional": VoiceName.LAOMEDEIA,
    
    # Customer Service
    "welcome_message": VoiceName.SULAFAR,
    "help_content": VoiceName.ACHIRD,
    "support": VoiceName.VINDEMIATRIX,
    
    # Entertainment & Media
    "podcast_intro": VoiceName.AOEDE,
    "sports_commentary": VoiceName.FENRIR,
    "character_voice": VoiceName.ALGENIB,
    
    # Personal & Intimate
    "personal_message": VoiceName.ENCELADUS,
    "meditation": VoiceName.ACHERNAR,
    "bedtime_story": VoiceName.VINDEMIATRIX,
    
    # Youth & Modern
    "app_notification": VoiceName.LEDA,
    "social_media": VoiceName.SADACHBIA,
    "gaming": VoiceName.FENRIR,
}
```

### By Audience

```python
# Audience-specific recommendations
AUDIENCE_VOICES = {
    "children": [VoiceName.LEDA, VoiceName.PUCK, VoiceName.SADACHBIA],
    "teenagers": [VoiceName.LEDA, VoiceName.ZEPHYR, VoiceName.LAOMEDEIA],
    "young_adults": [VoiceName.AOEDE, VoiceName.CALLIRHOE, VoiceName.ACHIRD],
    "professionals": [VoiceName.KORE, VoiceName.CHARON, VoiceName.RASALGETHI],
    "seniors": [VoiceName.GACRUX, VoiceName.SCHEDAR, VoiceName.SADALTAGER],
    "general": [VoiceName.SULAFAR, VoiceName.ACHIRD, VoiceName.CHARON],
}
```

## 🔧 Usage Patterns

### Basic Voice Selection

```python
from audio_api import AudioRequest, VoiceName

# Simple voice selection
request = AudioRequest(
    text="Your message here",
    voice_config={"voice_name": VoiceName.SULAFAR}
)
```

### Voice with Customization

```python
# Voice with speed and pitch adjustments
request = AudioRequest(
    text="Your message here",
    voice_config={
        "voice_name": VoiceName.CHARON,
        "speed": 1.1,  # Slightly faster
        "pitch": 1.0   # Normal pitch
    }
)
```

### Dynamic Voice Selection

```python
def select_voice_for_content(content_type: str) -> VoiceName:
    """Select appropriate voice based on content type."""
    voice_map = {
        "greeting": VoiceName.SULAFAR,
        "instruction": VoiceName.CHARON,
        "announcement": VoiceName.KORE,
        "celebration": VoiceName.PUCK,
        "warning": VoiceName.ORUS,
    }
    return voice_map.get(content_type, VoiceName.KORE)

# Usage
voice = select_voice_for_content("greeting")
request = AudioRequest(
    text="Welcome to our service!",
    voice_config={"voice_name": voice}
)
```

## 📊 Voice Characteristics Matrix

| Voice | Bright | Warm | Professional | Casual | Energetic | Calm |
|-------|--------|------|--------------|--------|-----------|------|
| Zephyr | ✅ | | | | ✅ | |
| Sulafar | | ✅ | | ✅ | | |
| Kore | | | ✅ | | | |
| Charon | | | ✅ | | | |
| Puck | ✅ | | | ✅ | ✅ | |
| Achernar | | ✅ | | | | ✅ |
| Gacrux | | | ✅ | | | ✅ |
| Fenrir | ✅ | | | | ✅ | |
| Schedar | | | ✅ | | | ✅ |

## 💡 Best Practices

### Voice Selection Tips

1. **Match Tone to Content**: Choose voices that complement your message's purpose
2. **Consider Your Audience**: Different demographics respond to different voice characteristics
3. **Test Multiple Options**: Generate samples with different voices to find the best fit
4. **Consistency**: Use the same voice throughout a project for brand consistency
5. **Context Matters**: Formal content needs professional voices, casual content can use friendly voices

### Common Combinations

```python
# Effective voice combinations for different scenarios
SCENARIO_VOICES = {
    "onboarding_flow": [
        VoiceName.SULAFAR,    # Welcome
        VoiceName.CHARON,     # Instructions
        VoiceName.PUCK        # Completion
    ],
    "error_handling": [
        VoiceName.ACHERNAR,   # Gentle error message
        VoiceName.ACHIRD,     # Helpful suggestion
        VoiceName.SULAFAR     # Reassurance
    ],
    "product_demo": [
        VoiceName.ZEPHYR,     # Introduction
        VoiceName.CHARON,     # Features explanation
        VoiceName.LAOMEDEIA   # Call to action
    ]
}
```

This comprehensive reference covers all 30 available voices with their characteristics, use cases, and implementation examples. Use this guide to select the perfect voice for your audio generation needs!