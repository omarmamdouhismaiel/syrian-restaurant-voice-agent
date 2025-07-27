#!/usr/bin/env python
# coding: utf-8

# In[ ]:


LIVEKIT_URL = "ws://127.0.0.1:7880"  # Replace with your actual LiveKit server URL
LIVEKIT_API_KEY = "devkey"
LIVEKIT_API_SECRET = "secret"

ROOM_NAME = "test-room"
PARTICIPANT_NAME = "VoiceAgent"

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

LIVEKIT_TOKEN = generate_token()