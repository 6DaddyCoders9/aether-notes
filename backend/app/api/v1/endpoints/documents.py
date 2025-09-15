from typing import List
import tempfile
import os
from fastapi import APIRouter, UploadFile, Depends, HTTPException, File, status
from sqlalchemy.orm import Session
from app.schemas import document as doc_schemas
from app.api.v1 import deps
from app.db import base as models
from app.core.supabase_client import supabase_client
from app.crud import document as doc_crud
from app.core.document_processor import DocumentProcessor

CHROMA_DB_DIRECTORY = os.getenv("CHROMA_DB_DIRECTORY", "chroma_db")
HUGGING_FACE_EMBEDDING_MODEL = os.getenv("HUGGING_FACE_EMBEDDING_MODEL","all-MiniLM-L6-v2")

router = APIRouter()

# Instantiate DocumentProcessor once globally for now.
# For larger applications, you might make this a FastAPI dependency.
document_processor = DocumentProcessor(
    chroma_db_directory=CHROMA_DB_DIRECTORY,
    embedding_model_name=HUGGING_FACE_EMBEDDING_MODEL
)

# Define upload enpoint in documents route
@router.post("/documents/upload", response_model=doc_schemas.Document)
def document_upload(
    db: Session = Depends(deps.get_db), 
    current_user: models.User = Depends(deps.get_current_user), 
    file: UploadFile = File(...)
):
    """
    Upload a document file for the authenticated user, store it in Supabase,
    and process its content for AI querying using LangChain and ChromaDB.
    """
    storage_path = f"user_{current_user.id}/{file.filename}"
    temp_file_path = None # Initialize outside try for finally block access

    try:
        # 1. Upload the file to Supabase
        file.file.seek(0) # Ensure file pointer is at the beginning
        supabase_client.storage.from_("document-uploads").upload(
            path=storage_path,
            file=file.file.read(),
            file_options={"content-type": file.content_type}
        )
        print(f"File uploaded to Supabase: {storage_path}")

        # 2. Download the file from Supabase to a temporary local file
        file_content = supabase_client.storage.from_("document-uploads").download(storage_path)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name # Assign path to external variable
        print(f"File downloaded to temporary local path: {temp_file_path}")

        # 3. Process the document with the dedicated DocumentProcessor
        processed_chunks_count = document_processor.process_and_store_document(temp_file_path)
        print(f"Document processed and {processed_chunks_count} chunks stored in ChromaDB.")

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Document processing failed: {e}"
        ) from e
    except Exception as e:
        # Catch any other exceptions during Supabase upload or document processing
        print(f"An unexpected error occurred during document processing: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process document: {e}"
        ) from e
    finally:
        # Clean up the temporary local file
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            print(f"Cleaned up temporary file: {temp_file_path}")

    # 4. Create the document record in your PostgreSQL database (metadata)
    document_schema = doc_schemas.DocumentCreate(file_name=file.filename)
    db_document = doc_crud.create_document(
        db=db, 
        document=document_schema, 
        user_id=current_user.id, 
        storage_path=storage_path
    )

    return db_document

# Define route to List documents
@router.get("/documents/", response_model=List[doc_schemas.Document])
def list_documents(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    return doc_crud.get_documents_by_user(db, current_user.id)

# Define delete endpoint in documents route
@router.delete("/documents/{document_id}", response_model=doc_schemas.Document)
def document_delete(
    document_id : int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    doc_to_delete = db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.user_id == current_user.id
    ).first()

    if not doc_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    try:
        # Delete the file
        supabase_client.storage.from_("document-uploads").remove(
            paths=[doc_to_delete.storage_path]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete file from storage: {e}"
        ) from e

    deleted_doc_record = doc_crud.delete_document(db=db, doc=doc_to_delete)

    return deleted_doc_record
