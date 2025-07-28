import pyaudio
import numpy as np

class AudioRecorder:
    def __init__(self, sample_rate=16000, chunk=1024, record_seconds=4):
        self.sample_rate = sample_rate
        self.chunk = chunk
        self.record_seconds = record_seconds
        self.p = pyaudio.PyAudio()
        self.stream_in = self.p.open(format=pyaudio.paInt16,
                                     channels=1,
                                     rate=self.sample_rate,
                                     input=True,
                                     frames_per_buffer=self.chunk)

    def stream(self):
        while True:
            frames = []
            for _ in range(int(self.sample_rate / self.chunk * self.record_seconds)):
                data = self.stream_in.read(self.chunk, exception_on_overflow=False)
                frames.append(np.frombuffer(data, dtype=np.int16))

            audio = np.concatenate(frames).astype(np.float32) / 32768.0
            yield audio
