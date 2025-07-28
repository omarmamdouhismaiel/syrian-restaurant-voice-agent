import sys
import os
import streamlit as st
from datetime import datetime

# Add parent directory to import audio modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from audio.asr import Transcriber
from audio.tts import TextToSpeech
from agent.voice_agent import detect_intent_and_entities

# Initialize components
transcriber = Transcriber()
tts = TextToSpeech()

st.set_page_config(page_title="Syrian Voice Agent", layout="centered")
st.title("🔊 Syrian Voice Agent UI")

# Session state initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_audio_path" not in st.session_state:
    st.session_state.last_audio_path = None

if "input_pending" not in st.session_state:
    st.session_state.input_pending = False

# Input mode
input_mode = st.radio("اختار طريقة الإدخال", ["📁 رفع ملف صوتي", "⌨️ كتابة بالعربية"])
transcript = None

# Audio input
if input_mode == "📁 رفع ملف صوتي":
    audio_file = st.file_uploader("ارفع ملف صوتي بصيغة WAV", type=["wav"])
    if audio_file and not st.session_state.input_pending:
        with open("temp.wav", "wb") as f:
            f.write(audio_file.read())
        transcript = transcriber.transcribe_audio("temp.wav")
        if transcript:
            st.success("✅ تم تحويل الصوت إلى نص")
            st.write("📝 النص المكتوب:", transcript)
            st.session_state.input_pending = True
        else:
            st.error("❌ فشل في التعرف على الكلام")

# Text input
elif input_mode == "⌨️ كتابة بالعربية":
    transcript_input = st.text_input("✍️ اكتب جملة بالعربية", key="text_input")
    if transcript_input and not st.session_state.input_pending:
        transcript = transcript_input
        st.session_state.input_pending = True

# Process input
if st.session_state.input_pending and not st.session_state.last_audio_path:
    transcript = transcript or transcript_input
    intent, entities = detect_intent_and_entities(transcript)

    # Response logic
    if intent == "ask_name":
        response_text = "أنا مساعد صوتي سوري."
    elif intent == "ask_time":
        response_text = f"الساعة الآن {datetime.now().strftime('%H:%M')}."
    elif intent == "order_food" and entities.get("items"):
        items_str = " و ".join(entities["items"])
        response_text = f"تم تسجيل طلبك: {items_str}."
    else:
        response_text = "لم أفهم قصدك، هل يمكنك التوضيح؟"

    # Save to chat history
    st.session_state.chat_history.append((transcript, response_text))

    # Generate audio
    with st.spinner("🔊 يتم توليد الرد صوتيًا..."):
        audio_path = tts.generate(response_text)
        if os.path.exists(audio_path):
            st.session_state.last_audio_path = audio_path
        else:
            st.error("❌ لم يتم توليد الملف الصوتي")

# Chat history
if st.session_state.chat_history:
    st.markdown("### 💬 سجل المحادثة")
    for user_msg, bot_msg in st.session_state.chat_history:
        st.markdown(f"**🧑‍🦱 المستخدم:** {user_msg}")
        st.markdown(f"**🤖 المساعد:** {bot_msg}")

# Play audio and reset input state
if st.session_state.last_audio_path:
    st.audio(st.session_state.last_audio_path, format="audio/mp3")
    if st.button("👂 استمع وأرسل رسالة جديدة"):
        st.session_state.last_audio_path = None
        st.session_state.input_pending = False
        st.rerun()

# Reset button
st.sidebar.markdown("---")
if st.sidebar.button("🧹 إعادة تعيين المحادثة"):
    st.session_state.chat_history = []
    st.session_state.last_audio_path = None
    st.session_state.input_pending = False
    st.rerun()
