from typing import List, Dict, Any
from collections import deque
from ..config.settings import MEMORY_CONFIG

class WindowBuffer:
    def __init__(self):
        self.window_size = MEMORY_CONFIG["window_size"]
        self.max_tokens = MEMORY_CONFIG["max_tokens"]
        self.buffer = deque(maxlen=self.window_size)
        
    def add(self, user_input: str, response: str) -> None:
        """
        Add a conversation turn to the buffer
        """
        conversation = {
            "user_input": user_input,
            "response": response,
            "timestamp": self._get_timestamp()
        }
        self.buffer.append(conversation)
    
    def get_context(self) -> List[Dict[str, Any]]:
        """
        Get the current conversation context
        """
        return list(self.buffer)
    
    def clear(self) -> None:
        """
        Clear the memory buffer
        """
        self.buffer.clear()
    
    def _get_timestamp(self) -> float:
        """
        Get current timestamp
        """
        from datetime import datetime
        return datetime.now().timestamp()
    
    def get_formatted_history(self) -> str:
        """
        Get formatted conversation history for LLM context
        """
        formatted_history = []
        for conv in self.buffer:
            formatted_history.extend([
                f"User: {conv['user_input']}",
                f"Assistant: {conv['response']}"
            ])
        return "\n".join(formatted_history) 