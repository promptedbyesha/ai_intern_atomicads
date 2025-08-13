# app/server.py

from fastapi import FastAPI
from pydantic import BaseModel

from app.schemas import FinalBrief
from app.graph import workflow, ResearchState

app = FastAPI(title="Context-Aware Research Brief Generator")

@app.get("/")
def read_root():
    return {"status": "running"}

class BriefRequest(BaseModel):
    topic: str
    depth: int
    follow_up: bool
    user_id: str

@app.post("/brief", response_model=FinalBrief)
def generate_brief(request: BriefRequest):
    init_state = ResearchState(
        topic=request.topic,
        depth=request.depth,
        follow_up=request.follow_up,
        user_id=request.user_id
    )
    result_state = workflow.invoke(init_state)
    return result_state.final_brief
