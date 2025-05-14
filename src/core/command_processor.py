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
import pygetwindow as gw
from pathlib import Path
from .screen_analyzer import ScreenAnalyzer
from .learning_manager import LearningManager

class EnhancedCommandProcessor:
    def __init__(self, llm_processor):
        self.llm = llm_processor
        self.screen_analyzer = ScreenAnalyzer()
        self.learning_manager = LearningManager()
        self.commands = {
            'open': self._open_application,
            'close': self._close_application,
            'search': self._search,
            'type': self._type_text,
            'click': self._click_element,
            'scroll': self._scroll,
            'system': self._system_control,
            'browser': self._browser_control,
            'file': self._file_operations,
            'folder': self._folder_operations,
            'media': self._media_control,
            'window': self._window_control
        }
        
        self.app_paths = self._get_installed_apps()
        
    def _get_installed_apps(self):
        """Get dictionary of installed applications"""
        apps = {
            'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'explorer': 'explorer.exe'
        }
        
        # Add Microsoft Office apps if installed
        office_path = r'C:\Program Files\Microsoft Office\root\Office16'
        if os.path.exists(office_path):
            apps.update({
                'word': os.path.join(office_path, 'WINWORD.EXE'),
                'excel': os.path.join(office_path, 'EXCEL.EXE'),
                'powerpoint': os.path.join(office_path, 'POWERPNT.EXE')
            })
            
        return apps

    def _open_application(self, params):
        """Open an application or URL"""
        try:
            app_name = params.get('name', '').lower()
            
            # Check if it's a known application
            if app_name in self.app_paths:
                subprocess.Popen(self.app_paths[app_name])
                return True
                
            # Try to open as a website if it contains domain indicators
            elif any(x in app_name for x in ['.com', '.org', '.net', 'www.']):
                url = app_name if app_name.startswith('http') else f'https://{app_name}'
                webbrowser.open(url)
                return True
                
            # Try to open as a general command
            else:
                os.system(f'start {app_name}')
                return True
        except Exception as e:
            print(f"Error opening application: {str(e)}")
            return False

    def _close_application(self, params):
        """Close an application"""
        try:
            app_name = params.get('name', '').lower()
            for proc in psutil.process_iter(['name']):
                if app_name in proc.info['name'].lower():
                    proc.kill()
            return True
        except Exception as e:
            print(f"Error closing application: {str(e)}")
            return False

    def _type_text(self, params):
        """Type text at current cursor position"""
        try:
            text = params.get('text', '')
            pyautogui.write(text)
            return True
        except Exception as e:
            print(f"Error typing text: {str(e)}")
            return False

    def _click_element(self, params):
        """Click on a screen element"""
        try:
            target = params.get('target', '')
            position = self.screen_analyzer.find_element(target)
            if position:
                pyautogui.click(position)
                return True
            return False
        except Exception as e:
            print(f"Error clicking element: {str(e)}")
            return False

    def _scroll(self, params):
        """Scroll the screen"""
        try:
            direction = params.get('direction', 'down')
            amount = int(params.get('amount', 1))
            
            if direction == 'down':
                pyautogui.scroll(-amount * 100)
            else:
                pyautogui.scroll(amount * 100)
            return True
        except Exception as e:
            print(f"Error scrolling: {str(e)}")
            return False

    def _search(self, params):
        """Perform a search operation"""
        try:
            query = params.get('query', '')
            location = params.get('location', 'web')
            
            if location == 'web':
                url = f'https://www.google.com/search?q={query}'
                webbrowser.open(url)
            elif location == 'local':
                # Windows file search
                os.system(f'explorer /root,, /select,"{query}"')
            return True
        except Exception as e:
            print(f"Error performing search: {str(e)}")
            return False

    def _system_control(self, params):
        """Control system operations"""
        try:
            action = params.get('action', '')
            if action == 'shutdown':
                os.system('shutdown /s /t 1')
            elif action == 'restart':
                os.system('shutdown /r /t 1')
            elif action == 'sleep':
                os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
            elif action == 'lock':
                os.system('rundll32.exe user32.dll,LockWorkStation')
            return True
        except Exception as e:
            print(f"Error in system control: {str(e)}")
            return False

    def _window_control(self, params):
        """Control window states"""
        try:
            action = params.get('action')
            target = params.get('target')
            
            windows = gw.getWindowsWithTitle(target)
            if windows:
                window = windows[0]
                if action == 'minimize':
                    window.minimize()
                elif action == 'maximize':
                    window.maximize()
                elif action == 'restore':
                    window.restore()
                elif action == 'switch':
                    window.activate()
                return True
            return False
        except Exception as e:
            print(f"Window control error: {str(e)}")
            return False

    def _file_operations(self, params):
        """Handle file operations"""
        try:
            action = params.get('action')
            path = params.get('path')
            
            if action == 'create':
                Path(path).touch()
            elif action == 'delete':
                os.remove(path)
            elif action == 'rename':
                os.rename(path, params.get('new_name'))
            elif action == 'move':
                os.rename(path, params.get('new_path'))
            return True
        except Exception as e:
            print(f"File operation error: {str(e)}")
            return False

    def _folder_operations(self, params):
        """Handle folder operations"""
        try:
            action = params.get('action')
            path = params.get('path')
            
            if not path:
                return False
                
            if action == 'create':
                os.makedirs(path, exist_ok=True)
            elif action == 'delete':
                os.rmdir(path)  # Only removes empty directories
            elif action == 'open':
                os.startfile(path)
            elif action == 'rename':
                new_name = params.get('new_name')
                if new_name:
                    os.rename(path, os.path.join(os.path.dirname(path), new_name))
            elif action == 'list':
                if os.path.exists(path):
                    return [f for f in os.listdir(path)]
                
            return True
        except Exception as e:
            print(f"Folder operation error: {str(e)}")
            return False

    def _browser_control(self, params):
        """Handle browser operations"""
        try:
            action = params.get('action')
            url = params.get('url')
            
            if not url.startswith('http'):
                url = f'https://{url}'
                
            webbrowser.open(url)
            return True
        except Exception as e:
            print(f"Browser control error: {str(e)}")
            return False

    def _media_control(self, params):
        """Control media playback and volume"""
        try:
            action = params.get('action', '').lower()
            
            # Map keys for media control
            key_map = {
                'play': 'playpause',
                'pause': 'playpause',
                'stop': 'stop',
                'next': 'nexttrack',
                'previous': 'prevtrack',
                'mute': 'volumemute',
                'volume_up': 'volumeup',
                'volume_down': 'volumedown'
            }
            
            if action in key_map:
                keyboard.press_and_release(key_map[action])
            elif action == 'volume':
                # Handle specific volume level
                level = params.get('level', 50)  # Default to 50%
                current_level = 0
                # Mute first to ensure we start from 0
                keyboard.press_and_release('volumemute')
                # Increase volume to desired level
                for _ in range(int(level/2)):  # Each press increases by ~2%
                    keyboard.press_and_release('volumeup')
                    current_level += 2
            
            return True
        except Exception as e:
            print(f"Media control error: {str(e)}")
            return False

    def _interact_with_element(self, params):
        """Handle screen element interaction"""
        try:
            action = params.get('action', 'click')
            target = params.get('target')
            
            if not target:
                return False
                
            # Find element on screen
            element_pos = self.screen_analyzer.find_element(target)
            if not element_pos:
                return False
            
            # Perform action
            if action == 'click':
                pyautogui.click(element_pos)
            elif action == 'double_click':
                pyautogui.doubleClick(element_pos)
            elif action == 'right_click':
                pyautogui.rightClick(element_pos)
            
            return True
        except Exception as e:
            print(f"Screen interaction error: {str(e)}")
            return False

    def process_command(self, command_text):
        try:
            llm_response = self.llm.process_query(command_text)
            response_data = json.loads(llm_response)
            
            success = False
            response = "I couldn't complete that action."
            
            if response_data['type'] == 'conversation':
                success = True
                response = response_data['response']
            
            elif response_data['type'] == 'command':
                action = response_data.get('action')
                if action in self.commands:
                    success = self.commands[action](response_data.get('parameters', {}))
                    response = response_data.get('response') if success else "I had trouble with that action."
            
            # Save interaction for learning
            self.learning_manager.save_interaction(command_text, response, success)
            
            return response
            
        except Exception as e:
            print(f"Command processing error: {str(e)}")
            return "I encountered an error processing your request."