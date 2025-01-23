from pathlib import Path
from typing import Dict
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base project paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_DIR = BASE_DIR / "models"

# Model configurations
MODEL_CONFIG = {
    "embedding": {
        "model_name": "sentence-transformers/all-MiniLM-L6-v2",
        "max_length": 512
    },
    "llm": {
        "model_name": os.getenv("MODEL_NAME", "mixtral-8x7b-instruct-v0.1"),
        "temperature": float(os.getenv("TEMPERATURE", 0.7)),
        "top_p": float(os.getenv("TOP_P", 0.9)),
        "max_length": int(os.getenv("MAX_LENGTH", 200))
    },
    "speech_to_text": {
        "model_name": "facebook/wav2vec2-base-960h"
    },
    "text_to_speech": {
        "model_name": "facebook/fastspeech2-en-ljspeech"
    },
    "image": {
        "model_name": "stabilityai/stable-diffusion-2-1"
    }
}

# Memory configuration
MEMORY_CONFIG = {
    "window_size": 5,  # Number of conversations to remember
    "max_tokens": 1000
}

# Tool configurations
TOOL_CONFIG = {
    "web_search": {
        "max_results": 5
    },
    "email": {
        "templates_path": str(BASE_DIR / "templates" / "email")
    },
    "content_creation": {
        "platforms": ["twitter", "instagram", "linkedin"]
    }
}

# API Keys
API_KEYS = {
    "nvidia": os.getenv("NVIDIA_API_KEY"),
    "tavily": os.getenv("TAVILY_API_KEY"),
    "huggingface": os.getenv("HUGGINGFACE_TOKEN")
} 