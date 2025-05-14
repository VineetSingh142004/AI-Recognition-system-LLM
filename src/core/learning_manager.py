import json
from datetime import datetime
import os

class LearningManager:
    def __init__(self, storage_path="data/learning"):
        self.storage_path = storage_path
        self.interaction_history = []
        self.load_history()
        
    def load_history(self):
        """Load previous interaction history"""
        try:
            if not os.path.exists(self.storage_path):
                os.makedirs(self.storage_path)
                
            history_file = os.path.join(self.storage_path, "interaction_history.json")
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    self.interaction_history = json.load(f)
        except Exception as e:
            print(f"Error loading history: {e}")
    
    def save_interaction(self, command, response, success):
        """Save new interaction"""
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'command': command,
            'response': response,
            'success': success
        }
        self.interaction_history.append(interaction)
        
        try:
            with open(os.path.join(self.storage_path, "interaction_history.json"), 'w') as f:
                json.dump(self.interaction_history, f, indent=2)
        except Exception as e:
            print(f"Error saving interaction: {e}")
    
    def analyze_patterns(self):
        """Analyze interaction patterns for learning"""
        patterns = {}
        for interaction in self.interaction_history:
            command = interaction['command'].lower()
            success = interaction['success']
            
            if command not in patterns:
                patterns[command] = {'success': 0, 'total': 0}
            
            patterns[command]['total'] += 1
            if success:
                patterns[command]['success'] += 1
        
        return patterns