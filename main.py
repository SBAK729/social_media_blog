# from slowapi import Limiter
# from slowapi.util import get_remote_address
# from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI, HTTPException, Request
import re
from src.social_media_blog.dispatcher import handle_user_query
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Social Media Blog Generator & Assistant",
    description="Handles blog content generation and chatbot assistant queries",
    version="1.0.0"
)

class QueryInput(BaseModel):
    query: str

class CrewOutput(BaseModel):
    response: dict

origins = [
    "http://localhost:3000",  # React/Vue local dev
    "https://story-loom-gsmw.vercel.app",
    "https://my-project-iota-coral-41.vercel.app"
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://story-loom-gsmw.vercel.app","https://my-project-iota-coral-41.vercel.app"], 
    allow_credentials=True,
    allow_methods=["POST"], 
    allow_headers=["*"], 
)


# limiter = Limiter(key_func=get_remote_address)
# app.state.limiter = limiter

# @app.middleware("http")
# async def rate_limit_middleware(request: Request, call_next):
#     response = await limiter.middleware(request, call_next)
#     return response

# @limiter.limit("4/minute")

def parse_crewai_response(raw_response: str):
    meta_desc_match = re.search(r"\*\*Meta description:\*\*\s*(.+?)\n", raw_response, re.DOTALL)
    tldr_match = re.search(r"\*\*TL;DR:\*\*\s*(.+?)\n", raw_response, re.DOTALL)
    hashtags_match = re.search(r"\*\*Hashtags:\*\*\s*(.+)", raw_response, re.DOTALL)

    meta_description = meta_desc_match.group(1).strip() if meta_desc_match else ""
    tldr = tldr_match.group(1).strip() if tldr_match else ""
    hashtags = hashtags_match.group(1).strip() if hashtags_match else ""

    # Extract title: split on ! or . and get the first sentence
    title = re.split(r'[!.]', meta_description)[0].strip()

    return {
        "response": {
            "title": title,
            "content": tldr,
            "hashtags": hashtags
        }
    }

@app.post("/api/generate-blog", response_model=CrewOutput)
async def generate_blog(query_input: QueryInput):
    try:
        response = handle_user_query(query_input.query)

        if hasattr(response, "raw"):
            print(response)
            return parse_crewai_response(response.raw)

        # If response is a dict or object
        return {"response": {"message":str(response)}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

