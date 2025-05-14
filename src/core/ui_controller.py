import pyautogui
import pygetwindow as gw
import cv2
import numpy as np
import pytesseract
from PIL import Image
import psutil
import os
import win32gui
import win32con
import win32api
import time

class UIController:
    def __init__(self):
        pyautogui.FAILSAFE = True
        self.active_window = None
        self.screen_elements = {}
        self.app_paths = self._get_installed_apps()

    def _get_installed_apps(self):
        """Get list of installed applications"""
        apps = {}
        # Common installation directories
        dirs = [
            os.environ.get('PROGRAMFILES', ''),
            os.environ.get('PROGRAMFILES(X86)', ''),
            os.environ.get('LOCALAPPDATA', ''),
            os.environ.get('APPDATA', '')
        ]
        
        # Search for executable files
        for directory in dirs:
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith('.exe'):
                        apps[file.lower().replace('.exe', '')] = os.path.join(root, file)
        return apps

    def analyze_window(self, window_title=None):
        """Analyze current active window"""
        try:
            # Get active window if not specified
            if not window_title:
                self.active_window = gw.getActiveWindow()
            else:
                windows = gw.getWindowsWithTitle(window_title)
                if windows:
                    self.active_window = windows[0]
                    self.active_window.activate()

            if self.active_window:
                # Take screenshot of window
                screenshot = pyautogui.screenshot(region=(
                    self.active_window.left,
                    self.active_window.top,
                    self.active_window.width,
                    self.active_window.height
                ))
                
                # Convert to CV2 format
                img_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                
                # Extract text and UI elements
                self.screen_elements = self._extract_elements(img_cv)
                return True
        except Exception as e:
            print(f"Window analysis error: {e}")
            return False

    def _extract_elements(self, img):
        """Extract clickable elements and text from image"""
        elements = {}
        
        # Extract text
        text_data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        
        for i, text in enumerate(text_data['text']):
            if text.strip():
                x = text_data['left'][i]
                y = text_data['top'][i]
                w = text_data['width'][i]
                h = text_data['height'][i]
                conf = text_data['conf'][i]
                
                elements[text.lower()] = {
                    'type': 'text',
                    'position': (x + w//2, y + h//2),
                    'bounds': (x, y, w, h),
                    'confidence': conf
                }
        
        return elements

    def execute_command(self, command_type, params):
        """Execute UI command"""
        try:
            if command_type == "open":
                return self._open_application(params.get('name', ''))
            elif command_type == "click":
                return self._click_element(params.get('target', ''))
            elif command_type == "type":
                return self._type_text(params.get('text', ''))
            elif command_type == "select":
                return self._select_element(params.get('target', ''))
            elif command_type == "window":
                return self._window_action(params.get('action', ''))
            return False
        except Exception as e:
            print(f"Command execution error: {e}")
            return False

    def _open_application(self, app_name):
        """Open any application"""
        try:
            app_name = app_name.lower()
            if app_name in self.app_paths:
                os.startfile(self.app_paths[app_name])
                time.sleep(1)  # Wait for app to start
                return self.analyze_window(app_name)
            else:
                # Try system commands
                os.system(f"start {app_name}")
                time.sleep(1)
                return True
        except Exception as e:
            print(f"Application launch error: {e}")
            return False

    def _click_element(self, target):
        """Click on UI element"""
        if not self.active_window:
            return False
            
        target = target.lower()
        if target in self.screen_elements:
            element = self.screen_elements[target]
            pyautogui.click(
                self.active_window.left + element['position'][0],
                self.active_window.top + element['position'][1]
            )
            return True
        return False

    def _type_text(self, text):
        """Type text in active window"""
        if self.active_window:
            self.active_window.activate()
            pyautogui.write(text)
            return True
        return False

    def _window_action(self, action):
        """Perform window action"""
        if not self.active_window:
            return False
            
        if action == "maximize":
            self.active_window.maximize()
        elif action == "minimize":
            self.active_window.minimize()
        elif action == "restore":
            self.active_window.restore()
        elif action == "close":
            self.active_window.close()
        return True