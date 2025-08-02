# src/social_media_blog/agents/crew_agents.py

import yaml, os
from crewai import Agent, LLM
# from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

api_key=os.getenv("GEMINI_API_KEY")

llm = LLM(
    model=os.getenv("GEMINI_MODEL"),
    temperature=0.7
)

def load_agents_from_yaml(path):
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
    agents = {}
    for a in data['agents']:
        agents[a['id']] = Agent(
            role=a['role'],
            goal=a['goal'],
            backstory=a['backstory'],
            memory=a.get('memory', False),
            verbose=a.get('verbose', False),
            llm=llm
        )
    return agents
