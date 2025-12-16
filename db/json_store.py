"""
Simple JSON-based storage with logging.
"""
import json
import os
from datetime import datetime
from typing import Optional
import logging

# Get logger
logger = logging.getLogger("json_store")

# Data file paths
DATA_DIR = os.path.dirname(os.path.dirname(__file__))
SESSIONS_FILE = os.path.join(DATA_DIR, "sessions.json")
RESEARCH_FILE = os.path.join(DATA_DIR, "career_research.json")


def _load_json(filepath: str) -> dict:
    """Load JSON file."""
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}


def _save_json(filepath: str, data: dict):
    """Save data to JSON file."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, default=str)


def save_career_info(interest: str, career_title: str, description: str, 
                     salary_range: str = "", skills: str = "") -> str:
    """
    Save career information to the JSON store.
    """
    logger.info(f"[NOTE] Saving career info: {career_title} for '{interest}'")
    
    research = _load_json(RESEARCH_FILE)
    interest_key = interest.lower()
    
    if interest_key not in research:
        research[interest_key] = []
    
    research[interest_key].append({
        "career_title": career_title,
        "description": description,
        "salary_range": salary_range,
        "skills": skills,
        "saved_at": datetime.now().isoformat()
    })
    
    _save_json(RESEARCH_FILE, research)
    
    result = f"[OK] Saved: {career_title} for interest '{interest}'"
    logger.info(result)
    return result


def lookup_career_info(interest: str) -> str:
    """
    Look up previously saved career information.
    """
    logger.info(f"[SEARCH] Looking up career info for: '{interest}'")
    
    research = _load_json(RESEARCH_FILE)
    interest_key = interest.lower()
    
    if interest_key not in research or not research[interest_key]:
        result = f"No saved career data found for interest: {interest}"
        logger.info(f"   {result}")
        return result
    
    results = research[interest_key]
    output = f"Found {len(results)} saved career(s) for '{interest}':\n"
    
    for i, career in enumerate(results, 1):
        output += f"\n{i}. {career.get('career_title', 'Unknown')}\n"
        output += f"   Description: {career.get('description', 'N/A')}\n"
        if career.get('salary_range'):
            output += f"   Salary: {career['salary_range']}\n"
        if career.get('skills'):
            output += f"   Skills: {career['skills']}\n"
    
    logger.info(f"   Found {len(results)} results")
    return output


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    print("Testing JSON storage...")
    
    save_career_info("math", "Data Scientist", "Analyze data", "$80k-$150k", "Python")
    print(lookup_career_info("math"))
    print("\n[OK] JSON storage working!")
