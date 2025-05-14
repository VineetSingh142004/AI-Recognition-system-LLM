# src/commands/system_commands.py

def open_application(app_name):
    """Launches the specified application."""
    import os
    os.system(f'start {app_name}')

def search_file(file_name):
    """Searches for the specified file in the system."""
    import os
    for root, dirs, files in os.walk("C:\\"):
        if file_name in files:
            return os.path.join(root, file_name)
    return None