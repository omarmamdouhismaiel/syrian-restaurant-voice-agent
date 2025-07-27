#!/usr/bin/env python
# coding: utf-8

# In[ ]:

'''
LIVEKIT_URL = "ws://127.0.0.1:7880"  
LIVEKIT_API_KEY = "devkey"
LIVEKIT_API_SECRET = "secret"

ROOM_NAME = "test-room"
PARTICIPANT_NAME = "VoiceAgent"
LANGUAGE = "ar"
MODEL_SIZE = "base"
DEVICE = "cpu"
SAMPLE_RATE = 16000

import jwt
import time

def generate_token(identity=PARTICIPANT_NAME):
    grant = {
        "video": {
            "roomJoin": True,
            "room": ROOM_NAME
        }
    }

    now = int(time.time())
    exp = now + 3600  # token valid for 1 hour

    payload = {
        "jti": f"{identity}-{now}",
        "iss": LIVEKIT_API_KEY,
        "sub": identity,
        "nbf": now,
        "exp": exp,
        "video": grant["video"]
    }

    token = jwt.encode(payload, LIVEKIT_API_SECRET, algorithm="HS256")
    return token

LIVEKIT_TOKEN = generate_token() '''
import os
import time
import jwt  # Install with: pip install PyJWT
from dotenv import load_dotenv
load_dotenv()
# LiveKit credentials
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "LIVEKIT_API_SECRET")
LIVEKIT_URL = os.getenv("LIVEKIT_URL", "ws://localhost:7880")

# Transcription model
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")  # or "small", "medium", "large-v2"

# Assistant config
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "OPENAI_API_KEY")
ASSISTANT_NAME = "Syrian Voice Agent"
MODEL_SIZE = os.getenv("MODEL_SIZE", "medium")
DEVICE = os.getenv("DEVICE", "cpu")
LANGUAGE = os.getenv("LANGUAGE", "ar") 
# LiveKit Token Generator
def generate_token(identity: str, name: str = "VoiceAgent") -> str:
    """
    Generate a secure LiveKit access token.
    """
    payload = {
        "jti": f"{identity}-{int(time.time())}",
        "iss": LIVEKIT_API_KEY,
        "sub": identity,
        "name": name,
        "nbf": int(time.time()) - 10,
        "exp": int(time.time()) + 3600,  # 1 hour expiry
        "video": True,
        "audio": True,
        "room": "*",  # Allow access to any room
    }

    token = jwt.encode(payload, LIVEKIT_API_SECRET, algorithm="HS256")
    return token