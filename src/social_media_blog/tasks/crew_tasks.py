# tasks/crew_tasks.py
from crewai import Task
from jinja2 import Template
import yaml

def render_prompt(template_str, context: dict) -> str:
    return Template(template_str).render(**context)

def load_tasks_from_yaml(task_yaml_path, agents: dict, prompt_templates: dict, context: dict):
    with open(task_yaml_path, "r") as f:
        task_defs = yaml.safe_load(f)["tasks"]

    tasks = []
    for t in task_defs:
        agent_id = t["agent_id"]
        template_str = prompt_templates["prompts"][agent_id]["template"]
        rendered_prompt = render_prompt(template_str, context)

        task = Task(
            description=rendered_prompt,
            expected_output=t["expected_output"],
            agent=agents[agent_id]
        )
        tasks.append(task)

    return tasks
