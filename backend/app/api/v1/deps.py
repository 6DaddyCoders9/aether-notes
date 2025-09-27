from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app.db import session
from app.crud import user as crud
from core import security

def get_db():
    db = session.SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = HTTPBearer()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = security.verify_token(token.credentials)
    if payload is None:
        raise credentials_exception

    email = payload.get("sub")
    db_user = crud.get_user_by_email(db, email=email)
    if not db_user:
        raise credentials_exception

    return db_user
