from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from enum import Enum
import os


class VoiceModel(str, Enum):
    GEMINI_TTS_PRO = "gemini-2.5-pro-preview-tts"
    GEMINI_TTS_FLASH = "gemini-2.5-flash-preview-tts"
    
    # Backward compatibility
    GEMINI_TTS = "gemini-2.5-pro-preview-tts"


class SpeakerMode(str, Enum):
    SINGLE = "single"
    MULTIPLE = "multiple"


class Language(str, Enum):
    # Original languages (keeping for backward compatibility)
    ENGLISH = "en-US"
    SPANISH = "es-US"
    FRENCH = "fr-FR"
    GERMAN = "de-DE"
    ITALIAN = "it-IT"
    PORTUGUESE = "pt-BR"
    RUSSIAN = "ru-RU"
    JAPANESE = "ja-JP"
    KOREAN = "ko-KR"
    CHINESE = "zh"  # Keeping as is for backward compatibility
    
    # All 24 supported languages with proper BCP-47 codes
    ARABIC_EGYPTIAN = "ar-EG"
    ENGLISH_US = "en-US"
    GERMAN_GERMANY = "de-DE"
    SPANISH_US = "es-US"
    FRENCH_FRANCE = "fr-FR"
    HINDI_INDIA = "hi-IN"
    INDONESIAN_INDONESIA = "id-ID"
    ITALIAN_ITALY = "it-IT"
    JAPANESE_JAPAN = "ja-JP"
    KOREAN_KOREA = "ko-KR"
    PORTUGUESE_BRAZIL = "pt-BR"
    RUSSIAN_RUSSIA = "ru-RU"
    DUTCH_NETHERLANDS = "nl-NL"
    POLISH_POLAND = "pl-PL"
    THAI_THAILAND = "th-TH"
    TURKISH_TURKEY = "tr-TR"
    VIETNAMESE_VIETNAM = "vi-VN"
    ROMANIAN_ROMANIA = "ro-RO"
    UKRAINIAN_UKRAINE = "uk-UA"
    BENGALI_BANGLADESH = "bn-BD"
    ENGLISH_INDIA_HINDI_BUNDLE = "en-IN"  # Special bundle case
    MARATHI_INDIA = "mr-IN"
    TAMIL_INDIA = "ta-IN"
    TELUGU_INDIA = "te-IN"


class VoiceName(str, Enum):
    # Bright Voices
    ZEPHYR = "zephyr"  # Bright
    AUTONOE = "autonoe"  # Bright
    
    # Upbeat Voices
    PUCK = "puck"  # Upbeat
    LAOMEDEIA = "laomedeia"  # Upbeat
    
    # Informative Voices
    CHARON = "charon"  # Informative
    RASALGETHI = "rasalgethi"  # Informative
    
    # Firm Voices
    KORE = "kore"  # Firm (default)
    ORUS = "orus"  # Firm
    ALNILAM = "alnilam"  # Firm
    
    # Excitable Voices
    FENRIR = "fenrir"  # Excitable
    
    # Youthful Voices
    LEDA = "leda"  # Youthful
    
    # Breezy Voices
    AOEDE = "aoede"  # Breezy
    
    # Easy-going Voices
    CALLIRRHOE = "callirrhoe"  # Easy-going (fixed spelling: double 'r')
    UMBRIEL = "umbriel"  # Easy-going
    
    # Breathy Voices
    ENCELADUS = "enceladus"  # Breathy
    
    # Clear Voices
    IAPETUS = "iapetus"  # Clear
    ERINOME = "erinome"  # Clear
    
    # Smooth Voices
    ALGIEBA = "algieba"  # Smooth
    DESPINA = "despina"  # Smooth
    
    # Gravelly Voices
    ALGENIB = "algenib"  # Gravelly
    
    # Soft Voices
    ACHERNAR = "achernar"  # Soft
    
    # Even Voices
    SCHEDAR = "schedar"  # Even
    
    # Mature Voices
    GACRUX = "gacrux"  # Mature
    
    # Friendly Voices
    ACHIRD = "achird"  # Friendly
    
    # Casual Voices
    ZUBENELGENUBI = "zubenelgenubi"  # Casual
    
    # Forward Voices
    PULCHERRIMA = "pulcherrima"  # Forward
    
    # Gentle Voices
    VINDEMIATRIX = "vindemiatrix"  # Gentle
    
    # Lively Voices
    SADACHBIA = "sadachbia"  # Lively
    
    # Knowledgeable Voices
    SADALTAGER = "sadaltager"  # Knowledgeable
    
    # Warm Voices
    SULAFAT = "sulafat"  # Warm (fixed spelling: ends with 't')


class AudioFormat(BaseModel):
    sample_rate: int = Field(default=24000, description="Sample rate in Hz")
    bit_depth: int = Field(default=16, description="Bit depth")
    channels: int = Field(default=1, description="Number of channels")


class VoiceConfig(BaseModel):
    voice_name: VoiceName = Field(default=VoiceName.KORE, description="Voice name for TTS")
    speed: Optional[float] = Field(default=None, ge=0.1, le=3.0, description="Speech speed (controlled via prompt)")
    pitch: Optional[float] = Field(default=None, ge=0.1, le=2.0, description="Speech pitch (controlled via prompt)")


class SpeakerConfig(BaseModel):
    """Configuration for a single speaker in multi-speaker TTS."""
    speaker_name: str = Field(..., description="Name of the speaker (must match name in text)")
    voice_name: VoiceName = Field(..., description="Voice to use for this speaker")


class MultiSpeakerConfig(BaseModel):
    """Configuration for multi-speaker TTS with up to 2 speakers."""
    speakers: List[SpeakerConfig] = Field(
        ..., min_items=2, max_items=2, description="List of speaker configurations (exactly 2 speakers)"
    )


class AudioRequest(BaseModel):
    text: str = Field(
        ..., min_length=1, max_length=10000, description="Text to convert to speech"
    )
    model: VoiceModel = Field(
        default_factory=lambda: VoiceModel(os.getenv("DEFAULT_TTS_MODEL", "gemini-2.5-pro-preview-tts")),
        description="TTS model to use (configurable via DEFAULT_TTS_MODEL env var)"
    )
    speaker_mode: SpeakerMode = Field(
        default=SpeakerMode.SINGLE, description="Single or multiple speaker mode"
    )
    language: Language = Field(default=Language.ENGLISH, description="Language for TTS")
    voice_config: Optional[VoiceConfig] = Field(
        default_factory=VoiceConfig, description="Voice configuration for single speaker mode"
    )
    multi_speaker_config: Optional[MultiSpeakerConfig] = Field(
        default=None, description="Multi-speaker configuration (required when speaker_mode=MULTIPLE)"
    )
    audio_format: AudioFormat = Field(
        default_factory=AudioFormat, description="Audio output format"
    )
    output_filename: Optional[str] = Field(
        default=None, description="Custom output filename"
    )
    
    def model_post_init(self, __context) -> None:
        """Validate speaker mode configuration."""
        if self.speaker_mode == SpeakerMode.MULTIPLE:
            if not self.multi_speaker_config:
                raise ValueError("multi_speaker_config is required when speaker_mode=MULTIPLE")
        elif self.speaker_mode == SpeakerMode.SINGLE:
            if self.multi_speaker_config:
                raise ValueError("multi_speaker_config should not be provided when speaker_mode=SINGLE")


class BatchAudioRequest(BaseModel):
    requests: List[AudioRequest] = Field(
        ..., min_items=1, max_items=100, description="List of audio requests"
    )
    batch_id: Optional[str] = Field(default=None, description="Custom batch ID")


class AudioResponse(BaseModel):
    success: bool
    message: str
    file_path: Optional[str] = None
    duration: Optional[float] = None
    error: Optional[str] = None


class BatchAudioResponse(BaseModel):
    batch_id: str
    total_requests: int
    completed: int
    failed: int
    results: List[AudioResponse]
    status: Literal["pending", "processing", "completed", "failed"]
