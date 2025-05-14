import unittest
import sys
import os
from unittest.mock import MagicMock, patch
import json

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.llm_processor import LLMProcessor
from src.core.command_processor import EnhancedCommandProcessor
from src.core.speech_synthesis import VoiceSynthesizer
from src.core.speech_recognition import VoiceRecognizer

class TestEnhancedVoiceAssistant(unittest.TestCase):
    def setUp(self):
        """Initialize test environment"""
        self.model_path = "models/mistral/Mistral-Nemo-Instruct-2407-Q4_K_M.gguf"
        self.llm = LLMProcessor(self.model_path)
        self.processor = EnhancedCommandProcessor(self.llm)
        self.synthesizer = VoiceSynthesizer()
        self.recognizer = VoiceRecognizer()

    # Basic Conversation Tests
    def test_greeting_responses(self):
        """Test various greeting patterns"""
        greetings = [
            "hello", "hi", "hey", "good morning", "good afternoon",
            "good evening", "what's up", "how are you"
        ]
        for greeting in greetings:
            response = self.processor.process_command(greeting)
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 0)

    # Application Control Tests
    def test_application_operations(self):
        """Test application control commands"""
        commands = [
            ("open chrome", "chrome"),
            ("open notepad", "notepad"),
            ("close chrome", "chrome"),
            ("minimize notepad", "notepad"),
            ("maximize calculator", "calculator")
        ]
        for command, app in commands:
            response = self.processor.process_command(command)
            self.assertIsNotNone(response)

    # Web Operations Tests
    def test_web_operations(self):
        """Test web-related commands"""
        web_commands = [
            "search for python tutorials",
            "open google.com",
            "browse youtube",
            "search stack overflow",
            "open github"
        ]
        for command in web_commands:
            response = self.processor.process_command(command)
            self.assertIsNotNone(response)

    # System Control Tests
    def test_system_operations(self):
        """Test system control commands"""
        system_commands = [
            "what time is it",
            "show me the date",
            "check system status",
            "show running applications",
            "check memory usage"
        ]
        for command in system_commands:
            response = self.processor.process_command(command)
            self.assertIsNotNone(response)

    # File Operations Tests
    def test_file_operations(self):
        """Test file handling commands"""
        file_commands = [
            "create file test.txt",
            "open document.pdf",
            "delete test.txt",
            "rename file old.txt to new.txt",
            "move file.txt to Documents"
        ]
        for command in file_commands:
            response = self.processor.process_command(command)
            self.assertIsNotNone(response)

    # Media Control Tests
    def test_media_controls(self):
        """Test media control commands"""
        media_commands = [
            "play music",
            "pause playback",
            "volume up",
            "volume down",
            "mute audio",
            "set volume 50"
        ]
        for command in media_commands:
            response = self.processor.process_command(command)
            self.assertIsNotNone(response)

    # Screen Interaction Tests
    def test_screen_interactions(self):
        """Test screen interaction commands"""
        screen_commands = [
            "click on Start",
            "double click Downloads",
            "right click desktop",
            "scroll down",
            "select text"
        ]
        for command in screen_commands:
            response = self.processor.process_command(command)
            self.assertIsNotNone(response)

    # Complex Command Tests
    def test_complex_commands(self):
        """Test complex multi-step commands"""
        complex_commands = [
            "open chrome and go to google.com",
            "search for python and open the first link",
            "create folder Projects and open it",
            "minimize all windows except chrome",
            "save this file and close notepad"
        ]
        for command in complex_commands:
            response = self.processor.process_command(command)
            self.assertIsNotNone(response)

    # Error Handling Tests
    def test_error_handling(self):
        """Test error handling capabilities"""
        error_cases = [
            "",  # Empty command
            "nonexistent_command",  # Invalid command
            "open nonexistent_app",  # Invalid application
            "delete system32",  # Dangerous command
            "12345"  # Numeric input
        ]
        for case in error_cases:
            response = self.processor.process_command(case)
            self.assertIsNotNone(response)

    # Learning System Tests
    def test_learning_system(self):
        """Test learning and adaptation capabilities"""
        test_interactions = [
            ("hello", True),
            ("open chrome", True),
            ("invalid_command", False),
            ("search python", True),
            ("close window", True)
        ]
        for command, expected_success in test_interactions:
            self.processor.learning_manager.save_interaction(command, "test response", expected_success)
            patterns = self.processor.learning_manager.analyze_patterns()
            self.assertIn(command.lower(), patterns)

    # Voice Recognition Tests
    @patch('speech_recognition.Recognizer.recognize_google')
    def test_voice_recognition(self, mock_recognize):
        """Test voice recognition accuracy"""
        test_phrases = [
            "hello jarvis",
            "open chrome browser",
            "what's the weather today",
            "set an alarm for 7 am",
            "send an email to john"
        ]
        for phrase in test_phrases:
            mock_recognize.return_value = phrase
            result = self.recognizer.listen()
            self.assertEqual(result, phrase)

    # Voice Synthesis Tests
    def test_voice_synthesis(self):
        """Test voice synthesis capabilities"""
        test_phrases = [
            "Hello, I am your AI assistant",
            "The current time is 12:00 PM",
            "Opening Chrome browser",
            "Command executed successfully",
            "I'm sorry, I didn't understand that"
        ]
        for phrase in test_phrases:
            try:
                self.synthesizer.speak(phrase)
                # If no exception is raised, consider it a pass
                self.assertTrue(True)
            except Exception as e:
                self.fail(f"Voice synthesis failed for '{phrase}': {str(e)}")

    # LLM Processing Tests
    def test_llm_processing(self):
        """Test LLM response processing"""
        test_queries = [
            "What's the weather like?",
            "Tell me a joke",
            "Explain quantum computing",
            "Write a python function",
            "Summarize this text"
        ]
        for query in test_queries:
            response = self.llm.process_query(query)
            self.assertIsInstance(response, str)
            try:
                json_response = json.loads(response)
                self.assertIn('type', json_response)
                self.assertIn('response', json_response)
            except json.JSONDecodeError:
                self.fail(f"Invalid JSON response for query: {query}")

if __name__ == '__main__':
    unittest.main(verbosity=2)