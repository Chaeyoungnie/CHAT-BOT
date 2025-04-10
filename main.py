from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from g4f.client import Client
import uvicorn

app = FastAPI()
chatbot = Client()

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

@app.post("/generate-topic")
async def generate_topic(request: Request):
    body = await request.json()
    user_message = body.get("message")

    if not user_message:
        return JSONResponse(content={"error": "No message provided"}, status_code=400)

    prompt = f"Generate a short, clear topic title based on this message: \"{user_message}\""

    response = chatbot.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        web_search=False
    )

    if hasattr(response, "choices") and response.choices:
        topic_title = response.choices[0].message.content.strip()
    else:
        topic_title = "Untitled Topic"

    return JSONResponse(content={"topic": topic_title})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
