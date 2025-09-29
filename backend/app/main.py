from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine
from app.db import base as models
from app.api.v1 import deps
from app.api.v1.endpoints import auth, google, documents, logout

# This creates all the database tables(if they don't exist)
models.Base.metadata.create_all(bind=engine)

# Create an instance of the FastAPI class
app = FastAPI(title="AetherNotes API")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    # Add your deployed frontend URL here later
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Allow only the specified origins
    allow_credentials=True, # Allow cookies and authorization headers
    allow_methods=["*"], # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"], # Allow all headers
)

# Define a route for the root URL ("/")
@app.get("/")
def read_root():
    return {"message": "Welcome to AetherNotes API"}

# Define a  simple, top-level health check endpoint
@app.get("/api/health")
def health_check(db: Session = Depends(deps.get_db)):
    try:
        db.execute(text('SELECT 1'))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "detail": str(e)}

# API routers
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(google.router, prefix="/api/v1", tags=["Google Authentication"])
app.include_router(documents.router, prefix="/api/v1", tags=["Document Upload"])
app.include_router(logout.router, prefix="/api/v1", tags=["Logout"])
