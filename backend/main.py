from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy import text
import database, models, schemas, crud, email_service, security, google_auth

# Create all database tables (if they don't exists)
models.Base.metadata.create_all(bind=database.engine)

# Create an instance of the FastAPI class
app = FastAPI()

# Connect to google router
app.include_router(google_auth.router)

# Create an instance of HTTPBearer class
oauth2_scheme = HTTPBearer()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
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

# Define a route for the root URL ("/")
@app.get("/")
def read_root():
    return {"message": "Hello from AetherNotes Backend"}

# Define a health check route
@app.get("/api/health")
def health_check(db: Session = Depends(database.get_db)):
    try:
        # Try to execute a simple query
        db.execute(text('SELECT 1'))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "detail": str(e)}

# Define users route    
@app.post("/users/", response_model= schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user) 

# Define user profile route
@app.get("/users/me", response_model= schemas.User)
def user_profile(current_user: models.User = Depends(get_current_user)):
    return current_user

# Define request-otp endpoint in auth route
@app.post("/auth/request-otp", response_model= schemas.UserOTP)
def request_otp(user_data: schemas.UserCreate, db: Session = Depends(database.get_db)):
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
@app.post("/auth/verify-otp", response_model= schemas.Token)
def verify_otp(verification_data: schemas.UserVerifyOTP, db: Session = Depends(database.get_db)):
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