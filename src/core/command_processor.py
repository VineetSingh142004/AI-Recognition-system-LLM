# command_processor.py

import pyautogui
import os
import webbrowser
import json
import psutil
import keyboard
from datetime import datetime
import win32gui
import win32con
import subprocess

class EnhancedCommandProcessor:
    def __init__(self, llm_processor):
        self.llm = llm_processor
        self.commands = {
            'open': self._open_application,
            'close': self._close_application,
            'search': self._search,
            'type': self._type_text,
            'click': self._click_element,
            'scroll': self._scroll,
            'minimize': self._minimize_window,
            'maximize': self._maximize_window,
            'switch': self._switch_window
        }
        
        # Common applications paths
        self.app_paths = {
            'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'word': r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE',
            'excel': r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE'
        }

    def process_command(self, command_text):
        try:
            # Get LLM response
            llm_response = self.llm.process_query(command_text)
            response_data = json.loads(llm_response)
            
            if response_data['type'] == 'conversation':
                return response_data['response']
            
            elif response_data['type'] == 'command':
                action = response_data.get('action')
                if action in self.commands:
                    success = self.commands[action](response_data.get('parameters', {}))
                    if success:
                        return f"I've completed the {action} command successfully."
                    return f"I had trouble with the {action} command. Please try again."
                return f"I understand you want me to {action}, but I'm not sure how to do that yet."
            
            return "I'm not sure how to help with that. Could you try rephrasing?"
            
        except json.JSONDecodeError:
            print(f"Debug - Invalid JSON: {llm_response}")
            return "I had trouble understanding that. Could you rephrase it?"
        except Exception as e:
            print(f"Debug - Error: {str(e)}")
            return "I encountered an error processing your request."

    def _open_application(self, params):
        app_name = params.get('name', '').lower()
        
        try:
            if app_name in self.app_paths:
                subprocess.Popen(self.app_paths[app_name])
            elif app_name.endswith('.exe'):
                subprocess.Popen(app_name)
            else:
                os.system(f"start {app_name}")
            return True
        except Exception as e:
            return False

    def _close_application(self, params):
        """Close an application"""
        try:
            app_name = params.get('name', '')
            os.system(f'taskkill /F /IM {app_name}.exe')
            return f"Closed {app_name}"
        except Exception as e:
            return f"Error closing application: {str(e)}"

    def _search(self, params):
        """Perform a search operation"""
        try:
            query = params.get('query', '')
            location = params.get('location', 'web')
            
            if location == 'web':
                webbrowser.open(f'https://google.com/search?q={query}')
                return f"Searching web for: {query}"
            elif location == 'local':
                # Implement local file search
                return f"Searching local files for: {query}"
            return "Search location not specified"
        except Exception as e:
            return f"Search failed: {str(e)}"

    def _click_element(self, params):
        """Click on screen elements"""
        try:
            # Use screen text extraction to find element
            elements = self.llm.get_screen_elements()
            target = params.get('target')
            if target in elements:
                pyautogui.click(elements[target])
                return f"Clicked on {target}"
            return "Element not found"
        except Exception as e:
            return f"Click failed: {str(e)}"

    def _type_text(self, params):
        """Type text at current cursor position"""
        try:
            text = params.get('text', '')
            keyboard.write(text)
            return f"Typed: {text}"
        except Exception as e:
            return f"Typing failed: {str(e)}"

    def _scroll(self, params):
        """Scroll the screen"""
        try:
            direction = params.get('direction', 'down')
            amount = params.get('amount', 1)
            
            if direction == 'down':
                pyautogui.scroll(-amount * 100)
            else:
                pyautogui.scroll(amount * 100)
            return f"Scrolled {direction}"
        except Exception as e:
            return f"Scroll failed: {str(e)}"

    def _minimize_window(self, params):
        """Minimize the current window"""
        try:
            hwnd = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            return "Window minimized"
        except Exception as e:
            return f"Failed to minimize window: {str(e)}"

    def _maximize_window(self, params):
        """Maximize the current window"""
        try:
            hwnd = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            return "Window maximized"
        except Exception as e:
            return f"Failed to maximize window: {str(e)}"

    def _switch_window(self, params):
        """Switch to another window"""
        try:
            window_name = params.get('name', '')
            hwnd = win32gui.FindWindow(None, window_name)
            if hwnd:
                win32gui.SetForegroundWindow(hwnd)
                return f"Switched to window: {window_name}"
            return "Window not found"
        except Exception as e:
            return f"Failed to switch window: {str(e)}"