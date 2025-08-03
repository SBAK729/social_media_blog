from crew import run_crew_with_context

if __name__ == "__main__":
    
    topic = "How AI Is Transforming Remote Work Culture"
    context = {
        "topic": topic,
        "tone":"professional",
        "platform": "Medium",
        "audience": "tech audience",
        "current_year": "2025"
    }
    final_output = run_crew_with_context(topic, context)
    
    print("📝 Blog Post Output:\n")
    # print(final_output)
    print(type(final_output))
