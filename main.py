from fastapi import FastAPI, HTTPException, Request
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
    response: str

origins = [
    "http://localhost:3000",  # React/Vue local dev
    "http://127.0.0.1:3000",
    "https://frontend-domain.com"
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)


@app.post("/api/generate-blog", response_model=CrewOutput)
async def generate_blog(query_input: QueryInput):
    try:
        response = handle_user_query(query_input.query)

        if hasattr(response, "raw"):
            return {"response": str(response.raw)}

        # If response is a dict or object
        return {"response": str(response)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

