# audio/tts.py
import pyttsx3
from gtts import gTTS

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)

    def generate(self, text: str, output_path: str = "response.mp3"):
        tts = gTTS(text=text, lang='ar')
        tts.save(output_path)
        return output_path
