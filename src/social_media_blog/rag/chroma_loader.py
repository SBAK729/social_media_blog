from langchain_community.vectorstores import Chroma
from src.social_media_blog.utils.helper import download_hugging_face_embeddings

def load_chroma_db(persist_directory: str = "chroma_db"):
    embedding = download_hugging_face_embeddings()
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
    return vectordb

# load_chroma_db()