from sqlalchemy.orm import Session
from app.db import base as models
from app.schemas import user as schemas
import random
from datetime import datetime, timedelta, timezone

# Check for existing user by email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Create new user
def create_user(db:Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Generate secure otp
def set_user_otp(db:Session, user: models.User):
    otp = str(random.randint(100000, 999999)) # Generate a 6-digit code
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=10) # Set expiration for 10 minutes
    user.otp = otp
    user.otp_expires_at = expires_at
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Verify otp
def verify_user_otp(db:Session, user: models.User, otp: str):
    if not user.otp_expires_at or datetime.now(timezone.utc) > user.otp_expires_at:
        # OTP has expired
        return False
    
    # In a real app, you would use a secure hash comparison here
    if user.otp != otp:
        # OTP does not match
        return False
    
    # OTP is valid, now invalidate it
    user.otp = None
    user.otp_expires_at = None
    db.add(user)
    db.commit()
    
    return True