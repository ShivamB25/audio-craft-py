import wave
import os
import asyncio
import aiofiles
import time
from typing import Optional, Dict, Any
from google import genai
from google.genai import types
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from audio_api.models import (
    AudioRequest,
    AudioResponse,
    VoiceModel,
    Language,
    SpeakerMode,
)
from audio_api.config import get_config, AudioConfig
from audio_api.logging_config import get_logger, log_performance, log_error_with_context

logger = get_logger(__name__)


class TTSError(Exception):
    """Base exception for TTS operations."""

    pass


class TTSAPIError(TTSError):
    """API-related errors that should be retried."""

    pass


class TTSValidationError(TTSError):
    """Validation errors that should not be retried."""

    pass


class TTSQuotaError(TTSError):
    """Quota exceeded errors."""

    pass


class TTSService:
    """
    Text-to-Speech service using Google Gemini TTS API.

    Note: Streaming audio is not supported in this library. While the Gemini API
    supports streaming, this library focuses on file-based audio generation for
    better reliability and simpler integration patterns.
    """

    def __init__(
        self,
        config: Optional[AudioConfig] = None,
        gemini_client: Optional[genai.Client] = None,
    ):
        """
        Initialize TTS service with dependency injection support.

        Args:
            config: Configuration instance (uses global config if None)
            gemini_client: Pre-configured Gemini client (creates new if None)
        """
        self.config = config or get_config()
        self.gemini_client = gemini_client or genai.Client(
            api_key=self.config.gemini_api_key
        )

    async def generate_audio(self, request: AudioRequest) -> AudioResponse:
        """Generate audio from text using Gemini TTS with retry logic and structured logging."""
        start_time = time.time()
        context = {
            "text_length": len(request.text),
            "language": request.language.value,
            "model": request.model.value,
            "speaker_mode": request.speaker_mode.value,
            "voice_name": getattr(request.voice_config, "voice_name", None),
        }

        try:
            logger.info("Starting audio generation", extra=context)
            result = await self._generate_gemini_audio_with_retry(request)
            duration = time.time() - start_time

            # Log performance metrics
            log_performance(
                logger,
                "audio_generation",
                duration,
                text_length=len(request.text),
                language=request.language.value,
                success=result.success,
            )

            return result

        except TTSValidationError as e:
            duration = time.time() - start_time
            log_error_with_context(
                logger, e, {**context, "duration": duration, "error_type": "validation"}
            )
            return AudioResponse(
                success=False, message="Validation failed", error=str(e)
            )
        except TTSQuotaError as e:
            duration = time.time() - start_time
            log_error_with_context(
                logger, e, {**context, "duration": duration, "error_type": "quota"}
            )
            return AudioResponse(
                success=False, message="API quota exceeded", error=str(e)
            )
        except Exception as e:
            duration = time.time() - start_time
            log_error_with_context(
                logger, e, {**context, "duration": duration, "error_type": "unexpected"}
            )
            return AudioResponse(
                success=False, message="Failed to generate audio", error=str(e)
            )

    async def _generate_gemini_audio_with_retry(
        self, request: AudioRequest
    ) -> AudioResponse:
        """Generate audio with retry logic for API errors."""
        # Create retry decorator with config values
        retry_decorator = retry(
            stop=stop_after_attempt(self.config.retry_attempts),
            wait=wait_exponential(
                multiplier=1,
                min=self.config.retry_min_wait,
                max=self.config.retry_max_wait,
            ),
            retry=retry_if_exception_type(TTSAPIError),
        )

        @retry_decorator
        async def _generate_with_retry():
            try:
                return await self._generate_gemini_audio(request)
            except Exception as e:
                error_msg = str(e).lower()

                # Categorize errors for appropriate retry behavior
                if "invalid_argument" in error_msg or "validation" in error_msg:
                    raise TTSValidationError(f"Invalid request parameters: {str(e)}")
                elif "quota" in error_msg or "rate_limit" in error_msg:
                    raise TTSQuotaError(f"API quota exceeded: {str(e)}")
                elif (
                    "unavailable" in error_msg
                    or "timeout" in error_msg
                    or "connection" in error_msg
                ):
                    logger.warning(f"Retryable API error: {str(e)}")
                    raise TTSAPIError(f"API temporarily unavailable: {str(e)}")
                else:
                    # Unknown error, don't retry
                    raise TTSError(f"Unknown TTS error: {str(e)}")

        return await _generate_with_retry()

    async def _generate_gemini_audio(self, request: AudioRequest) -> AudioResponse:
        """Generate audio using Gemini TTS."""
        # Configure speech settings based on speaker mode
        if request.speaker_mode == SpeakerMode.SINGLE:
            speech_config = self._create_single_speaker_config(request)
        else:  # MULTIPLE
            speech_config = self._create_multi_speaker_config(request)

        # Validate context window (32k tokens limit)
        formatted_text = self._format_text_for_gemini(request)
        self._validate_context_window(formatted_text)

        # Generate content with audio
        response = await asyncio.to_thread(
            self.gemini_client.models.generate_content,
            model=request.model.value,
            contents=formatted_text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=speech_config,
            ),
        )

        # Validate response structure
        if not response.candidates or not response.candidates[0].content.parts:
            raise TTSAPIError("Invalid response structure from Gemini API")

        # Extract and validate audio data
        audio_data = response.candidates[0].content.parts[0].inline_data.data
        self._validate_audio_data(audio_data)

        # Generate filename
        filename = request.output_filename or f"audio_{hash(request.text)}.wav"
        if not filename.endswith(".wav"):
            filename += ".wav"

        # Save as WAV with specified format
        file_path = await self._save_wav_file(
            filename,
            audio_data,
            request.audio_format.channels,
            request.audio_format.sample_rate,
            request.audio_format.bit_depth // 8,
        )

        # Validate saved file
        await self._validate_saved_audio_file(file_path)

        return AudioResponse(
            success=True,
            message="Audio generated successfully",
            file_path=file_path,
        )

    def _create_single_speaker_config(
        self, request: AudioRequest
    ) -> types.SpeechConfig:
        """Create speech config for single speaker."""
        voice_config = types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                voice_name=request.voice_config.voice_name
            )
        )
        return types.SpeechConfig(voice_config=voice_config)

    def _create_multi_speaker_config(self, request: AudioRequest) -> types.SpeechConfig:
        """Create speech config for multi-speaker."""
        speaker_voice_configs = []

        for speaker in request.multi_speaker_config.speakers:
            speaker_voice_config = types.SpeakerVoiceConfig(
                speaker=speaker.speaker_name,
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=speaker.voice_name
                    )
                ),
            )
            speaker_voice_configs.append(speaker_voice_config)

        multi_speaker_config = types.MultiSpeakerVoiceConfig(
            speaker_voice_configs=speaker_voice_configs
        )

        return types.SpeechConfig(multi_speaker_voice_config=multi_speaker_config)

    def _format_text_for_gemini(self, request: AudioRequest) -> str:
        """Format text with language, speaker, and style instructions for Gemini."""

        # Get language prefix
        language_prefix = self._get_language_prefix(request.language)

        # Get style instructions for speed/pitch
        style_instructions = self._get_style_instructions(request)

        # Combine all instructions
        instructions = []
        if language_prefix:
            instructions.append(language_prefix)
        if style_instructions:
            instructions.append(style_instructions)

        # Format final text
        if instructions:
            instruction_text = " ".join(instructions)
            return f"{instruction_text} {request.text}"
        else:
            return request.text

    def _get_language_prefix(self, language: Language) -> str:
        """Get language instruction prefix."""
        language_instructions = {
            # Original languages (backward compatibility)
            Language.ENGLISH: "",
            Language.SPANISH: "[Language: Spanish]",
            Language.FRENCH: "[Language: French]",
            Language.GERMAN: "[Language: German]",
            Language.ITALIAN: "[Language: Italian]",
            Language.PORTUGUESE: "[Language: Portuguese]",
            Language.RUSSIAN: "[Language: Russian]",
            Language.JAPANESE: "[Language: Japanese]",
            Language.KOREAN: "[Language: Korean]",
            Language.CHINESE: "[Language: Chinese]",
            # All 24 supported languages with BCP-47 codes
            Language.ARABIC_EGYPTIAN: "[Language: Arabic (Egyptian)]",
            Language.ENGLISH_US: "",  # Default, no prefix needed
            Language.GERMAN_GERMANY: "[Language: German]",
            Language.SPANISH_US: "[Language: Spanish]",
            Language.FRENCH_FRANCE: "[Language: French]",
            Language.HINDI_INDIA: "[Language: Hindi]",
            Language.INDONESIAN_INDONESIA: "[Language: Indonesian]",
            Language.ITALIAN_ITALY: "[Language: Italian]",
            Language.JAPANESE_JAPAN: "[Language: Japanese]",
            Language.KOREAN_KOREA: "[Language: Korean]",
            Language.PORTUGUESE_BRAZIL: "[Language: Portuguese]",
            Language.RUSSIAN_RUSSIA: "[Language: Russian]",
            Language.DUTCH_NETHERLANDS: "[Language: Dutch]",
            Language.POLISH_POLAND: "[Language: Polish]",
            Language.THAI_THAILAND: "[Language: Thai]",
            Language.TURKISH_TURKEY: "[Language: Turkish]",
            Language.VIETNAMESE_VIETNAM: "[Language: Vietnamese]",
            Language.ROMANIAN_ROMANIA: "[Language: Romanian]",
            Language.UKRAINIAN_UKRAINE: "[Language: Ukrainian]",
            Language.BENGALI_BANGLADESH: "[Language: Bengali]",
            Language.ENGLISH_INDIA_HINDI_BUNDLE: "[Language: English (India)]",
            Language.MARATHI_INDIA: "[Language: Marathi]",
            Language.TAMIL_INDIA: "[Language: Tamil]",
            Language.TELUGU_INDIA: "[Language: Telugu]",
        }
        return language_instructions.get(language, "")

    def _get_style_instructions(self, request: AudioRequest) -> str:
        """Get style instructions for speed and pitch control via natural language."""
        if request.speaker_mode == SpeakerMode.MULTIPLE:
            # For multi-speaker, style is typically controlled per speaker in the text
            return ""

        voice_config = request.voice_config
        if not voice_config or (not voice_config.speed and not voice_config.pitch):
            return ""

        instructions = []

        # Convert speed to natural language
        if voice_config.speed:
            if voice_config.speed < 0.8:
                instructions.append("speak slowly")
            elif voice_config.speed > 1.3:
                instructions.append("speak quickly")
            elif voice_config.speed < 0.9:
                instructions.append("speak a bit slowly")
            elif voice_config.speed > 1.1:
                instructions.append("speak a bit faster")

        # Convert pitch to natural language
        if voice_config.pitch:
            if voice_config.pitch < 0.8:
                instructions.append("with a lower pitch")
            elif voice_config.pitch > 1.3:
                instructions.append("with a higher pitch")
            elif voice_config.pitch < 0.9:
                instructions.append("with a slightly lower pitch")
            elif voice_config.pitch > 1.1:
                instructions.append("with a slightly higher pitch")

        if instructions:
            return f"[Style: {', '.join(instructions)}]"
        return ""

    def _validate_context_window(self, text: str) -> None:
        """
        Validate that the text doesn't exceed Gemini TTS context window limit.

        Gemini TTS has a configurable token limit. We use a rough approximation of
        4 characters per token for validation.
        """
        # Rough approximation: 4 characters per token
        estimated_tokens = len(text) / 4
        max_tokens = self.config.max_context_tokens

        if estimated_tokens > max_tokens:
            raise TTSValidationError(
                f"Text is too long. Estimated {estimated_tokens:.0f} tokens, "
                f"but Gemini TTS supports maximum {max_tokens} tokens. "
                f"Please reduce text length to approximately {max_tokens * 4} characters."
            )

    def _validate_audio_data(self, audio_data: bytes) -> None:
        """Validate audio data before processing."""
        if not audio_data:
            raise TTSValidationError("Received empty audio data from API")

        min_size = max(100, self.config.min_audio_size // 10)  # Allow smaller raw data
        if len(audio_data) < min_size:
            raise TTSValidationError(
                f"Audio data too small: {len(audio_data)} bytes (minimum: {min_size})"
            )

        # Check for common audio file headers (basic validation)
        if not (audio_data.startswith(b"RIFF") or audio_data.startswith(b"\x00\x00")):
            logger.warning("Audio data doesn't start with expected headers")

    async def _validate_saved_audio_file(self, file_path: str) -> None:
        """Validate the saved audio file."""
        try:
            if not os.path.exists(file_path):
                raise TTSError(f"Audio file was not created: {file_path}")

            file_size = os.path.getsize(file_path)
            if file_size < self.config.min_audio_size:
                raise TTSError(
                    f"Generated audio file too small: {file_size} bytes (minimum: {self.config.min_audio_size})"
                )

            # Basic WAV file validation
            async with aiofiles.open(file_path, "rb") as f:
                header = await f.read(12)
                if not header.startswith(b"RIFF") or b"WAVE" not in header:
                    raise TTSError("Generated file is not a valid WAV file")

            logger.info(f"Audio file validated: {file_path} ({file_size:,} bytes)")

        except Exception as e:
            logger.error(f"Audio file validation failed: {str(e)}")
            raise TTSError(f"Audio file validation failed: {str(e)}")

    async def _save_wav_file(
        self,
        filename: str,
        pcm_data: bytes,
        channels: int = 1,
        rate: int = 24000,
        sample_width: int = 2,
    ) -> str:
        """Save PCM data as WAV file with specified format."""
        try:
            # Ensure output directory exists
            os.makedirs(self.config.output_dir, exist_ok=True)
            file_path = os.path.join(self.config.output_dir, filename)

            # Use async file operations
            await self._write_wav_file_async(
                file_path, pcm_data, channels, rate, sample_width
            )

            return file_path
        except Exception as e:
            logger.error(f"Error saving WAV file: {str(e)}")
            raise TTSError(f"Failed to save audio file: {str(e)}")

    async def _write_wav_file_async(
        self,
        file_path: str,
        pcm_data: bytes,
        channels: int,
        rate: int,
        sample_width: int,
    ):
        """Asynchronous WAV file writing."""
        # Create WAV header
        wav_header = self._create_wav_header(
            len(pcm_data), channels, rate, sample_width
        )

        # Write file asynchronously
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(wav_header)
            await f.write(pcm_data)

    def _create_wav_header(
        self, data_size: int, channels: int, rate: int, sample_width: int
    ) -> bytes:
        """Create WAV file header."""
        # WAV file header structure
        chunk_size = data_size + 36
        subchunk2_size = data_size
        byte_rate = rate * channels * sample_width
        block_align = channels * sample_width
        bits_per_sample = sample_width * 8

        header = b"RIFF"
        header += chunk_size.to_bytes(4, "little")
        header += b"WAVE"
        header += b"fmt "
        header += (16).to_bytes(4, "little")  # Subchunk1Size
        header += (1).to_bytes(2, "little")  # AudioFormat (PCM)
        header += channels.to_bytes(2, "little")
        header += rate.to_bytes(4, "little")
        header += byte_rate.to_bytes(4, "little")
        header += block_align.to_bytes(2, "little")
        header += bits_per_sample.to_bytes(2, "little")
        header += b"data"
        header += subchunk2_size.to_bytes(4, "little")

        return header
