# app/graph.py

from langgraph.graph import StateGraph
from pydantic import BaseModel
from typing import List

from app.schemas import ResearchPlan, SourceSummary, FinalBrief

class ResearchState(BaseModel):
    topic: str
    depth: int
    follow_up: bool
    user_id: str
    history_summary: str = ""
    plan: ResearchPlan = ResearchPlan(steps=[])
    sources: List[str] = []
    summaries: List[SourceSummary] = []
    references: List[str] = []
    final_brief: FinalBrief = None

def context_summarization(state: ResearchState) -> ResearchState:
    if state.follow_up:
        state.history_summary = f"Previous briefs summary for user {state.user_id}"
    else:
        state.history_summary = "No prior history."
    return state

def planning_node(state: ResearchState) -> ResearchState:
    state.plan = ResearchPlan(
        steps=[f"Step {i+1} for research on {state.topic}" for i in range(state.depth)]
    )
    return state

def search_node(state: ResearchState) -> ResearchState:
    state.sources = [
        f"https://example.com/{state.topic.replace(' ', '_')}_article_{i+1}"
        for i in range(1, state.depth + 1)
    ]
    return state

def content_fetching_node(state: ResearchState) -> ResearchState:
    return state

def per_source_summary_node(state: ResearchState) -> ResearchState:
    state.summaries = [
        SourceSummary(source_url=src, summary=f"Summary for {src}") for src in state.sources
    ]
    return state

def synthesis_node(state: ResearchState) -> ResearchState:
    state.references = state.sources
    return state

def post_processing_node(state: ResearchState) -> ResearchState:
    state.final_brief = FinalBrief(
        topic=state.topic,
        plan=state.plan,
        sources=state.summaries,
        references=state.references
    )
    return state

graph = StateGraph(ResearchState)

graph.add_node("context_summarization", context_summarization)
graph.add_node("planning", planning_node)
graph.add_node("search", search_node)
graph.add_node("content_fetching", content_fetching_node)
graph.add_node("per_source_summary", per_source_summary_node)
graph.add_node("synthesis", synthesis_node)
graph.add_node("post_processing", post_processing_node)

graph.add_edge("context_summarization", "planning")
graph.add_edge("planning", "search")
graph.add_edge("search", "content_fetching")
graph.add_edge("content_fetching", "per_source_summary")
graph.add_edge("per_source_summary", "synthesis")
graph.add_edge("synthesis", "post_processing")

graph.set_entry_point("context_summarization")
graph.set_finish_point("post_processing")

workflow = graph.compile()
