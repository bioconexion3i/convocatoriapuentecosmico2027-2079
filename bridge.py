from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
import uvicorn
import os

app = FastAPI(title="Stardust Bridge", version="1.0")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")

@app.post("/api/chat")
async def chat_proxy(request: Request):
    data = await request.json()
    if "model" not in data:
        return JSONResponse(status_code=400, content={"error": "Modelo no especificado"})
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(f"{OLLAMA_HOST}/api/chat", json=data)
            return response.json()
    except httpx.RequestError as e:
        return JSONResponse(status_code=500, content={"error": f"Error de conexión con Ollama: {str(e)}"})

@app.get("/health")
async def health_check():
    return {"status": "Stardust Bridge activo y en línea. In lak'ech."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8082)
