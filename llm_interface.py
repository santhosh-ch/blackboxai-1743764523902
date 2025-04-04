from llama_cpp import Llama
import os
from typing import List, Dict

class LLMInterface:
    def __init__(self):
        model_path = os.getenv('LLM_MODEL_PATH', 'models/mistral-7b-instruct-v0.1.Q4_K_M.gguf')
        self.llm = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_threads=4,
            n_gpu_layers=1
        )
        self.conversation_history = []

    def generate_response(self, user_input: str) -> str:
        # Format prompt with conversation history
        prompt = self._format_prompt(user_input)
        
        # Generate response
        output = self.llm(
            prompt,
            max_tokens=150,
            temperature=0.7,
            top_p=0.9,
            echo=False,
            stop=["\n", " Human:", " AI:"]
        )
        
        # Extract and clean response
        response = output['choices'][0]['text'].strip()
        
        # Update conversation history
        self._update_history(user_input, response)
        
        return response

    def _format_prompt(self, user_input: str) -> str:
        prompt = "The following is a conversation with an AI sales assistant. The assistant is helpful, creative, and focused on making successful cold calls.\n\n"
        for turn in self.conversation_history[-4:]:  # Keep last 4 exchanges
            prompt += f"Human: {turn['user']}\nAI: {turn['assistant']}\n"
        prompt += f"Human: {user_input}\nAI:"
        return prompt

    def _update_history(self, user_input: str, response: str):
        self.conversation_history.append({
            'user': user_input,
            'assistant': response
        })

# Singleton instance
llm_interface = LLMInterface()

def generate_response(user_input: str) -> str:
    return llm_interface.generate_response(user_input)