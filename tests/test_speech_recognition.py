import unittest
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.speech_recognition import VoiceRecognizer

class TestVoiceRecognizer(unittest.TestCase):
    def setUp(self):
        """Initialize the voice recognizer before each test"""
        self.recognizer = VoiceRecognizer()

    def test_recognizer_initialization(self):
        """Test if the recognizer is properly initialized"""
        self.assertIsNotNone(self.recognizer)
        self.assertIsNotNone(self.recognizer.recognizer)
        self.assertIsNotNone(self.recognizer.microphone)

    def test_listen_with_no_audio(self):
        """Test behavior when no audio is provided"""
        result = self.recognizer.listen()
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()