import pyttsx3

class VoiceSynthesizer:
    def __init__(self):
        self.engine = pyttsx3.init()
        self._configure_voice()
        
    def _configure_voice(self):
        """Configure voice properties for natural speech"""
        voices = self.engine.getProperty('voices')
        # Select a more natural voice - adjust index based on available voices
        self.engine.setProperty('voice', voices[1].id)  # Usually index 1 is a better voice
        self.engine.setProperty('rate', 175)  # Slightly slower for clarity
        self.engine.setProperty('volume', 0.9)  # Slightly lower volume
        
    def speak(self, text):
        try:
            # Add speech marks for more natural pauses
            processed_text = self._process_text_for_speech(text)
            self.engine.say(processed_text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Speech synthesis error: {str(e)}")

    def _process_text_for_speech(self, text):
        """Add processing for more natural speech patterns"""
        # Add pauses at punctuation
        text = text.replace(',', ', ')
        text = text.replace('.', '. ')
        text = text.replace('!', '! ')
        text = text.replace('?', '? ')
        return text