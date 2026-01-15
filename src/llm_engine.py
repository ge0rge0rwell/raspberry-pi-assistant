import requests
import json

class LLMEngine:
    def __init__(self, model="tinyllama"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def generate(self, prompt):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            return response.json().get("response", "I'm sorry, I couldn't think of anything.")
        except Exception as e:
            return f"Error connecting to Ollama: {str(e)}"
