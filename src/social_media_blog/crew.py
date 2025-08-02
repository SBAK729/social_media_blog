# src/social_media_blog/crew.py

from crewai import Crew
from src.social_media_blog.agents.crew_agents import load_agents_from_yaml
from src.social_media_blog.tasks.crew_tasks import load_tasks_from_yaml
from src.social_media_blog.utils.prompt_loader import load_prompts

def run_crew(topic):
    agent_path = "src/social_media_blog/config/agents.yaml"
    task_path = "src/social_media_blog/config/tasks.yaml"
    prompt_path = "src/social_media_blog/prompts/prompts.yaml"

    # Load agents
    agents = load_agents_from_yaml(agent_path)

    # Load prompt templates
    prompt_templates = load_prompts(prompt_path)
    # print(prompt_templates)

    # Define context used for rendering prompts
    context = {
        "topic": topic,
        "tone": "professional",
        "platform": "Medium",
        "audience": "tech audience",
        "current_year": "2025"
    }

    # 🔥 FIXED: pass `context` as 4th argument
    tasks = load_tasks_from_yaml(task_path, agents, prompt_templates, context)

    crew = Crew(agents=list(agents.values()), tasks=tasks, verbose=True)
    result = crew.kickoff(inputs={"topic":topic})
    return result
