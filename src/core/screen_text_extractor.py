import pytesseract
import pyautogui
from PIL import Image
import numpy as np
import cv2

# Configure Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text(region=None):
    """Extract text from screen or specific region"""
    try:
        screenshot = pyautogui.screenshot(region=region)
        image_np = np.array(screenshot)
        gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        return text.strip()
    except Exception as e:
        print(f"Error extracting text: {str(e)}")
        return ""

def get_screen_elements():
    """Get clickable elements on screen"""
    try:
        screenshot = pyautogui.screenshot()
        image_np = np.array(screenshot)
        data = pytesseract.image_to_data(image_np, output_type=pytesseract.Output.DICT)
        elements = {}
        for i, text in enumerate(data['text']):
            if text.strip():
                x, y = data['left'][i], data['top'][i]
                elements[text] = (x, y)
        return elements
    except Exception as e:
        print(f"Error getting elements: {str(e)}")
        return {}