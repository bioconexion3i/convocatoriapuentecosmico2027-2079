from fastapi import FastAPI
from fastapi.responses import JSONResponse
import httpx
import os

app = FastAPI()
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")

@app.post("/chat")
async def chat_with_ollama(data: dict):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{OLLAMA_HOST}/api/chat", json=data)
            return response.json()
    except httpx.RequestError as e:
        print(f"Ollama connection error: {e}")
        return JSONResponse(status_code=500, content={"error": "Error de conexión con Ollama"})

@app.get("/health")
async def health_check():
    return {"status": "bridge_online"}
