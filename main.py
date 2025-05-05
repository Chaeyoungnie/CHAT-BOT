import os
import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# Set your OpenRouter API key
OPENROUTER_API_KEY = "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"

# CORS settings
origins = [
    "http://localhost:5501",
    "http://127.0.0.1:5501",
    "https://uplift-sia.web.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
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

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "openai/gpt-4o",
            "messages": [
                {"role": "system", "content": "You are a compassionate and empathetic mental health support assistant."},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 500  # Important: stays within free quota
        }

        async with httpx.AsyncClient() as client:
            response = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
            data = response.json()

        if "choices" not in data:
            return JSONResponse(content={"error": "Invalid response format from OpenRouter"}, status_code=500)

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
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 50  # Very short output for a topic title
        }

        async with httpx.AsyncClient() as client:
            response = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
            data = response.json()

        if "choices" not in data:
            return JSONResponse(content={"error": "Invalid response format from OpenRouter"}, status_code=500)

        topic = data["choices"][0]["message"]["content"].strip()
        return JSONResponse(content={"topic": topic})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
