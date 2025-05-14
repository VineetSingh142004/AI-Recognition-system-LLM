import cv2
import numpy as np
import pyautogui
import pytesseract
from PIL import Image
import torch
from transformers import AutoModelForObjectDetection, AutoFeatureExtractor

class ScreenAnalyzer:
    def __init__(self):
        self.screen_map = {}
        self.last_analyzed = None
        
    def analyze_screen(self):
        """Capture and analyze screen content"""
        screenshot = pyautogui.screenshot()
        img_np = np.array(screenshot)
        
        # Convert to grayscale for text detection
        gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
        
        # Extract text and clickable elements
        data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)
        
        # Map screen elements with their locations
        self.screen_map = {}
        for i, text in enumerate(data['text']):
            if text.strip():
                x, y = data['left'][i], data['top'][i]
                w, h = data['width'][i], data['height'][i]
                self.screen_map[text.lower()] = {
                    'position': (x + w//2, y + h//2),
                    'bounds': (x, y, w, h),
                    'confidence': data['conf'][i]
                }
        
        self.last_analyzed = screenshot
        return self.screen_map
    
    def find_element(self, target_text):
        """Find specific element on screen"""
        current_map = self.analyze_screen()
        
        # Try exact match first
        target_text = target_text.lower()
        if target_text in current_map:
            return current_map[target_text]['position']
        
        # Try fuzzy matching
        best_match = None
        best_ratio = 0
        for text, info in current_map.items():
            ratio = self._similarity_ratio(target_text, text)
            if ratio > 0.8 and ratio > best_ratio:
                best_ratio = ratio
                best_match = info['position']
        
        return best_match
    
    def _similarity_ratio(self, a, b):
        """Calculate text similarity ratio"""
        from difflib import SequenceMatcher
        return SequenceMatcher(None, a, b).ratio()