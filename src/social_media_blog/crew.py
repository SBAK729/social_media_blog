import os
from crewai import Crew
from social_media_blog.agents.crew_agents import load_agents_from_yaml
from social_media_blog.tasks.crew_tasks import load_tasks_from_yaml
from social_media_blog.utils.prompt_loader import load_prompts



AGENT_PATH = "src/social_media_blog/config/agents.yaml"
TASK_PATH = "src/social_media_blog/config/tasks.yaml"
PROMPT_PATH = "src/social_media_blog/prompts/prompts.yaml"



def run_crew_with_context(topic: str, context: dict):
    # Load agents and prompts
    agents = load_agents_from_yaml(AGENT_PATH)
    prompt_templates = load_prompts(PROMPT_PATH)

    # Load tasks using the provided context
    tasks = load_tasks_from_yaml(TASK_PATH, agents, prompt_templates, context)

    # Run CrewAI pipeline
    crew = Crew(agents=list(agents.values()), tasks=tasks, verbose=True)
    result = crew.kickoff(inputs={"topic": topic})

    return result
