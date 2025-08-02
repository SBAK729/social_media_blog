# utils/prompt_loader.py
import yaml

def load_prompts(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)
