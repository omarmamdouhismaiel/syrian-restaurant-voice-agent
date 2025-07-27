from faster_whisper import WhisperModel
import numpy as np

class Transcriber:
    def __init__(self):
        from agent.config import MODEL_SIZE, DEVICE, LANGUAGE
        self.model = WhisperModel(MODEL_SIZE, device=DEVICE)
        self.language = LANGUAGE

    def transcribe(self, audio):
        segments, _ = self.model.transcribe(audio, language=self.language, beam_size=1)
        text = " ".join([seg.text for seg in segments])
        return text.strip()
