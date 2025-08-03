import os
from typing import List
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
    UnstructuredFileLoader
)

def load_documents(data_path: str) -> List[Document]:
    """
    Load documents from a directory with multiple file types.
    Supports: .txt, .md, .yaml, .yml
    """
    if not os.path.exists(data_path):
        raise ValueError(f"Directory {data_path} does not exist")
    
    # Configure loaders for different file types
    loaders = [
        DirectoryLoader(data_path, glob="*.txt", loader_cls=TextLoader),
        DirectoryLoader(data_path, glob="*.md", loader_cls=UnstructuredMarkdownLoader),
        DirectoryLoader(data_path, glob="*.yaml", loader_cls=UnstructuredFileLoader),
        DirectoryLoader(data_path, glob="*.yml", loader_cls=UnstructuredFileLoader)
    ]
    
    # Load all documents
    documents = []
    for loader in loaders:
        try:
            docs = loader.load()
            documents.extend(docs)
        except Exception as e:
            print(f"Error loading documents with {loader.__class__.__name__}: {e}")
    
    return documents

def text_split(documents: List[Document], 
              chunk_size: int = 500, 
              chunk_overlap: int = 50) -> List[Document]:
    """
    Split documents into chunks for processing.
    Args:
        documents: List of documents to split
        chunk_size: Maximum size of each chunk
        chunk_overlap: Overlap between chunks
    """
    if not documents:
        return []
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )
    
    return text_splitter.split_documents(documents)

def download_hugging_face_embeddings(
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs: dict = {"device": "cpu"},
    encode_kwargs: dict = {"normalize_embeddings": False}
) -> HuggingFaceEmbeddings:
    """
    Download and initialize HuggingFace embeddings.
    Args:
        model_name: Name of the model to use
        model_kwargs: Arguments to pass to the model
        encode_kwargs: Arguments to pass to the encoder
    """
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

def validate_documents(documents: List[Document]) -> bool:
    """
    Validate that documents contain required fields.
    Returns True if all documents are valid.
    """
    if not documents:
        return False
    
    required_fields = {"page_content", "metadata"}
    for doc in documents:
        if not all(field in dir(doc) for field in required_fields):
            return False
        if not isinstance(doc.metadata, dict):
            return False
    
    return True