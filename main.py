import os
import sys
import time
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from counsellor.agent import counsellor_agent
from logging_config import main_logger, log_request, log_response

app = FastAPI(
    title="Career Counsellor API",
    description="API for the Career Counsellor multi-agent system using A2A protocol",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_service = InMemorySessionService()
APP_NAME = "counsellor_app"
runner = Runner(
    agent=counsellor_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

# Track initialized sessions
initialized_sessions = set()

class ChatRequest(BaseModel):
    message: str
    user_id: str = "default_user"

class ChatResponse(BaseModel):
    response: str
    user_id: str

@app.on_event("startup")
async def startup_event():
    main_logger.info("=" * 60)
    main_logger.info("  CAREER COUNSELLOR API STARTED")
    main_logger.info("=" * 60)

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    start_time = time.time()
    
    # Log incoming request
    log_request(main_logger, "/chat", {
        "user_id": request.user_id,
        "message": request.message[:100] + "..." if len(request.message) > 100 else request.message
    })
    
    try:
        user_id = request.user_id
        session_id = f"session_{user_id}"
        
        # Session management
        if session_id not in initialized_sessions:
            main_logger.info(f"[NOTE] Creating new session: {session_id}")
            await session_service.create_session(
                app_name=APP_NAME,
                user_id=user_id,
                session_id=session_id
            )
            initialized_sessions.add(session_id)
        else:
            main_logger.debug(f"[REUSE] Reusing session: {session_id}")
        
        # Create message content
        content = types.Content(
            role="user",
            parts=[types.Part(text=request.message)]
        )
        
        main_logger.info(f"[START] Starting agent run for session: {session_id}")
        
        # Run the agent
        response_text = ""
        event_count = 0
        
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content
        ):
            event_count += 1
            event_type = type(event).__name__
            main_logger.debug(f"   Event {event_count}: {event_type}")
            
            # Extract text from events
            if hasattr(event, 'content') and event.content:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        response_text += part.text
            elif hasattr(event, 'text'):
                response_text += event.text
        
        main_logger.info(f"[OK] Agent run complete. Events: {event_count}")
        
        if not response_text:
            response_text = "I'm sorry, I couldn't generate a response. Please try again."
            main_logger.warning("[WARN] Empty response from agent")
        
        duration_ms = (time.time() - start_time) * 1000
        log_response(main_logger, "/chat", {"response": response_text[:100]}, duration_ms)
        
        return ChatResponse(response=response_text, user_id=user_id)
    
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        main_logger.error(f"[ERROR] Error in chat ({duration_ms:.0f}ms): {e}")
        import traceback
        main_logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy", "agent": "counsellor", "version": "2.0.0"}

@app.get("/")
async def root():
    return {
        "name": "Career Counsellor API",
        "version": "2.0.0",
        "endpoints": {
            "chat": "POST /chat",
            "health": "GET /health"
        }
    }

if __name__ == "__main__":
    main_logger.info("Starting server on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
