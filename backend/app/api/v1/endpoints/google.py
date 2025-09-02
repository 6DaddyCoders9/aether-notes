from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport.requests import Request
import os   
from app.schemas import user as schemas
from app.api.v1.deps import get_db
from app.crud import user as crud
from app.core import security

# Get Google credentials from environment variables
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# Define the scopes (what we want to access)
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

# The URL our backend will listen on for the callback from Google
REDIRECT_URI = "http://localhost:8000/api/v1/auth/google/callback"

# Create an instance of the APIRouter class
router = APIRouter()

# Define /google/login endpoint
@router.get("/auth/google/login")
def google_login():
    # Create a client_config dictionary with your credentials
    client_config = {
        "web": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }

    # Create the Flow instance
    flow = Flow.from_client_config(client_config=client_config, scopes=SCOPES)
    
    # Set the redirect_uri
    flow.redirect_uri = REDIRECT_URI
    
    # Generate the authorization URL
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )

    # Return a response that redirects the user's browser to Google
    return RedirectResponse(url=authorization_url)

# Define /google/callback endpoint
@router.get("/auth/google/callback", response_model=schemas.Token)
def google_callback(code: str, state: str, db: Session = Depends(get_db)):
    client_config = {
        "web": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }
    flow = Flow.from_client_config(client_config=client_config, scopes=SCOPES)
    flow.redirect_uri = REDIRECT_URI
    
    try:
        user_cred = flow.fetch_token(code=code)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Could not fetch token from Google: {e}"
        )

    try:
        user_info = id_token.verify_oauth2_token(
            id_token=user_cred['id_token'], 
            request=Request(), 
            audience=GOOGLE_CLIENT_ID
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid token from Google: {e}"
        )
    
    user_email = user_info.get("email")
    if not user_email:
        raise HTTPException(status_code=400, detail="Could not retrieve email from Google")

    # Find or create the user
    db_user = crud.get_user_by_email(db, email=user_email)
    if not db_user:
        user_schema = schemas.UserCreate(email=user_email)
        db_user = crud.create_user(db=db, user=user_schema)
        
    # Create a session token for the user
    access_token = security.create_access_token(
        data={"sub": db_user.email}
    )
    
    # Return the token
    return {"access_token": access_token, "token_type": "bearer"}