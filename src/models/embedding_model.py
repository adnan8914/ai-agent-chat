from typing import List, Union
import torch
from transformers import AutoModel, AutoTokenizer
from ..config.settings import MODEL_CONFIG

class EmbeddingModel:
    def __init__(self):
        self.config = MODEL_CONFIG["embedding"]
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(self.config["model_name"])
        self.model = AutoModel.from_pretrained(self.config["model_name"]).to(self.device)
        
    def get_embeddings(self, texts: Union[str, List[str]]) -> List[float]:
        """
        Generate embeddings for input text(s)
        """
        if isinstance(texts, str):
            texts = [texts]
            
        # Tokenize texts
        encoded_input = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=self.config["max_length"],
            return_tensors="pt"
        ).to(self.device)
        
        # Generate embeddings
        with torch.no_grad():
            model_output = self.model(**encoded_input)
            embeddings = model_output.last_hidden_state[:, 0, :]  # Using [CLS] token
            
        # Convert tensor to list of floats
        return embeddings[0].cpu().tolist()  # Return first embedding as list
    
    def get_sentiment(self, text: str) -> dict:
        """
        Analyze sentiment of input text
        """
        embeddings = self.get_embeddings(text)
        # Here you would typically use a sentiment classification head
        # For now, we'll return a placeholder
        return {
            "sentiment": "neutral",
            "confidence": 0.0
        } 