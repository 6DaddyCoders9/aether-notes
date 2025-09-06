from fastapi import APIRouter, UploadFile, Depends, HTTPException, File, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas import document as doc_schemas
from app.api.v1 import deps
from app.db import base as models
from app.core.supabase_client import supabase_client
from app.crud import document as doc_crud

router = APIRouter()

# Define upload enpoint in documents route
@router.post("/documents/upload", response_model=doc_schemas.Document)
def document_upload(
    db: Session = Depends(deps.get_db), 
    current_user: models.User = Depends(deps.get_current_user), 
    file: UploadFile = File(...)
):
    # Define the path where the file will be stored
    storage_path = f"user_{current_user.id}/{file.filename}"

    try:
        # Upload the file 
        supabase_client.storage.from_("document-uploads").upload(
            path=storage_path,
            file=file.file.read(),
            file_options={"content-type": file.content_type}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file to storage: {e}"
        )
    
    # Create the schema object with the file name
    document_schema = doc_schemas.DocumentCreate(file_name=file.filename)
    
    # Create the document record in your PostgreSQL database
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

# Define delete endpoint in document route
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
        )
    
    deleted_doc_record = doc_crud.delete_document(db=db, doc=doc_to_delete)

    return deleted_doc_record