import unittest
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.command_processor import CommandProcessor

class TestCommandProcessor(unittest.TestCase):
    def setUp(self):
        """Initialize the command processor before each test"""
        self.command_processor = CommandProcessor()

    def test_process_command_open_application(self):
        """Test opening an application"""
        result = self.command_processor.process_command("open notepad")
        self.assertEqual(result, "Opening notepad")

    def test_process_command_search(self):
        """Test web search functionality"""
        result = self.command_processor.process_command("search python tutorial")
        self.assertEqual(result, "Searching for python tutorial")

    def test_get_time(self):
        """Test time command"""
        result = self.command_processor.process_command("time")
        self.assertIn("The current time is", result)

    def test_open_email(self):
        """Test email command"""
        result = self.command_processor.process_command("email")
        self.assertEqual(result, "Opening email")

    def test_browse_web(self):
        """Test web browsing command"""
        result = self.command_processor.process_command("browse youtube.com")
        self.assertEqual(result, "Opening https://youtube.com")

    def test_invalid_command(self):
        """Test handling of invalid commands"""
        result = self.command_processor.process_command("invalid command")
        self.assertEqual(result, "Command 'invalid' not recognized")

    def test_empty_command(self):
        """Test handling of empty commands"""
        result = self.command_processor.process_command("")
        self.assertEqual(result, "Sorry, I couldn't understand that")

if __name__ == '__main__':
    unittest.main()