import os
from loguru import logger
from fastapi import APIRouter, Depends, HTTPException, status
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from app.schemas.chat import ChatQuery, ChatResponse
from app.api.deps import get_db, get_current_user
from app.core.document_processor import DocumentProcessor

CHROMA_DB_DIRECTORY = os.getenv("CHROMA_DB_DIRECTORY", "chroma_db")
HUGGING_FACE_EMBEDDING_MODEL = os.getenv("HUGGING_FACE_EMBEDDING_MODEL","all-MiniLM-L6-v2")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")

router = APIRouter()

document_processor = DocumentProcessor(
    chroma_db_directory=CHROMA_DB_DIRECTORY,
    embedding_model_name=HUGGING_FACE_EMBEDDING_MODEL
)

llm = ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)
