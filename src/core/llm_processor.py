from llama_cpp import Llama
import json

class LLMProcessor:
    def __init__(self, model_path):
        try:
            # Optimize model settings for faster inference
            self.model = Llama(
                model_path=model_path,
                n_ctx=512,          # Reduced context window
                n_threads=4,        # Optimal thread count
                n_batch=8,          # Smaller batch size
                n_gpu_layers=1,     # Enable minimal GPU acceleration
                seed=42,
                verbose=False
            )
            # Pre-cache common responses
            self.quick_responses = {
                "hello": {"type": "conversation", "response": "Hello! How can I help?"},
                "hi": {"type": "conversation", "response": "Hi there!"},
                "bye": {"type": "conversation", "response": "Goodbye!"},
            }
        except Exception as e:
            raise Exception(f"Model initialization failed: {str(e)}")

    def process_query(self, query):
        # Quick response for common phrases
        lower_query = query.lower()
        if lower_query in self.quick_responses:
            return json.dumps(self.quick_responses[lower_query])

        # Pattern matching for common commands
        if "open" in lower_query:
            app = lower_query.replace("open", "").strip()
            return json.dumps({
                "type": "command",
                "action": "open",
                "parameters": {"name": app}
            })

        # Use LLM only for complex queries
        try:
            response = self.model(
                query,
                max_tokens=64,      # Reduced token limit
                temperature=0.7,
                stop=["User:", "\n"],
                echo=False
            )
            return json.dumps({
                "type": "conversation",
                "response": response['choices'][0]['text'].strip()
            })
        except Exception as e:
            print(f"LLM Error: {e}")
            return json.dumps({
                "type": "conversation",
                "response": "I encountered an error. Please try again."
            })