import torch
from abc import abstractmethod
from typing import List, Dict
from ollama import chat, ChatResponse

class LlamaWrapper():
    """
    A wrapper class for interacting with LLaMA models.
    """
    
    def __init__(self):
        self.model_name = 'llama3:8b'

    def set_model(self, model_name: str) -> None:
        self.model_name = model_name

    def chat(self, messages: List[Dict]) -> ChatResponse:
        try:
            response: ChatResponse = chat(
                model=self.model_name,
                messages=messages
            )
            return response
        except Exception as e:
            raise Exception(f"Error analyzing fields: {str(e)}")
