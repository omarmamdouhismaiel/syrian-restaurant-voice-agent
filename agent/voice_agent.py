from audio.recorder import AudioRecorder
from audio.asr import Transcriber
from audio.tts import TextToSpeech

class VoiceAgent:
    def __init__(self):
        self.recorder = AudioRecorder()
        self.transcriber = Transcriber()
        self.tts = TextToSpeech()

    def run(self):
        print("Voice Agent is running... Say something.")
        for audio_chunk in self.recorder.stream():
            if len(audio_chunk) == 0:
                continue
            try:
                # Transcribe speech to text
                text = self.transcriber.transcribe(audio_chunk)
                if text:
                    print(f"You said: {text}")

                    # Example response logic: echo
                    response = f"أنت قلت: {text}"
                    print(f"Responding: {response}")

                    # Speak the response
                    self.tts.speak(response)

            except Exception as e:
                print(f"[Error] {e}")
