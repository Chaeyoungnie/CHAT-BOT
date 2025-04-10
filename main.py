import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from g4f.client import Client
import uvicorn
import os

# Initialize FastAPI application
app = FastAPI()

# Initialize chatbot client
chatbot = Client()

# Configure allowed origins
origins = [
    "http://localhost:5501",
    "http://127.0.0.1:5501",
    "https://uplift-sia.web.app"
]

# CORS setup
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

        response = chatbot.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_message}],
            web_search=False
        )

        bot_response = response.choices[0].message.content if response.choices else "Sorry, I couldn't generate a response."

        return JSONResponse(content={"response": bot_response})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/generate-topic")
async def generate_topic(request: Request):
    try:
        body = await request.json()
        user_message = body.get("message")

        if not user_message:
            return JSONResponse(content={"error": "No message provided"}, status_code=400)

        topic_prompt = (
            f"Give a short topic title (3-5 words max) summarizing this conversation: \n{user_message}"
        )

        response = chatbot.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": topic_prompt}],
            web_search=False
        )

        topic = response.choices[0].message.content.strip() if response.choices else "General Conversation"

        return JSONResponse(content={"topic": topic})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)