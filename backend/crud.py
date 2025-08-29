from sqlalchemy.orm import Session
import models, schemas
import random
from datetime import datetime, timedelta

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
    expires_at = datetime.utcnow() + timedelta(minutes=10) # Set expiration for 10 minutes
    user.otp = otp
    user.otp_expires_at = expires_at
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user