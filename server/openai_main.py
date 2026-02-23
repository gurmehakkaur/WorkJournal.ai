from fastapi import FastAPI, Request
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import redis
import json

load_dotenv()
client = OpenAI()
app = FastAPI()
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Allow CORS for local development (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = "You are a very good friend who understands everything going on at user's workplace."
# TEMPORARY: Changed from 3600 (1 hour) to 10 seconds for testing Redis keyspace notifications
# Once testing is complete, change SESSION_EXPIRY back to 3600
SESSION_EXPIRY = 10  # 10 seconds for testing keyspace notifications
HARDCODED_USER_ID = "999999"

class ChatRequest(BaseModel):
    sessionId: str
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    session_id = request.sessionId
    user_message = request.message
    user_id = HARDCODED_USER_ID
    
    # 1. Retrieve session from Redis using userid:sessionid format
    redis_key = f"{user_id}:{session_id}"
    session_data = redis_client.get(redis_key)
    if session_data:
        session_messages = json.loads(session_data)
    else:
        session_messages = []
    
    # 2. Build full message array: system prompt + session history + new message
    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + session_messages + [{"role": "user", "content": user_message}]
    
    # 3. Call OpenAI
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=full_messages
    )
    assistant_reply = response.choices[0].message.content
    
    # 4. Append both user and assistant messages to session
    session_messages.append({"role": "user", "content": user_message})
    session_messages.append({"role": "assistant", "content": assistant_reply})
    
    # 5. Store updated session in Redis with 1 hour expiry
    redis_client.setex(
        redis_key,
        SESSION_EXPIRY,
        json.dumps(session_messages)
    )
    
    # 6. Return only the reply
    return {"reply": assistant_reply}

@app.get("/chat/history")
async def get_history(sessionId: str, limit: int = 20, offset: int = 0):
    """Retrieve conversation history from Redis with pagination"""
    user_id = HARDCODED_USER_ID
    redis_key = f"{user_id}:{sessionId}"
    session_data = redis_client.get(redis_key)
    
    if session_data:
        messages = json.loads(session_data)
        # Return last N messages (paginated)
        messages = messages[-limit-offset:-offset] if offset else messages[-limit:]
    else:
        messages = []
    
    return {"messages": messages}