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

# Configure allowed origins (you can add your frontend domain here for production)
origins = [
    "http://localhost:5501",           # Local dev
    "http://127.0.0.1:5501",           # Local dev
    "https://uplift-sia.web.app"       # Your deployed frontend domain
]

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow requests from the frontend
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

        if hasattr(response, "choices") and response.choices:
            bot_response = response.choices[0].message.content
        else:
            bot_response = "Sorry, I couldn't generate a response."

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

        # Prompt to generate a topic title from the user's first message
        prompt = f"Generate a short and clear topic title summarizing the user's message: \"{message}\""

        response = chatbot.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            web_search=False
        )

        if hasattr(response, "choices") and response.choices:
            topic = response.choices[0].message.content.strip()
        else:
            topic = "General Conversation"

        return JSONResponse(content={"topic": topic})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)