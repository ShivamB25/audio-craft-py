# Building a Voice Assistant Tutorial

Learn how to build a complete voice assistant using the Audio Generation Library. This step-by-step tutorial will guide you through creating an interactive voice assistant with multiple personalities and capabilities.

## 🎯 What We'll Build

By the end of this tutorial, you'll have:
- A voice assistant with multiple personalities
- Dynamic response generation
- Context-aware voice selection
- Error handling and fallbacks
- Extensible command system

## 📋 Prerequisites

- Audio Generation Library installed and configured
- Basic Python knowledge
- Gemini API key set up

## 🚀 Step 1: Basic Voice Assistant Structure

Let's start with a simple voice assistant framework:

```python
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional
from audio_api import AudioRequest, TTSService, VoiceName, Language

class VoiceAssistant:
    """A simple voice assistant with personality."""
    
    def __init__(self, name: str = "Assistant", personality: str = "friendly"):
        self.name = name
        self.personality = personality
        self.tts = TTSService()
        self.conversation_history = []
        
        # Personality-based voice mapping
        self.personality_voices = {
            "friendly": VoiceName.SULAFAR,      # Warm
            "professional": VoiceName.KORE,     # Firm
            "energetic": VoiceName.ZEPHYR,      # Bright
            "calm": VoiceName.ACHERNAR,         # Soft
            "informative": VoiceName.CHARON,    # Informative
        }
    
    def get_voice_for_context(self, context: str = "default") -> VoiceName:
        """Select voice based on context and personality."""
        
        # Context-specific overrides
        context_voices = {
            "greeting": VoiceName.SULAFAR,
            "error": VoiceName.ACHERNAR,
            "success": VoiceName.PUCK,
            "information": VoiceName.CHARON,
            "warning": VoiceName.KORE,
        }
        
        # Use context-specific voice if available, otherwise personality voice
        return context_voices.get(context, self.personality_voices.get(self.personality, VoiceName.SULAFAR))
    
    async def speak(self, text: str, context: str = "default") -> Optional[str]:
        """Generate speech for the given text."""
        
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": "assistant_response",
            "text": text,
            "context": context
        })
        
        voice = self.get_voice_for_context(context)
        
        # Create filename based on context and timestamp
        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"assistant_{context}_{timestamp}.wav"
        
        request = AudioRequest(
            text=text,
            voice_config={"voice_name": voice},
            output_filename=filename
        )
        
        result = await self.tts.generate_audio(request)
        
        if result.success:
            print(f"🎵 {self.name}: {text}")
            print(f"   📁 Audio: {result.file_path}")
            return result.file_path
        else:
            print(f"❌ Speech generation failed: {result.error}")
            return None

# Test the basic assistant
async def test_basic_assistant():
    assistant = VoiceAssistant("Alex", "friendly")
    
    await assistant.speak("Hello! I'm Alex, your friendly voice assistant.", "greeting")
    await assistant.speak("How can I help you today?", "default")

asyncio.run(test_basic_assistant())
```

## 🎭 Step 2: Adding Commands and Intelligence

Now let's add a command system:

```python
import re
from typing import Callable

class Command:
    """Represents a voice assistant command."""
    
    def __init__(self, name: str, patterns: List[str], handler: Callable, description: str):
        self.name = name
        self.patterns = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
        self.handler = handler
        self.description = description
    
    def matches(self, text: str) -> bool:
        """Check if the text matches any of the command patterns."""
        return any(pattern.search(text) for pattern in self.patterns)
    
    async def execute(self, assistant, text: str):
        """Execute the command."""
        return await self.handler(assistant, text)

class IntelligentVoiceAssistant(VoiceAssistant):
    """Voice assistant with command processing."""
    
    def __init__(self, name: str = "Assistant", personality: str = "friendly"):
        super().__init__(name, personality)
        self.commands = []
        self.setup_commands()
    
    def setup_commands(self):
        """Set up default commands."""
        
        # Time command
        async def tell_time(assistant, text):
            now = datetime.now()
            time_str = now.strftime("%I:%M %p")
            date_str = now.strftime("%A, %B %d, %Y")
            response = f"It's currently {time_str} on {date_str}."
            return await assistant.speak(response, "information")
        
        self.commands.append(Command(
            "time",
            [r"what time is it", r"current time", r"tell me the time"],
            tell_time,
            "Get the current time and date"
        ))
        
        # Joke command
        async def tell_joke(assistant, text):
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "I told my wife she was drawing her eyebrows too high. She looked surprised.",
                "Why don't eggs tell jokes? They'd crack each other up!"
            ]
            import random
            joke = random.choice(jokes)
            return await assistant.speak(joke, "default")
        
        self.commands.append(Command(
            "joke",
            [r"tell me a joke", r"joke", r"make me laugh"],
            tell_joke,
            "Tell a random joke"
        ))
        
        # Help command
        async def show_help(assistant, text):
            help_text = "I can help you with: "
            commands_list = [cmd.description for cmd in assistant.commands if cmd.name != "help"]
            help_text += ", ".join(commands_list)
            help_text += ". Just ask me naturally!"
            return await assistant.speak(help_text, "information")
        
        self.commands.append(Command(
            "help",
            [r"help", r"what can you do"],
            show_help,
            "Show available commands"
        ))
    
    async def process_input(self, user_input: str) -> Optional[str]:
        """Process user input and execute appropriate command."""
        
        # Log user input
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": "user_input",
            "text": user_input
        })
        
        # Find matching command
        for command in self.commands:
            if command.matches(user_input):
                print(f"🎯 Executing command: {command.name}")
                return await command.execute(self, user_input)
        
        # No command matched
        response = "I'm not sure how to help with that. Try saying 'help' to see what I can do!"
        return await self.speak(response, "default")

# Test intelligent assistant
async def test_intelligent_assistant():
    assistant = IntelligentVoiceAssistant("SmartBot", "friendly")
    
    await assistant.speak("Hello! I'm your smart assistant.", "greeting")
    
    # Test commands
    test_inputs = [
        "What time is it?",
        "Tell me a joke",
        "Help me",
        "I want to fly to the moon",  # Unknown command
    ]
    
    for user_input in test_inputs:
        print(f"\n👤 User: {user_input}")
        await assistant.process_input(user_input)

asyncio.run(test_intelligent_assistant())
```

## 🎨 Step 3: Complete Application

Finally, let's create a complete interactive application:

```python
class VoiceAssistantApp:
    """Complete voice assistant application."""
    
    def __init__(self):
        self.assistant = None
        self.running = False
    
    async def setup_assistant(self):
        """Set up the assistant with user preferences."""
        print("🎵 Voice Assistant Setup")
        print("=" * 40)
        
        name = input("Assistant name (default: Alex): ").strip() or "Alex"
        
        print("\nPersonalities: 1) Friendly 2) Professional 3) Energetic 4) Calm")
        choice = input("Choose (1-4, default: 1): ").strip() or "1"
        personalities = ["friendly", "professional", "energetic", "calm"]
        personality = personalities[int(choice) - 1] if choice.isdigit() and 1 <= int(choice) <= 4 else "friendly"
        
        self.assistant = IntelligentVoiceAssistant(name, personality)
        print(f"\n✅ Created {name} with {personality} personality")
        return self.assistant
    
    async def conversation_loop(self):
        """Main conversation loop."""
        if not self.assistant:
            await self.setup_assistant()
        
        self.running = True
        await self.assistant.speak("Hello! I'm ready to help you.", "greeting")
        
        print("\n💬 Conversation started! Type 'quit' to exit.")
        print("=" * 50)
        
        while self.running:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    await self.assistant.speak("Goodbye! Have a great day!", "greeting")
                    self.running = False
                    break
                
                await self.assistant.process_input(user_input)
                
            except KeyboardInterrupt:
                print("\n\n🛑 Interrupted by user")
                await self.assistant.speak("Goodbye!", "greeting")
                self.running = False
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                await self.assistant.speak("Sorry, I encountered an error.", "error")

# Main application
async def main():
    """Main application entry point."""
    app = VoiceAssistantApp()
    await app.conversation_loop()
    print("\n👋 Thank you for using the Voice Assistant!")

# Run the application
if __name__ == "__main__":
    asyncio.run(main())
```

## 🧪 Testing Your Assistant

Create a test script:

```python
# test_assistant.py
async def test_all_features():
    """Test all voice assistant features."""
    
    print("🧪 Testing Voice Assistant")
    print("=" * 30)
    
    # Test different personalities
    personalities = ["friendly", "professional", "energetic", "calm"]
    
    for personality in personalities:
        print(f"\n🎭 Testing {personality.title()}:")
        assistant = IntelligentVoiceAssistant(f"{personality.title()}Bot", personality)
        
        await assistant.speak(f"Hello! I'm in {personality} mode.", "greeting")
        await assistant.process_input("What time is it?")
        
        print(f"✅ {personality.title()} test completed")

asyncio.run(test_all_features())
```

## 🚀 Next Steps

1. **Add More Commands**: Extend the command system with weather, reminders, calculations
2. **Multi-Language Support**: Add language switching capabilities
3. **Context Awareness**: Implement conversation context tracking
4. **Voice Customization**: Allow users to adjust voice speed and pitch
5. **Integration**: Connect to external APIs for weather, news, etc.

## 💡 Tips for Enhancement

- **Error Handling**: Add robust error handling for network issues
- **Logging**: Implement comprehensive logging for debugging
- **Configuration**: Add configuration files for easy customization
- **Testing**: Create unit tests for all components
- **Documentation**: Document your custom commands and features

This tutorial provides a solid foundation for building sophisticated voice assistants with the Audio Generation Library!