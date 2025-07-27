# ui/app.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import requests
from audio.asr import transcribe_audio
from audio.tts import text_to_speech
from agent.voice_agent import detect_intent_and_entities

st.title("🔊 Syrian Voice Agent UI")
input_mode = st.radio("Input mode", ["Upload Audio", "Type Arabic"])

if input_mode == "Upload Audio":
    audio_file = st.file_uploader("Upload an Arabic audio file (.wav)", type=["wav"])
    if audio_file:
        with open("temp.wav", "wb") as f:
            f.write(audio_file.read())
        transcript = transcribe_audio("temp.wav")
        st.write("📝 Transcription:", transcript)

elif input_mode == "Type Arabic":
    text_input = st.text_input("اكتب بالعربية")
    if text_input:
        transcript = text_input
        st.write("📝 Transcription:", transcript)

if transcript:
    intent, entities = detect_intent_and_entities(transcript)
    st.write("📌 Intent:", intent)
    st.write("🍟 Order Items:", entities.get("items", []))

    response_text = f"أنت قلت: {transcript}"
    st.write("🗣️ Agent Response:", response_text)

    if st.button("🔊 Hear it"):
        audio_path = text_to_speech(response_text)
        audio_file = open(audio_path, 'rb')
        st.audio(audio_file.read(), format='audio/wav')
