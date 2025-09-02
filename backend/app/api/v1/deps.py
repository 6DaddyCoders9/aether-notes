from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app.db import session
from app.crud import user as crud
from app.core import security 



# Dependency to get a database session
def get_db():
    db = session.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create an instance of HTTPBearer class
oauth2_scheme = HTTPBearer()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Define the exception to be raised if authentication fails
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    user_email = security.verify_token(token.credentials)
    
    if user_email is None:
        raise credentials_exception
    
    db_user = crud.get_user_by_email(db, email=user_email)
    
    if not db_user:
        raise credentials_exception
    
    return db_user