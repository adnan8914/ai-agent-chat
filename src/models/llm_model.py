from typing import Dict, Any
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from ..config.settings import MODEL_CONFIG, API_KEYS

class LLMModel:
    def __init__(self):
        try:
            self.config = MODEL_CONFIG["llm"]
            if not API_KEYS["nvidia"]:
                raise ValueError("NVIDIA API key not found")
            
            self.client = ChatNVIDIA(
                model=self.config["model_name"],
                api_key=API_KEYS["nvidia"],
                temperature=self.config["temperature"],
                top_p=self.config["top_p"],
                max_tokens=self.config["max_length"],
            )
        except Exception as e:
            print(f"Error initializing LLM: {str(e)}")
            self.use_fallback = True
        
    def generate(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate response based on input state"""
        if hasattr(self, 'use_fallback'):
            return {
                "response": "I'm a helpful AI assistant. I can help you with questions, coding, analysis, and more. What would you like to know?"
            }

        system_prompt = """You are a helpful and friendly AI assistant. Maintain a natural conversation flow.
        
        Core capabilities:
        - Answer questions and provide information
        - Help with analysis and problem-solving
        - Explain complex topics simply
        - Engage in casual conversation
        - Provide suggestions and recommendations"""
        
        user_query = state.get('input', '')
        if not user_query:
            return {"response": "I didn't catch that. Could you please try again?"}
        
        # Format context for conversation flow
        context_str = ""
        if state.get('memory'):
            last_exchanges = state['memory'][-3:]
            context_str = "\nPrevious conversation:\n" + "\n".join(
                [f"User: {c['input']}\nAssistant: {c['response']}" for c in last_exchanges]
            )
        
        prompt = f"{system_prompt}\n\n{context_str}\nUser: {user_query}\nAssistant:"
        
        try:
            response = self.client.invoke(prompt)
            content = response.content if hasattr(response, 'content') else str(response)
            
            if not content:
                return {"response": "Could you please rephrase that?"}
                
            return {"response": self._clean_response(content)}
            
        except Exception as e:
            print(f"Generation error: {str(e)}")
            return {"response": "I'm having trouble processing that. Could you try again?"}
            
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