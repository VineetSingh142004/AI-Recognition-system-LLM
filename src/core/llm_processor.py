from llama_cpp import Llama
import pyautogui
import os
import keyboard
from . import screen_text_extractor  # Update import statement

class LLMProcessor:
    def __init__(self, model_path):
        try:
            self.model = Llama(
                model_path=model_path,
                n_ctx=2048,  # Context window
                n_threads=4   # Adjust based on your CPU
            )
            self.context_history = []
        except Exception as e:
            raise Exception(f"Failed to load model: {str(e)}")

    def process_query(self, query):
        """Process the user query and return structured command"""
        system_prompt = """
        You are an AI assistant that helps control computer operations.
        Convert user requests into structured commands.
        Use format: 'action: [command], params: [parameters]'
        Available actions: open, close, search, click, type, scroll
        """
        
        full_prompt = f"{system_prompt}\n\nUser: {query}\nAssistant:"
        
        response = self.model(
            full_prompt,
            max_tokens=100,
            temperature=0.7,
            stop=["User:", "\n\n"]
        )
        
        return response['choices'][0]['text'].strip()

    def extract_screen_text(self, region=None):
        """Extract text from current screen"""
        return screen_text_extractor.extract_text(region)

    def get_screen_elements(self):
        """Get clickable elements on screen"""
        return screen_text_extractor.get_clickable_elements()