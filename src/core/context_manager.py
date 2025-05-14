import json
from datetime import datetime
import difflib
import os

class ContextManager:
    def __init__(self):
        self.current_context = {
            "time": datetime.now().isoformat(),
            "active_app": None,
            "previous_commands": [],
            "conversation_topic": None,
            "user_intent": None,
            "system_state": {}
        }
        self.context_history = []
        self.max_history = 10
        self.context_file = "data/context/context_state.json"
        self._load_context()

    def update_context(self, command):
        """Update current context based on new command"""
        self.current_context["time"] = datetime.now().isoformat()
        self.current_context["previous_commands"].append(command)
        
        # Keep only recent commands
        if len(self.current_context["previous_commands"]) > 5:
            self.current_context["previous_commands"].pop(0)
            
        # Update topic and intent
        self._analyze_command(command)
        
        # Add to history
        self.context_history.append(self.current_context.copy())
        if len(self.context_history) > self.max_history:
            self.context_history.pop(0)
        
        # Auto-save context
        self.save_context()

    def _analyze_command(self, command):
        """Analyze command for topic and intent"""
        command = command.lower()
        
        # Topic detection
        topics = {
            "system": ["open", "close", "restart", "shutdown", "launch"],
            "browser": ["search", "browse", "website", "internet", "google"],
            "media": ["play", "pause", "volume", "music", "video"],
            "file": ["create", "delete", "save", "document", "folder"],
            "app": ["application", "program", "software", "install"],
            "utility": ["calculator", "notepad", "paint", "terminal"]
        }
        
        # Intent detection
        intents = {
            "action": ["open", "close", "start", "stop", "create", "delete"],
            "query": ["what", "how", "why", "when", "where", "who"],
            "control": ["increase", "decrease", "adjust", "set", "change"],
            "navigation": ["go to", "move to", "switch to", "back to"]
        }
        
        # Set topic
        for topic, keywords in topics.items():
            if any(keyword in command for keyword in keywords):
                self.current_context["conversation_topic"] = topic
                break
                
        # Set intent
        for intent, keywords in intents.items():
            if any(keyword in command for keyword in keywords):
                self.current_context["user_intent"] = intent
                break

    def get_current_context(self):
        """Get current context state"""
        return self.current_context

    def is_similar_context(self, cmd1, cmd2):
        """Check if two commands have similar context"""
        ratio = difflib.SequenceMatcher(None, cmd1.lower(), cmd2.lower()).ratio()
        return ratio > 0.8

    def save_context(self):
        """Save context to file"""
        try:
            os.makedirs(os.path.dirname(self.context_file), exist_ok=True)
            with open(self.context_file, "w") as f:
                json.dump({
                    "current_context": self.current_context,
                    "history": self.context_history,
                    "last_updated": datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            print(f"Error saving context: {e}")

    def _load_context(self):
        """Load context from file"""
        try:
            if os.path.exists(self.context_file):
                with open(self.context_file, "r") as f:
                    data = json.load(f)
                    self.current_context = data["current_context"]
                    self.context_history = data["history"]
        except Exception as e:
            print(f"Error loading context: {e}")

    def update_system_state(self, state_updates):
        """Update system state in context"""
        self.current_context["system_state"].update(state_updates)
        self.save_context()

    def clear_context(self):
        """Reset context to initial state"""
        self.current_context = {
            "time": datetime.now().isoformat(),
            "active_app": None,
            "previous_commands": [],
            "conversation_topic": None,
            "user_intent": None,
            "system_state": {}
        }
        self.context_history = []
        self.save_context()