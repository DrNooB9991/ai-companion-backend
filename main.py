import base64
from fastapi import FastAPI, WebSocket
from brain import process_input

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "AI Companion Backend Running"}

@app.websocket("/ws/companion")
async def companion_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_json()
            audio_bytes = base64.b64decode(data.get("audio_b64", "")) if data.get("audio_b64") else b""
            image_b64 = data.get("image_b64", "")

            result = await process_input(audio_bytes, image_b64)
            await websocket.send_json(result)
        except Exception as e:
            print(f"Error: {e}")
            break
