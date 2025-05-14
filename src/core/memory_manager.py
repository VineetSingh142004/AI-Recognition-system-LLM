import json
import os
from datetime import datetime
from collections import defaultdict

class MemoryManager:
    def __init__(self, storage_path):
        self.storage_path = storage_path
        self.interactions = []
        self.patterns = defaultdict(int)
        self.successful_patterns = defaultdict(int)
        self.load_state()

    def store_interaction(self, interaction_data):
        """Store new interaction"""
        self.interactions.append(interaction_data)
        
        # Update pattern recognition
        command = interaction_data["command"].lower()
        success = interaction_data["success"]
        
        self.patterns[command] += 1
        if success:
            self.successful_patterns[command] += 1
        
        # Auto-save after significant changes
        if len(self.interactions) % 10 == 0:
            self.save_state()

    def get_success_rate(self, command):
        """Get success rate for a command pattern"""
        command = command.lower()
        if command in self.patterns:
            total = self.patterns[command]
            successful = self.successful_patterns[command]
            return successful / total
        return 0

    def get_similar_interactions(self, command, threshold=0.8):
        """Find similar successful interactions"""
        from difflib import SequenceMatcher
        
        similar = []
        for interaction in self.interactions:
            similarity = SequenceMatcher(None, 
                                       command.lower(), 
                                       interaction["command"].lower()).ratio()
            if similarity >= threshold and interaction["success"]:
                similar.append(interaction)
        return similar

    def analyze_patterns(self):
        """Analyze interaction patterns"""
        analysis = {
            "total_interactions": len(self.interactions),
            "success_rate": sum(1 for i in self.interactions if i["success"]) / len(self.interactions),
            "common_patterns": dict(sorted(self.patterns.items(), key=lambda x: x[1], reverse=True)[:10]),
            "successful_patterns": dict(sorted(self.successful_patterns.items(), key=lambda x: x[1], reverse=True)[:10])
        }
        return analysis

    def save_state(self):
        """Save current state to storage"""
        os.makedirs(self.storage_path, exist_ok=True)
        
        state = {
            "interactions": self.interactions,
            "patterns": dict(self.patterns),
            "successful_patterns": dict(self.successful_patterns),
            "last_updated": datetime.now().isoformat()
        }
        
        with open(os.path.join(self.storage_path, "memory_state.json"), "w") as f:
            json.dump(state, f, indent=2)

    def load_state(self):
        """Load state from storage"""
        try:
            path = os.path.join(self.storage_path, "memory_state.json")
            if os.path.exists(path):
                with open(path, "r") as f:
                    state = json.load(f)
                    self.interactions = state["interactions"]
                    self.patterns = defaultdict(int, state["patterns"])
                    self.successful_patterns = defaultdict(int, state["successful_patterns"])
        except Exception as e:
            print(f"Error loading memory state: {e}")