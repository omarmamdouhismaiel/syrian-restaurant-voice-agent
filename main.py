import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from audio.recorder import AudioRecorder
from agent.voice_agent import VoiceAgent
import signal
import datetime

# ----------------------------
# 1. Global Variables
# ----------------------------
order_items = []
running = True

# ----------------------------
# 2. Handle Ctrl+C gracefully
# ----------------------------
def signal_handler(sig, frame):
    global running
    print("\n⛔ Exiting...")
    running = False

signal.signal(signal.SIGINT, signal_handler)

# ----------------------------
# 3. Phrases that end the call
# ----------------------------
def is_goodbye(text):
    return any(word in text for word in ["شكرا", "شكراً", "مع السلامة", "خلصت", "هذا كل شيء", "باي"])

# ----------------------------
# 4. Extract simple food orders
# ----------------------------
def detect_food_items(text):
    menu_items = ["بطاطس", "شاورما", "بيبسي", "كولا", "برجر", "عصير", "بيتزا", "ماء", "كباب", "فلافل"]
    found = [item for item in menu_items if item in text]
    return found

# ----------------------------
# 5. Save Order to File
# ----------------------------
def save_order_to_file(order_items):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"order_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("🧾 Order Summary:\n")
        for i, item in enumerate(order_items, 1):
            f.write(f"{i}. {item}\n")
    print(f"✅ Order saved to {filename}")

# ----------------------------
# 6. Main Application Logic
# ----------------------------
def main():
    global running
    agent = VoiceAgent()
    recorder = AudioRecorder()

    print("🎙️ Voice Agent is running... Say something.")
    for audio_chunk in recorder.stream():
        if not running:
            break

        text = text = agent.transcriber.transcribe(audio_chunk)
        if not text:
            continue

        print(f"You said: {text}")

        # 🛑 Exit command
        if is_goodbye(text):
            response = "شكرًا لطلبك! سيتم تجهيز طلبك حالًا. مع السلامة!"
            agent.respond(response)
            save_order_to_file(order_items)
            break

        # 🍔 Detect order items
        food = detect_food_items(text)
        if food:
            order_items.extend(food)
            response = f"تم إضافة {' و '.join(food)} إلى طلبك."
        else:
            response = f"أنت قلت: {text}"

        agent.respond(response)

    recorder.close()

if __name__ == "__main__":
    main()
