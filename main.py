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
    "https://uplift-sia.web.app"  # Replace with your actual frontend domain
]

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow requests from the frontend
    allow_credentials=True,
    allow_methods=["*"],    # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],    # Allow all headers
)

@app.get("/")
async def root():
    return {"message": "Chatbot backend is running!"}

@app.post("/chat")
async def chat(request: Request):
    try:
        # Parse the incoming JSON body
        body = await request.json()
        user_message = body.get("message")

        # Check if message is provided
        if not user_message:
            return JSONResponse(content={"error": "No message provided"}, status_code=400)

        # Get the bot response from the chatbot
        response = chatbot.chat.completions.create(
            model="gpt-4o-turbo",
            messages=[{"role": "user", "content": user_message}],
            web_search=False
        )

        # Check if the response has choices and return the first choice's content
        if hasattr(response, "choices") and response.choices:
            bot_response = response.choices[0].message.content
        else:
            bot_response = "Sorry, I couldn't generate a response."

        # Return the bot response as JSON
        return JSONResponse(content={"response": bot_response})

    except Exception as e:
        # Return error message if an exception occurs
        return JSONResponse(content={"error": str(e)}, status_code=500)

# To run the application with Uvicorn
if __name__ == "__main__":
    # Running with uvicorn for production
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
