#!/usr/bin/env python3
"""
Example demonstrating model override behavior.
Shows how environment defaults can be overridden in code.
"""

import os
from dotenv import load_dotenv
from audio_api import AudioRequest, VoiceModel, VoiceName

# Load environment variables
load_dotenv()


def demonstrate_model_override():
    """Demonstrate how model selection works with environment defaults and code overrides."""

    print("🤖 Model Override Demonstration")
    print("=" * 50)

    # Check current environment setting
    env_model = os.getenv("DEFAULT_TTS_MODEL", "Not set")
    print(f"Environment DEFAULT_TTS_MODEL: {env_model}")
    print()

    # 1. Using environment default (no model specified)
    print("1️⃣ Using Environment Default:")
    default_request = AudioRequest(
        text="This uses the environment default model",
        voice_config={"voice_name": VoiceName.KORE},
    )
    print(f"   Model used: {default_request.model}")
    print(f"   Text: {default_request.text}")
    print()

    # 2. Explicit override to Flash model
    print("2️⃣ Explicit Override to Flash Model:")
    flash_request = AudioRequest(
        text="This explicitly uses the Flash model for speed",
        model=VoiceModel.GEMINI_TTS_FLASH,
        voice_config={"voice_name": VoiceName.PUCK},
    )
    print(f"   Model used: {flash_request.model}")
    print(f"   Text: {flash_request.text}")
    print()

    # 3. Explicit override to Pro model
    print("3️⃣ Explicit Override to Pro Model:")
    pro_request = AudioRequest(
        text="This explicitly uses the Pro model for quality",
        model=VoiceModel.GEMINI_TTS_PRO,
        voice_config={"voice_name": VoiceName.SULAFAR},
    )
    print(f"   Model used: {pro_request.model}")
    print(f"   Text: {pro_request.text}")
    print()

    # 4. Dynamic model selection based on conditions
    print("4️⃣ Dynamic Model Selection:")

    def create_request_for_use_case(text: str, use_case: str):
        """Select model based on use case."""
        if use_case == "real-time":
            model = VoiceModel.GEMINI_TTS_FLASH
            voice = VoiceName.CHARON  # Clear and efficient
        elif use_case == "production":
            model = VoiceModel.GEMINI_TTS_PRO
            voice = VoiceName.SULAFAR  # Warm and professional
        else:
            # Use environment default
            model = None  # Will use default from environment
            voice = VoiceName.KORE

        if model:
            return AudioRequest(
                text=text, model=model, voice_config={"voice_name": voice}
            )
        else:
            return AudioRequest(text=text, voice_config={"voice_name": voice})

    # Real-time use case
    realtime_request = create_request_for_use_case(
        "Quick notification sound", "real-time"
    )
    print(f"   Real-time request model: {realtime_request.model}")

    # Production use case
    production_request = create_request_for_use_case(
        "Professional audiobook narration", "production"
    )
    print(f"   Production request model: {production_request.model}")

    # Default use case
    default_case_request = create_request_for_use_case(
        "General purpose audio", "general"
    )
    print(f"   General request model: {default_case_request.model}")
    print()

    print("✅ Summary:")
    print("   • Environment variable sets the DEFAULT model")
    print("   • Code can ALWAYS override by specifying model parameter")
    print("   • This provides flexibility for different use cases")
    print("   • No breaking changes to existing code")


if __name__ == "__main__":
    demonstrate_model_override()
