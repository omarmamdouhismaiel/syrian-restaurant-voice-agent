from flask import Flask, request, jsonify, send_file
import uuid
import json
from gtts import gTTS
import os

app = Flask(__name__)
orders = []

def generate_audio(text):
    tts = gTTS(text, lang="ar")
    tts.save("response.mp3")

@app.route("/submit-order", methods=["POST"])
def submit_order():
    data = request.get_json()
    name = data.get("name")
    order_list = data.get("order")

    order_id = str(uuid.uuid4())[:8]
    eta = "15 minutes"

    order_entry = {
        "id": order_id,
        "name": name,
        "order": order_list,
        "eta": eta
    }
    orders.append(order_entry)

    with open("orders.json", "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

    return jsonify({"order_id": order_id, "eta": eta})

@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()
    text = data.get("text", "")
    
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        generate_audio(text)
        return send_file("response.mp3", mimetype="audio/mpeg")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
