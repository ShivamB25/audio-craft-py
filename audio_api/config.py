"""
Centralized configuration management for the Audio Generation Library.
"""

import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def _safe_int(value: str, default: int) -> int:
    """
    Safely convert a string to int, returning default on failure.
    
    Args:
        value: String value to convert
        default: Default value to return if conversion fails
        
    Returns:
        Converted integer or default value
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


class AudioConfig(BaseModel):
    """Centralized configuration for the audio generation library."""

    # API Configuration
    gemini_api_key: str = Field(
        default_factory=lambda: os.getenv("GEMINI_API_KEY", ""),
        description="Google Gemini API key",
    )
    default_model: str = Field(
        default_factory=lambda: os.getenv(
            "DEFAULT_TTS_MODEL", "gemini-2.5-pro-preview-tts"
        ),
        description="Default TTS model to use",
    )

    # Audio Configuration
    output_dir: str = Field(
        default_factory=lambda: os.getenv("OUTPUT_DIR", "output"),
        description="Directory for output audio files",
    )
    default_sample_rate: int = Field(
        default_factory=lambda: _safe_int(os.getenv("DEFAULT_SAMPLE_RATE", "24000"), 24000),
        description="Default audio sample rate in Hz",
    )
    default_bit_depth: int = Field(
        default_factory=lambda: _safe_int(os.getenv("DEFAULT_BIT_DEPTH", "16"), 16),
        description="Default audio bit depth",
    )
    default_channels: int = Field(
        default_factory=lambda: _safe_int(os.getenv("DEFAULT_CHANNELS", "1"), 1),
        description="Default number of audio channels",
    )

    # Performance Configuration
    max_context_tokens: int = Field(
        default_factory=lambda: _safe_int(os.getenv("MAX_CONTEXT_TOKENS", "32000"), 32000),
        description="Maximum context tokens for Gemini TTS",
    )
    retry_attempts: int = Field(
        default_factory=lambda: _safe_int(os.getenv("RETRY_ATTEMPTS", "3"), 3),
        description="Number of retry attempts for API calls",
    )
    retry_min_wait: int = Field(
        default_factory=lambda: _safe_int(os.getenv("RETRY_MIN_WAIT", "4"), 4),
        description="Minimum wait time between retries (seconds)",
    )
    retry_max_wait: int = Field(
        default_factory=lambda: _safe_int(os.getenv("RETRY_MAX_WAIT", "10"), 10),
        description="Maximum wait time between retries (seconds)",
    )

    # Redis Configuration
    redis_url: str = Field(
        default_factory=lambda: os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        description="Redis connection URL",
    )
    redis_pool_size: int = Field(
        default_factory=lambda: _safe_int(os.getenv("REDIS_POOL_SIZE", "10"), 10),
        description="Redis connection pool size",
    )

    # Worker Configuration
    num_workers: int = Field(
        default_factory=lambda: _safe_int(os.getenv("NUM_WORKERS", "3"), 3),
        description="Number of worker processes",
    )
    task_timeout: int = Field(
        default_factory=lambda: _safe_int(os.getenv("TASK_TIMEOUT", "300"), 300),
        description="Task timeout in seconds",
    )

    # Logging Configuration
    log_level: str = Field(
        default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"),
        description="Logging level",
    )
    enable_structured_logging: bool = Field(
        default_factory=lambda: os.getenv("ENABLE_STRUCTURED_LOGGING", "false").lower()
        == "true",
        description="Enable structured logging",
    )

    # Validation Configuration
    min_audio_size: int = Field(
        default_factory=lambda: _safe_int(os.getenv("MIN_AUDIO_SIZE", "1000"), 1000),
        description="Minimum audio file size in bytes",
    )
    max_text_length: int = Field(
        default_factory=lambda: _safe_int(os.getenv("MAX_TEXT_LENGTH", "10000"), 10000),
        description="Maximum text length for TTS",
    )

    def validate_config(self) -> None:
        """Validate configuration values."""
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is required")

        if self.max_context_tokens <= 0:
            raise ValueError("MAX_CONTEXT_TOKENS must be positive")

        if self.retry_attempts < 0:
            raise ValueError("RETRY_ATTEMPTS must be non-negative")

        if self.default_sample_rate <= 0:
            raise ValueError("DEFAULT_SAMPLE_RATE must be positive")

    @classmethod
    def load_config(cls) -> "AudioConfig":
        """Load and validate configuration."""
        config = cls()
        config.validate_config()
        return config


# Global configuration instance
_config: Optional[AudioConfig] = None


def get_config() -> AudioConfig:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = AudioConfig.load_config()
    return _config


def reload_config() -> AudioConfig:
    """Reload configuration from environment."""
    global _config
    load_dotenv(override=True)  # Reload .env file
    _config = AudioConfig.load_config()
    return _config
