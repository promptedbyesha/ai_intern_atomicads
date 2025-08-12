from fastapi import FastAPI
from research_brief.schemas import BriefRequest, FinalBrief
from research_brief.main import generate_brief as generate_research_brief

app = FastAPI(title="AI Intern App with Research Brief API")

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Hello, AI Intern!"}

# Research Brief endpoint
@app.post("/brief", response_model=FinalBrief)
async def generate_brief(request: BriefRequest):
    return await generate_research_brief(request)
