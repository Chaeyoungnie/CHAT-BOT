import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from g4f.client import Client
import uvicorn

# Initialize FastAPI application
app = FastAPI()

# Initialize chatbot client
chatbot = Client()

# Enable CORS for your Firebase frontend
origins = [
    "https://uplift-sia.web.app",  # Replace with your actual Firebase URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow requests from the Firebase frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

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
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_message}],
            web_search=False
        )

        # Debug print to check the response from the chatbot
        print("Response from chatbot:", response)

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


#PUSH TRY AGAIN 