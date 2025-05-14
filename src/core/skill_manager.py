import os
import json
import importlib.util
from datetime import datetime

class SkillManager:
    def __init__(self):
        self.skills = {}
        self.learned_skills = {}
        self.skill_patterns = {}
        self.load_skills()

    def load_skills(self):
        """Load all skills from skills directory"""
        skills_dir = "data/skills"
        os.makedirs(skills_dir, exist_ok=True)
        
        # Load built-in skills
        self._load_built_in_skills()
        
        # Load learned skills
        self._load_learned_skills()

    def _load_built_in_skills(self):
        """Load built-in system skills"""
        self.skills.update({
            "system_control": {
                "patterns": ["shutdown", "restart", "sleep", "lock"],
                "handler": self._system_control_skill
            },
            "media_control": {
                "patterns": ["play", "pause", "volume", "mute"],
                "handler": self._media_control_skill
            },
            "file_operations": {
                "patterns": ["create file", "delete file", "rename"],
                "handler": self._file_operation_skill
            }
        })

    def _load_learned_skills(self):
        """Load learned skills from storage"""
        try:
            with open("data/skills/learned_skills.json", "r") as f:
                self.learned_skills = json.load(f)
        except FileNotFoundError:
            self.learned_skills = {}

    def has_skill_for(self, command):
        """Check if a skill exists for the command"""
        command = command.lower()
        
        # Check built-in skills
        for skill in self.skills.values():
            if any(pattern in command for pattern in skill["patterns"]):
                return True
                
        # Check learned skills
        for patterns in self.learned_skills.values():
            if any(pattern in command for pattern in patterns):
                return True
                
        return False

    def execute_skill(self, command):
        """Execute appropriate skill for command"""
        command = command.lower()
        
        # Try built-in skills
        for skill_name, skill in self.skills.items():
            if any(pattern in command for pattern in skill["patterns"]):
                return skill["handler"](command)
                
        # Try learned skills
        for skill_name, patterns in self.learned_skills.items():
            if any(pattern in command for pattern in patterns):
                return self._execute_learned_skill(skill_name, command)
                
        return "No skill found for this command"

    def _system_control_skill(self, command):
        """Built-in system control skill"""
        import os
        if "shutdown" in command:
            os.system("shutdown /s /t 1")
            return "Shutting down system"
        elif "restart" in command:
            os.system("shutdown /r /t 1")
            return "Restarting system"
        elif "sleep" in command:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            return "Putting system to sleep"
        return "System command not recognized"

    def _media_control_skill(self, command):
        """Built-in media control skill"""
        import pyautogui
        if "play" in command or "pause" in command:
            pyautogui.press("playpause")
            return "Toggled play/pause"
        elif "volume up" in command:
            pyautogui.press("volumeup")
            return "Increased volume"
        elif "volume down" in command:
            pyautogui.press("volumedown")
            return "Decreased volume"
        return "Media command not recognized"

    def _file_operation_skill(self, command):
        """Built-in file operation skill"""
        import os
        if "create file" in command:
            filename = command.split("create file")[-1].strip()
            open(filename, 'a').close()
            return f"Created file: {filename}"
        elif "delete file" in command:
            filename = command.split("delete file")[-1].strip()
            os.remove(filename)
            return f"Deleted file: {filename}"
        return "File operation not recognized"

    def learn_new_skill(self, name, patterns, actions):
        """Learn a new skill from user interaction"""
        self.learned_skills[name] = {
            "patterns": patterns,
            "actions": actions,
            "learned_at": datetime.now().isoformat()
        }
        self.save_learned_skills()

    def save_learned_skills(self):
        """Save learned skills to storage"""
        with open("data/skills/learned_skills.json", "w") as f:
            json.dump(self.learned_skills, f, indent=2)