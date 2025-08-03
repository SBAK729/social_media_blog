import os
import requests
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from src.social_media_blog.rag.chroma_loader import load_chroma_db
# from social_media_blog.utils.helper import download_hugging_face_embeddings
# from social_media_blog.rag.serper_fallback import search_web


load_dotenv()



SERPER_API_KEY = os.getenv("SERPER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama3-70b-8192",
    temperature=0.1,
    max_tokens=512
)

def answer_question(query: str, mode: str = "blog") -> str:
    """
    Performs RAG search with fallback to Serper. 
    Mode can be "blog" or "assistant"
    """
    db = load_chroma_db()
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 4})


    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type="stuff"
    )

    result = rag_chain.invoke({"query": query})
    context = result.get("result")

    return context

def search_and_generate_answer(query: str) -> str:
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "q": query,
        "gl": "us",
        "hl": "en"
    }

    try:
        response = requests.post("https://google.serper.dev/search", headers=headers, json=payload)
        response.raise_for_status()
        results = response.json()

        snippets = []
        for result in results.get("organic", [])[:3]:
            title = result.get("title", "")
            snippet = result.get("snippet", "")
            snippets.append(f"{title}: {snippet}")

        context = "\n\n".join(snippets)

        # Ask Groq LLM to answer using the search context
        prompt = f"""
        Use the following search snippets to answer the question:

        {context}

        Question: {query}
        """

        answer = llm.predict(prompt)

        return answer

    except Exception as e:
        print(f"[Serper fallback failed]: {e}")
        return "I'm sorry, I couldn’t find relevant information for your question at the moment."
