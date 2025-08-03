from social_media_blog.utils.helper import (
    load_documents, 
    text_split, 
    download_hugging_face_embeddings
)
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os

load_dotenv()

persist_directory = "chroma_db"  # folder to store vectors locally

# Load and process documents
documents = load_documents("knowledge/")
text_chunks = text_split(documents)
embeddings = download_hugging_face_embeddings()

# Create or load Chroma vector store
docsearch = Chroma.from_documents(
    documents=text_chunks,
    embedding=embeddings,
    persist_directory=persist_directory
)

# Save to disk
docsearch.persist()

print(f"Stored {len(text_chunks)} chunks in ChromaDB at {persist_directory}")
