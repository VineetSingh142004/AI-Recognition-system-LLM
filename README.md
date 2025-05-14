# Voice Assistant

A sophisticated voice-activated AI assistant that transforms your PC into an intelligent interface, similar to JARVIS from Iron Man. This assistant leverages advanced speech recognition and synthesis to understand verbal commands and execute various system operations.

## Comprehensive Features

### 1. Voice Recognition System

- Real-time speech-to-text conversion using Google's Speech Recognition API
- Ambient noise adjustment for better accuracy
- Continuous listening capability
- Error handling for unrecognized speech

### 2. Voice Synthesis Engine

- Text-to-speech conversion using pyttsx3
- Configurable voice properties:
  - Speech rate: 180 words per minute (adjustable)
  - Volume control (0.0 to 1.0)
  - Multiple voice options (male/female)
  - Custom voice modulation

### 3. Command Processing System

#### Basic Commands

- `open [application_name]`: Launches system applications
- `search [query]`: Performs Google search
- `time`: Reports current time
- `email`: Opens default email client
- `browse [url]`: Opens specified website

### 4. Custom Command Framework

Users can define custom commands through the `CustomCommands` class:

```python
custom_commands.add_command("my_command", command_function)
```

## Technical Architecture

### Directory Structure

```
voice-assistant/
├── src/
│   ├── core/
│   │   ├── speech_recognition.py   # Voice input processing
│   │   ├── speech_synthesis.py     # Voice output generation
│   │   └── command_processor.py    # Command interpretation
│   ├── commands/
│   │   ├── system_commands.py      # Built-in system operations
│   │   └── custom_commands.py      # User-defined commands
│   ├── utils/
│   │   └── helpers.py             # Utility functions
│   ├── config/
│   │   └── settings.py           # Configuration management
│   └── main.py                   # Application entry point
├── tests/
│   ├── test_speech_recognition.py
│   └── test_command_processor.py
├── requirements.txt              # Dependencies
└── setup.py                     # Package configuration
```

## Detailed Installation Guide

### Prerequisites

- Python 3.6 or higher
- Windows OS (for full system command support)
- Working microphone
- Internet connection (for Google Speech Recognition)

### Installation Steps

1. Clone the repository:

```bash
git clone https://github.com/VineetSingh142004/AI-Recognition-system-.git
cd AI-Recognition-system-
```

2. Create and activate virtual environment:

```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

4. Configure settings:
   Edit `src/config/settings.py`:

```python
class Config:
    API_KEY = "your_google_api_key"
    SYSTEM_PATH = "C:\\Program Files"
    CUSTOM_COMMANDS_PATH = "path_to_custom_commands"
    LOG_FILE = "voice_assistant.log"
```

## Usage Guide

### Starting the Assistant

```bash
python src/main.py
```

### Available Voice Commands

1. System Operations:

   - "open notepad" - Launches Notepad
   - "open chrome" - Launches Chrome browser
   - "open calculator" - Launches Calculator

2. Web Operations:

   - "search python programming" - Performs Google search
   - "browse youtube.com" - Opens YouTube
   - "email" - Opens default email client

3. Utility Commands:
   - "time" - Tells current time
   - "date" - Tells current date
   - "weather" - Checks weather (requires API setup)

### Adding Custom Commands

```python
from src.commands.custom_commands import CustomCommands

commands = CustomCommands()
commands.add_command("my_command", lambda: print("Custom action"))
```

## Troubleshooting

Common Issues and Solutions:

1. Speech Recognition Errors

   - Check microphone connections
   - Verify internet connectivity
   - Adjust microphone sensitivity

2. Command Execution Failures
   - Verify system paths
   - Check application availability
   - Confirm permissions

## Development Guide

### Adding New Commands

1. Create command function in `system_commands.py` or `custom_commands.py`
2. Register command in `CommandProcessor` class
3. Add error handling and logging
4. Update tests

### Running Tests

```bash
python -m pytest tests/
```

## Contributing Guidelines

1. Fork the repository
2. Create feature branch
3. Implement changes
4. Add tests
5. Submit pull request

## Future Development Plans

### 1. LLM Integration

- Integration with GPT-4 or similar LLMs for:
  - Natural language understanding
  - Context-aware conversations
  - Complex task planning and execution
  - Code generation and explanation
  - Document analysis and summarization

### 2. Advanced Features

- **Contextual Understanding**

  - Maintain conversation history
  - Remember user preferences
  - Learn from past interactions (self learning)

- **Multi-modal Interaction**
  - Computer vision integration
  - Screen analysis and interaction
  - Gesture recognition
  - Face recognition for personalization

### 4. Enhanced AI Capabilities

- **Natural Language Processing**
  - Improved command understanding
  - Multiple language support
  - Sentiment analysis
  - Context-aware responses

## Contribution Opportunities

The above features present excellent opportunities for contributors. Priority areas:

1. LLM integration framework
2. Plugin system development
3. Machine learning components

## License

MIT License - See LICENSE file for details

## Version History

- v0.1 - Initial release
  - Basic voice recognition
  - Core command processing
  - System commands implementation
