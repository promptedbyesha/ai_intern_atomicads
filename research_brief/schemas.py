# research_brief/schemas.py
from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class BriefRequest(BaseModel):
    topic: str
    depth: int
    follow_up: bool
    user_id: str

class Reference(BaseModel):
    url: HttpUrl
    title: str
    snippet: Optional[str] = None

class FinalBrief(BaseModel):
    topic: str
    depth: int
    follow_up: bool
    user_id: str
    summary: str
    references: List[Reference]
