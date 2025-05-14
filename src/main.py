# src/main.py

import signal
import sys
import os
import time
import json
from datetime import datetime
from core.speech_recognition import VoiceRecognizer
from core.speech_synthesis import VoiceSynthesizer
from core.llm_processor import LLMProcessor
from core.command_processor import EnhancedCommandProcessor
from core.memory_manager import MemoryManager
from core.skill_manager import SkillManager
from core.context_manager import ContextManager

class EnhancedVoiceAssistant:
    def __init__(self, llm_model_path):
        # Initialize core components
        self.recognizer = VoiceRecognizer()
        self.synthesizer = VoiceSynthesizer()
        self.llm = LLMProcessor(llm_model_path)
        self.processor = EnhancedCommandProcessor(self.llm)
        
        # Initialize enhanced components
        self.memory = MemoryManager("data/memory")
        self.skills = SkillManager()
        self.context = ContextManager()
        
        # Setup basic configurations
        self.setup_signal_handlers()
        self.response_cache = {}
        self.command_history = []
        self.last_command_time = 0
        self.wake_word = "jarvis"
        self.is_active = True
        self.conversation_context = []
        
    def setup_signal_handlers(self):
        signal.signal(signal.SIGINT, self.graceful_exit)
        signal.signal(signal.SIGTERM, self.graceful_exit)

    def wake_word_detected(self, audio_input):
        """Check if wake word is detected"""
        return self.wake_word in audio_input.lower()

    def process_conversation_context(self, command):
        """Process and maintain conversation context"""
        self.conversation_context.append({
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "context": self.context.get_current_context()
        })
        if len(self.conversation_context) > 5:
            self.conversation_context.pop(0)

    def learn_from_interaction(self, command, response, success):
        """Learn from user interactions"""
        self.memory.store_interaction({
            "command": command,
            "response": response,
            "success": success,
            "timestamp": datetime.now().isoformat(),
            "context": self.context.get_current_context()
        })

    def smart_cache_lookup(self, command):
        """Intelligent cache lookup with context awareness"""
        for cached_cmd, cached_response in self.response_cache.items():
            if self.context.is_similar_context(cached_cmd, command):
                return cached_response
        return None

    def run(self):
        self.synthesizer.speak("AI Assistant initialized and ready!")
        
        while True:
            try:
                # Listen for command
                audio_input = self.recognizer.listen()
                if not audio_input:
                    continue

                # Wake word detection
                if not self.is_active and not self.wake_word_detected(audio_input):
                    continue
                
                # Process command
                print(f"Processing: {audio_input}")
                
                # Update context
                self.context.update_context(audio_input)
                
                # Check cache with context awareness
                cached_response = self.smart_cache_lookup(audio_input)
                if cached_response:
                    self.synthesizer.speak(cached_response)
                    continue
                
                # Process command with skills
                if self.skills.has_skill_for(audio_input):
                    response = self.skills.execute_skill(audio_input)
                else:
                    response = self.processor.process_command(audio_input)
                
                # Learn from interaction
                success = "error" not in response.lower()
                self.learn_from_interaction(audio_input, response, success)
                
                # Update conversation context
                self.process_conversation_context(audio_input)
                
                # Cache successful responses
                if success:
                    self.response_cache[audio_input] = response
                
                # Speak response
                self.synthesizer.speak(response)
                
                # Update command history
                self.command_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "command": audio_input,
                    "response": response,
                    "success": success
                })
                
            except KeyboardInterrupt:
                self.graceful_exit(None, None)
            except Exception as e:
                print(f"Error in main loop: {str(e)}")
                self.synthesizer.speak("I encountered an error. Please try again.")

    def graceful_exit(self, signum, frame):
        """Enhanced graceful exit with state saving"""
        try:
            # Save current state
            self.memory.save_state()
            self.context.save_context()
            self.skills.save_learned_skills()
            
            # Save command history
            with open("data/history/command_history.json", "w") as f:
                json.dump(self.command_history, f, indent=2)
                
            self.synthesizer.speak("Saving state and shutting down. Goodbye!")
        except Exception as e:
            print(f"Error during shutdown: {e}")
        finally:
            sys.exit(0)

if __name__ == "__main__":
    # Set performance environment variables
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    os.environ['OMP_NUM_THREADS'] = '4'
    os.environ['MKL_NUM_THREADS'] = '4'

    # Create necessary directories
    os.makedirs("data/memory", exist_ok=True)
    os.makedirs("data/history", exist_ok=True)
    os.makedirs("data/skills", exist_ok=True)
    os.makedirs("data/context", exist_ok=True)

    MODEL_PATH = "models/mistral/Mistral-Nemo-Instruct-2407-Q4_K_M.gguf"
    assistant = EnhancedVoiceAssistant(MODEL_PATH)
    assistant.run()