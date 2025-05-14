class CustomCommands:
    def __init__(self):
        self.custom_commands = {}
    
    def add_command(self, name, function):
        """Add a new custom command"""
        self.custom_commands[name] = function
    
    def execute_command(self, name, *args):
        """Execute a custom command"""
        if name in self.custom_commands:
            return self.custom_commands[name](*args)
        return f"Custom command '{name}' not found"