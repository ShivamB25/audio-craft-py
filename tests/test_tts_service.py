"""
Unit tests for TTSService with mocking and comprehensive coverage.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from audio_api.services.tts_service import (
    TTSService,
    TTSValidationError,
)
from audio_api.models import (
    AudioRequest,
    VoiceModel,
    Language,
    SpeakerMode,
)
from audio_api.config import AudioConfig


@pytest.fixture
def mock_config():
    """Create a mock configuration for testing."""
    config = MagicMock(spec=AudioConfig)
    config.gemini_api_key = "test_api_key"
    config.output_dir = "test_output"
    config.max_context_tokens = 32000
    config.retry_attempts = 3
    config.retry_min_wait = 1
    config.retry_max_wait = 5
    config.min_audio_size = 1000
    return config


@pytest.fixture
def mock_gemini_client():
    """Create a mock Gemini client."""
    client = MagicMock()
    return client


@pytest.fixture
def tts_service(mock_config, mock_gemini_client):
    """Create a TTSService instance with mocked dependencies."""
    return TTSService(config=mock_config, gemini_client=mock_gemini_client)


@pytest.fixture
def sample_audio_request():
    """Create a sample audio request for testing."""
    return AudioRequest(
        text="Hello, this is a test message.",
        model=VoiceModel.GEMINI_TTS_PRO,
        language=Language.ENGLISH_US,
        speaker_mode=SpeakerMode.SINGLE,
    )


class TestTTSService:
    """Test cases for TTSService."""

    @pytest.mark.asyncio
    async def test_successful_audio_generation(
        self, tts_service, sample_audio_request, mock_gemini_client
    ):
        """Test successful audio generation."""
        # Mock the Gemini API response
        mock_response = MagicMock()
        mock_response.candidates = [MagicMock()]
        mock_response.candidates[0].content.parts = [MagicMock()]
        mock_response.candidates[0].content.parts[0].inline_data.data = (
            b"fake_audio_data" * 100
        )

        mock_gemini_client.models.generate_content = MagicMock(
            return_value=mock_response
        )

        # Mock file operations
        with (
            patch("audio_api.services.tts_service.os.makedirs"),
            patch(
                "audio_api.services.tts_service.aiofiles.open", create=True
            ) as mock_open,
            patch("audio_api.services.tts_service.os.path.exists", return_value=True),
            patch("audio_api.services.tts_service.os.path.getsize", return_value=2000),
        ):

            mock_file = AsyncMock()
            mock_open.return_value.__aenter__.return_value = mock_file
            mock_file.read.return_value = b"RIFF" + b"\x00" * 8 + b"WAVE"
            mock_file.write = AsyncMock()

            result = await tts_service.generate_audio(sample_audio_request)

            assert result.success is True
            assert result.file_path is not None
            assert "test_output" in result.file_path

    @pytest.mark.asyncio
    async def test_validation_error_text_too_long(self, tts_service, mock_config):
        """Test validation error for text that's too long."""
        mock_config.max_context_tokens = 100  # Very small limit

        long_text_request = AudioRequest(
            text="x" * 1000, language=Language.ENGLISH_US  # Very long text
        )

        result = await tts_service.generate_audio(long_text_request)

        assert result.success is False
        assert "too long" in result.error.lower()

    @pytest.mark.asyncio
    async def test_api_error_with_retry(
        self, tts_service, sample_audio_request, mock_gemini_client
    ):
        """Test API error handling with retry logic."""
        # Mock API to fail twice then succeed
        call_count = 0

        def mock_generate_content(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count <= 2:
                raise Exception("Service temporarily unavailable")

            # Success on third try
            mock_response = MagicMock()
            mock_response.candidates = [MagicMock()]
            mock_response.candidates[0].content.parts = [MagicMock()]
            mock_response.candidates[0].content.parts[0].inline_data.data = (
                b"fake_audio_data" * 100
            )
            return mock_response

        mock_gemini_client.models.generate_content = mock_generate_content

        with (
            patch("audio_api.services.tts_service.os.makedirs"),
            patch(
                "audio_api.services.tts_service.aiofiles.open", create=True
            ) as mock_open,
            patch("audio_api.services.tts_service.os.path.exists", return_value=True),
            patch("audio_api.services.tts_service.os.path.getsize", return_value=2000),
        ):

            mock_file = AsyncMock()
            mock_open.return_value.__aenter__.return_value = mock_file
            mock_file.read.return_value = b"RIFF" + b"\x00" * 8 + b"WAVE"
            mock_file.write = AsyncMock()

            result = await tts_service.generate_audio(sample_audio_request)

            assert result.success is True
            assert call_count == 3  # Should have retried twice

    @pytest.mark.asyncio
    async def test_quota_error_no_retry(
        self, tts_service, sample_audio_request, mock_gemini_client
    ):
        """Test quota error handling (should not retry)."""
        mock_gemini_client.models.generate_content.side_effect = Exception(
            "Quota exceeded"
        )

        result = await tts_service.generate_audio(sample_audio_request)

        assert result.success is False
        assert "quota" in result.error.lower()

    @pytest.mark.asyncio
    async def test_invalid_audio_data(
        self, tts_service, sample_audio_request, mock_gemini_client
    ):
        """Test handling of invalid audio data from API."""
        # Mock API to return empty audio data
        mock_response = MagicMock()
        mock_response.candidates = [MagicMock()]
        mock_response.candidates[0].content.parts = [MagicMock()]
        mock_response.candidates[0].content.parts[
            0
        ].inline_data.data = b""  # Empty data

        mock_gemini_client.models.generate_content = MagicMock(
            return_value=mock_response
        )

        result = await tts_service.generate_audio(sample_audio_request)

        assert result.success is False
        assert "empty audio data" in result.error.lower()

    @pytest.mark.asyncio
    async def test_file_validation_failure(
        self, tts_service, sample_audio_request, mock_gemini_client
    ):
        """Test file validation failure."""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.candidates = [MagicMock()]
        mock_response.candidates[0].content.parts = [MagicMock()]
        mock_response.candidates[0].content.parts[0].inline_data.data = (
            b"fake_audio_data" * 100
        )

        mock_gemini_client.models.generate_content = MagicMock(
            return_value=mock_response
        )

        # Mock file operations to simulate validation failure
        with (
            patch("audio_api.services.tts_service.os.makedirs"),
            patch(
                "audio_api.services.tts_service.aiofiles.open", create=True
            ) as mock_open,
            patch("audio_api.services.tts_service.os.path.exists", return_value=True),
            patch("audio_api.services.tts_service.os.path.getsize", return_value=100),
        ):  # Too small

            mock_file = AsyncMock()
            mock_open.return_value.__aenter__.return_value = mock_file
            mock_file.write = AsyncMock()

            result = await tts_service.generate_audio(sample_audio_request)

            assert result.success is False
            assert "too small" in result.error.lower()

    def test_context_window_validation(self, tts_service):
        """Test context window validation."""
        # Test valid text
        tts_service._validate_context_window("Short text")  # Should not raise

        # Test text that's too long
        long_text = "x" * 200000  # Very long text
        with pytest.raises(TTSValidationError):
            tts_service._validate_context_window(long_text)

    def test_audio_data_validation(self, tts_service):
        """Test audio data validation."""
        # Test valid audio data
        valid_data = b"RIFF" + b"x" * 1000
        tts_service._validate_audio_data(valid_data)  # Should not raise

        # Test empty audio data
        with pytest.raises(TTSValidationError):
            tts_service._validate_audio_data(b"")

        # Test audio data that's too small
        with pytest.raises(TTSValidationError):
            tts_service._validate_audio_data(b"small")

    def test_wav_header_creation(self, tts_service):
        """Test WAV header creation."""
        header = tts_service._create_wav_header(
            data_size=1000, channels=1, rate=24000, sample_width=2
        )

        assert header.startswith(b"RIFF")
        assert b"WAVE" in header
        assert b"fmt " in header
        assert b"data" in header
        assert len(header) == 44  # Standard WAV header size

    @pytest.mark.asyncio
    async def test_multi_speaker_config(self, tts_service, mock_gemini_client):
        """Test multi-speaker configuration."""
        from audio_api.models import MultiSpeakerConfig, SpeakerConfig, VoiceName

        multi_speaker_request = AudioRequest(
            text="Alice: Hello! Bob: Hi there!",
            speaker_mode=SpeakerMode.MULTIPLE,
            multi_speaker_config=MultiSpeakerConfig(
                speakers=[
                    SpeakerConfig(speaker_name="Alice", voice_name=VoiceName.KORE),
                    SpeakerConfig(speaker_name="Bob", voice_name=VoiceName.CHARON),
                ]
            ),
        )

        # Mock successful API response
        mock_response = MagicMock()
        mock_response.candidates = [MagicMock()]
        mock_response.candidates[0].content.parts = [MagicMock()]
        mock_response.candidates[0].content.parts[0].inline_data.data = (
            b"fake_audio_data" * 100
        )

        mock_gemini_client.models.generate_content = MagicMock(
            return_value=mock_response
        )

        with (
            patch("audio_api.services.tts_service.os.makedirs"),
            patch(
                "audio_api.services.tts_service.aiofiles.open", create=True
            ) as mock_open,
            patch("audio_api.services.tts_service.os.path.exists", return_value=True),
            patch("audio_api.services.tts_service.os.path.getsize", return_value=2000),
        ):

            mock_file = AsyncMock()
            mock_open.return_value.__aenter__.return_value = mock_file
            mock_file.read.return_value = b"RIFF" + b"\x00" * 8 + b"WAVE"
            mock_file.write = AsyncMock()

            result = await tts_service.generate_audio(multi_speaker_request)

            assert result.success is True


@pytest.mark.asyncio
async def test_tts_service_integration():
    """Integration test for TTSService (requires actual API key)."""
    import os

    # Skip if no API key available
    if not os.getenv("GEMINI_API_KEY"):
        pytest.skip("GEMINI_API_KEY not available for integration test")

    tts_service = TTSService()
    request = AudioRequest(
        text="This is a short integration test.", language=Language.ENGLISH_US
    )

    result = await tts_service.generate_audio(request)

    # Should succeed with real API
    assert result.success is True
    assert result.file_path is not None
    assert os.path.exists(result.file_path)
