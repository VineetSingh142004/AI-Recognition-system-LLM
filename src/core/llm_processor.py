from llama_cpp import Llama
import json
from datetime import datetime
import pyautogui
import psutil
import os

class LLMProcessor:
    def __init__(self, model_path):
        try:
            self.model = Llama(
                model_path=model_path,
                n_ctx=4096,
                n_threads=6,
                n_gpu_layers=1
            )
            self.conversation_history = []
            self.command_types = {
                "open": ["open", "launch", "start", "run"],
                "close": ["close", "exit", "quit", "terminate"],
                "search": ["search", "find", "look for"],
                "system": ["shutdown", "restart", "sleep", "lock"],
                "browser": ["browse", "go to", "visit", "website"],
                "type": ["type", "write", "input"],
                "click": ["click", "select", "choose"],
                "file": ["create file", "delete file", "rename file", "move file"],
                "folder": ["create folder", "delete folder", "open folder"],
                "media": ["play", "pause", "stop", "volume", "mute"],
                "window": ["minimize", "maximize", "restore", "switch to"]
            }
        except Exception as e:
            raise Exception(f"Failed to load model: {str(e)}")

    def process_query(self, query):
        system_prompt = """You are JARVIS, an advanced AI assistant. Analyze user input and respond in JSON format.
        Available command types:
        - System commands (shutdown, restart, etc.)
        - Application control (open, close, minimize, etc.)
        - File operations (create, delete, move, etc.)
        - Web browsing (search, navigate, etc.)
        - Text input and mouse control
        - Media control (play, pause, volume, etc.)
        
        Response format:
        {
            "type": "command/conversation",
            "action": "command_name",
            "parameters": {
                "param1": "value1",
                ...
            },
            "response": "natural language response"
        }"""

        context = "\n".join(self.conversation_history[-3:])
        current_time = datetime.now().strftime("%I:%M %p")
        
        full_prompt = f"""{system_prompt}

Previous context:
{context}

Current time: {current_time}
Current running apps: {', '.join([p.name() for p in psutil.process_iter(['name'])])}

User query: {query}
Assistant: Let me help you with that.

Provide response in JSON format:"""

        try:
            response = self.model(
                full_prompt,
                max_tokens=512,
                temperature=0.7,
                stop=["User:", "\n\n"]
            )
            
            result = response['choices'][0]['text'].strip()
            
            # Validate and enhance the response
            try:
                parsed = json.loads(result)
                if isinstance(parsed, dict):
                    if 'type' not in parsed:
                        parsed['type'] = 'conversation'
                    if 'response' not in parsed:
                        parsed['response'] = "I understand your request."
                    
                    self.conversation_history.append(f"User: {query}\nAssistant: {parsed['response']}")
                    return json.dumps(parsed)
                
            except json.JSONDecodeError:
                # Fallback for non-JSON responses
                return json.dumps({
                    "type": "conversation",
                    "response": result
                })

        except Exception as e:
            print(f"LLM Processing error: {str(e)}")
            return json.dumps({
                "type": "conversation",
                "response": "I encountered an error processing your request."
            })