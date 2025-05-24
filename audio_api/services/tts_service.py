import wave
import os
import asyncio
import aiofiles
import logging
from google import genai
from google.genai import types
from audio_api.models import AudioRequest, AudioResponse, VoiceModel, Language, SpeakerMode

logger = logging.getLogger(__name__)


class TTSService:
    def __init__(self):
        self.gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    async def generate_audio(self, request: AudioRequest) -> AudioResponse:
        """Generate audio from text using Gemini TTS."""
        try:
            return await self._generate_gemini_audio(request)
        except Exception as e:
            logger.error(f"Error generating audio: {str(e)}")
            return AudioResponse(
                success=False, message="Failed to generate audio", error=str(e)
            )

    async def _generate_gemini_audio(self, request: AudioRequest) -> AudioResponse:
        """Generate audio using Gemini TTS."""
        try:
            # Configure speech settings based on speaker mode
            if request.speaker_mode == SpeakerMode.SINGLE:
                speech_config = self._create_single_speaker_config(request)
            else:  # MULTIPLE
                speech_config = self._create_multi_speaker_config(request)

            # Generate content with audio
            response = await asyncio.to_thread(
                self.gemini_client.models.generate_content,
                model="gemini-2.5-pro-preview-tts",
                contents=self._format_text_for_gemini(request),
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=speech_config,
                ),
            )

            # Extract audio data
            audio_data = response.candidates[0].content.parts[0].inline_data.data

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

            return AudioResponse(
                success=True,
                message="Audio generated successfully",
                file_path=file_path,
            )

        except Exception as e:
            logger.error(f"Gemini TTS error: {str(e)}")
            return AudioResponse(
                success=False,
                message="Failed to generate audio with Gemini",
                error=str(e),
            )

    def _create_single_speaker_config(self, request: AudioRequest) -> types.SpeechConfig:
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
                )
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

    async def _save_wav_file(
        self,
        filename: str,
        pcm_data: bytes,
        channels: int = 1,
        rate: int = 24000,
        sample_width: int = 2,
    ) -> str:
        """Save PCM data as WAV file with specified format (24kHz, 16-bit PCM)."""
        try:
            # Ensure output directory exists
            os.makedirs("output", exist_ok=True)
            file_path = os.path.join("output", filename)

            # Use asyncio.to_thread for file I/O
            await asyncio.to_thread(
                self._write_wav_file, file_path, pcm_data, channels, rate, sample_width
            )

            return file_path
        except Exception as e:
            logger.error(f"Error saving WAV file: {str(e)}")
            raise

    def _write_wav_file(
        self,
        file_path: str,
        pcm_data: bytes,
        channels: int,
        rate: int,
        sample_width: int,
    ):
        """Synchronous WAV file writing."""
        with wave.open(file_path, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            wf.writeframes(pcm_data)
