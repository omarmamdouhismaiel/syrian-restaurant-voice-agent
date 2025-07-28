from audio.recorder import AudioRecorder
from audio.asr import Transcriber
from audio.tts import TextToSpeech
from datetime import datetime
import re

# ✅ Enhanced intent + entity detection
def detect_intent_and_entities(text):
    text = text.strip().lower()
    
    # Normalize Arabic characters
    text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ة", "ه").replace("ى", "ي")

    # Detect asking name or time
    if "اسمك" in text or "من انت" in text:
        return "ask_name", {}
    elif "الوقت" in text or "الساعة" in text:
        return "ask_time", {}

    # Detect food order
    food_items = ["شاورما", "بيبسي", "بطاطا", "كولا", "برجر", "بيتزا", "ماء", "عصير"]
    ordered = [item for item in food_items if item in text]
    if ordered:
        return "order_food", {"items": ordered}

    return "unknown", {}

class VoiceAgent:
    def __init__(self):
        self.recorder = AudioRecorder()
        self.transcriber = Transcriber()
        self.tts = TextToSpeech()

    def run(self):
        print("🎤 Voice Agent is running... Say something.")

        for audio_chunk in self.recorder.stream():
            if not audio_chunk:
                continue

            try:
                # 1. Transcribe speech to text
                text = self.transcriber.transcribe_audio(audio_chunk)
                if text:
                    print(f"👤 You said: {text}")

                    # 2. Detect intent and entities
                    intent, entities = detect_intent_and_entities(text)

                    # 3. Generate response
                    if intent == "ask_name":
                        response = "أنا مساعد صوتي سوري."
                    elif intent == "ask_time":
                        response = f"الساعة الآن {datetime.now().strftime('%H:%M')}."
                    elif intent == "order_food":
                        items = " و ".join(entities.get("items", []))
                        response = f"طلبت {items}. هل هذا صحيح؟"
                    else:
                        response = "لم أفهم قصدك، هل يمكنك التوضيح؟"

                    print(f"🤖 Responding: {response}")

                    # 4. Speak the response
                    self.tts.speak(response)

            except Exception as e:
                print(f"[❌ Error] {e}")
