from typing import Dict, Any
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from ..config.settings import MODEL_CONFIG, API_KEYS

class LLMModel:
    def __init__(self):
        self.config = MODEL_CONFIG["llm"]
        self.client = ChatNVIDIA(
            model=self.config["model_name"],
            api_key=API_KEYS["nvidia"],
            temperature=self.config["temperature"],
            top_p=self.config["top_p"],
            max_tokens=self.config["max_length"],
        )
        
    def generate(self, state: Dict[str, Any]) -> str:
        """
        Generate response based on input state
        """
        # Create a prompt template
        system_prompt = """You are a helpful AI assistant. Please provide detailed, accurate, 
        and helpful responses to user queries. Use the context provided to give relevant information."""
        
        user_query = state['input']
        context = state.get('memory', [])
        
        # Format context if available
        context_str = ""
        if context:
            context_str = "\nPrevious conversation:\n" + "\n".join(
                [f"User: {c['input']}\nAssistant: {c['response']}" for c in context]
            )
        
        # Combine all parts into final prompt
        prompt = f"{system_prompt}\n{context_str}\n\nUser: {user_query}\nAssistant:"
        
        try:
            # Generate response using NVIDIA AI endpoint
            response = self.client.invoke(prompt)
            # Extract content from AIMessage
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return "I apologize, but I encountered an error. Could you please try again?"
    
    def _format_context(self, context: list) -> str:
        """
        Format conversation context for the model
        """
        if not context:
            return ""
        
        formatted_context = []
        for conv in context:
            formatted_context.extend([
                f"User: {conv['user_input']}",
                f"Assistant: {conv['response']}"
            ])
        return "\n".join(formatted_context)
    
    def _create_prompt(self, context: str, user_input: str, sentiment: str) -> str:
        """
        Create a prompt for the model
        """
        system_prompt = (
            "You are a helpful AI assistant. "
            "Consider the user's sentiment and previous context when responding."
        )
        
        prompt = f"{system_prompt}\n\n"
        if context:
            prompt += f"Previous conversation:\n{context}\n\n"
        
        prompt += f"User sentiment: {sentiment}\n"
        prompt += f"User: {user_input}\nAssistant:"
        
        return prompt
    
    def _extract_response(self, generated_text: str) -> str:
        """
        Extract the actual response from generated text
        """
        # Find the last "Assistant:" in the text and return everything after it
        if "Assistant:" in generated_text:
            response = generated_text.split("Assistant:")[-1].strip()
            return response
        return generated_text.strip() 