

from social_media_blog.utils.extract import extract_context_entities
from social_media_blog.rag.qa_pipeline import answer_question, search_and_generate_answer
from social_media_blog.crew import run_crew_with_context
from langchain.schema import HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

groq_llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama3-70b-8192",
    temperature=0.2,
    max_tokens=512
)



def classify_intent(query: str) -> str:
    writing_keywords = ['write', 'generate', 'post', 'caption', 'blog', 'create']
    if any(word in query.lower() for word in writing_keywords):
        return "social_blog"
    return "assistant"


def get_context_from_vector_or_search(query: str) -> str:
    rag_result = answer_question(query)
    return rag_result if rag_result else search_and_generate_answer(query)


def assistant_chat(query: str) -> str:
        assistant_prompt = f"""
        You are a helpful assistant for a social media blog platform. Answer the following question based on general knowledge and tone best suited for online creators:

        {query}
        """
        response = groq_llm.predict(assistant_prompt)
        return  response


def run_social_blog_crew(query: str) -> str:
    context_entities = extract_context_entities(query)
    retrieved_context = get_context_from_vector_or_search(query)


    context = {
        "topic": query,
        "retrieved_context": retrieved_context,
        "tone": context_entities.get("tone", "professional"),
        "platform": context_entities.get("platform", "Medium"),
        "audience": context_entities.get("audience", "tech audience"),
        "current_year": "2025"
    }
    topic=query

    response = run_crew_with_context(topic, context)

    return response


def handle_user_query(query: str) -> str:
    intent = classify_intent(query)
    if intent == "social_blog":
        return run_social_blog_crew(query)
    else:
        return assistant_chat(query)

