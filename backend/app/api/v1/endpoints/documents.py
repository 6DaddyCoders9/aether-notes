from fastapi import APIRouter, UploadFile, Depends, HTTPException, File, status
from sqlalchemy.orm import Session
from app.schemas import document as doc_schemas
from app.api.v1 import deps
from app.db import base as models
from app.core.supabase_client import supabase_client
from app.crud import document as doc_crud

router = APIRouter()

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