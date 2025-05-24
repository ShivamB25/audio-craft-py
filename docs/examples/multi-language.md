# Multi-Language Support Guide

The Audio Generation Library supports 24 languages with proper BCP-47 language codes. This guide shows you how to generate audio in different languages effectively.

## 🌍 All Supported Languages

### Core Languages (12)

```python
from audio_api import AudioRequest, TTSService, Language

async def core_languages():
    tts = TTSService()
    
    core_examples = [
        (Language.ARABIC_EGYPTIAN, "مرحبا بالعالم!", "Arabic (Egyptian)"),
        (Language.ENGLISH_US, "Hello, world!", "English (US)"),
        (Language.GERMAN_GERMANY, "Hallo, Welt!", "German (Germany)"),
        (Language.SPANISH_US, "¡Hola, mundo!", "Spanish (US)"),
        (Language.FRENCH_FRANCE, "Bonjour, le monde!", "French (France)"),
        (Language.HINDI_INDIA, "नमस्ते दुनिया!", "Hindi (India)"),
        (Language.INDONESIAN_INDONESIA, "Halo, dunia!", "Indonesian"),
        (Language.ITALIAN_ITALY, "Ciao, mondo!", "Italian (Italy)"),
        (Language.JAPANESE_JAPAN, "こんにちは世界！", "Japanese (Japan)"),
        (Language.KOREAN_KOREA, "안녕하세요, 세계!", "Korean (Korea)"),
        (Language.PORTUGUESE_BRAZIL, "Olá, mundo!", "Portuguese (Brazil)"),
        (Language.RUSSIAN_RUSSIA, "Привет, мир!", "Russian (Russia)"),
    ]
    
    for lang, text, description in core_examples:
        request = AudioRequest(
            text=text,
            language=lang,
            output_filename=f"hello_{lang.value.replace('-', '_')}.wav"
        )
        
        result = await tts.generate_audio(request)
        if result.success:
            print(f"✅ {description}: {result.file_path}")

import asyncio
asyncio.run(core_languages())
```

### Additional Languages (12)

```python
async def additional_languages():
    tts = TTSService()
    
    additional_examples = [
        (Language.DUTCH_NETHERLANDS, "Hallo, wereld!", "Dutch (Netherlands)"),
        (Language.POLISH_POLAND, "Witaj, świecie!", "Polish (Poland)"),
        (Language.THAI_THAILAND, "สวัสดีชาวโลก!", "Thai (Thailand)"),
        (Language.TURKISH_TURKEY, "Merhaba, dünya!", "Turkish (Turkey)"),
        (Language.VIETNAMESE_VIETNAM, "Xin chào, thế giới!", "Vietnamese"),
        (Language.ROMANIAN_ROMANIA, "Salut, lume!", "Romanian (Romania)"),
        (Language.UKRAINIAN_UKRAINE, "Привіт, світ!", "Ukrainian (Ukraine)"),
        (Language.BENGALI_BANGLADESH, "হ্যালো, বিশ্ব!", "Bengali (Bangladesh)"),
        (Language.ENGLISH_INDIA_HINDI_BUNDLE, "Hello, world! नमस्ते!", "English-Hindi Bundle"),
        (Language.MARATHI_INDIA, "नमस्कार, जग!", "Marathi (India)"),
        (Language.TAMIL_INDIA, "வணக்கம், உலகம்!", "Tamil (India)"),
        (Language.TELUGU_INDIA, "హలో, ప్రపంచం!", "Telugu (India)"),
    ]
    
    for lang, text, description in additional_examples:
        request = AudioRequest(
            text=text,
            language=lang,
            output_filename=f"hello_{lang.value.replace('-', '_')}.wav"
        )
        
        result = await tts.generate_audio(request)
        if result.success:
            print(f"✅ {description}: {result.file_path}")

asyncio.run(additional_languages())
```

## 🎯 Language-Specific Examples

### Business Greetings

```python
async def business_greetings():
    tts = TTSService()
    
    business_phrases = [
        (Language.ENGLISH_US, "Good morning, welcome to our company."),
        (Language.SPANISH_US, "Buenos días, bienvenido a nuestra empresa."),
        (Language.FRENCH_FRANCE, "Bonjour, bienvenue dans notre entreprise."),
        (Language.GERMAN_GERMANY, "Guten Morgen, willkommen in unserem Unternehmen."),
        (Language.JAPANESE_JAPAN, "おはようございます。弊社へようこそ。"),
        (Language.KOREAN_KOREA, "안녕하세요, 저희 회사에 오신 것을 환영합니다."),
        (Language.CHINESE, "早上好，欢迎来到我们公司。"),
    ]
    
    for lang, text in business_phrases:
        request = AudioRequest(
            text=text,
            language=lang,
            voice_config={"voice_name": VoiceName.KORE},  # Professional voice
            output_filename=f"business_{lang.value.replace('-', '_')}.wav"
        )
        
        result = await tts.generate_audio(request)
        if result.success:
            print(f"✅ Business greeting in {lang.name}")

asyncio.run(business_greetings())
```

### Educational Content

```python
async def educational_content():
    tts = TTSService()
    
    educational_phrases = [
        (Language.ENGLISH_US, "Today we will learn about renewable energy sources."),
        (Language.SPANISH_US, "Hoy aprenderemos sobre fuentes de energía renovable."),
        (Language.FRENCH_FRANCE, "Aujourd'hui, nous allons apprendre les sources d'énergie renouvelable."),
        (Language.HINDI_INDIA, "आज हम नवीकरणीय ऊर्जा स्रोतों के बारे में सीखेंगे।"),
        (Language.ARABIC_EGYPTIAN, "اليوم سنتعلم عن مصادر الطاقة المتجددة."),
    ]
    
    for lang, text in educational_phrases:
        request = AudioRequest(
            text=text,
            language=lang,
            voice_config={"voice_name": VoiceName.CHARON},  # Informative voice
            output_filename=f"education_{lang.value.replace('-', '_')}.wav"
        )
        
        result = await tts.generate_audio(request)
        if result.success:
            print(f"✅ Educational content in {lang.name}")

asyncio.run(educational_content())
```

### Customer Service

```python
async def customer_service():
    tts = TTSService()
    
    service_phrases = [
        (Language.ENGLISH_US, "Thank you for calling. How can I help you today?"),
        (Language.SPANISH_US, "Gracias por llamar. ¿Cómo puedo ayudarle hoy?"),
        (Language.FRENCH_FRANCE, "Merci d'avoir appelé. Comment puis-je vous aider aujourd'hui?"),
        (Language.GERMAN_GERMANY, "Danke für Ihren Anruf. Wie kann ich Ihnen heute helfen?"),
        (Language.ITALIAN_ITALY, "Grazie per aver chiamato. Come posso aiutarla oggi?"),
        (Language.PORTUGUESE_BRAZIL, "Obrigado por ligar. Como posso ajudá-lo hoje?"),
    ]
    
    for lang, text in service_phrases:
        request = AudioRequest(
            text=text,
            language=lang,
            voice_config={"voice_name": VoiceName.SULAFAR},  # Warm voice
            output_filename=f"service_{lang.value.replace('-', '_')}.wav"
        )
        
        result = await tts.generate_audio(request)
        if result.success:
            print(f"✅ Customer service in {lang.name}")

asyncio.run(customer_service())
```

## 🎭 Language + Voice Combinations

### Matching Voices to Languages

```python
async def language_voice_combinations():
    tts = TTSService()
    
    # Recommended voice-language combinations
    combinations = [
        # Warm languages with warm voices
        (Language.SPANISH_US, VoiceName.SULAFAR, "¡Bienvenidos a nuestro hogar!"),
        (Language.ITALIAN_ITALY, VoiceName.ACHIRD, "Benvenuti nella nostra famiglia!"),
        
        # Professional languages with firm voices
        (Language.GERMAN_GERMANY, VoiceName.KORE, "Wir garantieren höchste Qualität."),
        (Language.ENGLISH_US, VoiceName.ORUS, "We deliver professional excellence."),
        
        # Educational content with informative voices
        (Language.FRENCH_FRANCE, VoiceName.CHARON, "Explorons les merveilles de la science."),
        (Language.JAPANESE_JAPAN, VoiceName.RASALGETHI, "科学の素晴らしさを探求しましょう。"),
        
        # Energetic content with bright voices
        (Language.KOREAN_KOREA, VoiceName.ZEPHYR, "새로운 모험을 시작해봅시다!"),
        (Language.HINDI_INDIA, VoiceName.PUCK, "आइए एक नया साहसिक कार्य शुरू करते हैं!"),
    ]
    
    for lang, voice, text in combinations:
        request = AudioRequest(
            text=text,
            language=lang,
            voice_config={"voice_name": voice},
            output_filename=f"combo_{lang.value.replace('-', '_')}_{voice.value.lower()}.wav"
        )
        
        result = await tts.generate_audio(request)
        if result.success:
            print(f"✅ {lang.name} + {voice.value}: {result.file_path}")

asyncio.run(language_voice_combinations())
```

## 🌏 Regional Variants

### Understanding Regional Differences

```python
async def regional_variants():
    tts = TTSService()
    
    # Same language, different regions
    regional_examples = [
        # English variants
        (Language.ENGLISH_US, "I'm going to the store to buy some candy."),
        (Language.ENGLISH_INDIA_HINDI_BUNDLE, "I'm going to the shop to buy some sweets."),
        
        # Spanish variants (US Spanish vs others)
        (Language.SPANISH_US, "Voy a la tienda a comprar dulces."),
        
        # French (France specific)
        (Language.FRENCH_FRANCE, "Je vais au magasin acheter des bonbons."),
        
        # German (Germany specific)
        (Language.GERMAN_GERMANY, "Ich gehe in den Laden, um Süßigkeiten zu kaufen."),
    ]
    
    for lang, text in regional_examples:
        request = AudioRequest(
            text=text,
            language=lang,
            output_filename=f"regional_{lang.value.replace('-', '_')}.wav"
        )
        
        result = await tts.generate_audio(request)
        if result.success:
            print(f"✅ {lang.name}: {result.file_path}")

asyncio.run(regional_variants())
```

## 🔄 Backward Compatibility

### Using Legacy Language Codes

```python
async def backward_compatibility():
    tts = TTSService()
    
    # Old style (still works)
    legacy_examples = [
        (Language.ENGLISH, "This uses the legacy English code"),
        (Language.SPANISH, "Esto usa el código español heredado"),
        (Language.FRENCH, "Ceci utilise le code français hérité"),
        (Language.GERMAN, "Dies verwendet den alten deutschen Code"),
        (Language.ITALIAN, "Questo usa il codice italiano legacy"),
        (Language.PORTUGUESE, "Isso usa o código português legado"),
        (Language.RUSSIAN, "Это использует устаревший русский код"),
        (Language.JAPANESE, "これは従来の日本語コードを使用します"),
        (Language.KOREAN, "이것은 레거시 한국어 코드를 사용합니다"),
    ]
    
    for lang, text in legacy_examples:
        request = AudioRequest(
            text=text,
            language=lang,
            output_filename=f"legacy_{lang.name.lower()}.wav"
        )
        
        result = await tts.generate_audio(request)
        if result.success:
            print(f"✅ Legacy {lang.name}: {result.file_path}")

asyncio.run(backward_compatibility())
```

## 🎯 Language Detection vs Explicit Setting

### Automatic vs Manual Language Setting

```python
async def language_detection_demo():
    tts = TTSService()
    
    # Gemini TTS can auto-detect, but explicit is better
    mixed_content = [
        # Auto-detection (not recommended for mixed content)
        AudioRequest(
            text="Hello world! Bonjour le monde! ¡Hola mundo!",
            # No language specified - will auto-detect
            output_filename="auto_detect.wav"
        ),
        
        # Explicit language (recommended)
        AudioRequest(
            text="Hello world! This is clearly English content.",
            language=Language.ENGLISH_US,
            output_filename="explicit_english.wav"
        ),
        
        AudioRequest(
            text="Bonjour le monde! Ceci est clairement du contenu français.",
            language=Language.FRENCH_FRANCE,
            output_filename="explicit_french.wav"
        ),
    ]
    
    for request in mixed_content:
        result = await tts.generate_audio(request)
        if result.success:
            print(f"✅ Generated: {result.file_path}")

asyncio.run(language_detection_demo())
```

## 📚 Complete Language Reference

### All 24 Languages with Codes

```python
# Complete language reference
LANGUAGE_REFERENCE = {
    # Core Languages
    "ar-EG": (Language.ARABIC_EGYPTIAN, "Arabic (Egyptian)"),
    "en-US": (Language.ENGLISH_US, "English (United States)"),
    "de-DE": (Language.GERMAN_GERMANY, "German (Germany)"),
    "es-US": (Language.SPANISH_US, "Spanish (United States)"),
    "fr-FR": (Language.FRENCH_FRANCE, "French (France)"),
    "hi-IN": (Language.HINDI_INDIA, "Hindi (India)"),
    "id-ID": (Language.INDONESIAN_INDONESIA, "Indonesian (Indonesia)"),
    "it-IT": (Language.ITALIAN_ITALY, "Italian (Italy)"),
    "ja-JP": (Language.JAPANESE_JAPAN, "Japanese (Japan)"),
    "ko-KR": (Language.KOREAN_KOREA, "Korean (Korea)"),
    "pt-BR": (Language.PORTUGUESE_BRAZIL, "Portuguese (Brazil)"),
    "ru-RU": (Language.RUSSIAN_RUSSIA, "Russian (Russia)"),
    
    # Additional Languages
    "nl-NL": (Language.DUTCH_NETHERLANDS, "Dutch (Netherlands)"),
    "pl-PL": (Language.POLISH_POLAND, "Polish (Poland)"),
    "th-TH": (Language.THAI_THAILAND, "Thai (Thailand)"),
    "tr-TR": (Language.TURKISH_TURKEY, "Turkish (Turkey)"),
    "vi-VN": (Language.VIETNAMESE_VIETNAM, "Vietnamese (Vietnam)"),
    "ro-RO": (Language.ROMANIAN_ROMANIA, "Romanian (Romania)"),
    "uk-UA": (Language.UKRAINIAN_UKRAINE, "Ukrainian (Ukraine)"),
    "bn-BD": (Language.BENGALI_BANGLADESH, "Bengali (Bangladesh)"),
    "en-IN": (Language.ENGLISH_INDIA_HINDI_BUNDLE, "English (India) & Hindi"),
    "mr-IN": (Language.MARATHI_INDIA, "Marathi (India)"),
    "ta-IN": (Language.TAMIL_INDIA, "Tamil (India)"),
    "te-IN": (Language.TELUGU_INDIA, "Telugu (India)"),
}

async def test_all_languages():
    """Test all 24 supported languages"""
    tts = TTSService()
    
    # Generic greeting in each language
    greetings = {
        "ar-EG": "مرحبا ومرحبا بكم",
        "en-US": "Hello and welcome",
        "de-DE": "Hallo und willkommen",
        "es-US": "Hola y bienvenidos",
        "fr-FR": "Bonjour et bienvenue",
        "hi-IN": "नमस्ते और स्वागत है",
        "id-ID": "Halo dan selamat datang",
        "it-IT": "Ciao e benvenuti",
        "ja-JP": "こんにちは、ようこそ",
        "ko-KR": "안녕하세요, 환영합니다",
        "pt-BR": "Olá e bem-vindos",
        "ru-RU": "Привет и добро пожаловать",
        "nl-NL": "Hallo en welkom",
        "pl-PL": "Cześć i witamy",
        "th-TH": "สวัสดีและยินดีต้อนรับ",
        "tr-TR": "Merhaba ve hoş geldiniz",
        "vi-VN": "Xin chào và chào mừng",
        "ro-RO": "Salut și bun venit",
        "uk-UA": "Привіт і ласкаво просимо",
        "bn-BD": "হ্যালো এবং স্বাগতম",
        "en-IN": "Hello and welcome, नमस्ते",
        "mr-IN": "नमस्कार आणि स्वागत",
        "ta-IN": "வணக்கம் மற்றும் வரவேற்கிறோம்",
        "te-IN": "హలో మరియు స్వాగతం",
    }
    
    for code, (lang_enum, description) in LANGUAGE_REFERENCE.items():
        text = greetings.get(code, "Hello and welcome")
        
        request = AudioRequest(
            text=text,
            language=lang_enum,
            output_filename=f"test_{code.replace('-', '_')}.wav"
        )
        
        result = await tts.generate_audio(request)
        if result.success:
            print(f"✅ {code:5} - {description}")
        else:
            print(f"❌ {code:5} - Failed: {result.error}")

# Run comprehensive test
asyncio.run(test_all_languages())
```

## 💡 Best Practices

### Language Selection Tips

1. **Use Specific Codes**: Prefer `Language.ENGLISH_US` over `Language.ENGLISH`
2. **Match Content**: Ensure the language code matches your text content
3. **Regional Awareness**: Consider regional differences (US vs UK English, etc.)
4. **Voice Pairing**: Some voices work better with certain languages
5. **Testing**: Always test with native speakers when possible

### Common Pitfalls

```python
# ❌ Don't do this
request = AudioRequest(
    text="Hello world",  # English text
    language=Language.SPANISH_US  # Spanish language setting
)

# ✅ Do this instead
request = AudioRequest(
    text="Hello world",
    language=Language.ENGLISH_US  # Matching language
)

# ✅ Or this for Spanish
request = AudioRequest(
    text="Hola mundo",
    language=Language.SPANISH_US
)
```

## 🧪 Testing Multi-Language

Use the provided test script:

```bash
python test_languages.py
```

This will generate audio samples in multiple languages to verify everything works correctly.

## 🌐 International Applications

### Building Multi-Language Apps

```python
async def international_app_example():
    """Example of building content for international users"""
    tts = TTSService()
    
    # User preferences
    user_languages = [
        Language.ENGLISH_US,
        Language.SPANISH_US,
        Language.FRENCH_FRANCE,
        Language.GERMAN_GERMANY,
    ]
    
    # Same message in multiple languages
    messages = {
        Language.ENGLISH_US: "Your order has been confirmed.",
        Language.SPANISH_US: "Su pedido ha sido confirmado.",
        Language.FRENCH_FRANCE: "Votre commande a été confirmée.",
        Language.GERMAN_GERMANY: "Ihre Bestellung wurde bestätigt.",
    }
    
    # Generate for each language
    for lang in user_languages:
        request = AudioRequest(
            text=messages[lang],
            language=lang,
            voice_config={"voice_name": VoiceName.SULAFAR},  # Friendly voice
            output_filename=f"order_confirmation_{lang.value.replace('-', '_')}.wav"
        )
        
        result = await tts.generate_audio(request)
        if result.success:
            print(f"✅ Order confirmation ready for {lang.name}")

asyncio.run(international_app_example())
```

This comprehensive guide covers all aspects of multi-language support in the Audio Generation Library. Use these examples as starting points for your international audio projects!