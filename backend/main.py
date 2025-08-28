from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
import database

# Create all database tables (if they don't exists)
database.Base.metadata.create_all(bind=database.engine)

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