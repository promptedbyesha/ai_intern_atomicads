# app/schemas.py

from pydantic import BaseModel
from typing import List

class ResearchPlan(BaseModel):
    steps: List[str]

class SourceSummary(BaseModel):
    source_url: str
    summary: str

class FinalBrief(BaseModel):
    topic: str
    plan: ResearchPlan
    sources: List[SourceSummary]
    references: List[str]
