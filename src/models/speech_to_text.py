import torch
import numpy as np
from typing import Union
from pathlib import Path
import nemo.collections.asr as nemo_asr
from ..config.settings import MODEL_CONFIG

class SpeechToText:
    def __init__(self):
        self.config = MODEL_CONFIG["speech_to_text"]
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # Load NeMo ASR model
        self.model = nemo_asr.models.EncDecCTCModel.from_pretrained(
            self.config["model_name"]
        ).to(self.device)
        
    def transcribe(self, audio_input: Union[str, Path, np.ndarray]) -> str:
        """
        Transcribe audio to text
        
        Args:
            audio_input: Can be either a path to audio file or numpy array of audio data
        Returns:
            str: Transcribed text
        """
        try:
            if isinstance(audio_input, (str, Path)):
                # Process audio file
                transcription = self.model.transcribe([str(audio_input)])[0]
            else:
                # Process numpy array
                transcription = self.model.transcribe(audio_input)[0]
            
            return self._post_process_text(transcription)
            
        except Exception as e:
            raise Exception(f"Error in transcription: {str(e)}")
    
    def _post_process_text(self, text: str) -> str:
        """
        Clean up the transcribed text
        """
        # Remove multiple spaces
        text = ' '.join(text.split())
        # Capitalize first letter
        text = text.capitalize()
        return text 