from dotenv import load_dotenv

load_dotenv()

import uvicorn
from counsellor.agent import a2a_app

if __name__ == "__main__":
    researcher_url = os.environ.get("RESEARCHER_URL", "http://localhost:8001")
    
    print("=" * 50)
    print("  COUNSELLOR A2A SERVER")
    print("=" * 50)
    print("  URL: http://localhost:8000")
    print("  Agent Card: http://localhost:8000/.well-known/agent.json")
    print(f"  Researcher: {researcher_url}")
    print("=" * 50)
    
    uvicorn.run(a2a_app, host="0.0.0.0", port=8000)
