from pydantic import BaseModel
from datetime import datetime

# Shared properties
class DocumentBase(BaseModel):
    file_name: str
    
# Properties to receive via API on creation
class DocumentCreate(DocumentBase):
    pass

# Properties to return to client
class Document(DocumentBase):
    id: int
    created_at: datetime
    user_id: int
    
    class Config:
        from_attributes = True