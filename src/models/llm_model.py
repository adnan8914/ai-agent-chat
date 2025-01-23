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
        
    def generate(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate response based on input state"""
        try:
            # Create a better prompt template
            system_prompt = """You are a helpful and friendly AI assistant. Maintain a natural conversation flow.

Core capabilities:
- Answer questions and provide information
- Help with analysis and problem-solving
- Explain complex topics simply
- Engage in casual conversation
- Provide suggestions and recommendations

Style guidelines:
- Be friendly and conversational
- Keep responses concise but informative
- Show understanding and empathy
- Ask follow-up questions when appropriate
- Stay focused on the user's needs

Remember previous context and maintain conversation continuity."""
            
            user_query = state.get('input', '')
            context = state.get('memory', [])
            
            # Format context for conversation flow
            context_str = ""
            if context:
                last_exchanges = context[-3:]  # Get last 3 exchanges for context
                context_str = "\nPrevious conversation:\n" + "\n".join(
                    [f"User: {c['input']}\nAssistant: {c['response']}" for c in last_exchanges]
                )
            
            # Combine all parts into final prompt
            prompt = f"{system_prompt}\n\n{context_str}\nUser: {user_query}\nAssistant:"
            
            try:
                response = self.client.invoke(prompt)
                content = response.content if hasattr(response, 'content') else str(response)
                
                if not content:
                    return {"response": "Could you please rephrase that? I want to make sure I understand correctly."}
                    
                cleaned_response = self._clean_response(content)
                return {"response": cleaned_response}
                
            except Exception as e:
                print(f"LLM Error: {str(e)}")
                return {"response": "I'd like to help but having a small technical issue. Could you try asking that again?"}
                
        except Exception as e:
            print(f"Generation Error: {str(e)}")
            return {"response": "Let's start fresh - what would you like to know?"}
    
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

    def _clean_response(self, response: str) -> str:
        """Clean up the response text"""
        # Remove any "Assistant:" prefix
        response = response.replace("Assistant:", "").strip()
        
        # Remove any JSON formatting if present
        if response.startswith('{"response":'):
            try:
                response = eval(response)["response"]
            except:
                pass
            
        return response 