from sqlalchemy.orm import Session
from app.db import base as models
from app.schemas import document as schemas

# Create new document
def create_document(db: Session, document: schemas.DocumentCreate, user_id: int, storage_path: str):
    db_document = models.Document(
        user_id=user_id,
        file_name=document.file_name,
        storage_path=storage_path
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

# Check for existing documents for specific user
def get_documents_by_user(db: Session, user_id: int):
    return db.query(models.Document).filter(models.Document.user_id == user_id).all()