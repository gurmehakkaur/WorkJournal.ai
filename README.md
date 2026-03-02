# WorkJournal.ai

## Home Page Chat Architecture

### TL;DR

Frontend shows live chat in Redis-backed sessions (1 hour window). When session expires, Redis Keyspace Notifications trigger a listener that vectorizes the conversation. Multi-device sync via Redis. Simple, scalable, production-ready.

---

## Architecture Overview

### Frontend

1. **On page load:** Check localStorage for `chatSessionId`
2. **If exists:** Load cached messages from localStorage + fetch fresh from Redis (background)
3. **User sends message:**
   - If no sessionId: Generate `sessionId = 'session_' + Date.now()`, store in localStorage
   - Add message to local state (optimistic UI update)
   - POST `/chat { sessionId, message }`
4. **Receive reply:** Display in UI → Update localStorage cache

### Backend

5. Receive `{ sessionId, message }`
6. Get session from Redis: `999999:{sessionId}`
7. If exists: Load messages
8. If not: Start fresh (listener already vectorized old one)
9. Build prompt: `[system_prompt + session_messages + new_message]`
10. Call OpenAI → Get reply
11. Append both messages → Store back in Redis with 1-hour TTL + `last_activity` timestamp
12. Return `{ reply }`

### Redis Listener (Background)

13. Monitor Redis expiry events (`__keyevent@0__:expired`)
14. When session key expires (1 hour inactive):
    - Vectorize + store to Vector DB
    - Delete from Redis
    - Log: "Session expired, saved to Vector DB"

### Multi-Device Support

- **Device 1:** Chat → Stored in Redis
- **Device 2:** Opens same sessionId → Fetches from Redis (synced instantly)
- Works across browsers & devices

---

## Verification Checklist

- [ ] Send message → Appears in UI
- [ ] Refresh page → Messages load from localStorage
- [ ] Open on different device → Same session loads from Redis
- [ ] Wait 1 hour idle → Listener logs session expired

---

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| **1-hour window** | Balance between active usage and memory efficiency |
| **localStorage** | Device-specific caching for instant UX (not a sync mechanism) |
| **Redis as source of truth** | Enables multi-device sync without database |
| **Listener at replicas=1** | Prevents duplication; API can scale independently |

---

## Tech Stack

- **Frontend:** Next.js (React) + TypeScript
- **Backend:** FastAPI (Python)
- **Cache:** Redis
- **LLM:** OpenAI GPT-4o
- **Deploy:** Docker + Docker Compose

## Running Locally

```bash
# Terminal 1: Start FastAPI
cd server
uvicorn openai_main:app --reload

# Terminal 2: Start Redis Listener
cd server
python redis_listener.py

# Terminal 3: Start Next.js
cd my-app
npm run dev
