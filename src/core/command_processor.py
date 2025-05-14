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
from .ui_controller import UIController

class EnhancedCommandProcessor:
    def __init__(self, llm_processor):
        self.llm = llm_processor
        self.ui_controller = UIController()

    def process_command(self, command_text):
        try:
            # Get LLM response
            response = self.llm.process_query(command_text)
            command_data = json.loads(response)
            
            if command_data['type'] == 'command':
                # Execute UI command
                success = self.ui_controller.execute_command(
                    command_data['action'],
                    command_data.get('parameters', {})
                )
                
                if success:
                    return command_data.get('response', 'Command executed successfully')
                return "I couldn't complete that action"
                
            return command_data.get('response', "I understand")
            
        except Exception as e:
            print(f"Command processing error: {e}")
            return "I encountered an error processing your request"