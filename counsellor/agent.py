import os
import sys
import asyncio

from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent, AGENT_CARD_WELL_KNOWN_PATH
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from logging_config import counsellor_logger, a2a_logger
from google.adk.models import Gemini

model = Gemini(model="gemini-flash-latest")

RESEARCHER_URL = os.environ.get("RESEARCHER_URL", "http://localhost:8001")

counsellor_logger.info(f"[LINK] Connecting to Researcher at: {RESEARCHER_URL}")

researcher_remote = RemoteA2aAgent(
    name="researcher",
    description="Career research agent.",
    agent_card=f"{RESEARCHER_URL}{AGENT_CARD_WELL_KNOWN_PATH}",
    timeout=120,
)

counsellor_agent = Agent(
    name="counsellor",
    model=model,
    instruction="""
    You are a Career Counsellor coordinator. Your goal is to provide comprehensive, actionable career advice.
    
    CORE RESPONSIBILITIES:
    1. UNDERSTAND: Analyze the user's request. If it's too broad (e.g., "science courses"), you MUST ask clarifying questions (e.g., "Biology or Physics?", "Pure science or applied?", "Diploma or Degree?").
    2. DELEGATE: Delegate to the 'researcher' agent to fetch FACTS, DATA, and LINKS.
    3. SYNTHESIZE: Present the Researcher's findings in a structured, easy-to-read format.
    
    CRITICAL RULES:
    - ALWAYS include the LINKS provided by the Researcher. A response without links is a FAILURE.
    - If the Researcher gives you a list of 10 items, do not just say "I found 10 items". List the top 3-5 with details and offer to show more.
    - If the answer is vague, apologize and ask the user for more specific preferences to narrow the search.
    - tone: Professional, encouraging, and detailed.
    
    WHEN TO DELEGATE TO 'researcher':
    - User asks about "best courses" -> Delegate: "Find top 5 BSc courses in India with college links and eligibility"
    - User asks about "career options" -> Delegate: "Find career paths for math lovers with salary ranges and job market outlook"
    
    FORMAT YOUR RESPONSE:
    - **Summary**: Brief overview.
    - **Top Options**: Bullet points with Key feature + [Link].
    - **Follow-up**: "To give you better advice, could you tell me..."
    """,
    sub_agents=[researcher_remote],
    description="Main career counselling agent that helps students discover career paths.",
)

counsellor_logger.info("[OK] Counsellor agent created with 'researcher' sub-agent")

a2a_app = to_a2a(counsellor_agent, port=8000)

counsellor_logger.info("[OK] A2A application created on port 8000")

if __name__ == "__main__":
    import uvicorn
    counsellor_logger.info("=" * 50)
    counsellor_logger.info("  COUNSELLOR A2A SERVER")
    counsellor_logger.info("=" * 50)
    uvicorn.run(a2a_app, host="0.0.0.0", port=8000)
