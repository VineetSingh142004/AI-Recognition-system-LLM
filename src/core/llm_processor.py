from llama_cpp import Llama
import json
from datetime import datetime

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
        except Exception as e:
            raise Exception(f"Failed to load model: {str(e)}")

    def process_query(self, query):
        system_prompt = """You are JARVIS, an AI assistant. Your responses should be natural and helpful.
        For tasks, respond in JSON format with 'type' and other relevant fields.
        For conversations, be engaging and natural.
        
        Examples:
        - "open chrome" -> {"type": "command", "action": "open", "parameters": {"name": "chrome"}}
        - "hello" -> {"type": "conversation", "response": "Hello! How can I help you today?"}
        - "what's the weather" -> {"type": "conversation", "response": "I'd be happy to check the weather for you."}
        """

        context = "\n".join(self.conversation_history[-3:])
        full_prompt = f"{system_prompt}\n\nPrevious context:\n{context}\n\nUser: {query}\nAssistant:"

        try:
            response = self.model(
                full_prompt,
                max_tokens=256,
                temperature=0.7,
                stop=["User:", "\n\n"]
            )

            result = response['choices'][0]['text'].strip()
            
            # Try to parse as JSON for commands
            try:
                parsed = json.loads(result)
                if isinstance(parsed, dict) and 'type' in parsed:
                    self.conversation_history.append(f"User: {query}\nAssistant: {result}")
                    return result
            except json.JSONDecodeError:
                # If not JSON, treat as conversation
                return json.dumps({
                    "type": "conversation",
                    "response": result
                })

        except Exception as e:
            return json.dumps({
                "type": "conversation",
                "response": "I apologize, but I encountered an error processing that request."
            })