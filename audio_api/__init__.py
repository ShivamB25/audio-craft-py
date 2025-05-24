"""Audio Generation API Package."""

__version__ = "1.0.0"

from .models import (
    AudioRequest,
    BatchAudioRequest,
    AudioResponse,
    BatchAudioResponse,
    VoiceModel,
    SpeakerMode,
    Language,
    AudioFormat,
    VoiceConfig,
    VoiceName,
    SpeakerConfig,
    MultiSpeakerConfig,
)
from .services import TTSService, QueueService, WorkerService, WorkerManager

__all__ = [
    "AudioRequest",
    "BatchAudioRequest",
    "AudioResponse",
    "BatchAudioResponse",
    "VoiceModel",
    "SpeakerMode",
    "Language",
    "AudioFormat",
    "VoiceConfig",
    "VoiceName",
    "SpeakerConfig",
    "MultiSpeakerConfig",
    "TTSService",
    "QueueService",
    "WorkerService",
    "WorkerManager",
]
