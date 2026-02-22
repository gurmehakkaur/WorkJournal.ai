from fastapi import FastAPI, Request
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
client = OpenAI()
app = FastAPI()

# Allow CORS for local development (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = "You are a very good friend who understands everything going on at user's workplace."

class ChatRequest(BaseModel):
    messages: list

@app.post("/chat")
async def chat(request: ChatRequest):
    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + request.messages

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=full_messages
    )
    reply = response.choices[0].message.content
    return {"reply": reply}