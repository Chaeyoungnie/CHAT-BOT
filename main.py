from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from g4f.client import Client
from typing import List
import uvicorn


app = FastAPI()
chatbot = Client()

# Simulated memory per session (in-memory for now)
conversation_history: List[dict] = []

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
    global conversation_history

    try:
        body = await request.json()
        user_message = body.get("message")

        if not user_message:
            return JSONResponse(content={"error": "No message provided"}, status_code=400)

        # Detect emotion

        # Add the user message to conversation history
        conversation_history.append({"role": "user", "content": user_message})

        # Maintain the last 6 messages (user + bot)
        conversation_history = conversation_history[-6:]

        # Add a system prompt only once (at the beginning)
        messages = [
            {"role": "system", "content": f"You are a compassionate mental health assistant. Speak in a natural, human tone. Be empathetic and contextual."},
            *conversation_history
        ]

        # Get response
        response = chatbot.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            web_search=False
        )

        bot_response = response.choices[0].message.content if hasattr(response, "choices") and response.choices else "Sorry, I couldn't generate a response."

        # Add bot reply to history
        conversation_history.append({"role": "assistant", "content": bot_response})


    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)