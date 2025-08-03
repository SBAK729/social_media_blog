import os
import re
import json
from typing import Dict
from langchain.schema import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()
# Load GROQ API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Fallback default context
DEFAULT_CONTEXT = {
    "tone": "informative",
    "platform": "generic",
    "audience": "general audience"
}

# Create LLM instance
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama3-70b-8192",
    temperature=0.3,
    max_tokens=512
)

def extract_context_entities(query: str) -> Dict[str, str]:
    """
    Extract tone, platform, and audience from user query using Groq's LLM.
    """
    prompt = f"""
Given the following user query, extract the appropriate writing tone, target platform, and audience.
Respond ONLY in JSON with the following keys: tone, platform, audience.

Query: "{query}"
"""

    try:
        response = llm([
            SystemMessage(content="You are a helpful assistant that extracts tone, platform, and audience from a user's writing query."),
            HumanMessage(content=prompt)
        ])
        
        # Try to extract JSON from the response
        match = re.search(r'\{.*\}', response.content, re.DOTALL)
        if match:
            return json.loads(match.group(0))

        return DEFAULT_CONTEXT

    except Exception as e:
        print(f"[Groq Extraction Error]: {e}")
        return DEFAULT_CONTEXT
