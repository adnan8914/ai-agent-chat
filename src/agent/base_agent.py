from typing import Dict, Any, List
from ..models.llm_model import LLMModel

class AIAgent:
    def __init__(self):
        self.llm = LLMModel()
        self.conversation_history = []
        
    def process(self, user_input: str, context: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process user input and generate response"""
        try:
            # Format the state
            state = {
                'input': user_input,
                'memory': self._format_context(context) if context else [],
                'sentiment': 'neutral'
            }
            
            # Generate response with error handling
            try:
                response = self.llm.generate(state)
                if not response or 'response' not in response:
                    raise ValueError("Invalid response format")
                return response
                
            except Exception as e:
                print(f"LLM error: {str(e)}")
                return {
                    "response": "I'm having trouble understanding. Could you rephrase your question?"
                }
                
        except Exception as e:
            print(f"Processing error: {str(e)}")
            return {
                "response": "Something went wrong. Please try again."
            }
            
    def _format_context(self, context: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Format context for the LLM"""
        formatted_context = []
        for msg in context:
            formatted_context.append({
                'input': msg['content'] if msg['role'] == 'user' else '',
                'response': msg['content'] if msg['role'] == 'assistant' else ''
            })
        return formatted_context 