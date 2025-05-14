# command_processor.py

import pyautogui
import os
import webbrowser
from datetime import datetime
import keyboard
from .screen_text_extractor import extract_text  # Update relative import

class EnhancedCommandProcessor:
    def __init__(self, llm_processor):
        self.llm = llm_processor
        self.commands = {
            'open': self._open_application,
            'close': self._close_application,
            'search': self._search,
            'click': self._click_element,
            'type': self._type_text,
            'scroll': self._scroll,
            'select': self._select,
            'file': self._file_operations
        }

    def process_command(self, command_text):
        """Process natural language commands using LLM"""
        # First, let LLM understand the intent
        llm_response = self.llm.process_query(command_text)
        
        # Extract action and parameters
        action, params = self._parse_llm_response(llm_response)
        
        if action in self.commands:
            return self.commands[action](params)
        else:
            # Handle as general conversation
            return llm_response

    def _parse_llm_response(self, response):
        """
        Parse the LLM response to extract action and parameters
        Example response format: "action: open, params: {"name": "chrome"}"
        """
        try:
            # Default values
            action = "unknown"
            params = {}
            
            if not response:
                return action, params

            # Simple parsing based on common keywords
            response = response.lower()
            
            # Check for actions
            if "open" in response:
                action = "open"
                # Extract application name
                params["name"] = response.split("open")[-1].strip()
            elif "close" in response:
                action = "close"
                params["name"] = response.split("close")[-1].strip()
            elif "search" in response:
                action = "search"
                query = response.split("search")[-1].strip()
                params["query"] = query
                params["location"] = "web" if "web" in response else "local"
            elif "click" in response:
                action = "click"
                params["target"] = response.split("click")[-1].strip()
            elif "type" in response:
                action = "type"
                params["text"] = response.split("type")[-1].strip()
            elif "scroll" in response:
                action = "scroll"
                params["direction"] = "down" if "down" in response else "up"
                params["amount"] = 1
            
            return action, params
        except Exception as e:
            print(f"Error parsing LLM response: {str(e)}")
            return "unknown", {}

    def _open_application(self, params):
        """Open an application or URL"""
        try:
            app_name = params.get('name', '').lower()
            if 'chrome' in app_name or 'browser' in app_name:
                webbrowser.open('https://google.com')
                return f"Opened {app_name}"
            elif 'notepad' in app_name:
                os.system('notepad.exe')
                return f"Opened {app_name}"
            else:
                try:
                    os.startfile(app_name)
                    return f"Opened {app_name}"
                except:
                    return f"Could not open {app_name}"
        except Exception as e:
            return f"Error opening application: {str(e)}"

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

    def _select(self, params):
        """Select text or elements"""
        try:
            target = params.get('target', '')
            elements = self.llm.get_screen_elements()
            
            if target in elements:
                pyautogui.click(elements[target])
                pyautogui.dragTo(elements[target][0] + 100, elements[target][1], duration=0.2)
                return f"Selected {target}"
            return "Element not found"
        except Exception as e:
            return f"Selection failed: {str(e)}"

    def _file_operations(self, params):
        """Handle file operations (open, save, delete, etc.)"""
        operation = params.get('operation')
        path = params.get('path')
        
        if operation == 'find':
            return self._find_file(path)
        elif operation == 'open':
            return self._open_file(path)
        # Add more file operations

    def _find_file(self, path):
        """Find a file in the specified path"""
        try:
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.lower() == path.lower():
                        return os.path.join(root, file)
            return "File not found"
        except Exception as e:
            return f"File search failed: {str(e)}"

    def _open_file(self, path):
        """Open a file"""
        try:
            os.startfile(path)
            return f"Opened file: {path}"
        except Exception as e:
            return f"Failed to open file: {str(e)}"