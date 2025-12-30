import os
import sys
import asyncio
from google.adk.agents import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a

from logging_config import researcher_logger, log_tool_call, log_tool_result

try:
    from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
    from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
    from mcp.client.stdio import StdioServerParameters
    MCP_AVAILABLE = True
    researcher_logger.info("[OK] MCP tools available")
except ImportError as e:
    researcher_logger.warning(f"[WARN] MCP tools not available: {e}")
    MCP_AVAILABLE = False
    
from google.adk.models import Gemini
from db.json_store import save_career_info as _save_career_info, lookup_career_info as _lookup_career_info

model = Gemini(model="gemini-flash-latest")

def save_career_info(interest: str, career_title: str, description: str, 
                     salary_range: str = "", skills: str = "") -> str:
    """Save career information with logging."""
    log_tool_call(researcher_logger, "save_career_info", {
        "interest": interest,
        "career_title": career_title,
        "description": description[:50]
    })
    result = _save_career_info(interest, career_title, description, salary_range, skills)
    log_tool_result(researcher_logger, "save_career_info", result)
    return result

def lookup_career_info(interest: str) -> str:
    """Look up career information with logging."""
    log_tool_call(researcher_logger, "lookup_career_info", {"interest": interest})
    result = _lookup_career_info(interest)
    log_tool_result(researcher_logger, "lookup_career_info", result)
    return result

tools = [save_career_info, lookup_career_info]
researcher_logger.info("[OK] JSON storage tools loaded")

if MCP_AVAILABLE:
    try:
        server_params = StdioServerParameters(
            command="npx",
            args=["-y", "@playwright/mcp"]
        )
        playwright_params = StdioConnectionParams(
            server_params=server_params,
            timeout=120  # 2 minutes timeout
        )
        playwright_toolset = McpToolset(connection_params=playwright_params)
        tools.append(playwright_toolset)
        researcher_logger.info("[OK] Playwright MCP toolset loaded")
    except Exception as e:
        researcher_logger.error(f"[ERROR] Could not load Playwright MCP: {e}")

researcher_agent = Agent(
    name="researcher",
    model=model,
    instruction="""
    You are a Career Researcher agent. Your job is to find deep, verifiable career information.
    
    CRITICAL OBJECTIVE:
    You must return ACTUAL LINKS, SALARY DATA, and COURSE DETAILS found using your tools.
    
    Available Tools:
    1. Playwright (Web Browsing):
       - Use this to search Google/Bing.
       - VISIT specific pages to get details.
       - EXTRACT: Course names, College names, URLs, Eligibility, Fees.
    
    2. save_career_info: Save findings to DB.
    3. lookup_career_info: Check DB first.
    
    WORKFLOW:
    1. PLAN: Break down the research query.
    2. SEARCH: Use Playwright to find legitimate sources (University websites, Career portals).
    3. EXTRACT:
       - **Source URL**: YOU MUST PROVIDE THE LINKS YOU FOUND.
       - **Key Details**: Don't just headings. Get 1-2 sentences of substance.
    4. SAVE: Store valuable evergreen info.
    5. REPORT: Return a detailed report to the Counsellor.
       - Format: Markdown.
       - Include: "Source: [Link]" for every major claim.
    
    Do NOT give generic advice like "You can do engineering".
    INSTEAD say: "B.Tech in CS is available at [Institute Name](URL) with a cutoff of..."
    """,
    tools=tools,
    description="Career research agent that searches the web and stores findings.",
)

researcher_logger.info(f"[OK] Researcher agent created with {len(tools)} tools")

a2a_app = to_a2a(researcher_agent, port=8001)

researcher_logger.info("[OK] A2A application created on port 8001")

if __name__ == "__main__":
    import uvicorn
    researcher_logger.info("=" * 50)
    researcher_logger.info("  RESEARCHER A2A SERVER")
    researcher_logger.info("=" * 50)
    uvicorn.run(a2a_app, host="0.0.0.0", port=8001)
