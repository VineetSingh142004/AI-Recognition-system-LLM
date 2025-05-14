# src/main.py

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
        
    def run(self):
        self.synthesizer.speak("Enhanced AI Assistant is ready. How can I help you?")
        
        while True:
            command = self.recognizer.listen()
            
            if command:
                # Process through LLM first
                response = self.processor.process_command(command)
                self.synthesizer.speak(response)

if __name__ == "__main__":
    MODEL_PATH = "C:/Users/vinee/.lmstudio/models/lmstudio-community/Mistral-Nemo-Instruct-2407-GGUF/Mistral-Nemo-Instruct-2407-Q4_K_M.gguf"
        
      # Update this path with your LLM model path
    assistant = EnhancedVoiceAssistant(MODEL_PATH)
    assistant.run()