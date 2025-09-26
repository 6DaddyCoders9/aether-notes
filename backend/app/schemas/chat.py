from pydantic import BaseModel
from typing import List

class ChatQuery(BaseModel):
    query: str
    
class ChatResponse(BaseModel):
    answer: str
    sources: List[str] = []