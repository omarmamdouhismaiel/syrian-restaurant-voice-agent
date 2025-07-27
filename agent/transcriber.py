#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from faster_whisper import WhisperModel
import numpy as np

class Transcriber:
    def __init__(self, model_size="medium", device="cpu", compute_type="int8"):
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)

    def transcribe(self, audio_array):
        if not isinstance(audio_array, np.ndarray):
            return None
        segments, _ = self.model.transcribe(audio_array, language="ar", beam_size=5)
        return " ".join([segment.text for segment in segments])

