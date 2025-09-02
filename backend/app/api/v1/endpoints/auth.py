from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import user as schemas
from app.api.v1.deps import get_db, get_current_user
from app.crud import user as crud
from app.db import base as models
from app.core import email_service, security

# Create an instance of the APIRouter class
router = APIRouter()

# Define users route    
@router.post("/users/", response_model= schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user) 

# Define user profile route
@router.get("/users/me", response_model= schemas.User)
def user_profile(current_user: models.User = Depends(get_current_user)):
    return current_user

# Define request-otp endpoint in auth route
@router.post("/auth/request-otp", response_model= schemas.UserOTP)
def request_otp(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user exists, if not, create one
    db_user = crud.get_user_by_email(db, email=user_data.email)
    if not db_user:
        db_user = crud.create_user(db=db, user=user_data) 
    
    # Set a new OTP for the user
    user_with_otp = crud.set_user_otp(db, user= db_user)
    
    # Send the OTP via email
    email_service.send_otp_email(to_email=user_with_otp.email, otp=user_with_otp.otp)
    
    # For security, don't return the OTP in the response
    return {"email": user_with_otp.email, "otp": "Email has been sent"} # Returning a placeholder

# Define verify-otp endpoint in auth route
@router.post("/auth/verify-otp", response_model= schemas.Token)
def verify_otp(verification_data: schemas.UserVerifyOTP, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=verification_data.email)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    is_valid = crud.verify_user_otp(db, user=user, otp=verification_data.otp)
    
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    
    # Create and return the access token
    access_token = security.create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}