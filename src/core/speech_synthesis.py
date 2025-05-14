import pyttsx3

class VoiceSynthesizer:
    def __init__(self):
        self.engine = pyttsx3.init()
        # Configure voice properties
        self.engine.setProperty('rate', 180)    # Speed of speech
        self.engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
        
        # voice (0 female or 1 male)
        voices = self.engine.getProperty('voices')
        
        # If we have more voices
        #self.engine.setProperty('voice', voices[n].id) # n is the index of the voice


        self.engine.setProperty('voice', voices[0].id)

    def speak(self, text):
        """Convert text to speech"""
        try:
            print(f"Assistant: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error in speech synthesis: {str(e)}")