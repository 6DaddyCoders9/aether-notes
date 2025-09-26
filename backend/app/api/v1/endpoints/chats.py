import os
from loguru import logger
from fastapi import APIRouter, Depends, HTTPException, status
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from sqlalchemy.orm import Session
from app.schemas.chat import ChatQuery, ChatResponse
from app.schemas.user import User
from app.api.v1 import deps
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

template = ChatPromptTemplate.from_messages(
    [
        ("system", "Answer the user's question based strictly on the provided context.If you don't have enough information from the context to answer, state that clearly."),
        ("user", "Context: {context}\n\nQuestion: {input}")
    ]
)

document_chain = create_stuff_documents_chain(llm, template)

retriever = document_processor.vectorstore.as_retriever()

retrieval_chain = create_retrieval_chain(retriever, document_chain)

logger.info("RAG chain initialized successfully.")

# define query endpoint in chat route
@router.post("/chat/query", response_model=ChatResponse)
async def chat_with_documents(
    query_data: ChatQuery,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
    ):
    try:
        logger.info(f"Received query: {query_data.query} from user: {current_user.email}")
    
        result = retrieval_chain.invoke({"input": query_data.query})

        answer = result["answer"]

        context_documents = result["context"]
        sources = [doc.metadata.get("source", "unknown") for doc in context_documents]
        unique_sources = list(set(sources))
        
        return ChatResponse(answer=answer, sources=unique_sources)
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error processing query: {e}")
