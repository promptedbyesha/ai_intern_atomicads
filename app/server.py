from fastapi import FastAPI

app = FastAPI(title="Context-Aware Research Brief Generator")

@app.get("/")
def read_root():
    return {"status": "running"}

# Example endpoint matching your API spec
from pydantic import BaseModel

class BriefRequest(BaseModel):
    topic: str
    depth: int
    follow_up: bool
    user_id: str

@app.post("/brief")
def generate_brief(request: BriefRequest):
    return {"message": f"Received topic '{request.topic}' for user {request.user_id}"}
