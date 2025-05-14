import speech_recognition as sr
import time
import sys
import os

# Adding the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.config.settings import Config

class VoiceRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.setup_recognizer()
        
    def setup_recognizer(self):
        """Configure the recognizer for better accuracy"""
        # Adjust for ambient noise
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = 4000  # Increase if in noisy environment
        self.recognizer.pause_threshold = 0.8    # Time of silence to consider the end of a phrase
        self.recognizer.phrase_threshold = 0.3   # Minimum seconds of speaking to consider a phrase
        
    def listen(self):
        """Listen for voice input with improved error handling"""
        with sr.Microphone() as source:
            print("Listening...")
            try:
                # Adjust for ambient noise before each listen
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Get audio input
                audio = self.recognizer.listen(source, 
                                             timeout=5.0,
                                             phrase_time_limit=15.0)
                
                print("Processing...")
                
                # Try multiple recognition services
                try:
                    # Try Google's recognizer first
                    text = self.recognizer.recognize_google(audio)
                except:
                    try:
                        # Fallback to Sphinx (offline)
                        text = self.recognizer.recognize_sphinx(audio)
                    except:
                        print("Could not understand audio")
                        return None
                
                print(f"Recognized: {text}")
                return text
                
            except sr.WaitTimeoutError:
                print("Listening timed out. Please try again.")
                return None
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                return None
            except Exception as e:
                print(f"Error in speech recognition: {e}")
                return None