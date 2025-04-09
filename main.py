import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from g4f.client import Client
import os

# Initialize FastAPI app
app = FastAPI()

# Initialize chatbot client
chatbot = Client()

# Configure allowed origins (you can add your frontend domain here for production)
origins = [
    "http://localhost:5501",           # Local dev
    "http://127.0.0.1:5501",           # Local dev
    "https://uplift-sia.web.app"  # Replace with your actual frontend domain
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

        # Use g4f to generate the chatbot response
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
        print("Error:", str(e))
        return JSONResponse(content={"error": "Internal server error."}, status_code=500)


# This section is ignored on Render — it's only for local dev
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
