import os
import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# Set your OpenRouter API key
OPENROUTER_API_KEY = "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"  # <-- replace with your key or load from env

# CORS settings
origins = [
    "http://localhost:5501",
    "http://127.0.0.1:5501",
    "https://uplift-sia.web.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Chatbot backend is running!"}

@app.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()
        user_message = body.get("message")

        if not user_message:
            return JSONResponse(content={"error": "No message provided"}, status_code=400)

        # Send request to OpenRouter
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "openai/gpt-4o",  # or try "mistralai/mixtral-8x7b"
            "messages": [{"role": "user", "content": user_message}]
        }

        async with httpx.AsyncClient() as client:
            response = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
            data = response.json()

        bot_response = data["choices"][0]["message"]["content"]
        return JSONResponse(content={"response": bot_response})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/generate-topic")
async def generate_topic(request: Request):
    try:
        body = await request.json()
        message = body.get("message")

        if not message:
            return JSONResponse(content={"error": "No message provided"}, status_code=400)

        prompt = f"Generate a short and clear topic title summarizing the user's message: \"{message}\""

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "openai/gpt-3.5",
            "messages": [{"role": "user", "content": prompt}]
        }

        async with httpx.AsyncClient() as client:
            response = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
            data = response.json()

        topic = data["choices"][0]["message"]["content"].strip()
        return JSONResponse(content={"topic": topic})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

