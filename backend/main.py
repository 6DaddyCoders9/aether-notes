from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import database, models, schemas, crud, email_service

# Create all database tables (if they don't exists)
models.Base.metadata.create_all(bind=database.engine)

# Create an instance of the FastAPI class
app = FastAPI()

# Dependency to get a database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define a route for the root URL ("/")
@app.get("/")
def read_root():
    return {"message": "Hello from AetherNotes Backend"}

# Define a health check route
@app.get("/api/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # Try to execute a simple query
        db.execute(text('SELECT 1'))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "detail": str(e)}

# Define users route    
@app.post("/users/", response_model= schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user) 

# Define request-otp endpoint in auth route
@app.post("/auth/request-otp", response_model= schemas.UserOTP)
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