from dotenv import load_dotenv

load_dotenv()

import uvicorn
from researcher.agent import a2a_app

if __name__ == "__main__":
    print("=" * 50)
    print("  RESEARCHER A2A SERVER")
    print("=" * 50)
    print("  URL: http://localhost:8001")
    print("  Agent Card: http://localhost:8001/.well-known/agent.json")
    print("=" * 50)
    
    uvicorn.run(a2a_app, host="0.0.0.0", port=8001)
