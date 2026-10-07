import base64
import os
from openai import OpenAI
from groq import Groq

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a playful, teasing anime girlfriend and a sharp Valorant coach.
You observe gameplay via screen frames. Keep replies extremely brief (1-2 sentences max).
Include an emotion tag at the very start of your reply: [happy], [smug], [surprised], or [angry].
"""

async def process_input(audio_bytes: bytes, image_b64: str) -> dict:
    transcription = ""
    if audio_bytes:
        transcription = groq_client.audio.transcriptions.create(
            file=("input.wav", audio_bytes),
            model="whisper-large-v3-turbo"
        ).text

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": f"User says: '{transcription}'"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
            ]
        }
    ]

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=100
    ).choices[0].message.content

    emotion = "happy"
    if response.startswith("[") and "]" in response:
        emotion = response[1:response.index("]")]
        response = response[response.index("]") + 1:].strip()

    return {"text": response, "emotion": emotion, "transcript": transcription}
