from fastapi import FastAPI

# Create an instance of the FastAPI class
app = FastAPI()

# Define a route for the root URL ("/")
@app.get("/")
def read_root():
    return {"message": "Hello from AetherNotes Backend"}

# Define a health check route
@app.get("/api/health")
def health_check():
    return {"status": "ok"}