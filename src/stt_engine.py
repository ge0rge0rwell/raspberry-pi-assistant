from faster_whisper import WhisperModel
import numpy as np

class STTEngine:
    def __init__(self, model_size="tiny"):
        # Run on CPU with int8 quantization for speed on RPi
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")

    def transcribe(self, audio_data):
        # audio_data should be a float32 numpy array
        segments, info = self.model.transcribe(audio_data, beam_size=5)
        text = " ".join([segment.text for segment in segments])
        return text.strip()
