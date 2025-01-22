import torch
import numpy as np
from typing import Union
from pathlib import Path
import nemo.collections.tts as nemo_tts
from ..config.settings import MODEL_CONFIG

class TextToSpeech:
    def __init__(self):
        self.config = MODEL_CONFIG["text_to_speech"]
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # Load NeMo TTS models
        self.spec_generator = nemo_tts.models.FastPitchModel.from_pretrained(
            self.config["model_name"]
        ).to(self.device)
        self.vocoder = nemo_tts.models.HifiGanModel.from_pretrained(
            "nvidia/nemo-tts-hifigan-en"
        ).to(self.device)
        
    def synthesize(self, text: str, output_path: Union[str, Path] = None) -> np.ndarray:
        """
        Convert text to speech
        
        Args:
            text: Input text to convert to speech
            output_path: Optional path to save the audio file
        Returns:
            np.ndarray: Audio waveform
        """
        try:
            # Generate spectrogram
            parsed = self.spec_generator.parse(text)
            spectrogram = self.spec_generator.generate_spectrogram(
                tokens=parsed
            )
            
            # Convert spectrogram to audio
            audio = self.vocoder.convert_spectrogram_to_audio(
                spec=spectrogram
            )
            
            if output_path:
                self._save_audio(audio, output_path)
            
            return audio.cpu().numpy()
            
        except Exception as e:
            raise Exception(f"Error in speech synthesis: {str(e)}")
    
    def _save_audio(self, audio: torch.Tensor, path: Union[str, Path]) -> None:
        """
        Save audio to file
        """
        import soundfile as sf
        
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        audio_np = audio.cpu().numpy()
        sf.write(str(path), audio_np, samplerate=22050) 