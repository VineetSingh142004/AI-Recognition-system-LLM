# src/main.py

import signal
import sys
from core.speech_recognition import VoiceRecognizer
from core.speech_synthesis import VoiceSynthesizer
from core.llm_processor import LLMProcessor
from core.command_processor import EnhancedCommandProcessor

class EnhancedVoiceAssistant:
    def __init__(self, llm_model_path):
        self.recognizer = VoiceRecognizer()
        self.synthesizer = VoiceSynthesizer()
        self.llm = LLMProcessor(llm_model_path)
        self.processor = EnhancedCommandProcessor(self.llm)
        self.setup_signal_handlers()
        
    def setup_signal_handlers(self):
        signal.signal(signal.SIGINT, self.graceful_exit)
        signal.signal(signal.SIGTERM, self.graceful_exit)
        
    def graceful_exit(self, signum, frame):
        self.synthesizer.speak("Goodbye! Have a great day!")
        sys.exit(0)
        
    def run(self):
        self.synthesizer.speak("Hello! I'm GANDU, your AI assistant. How can I help you today?")
        
        while True:
            try:
                command = self.recognizer.listen()
                
                if command:
                    print(f"Debug - Heard command: {command}")  # Debug logging
                    response = self.processor.process_command(command)
                    print(f"Debug - Response: {response}")  # Debug logging
                    self.synthesizer.speak(response)
            except Exception as e:
                print(f"Critical error: {str(e)}")  # Debug logging
                self.synthesizer.speak("I encountered an error. Please try again.")

if __name__ == "__main__":
    MODEL_PATH = "models/mistral/Mistral-Nemo-Instruct-2407-Q4_K_M.gguf"
    assistant = EnhancedVoiceAssistant(MODEL_PATH)
    assistant.run()