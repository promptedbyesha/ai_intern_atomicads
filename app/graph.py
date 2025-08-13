from langgraph.graph import StateGraph
from pydantic import BaseModel
from typing import List

from app.schemas import ResearchPlan, SourceSummary, FinalBrief

# Import the checkpointing and retry utilities
from utils.checkpointing import save_checkpoint, load_checkpoint, retry

# Import the persistent user context storage helpers
from utils.context_store import save_user_context, load_user_context


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


@retry(max_attempts=3, delay=2)
def context_summarization(state: ResearchState) -> ResearchState:
    if state.follow_up:
        # Load previous context summary from SQLite DB
        previous_context = load_user_context(state.user_id) or ""
        state.history_summary = f"Previous briefs summary for user {state.user_id}: {previous_context}"
    else:
        state.history_summary = "No prior history."
    # Save the updated context persistently
    save_user_context(state.user_id, state.history_summary)
    # Save checkpoint of current state
    save_checkpoint(state.user_id, "context_summarization", state.model_dump())
    return state


@retry(max_attempts=3, delay=2)
def planning_node(state: ResearchState) -> ResearchState:
    state.plan = ResearchPlan(
        steps=[f"Step {i+1} for research on {state.topic}" for i in range(state.depth)]
    )
    save_checkpoint(state.user_id, "planning", state.model_dump())
    return state


@retry(max_attempts=3, delay=2)
def search_node(state: ResearchState) -> ResearchState:
    state.sources = [
        f"https://example.com/{state.topic.replace(' ', '_')}_article_{i+1}"
        for i in range(1, state.depth + 1)
    ]
    save_checkpoint(state.user_id, "search", state.model_dump())
    return state


@retry(max_attempts=3, delay=2)
def content_fetching_node(state: ResearchState) -> ResearchState:
    save_checkpoint(state.user_id, "content_fetching", state.model_dump())
    return state


@retry(max_attempts=3, delay=2)
def per_source_summary_node(state: ResearchState) -> ResearchState:
    state.summaries = [
        SourceSummary(source_url=src, summary=f"Summary for {src}") for src in state.sources
    ]
    save_checkpoint(state.user_id, "per_source_summary", state.model_dump())
    return state


@retry(max_attempts=3, delay=2)
def synthesis_node(state: ResearchState) -> ResearchState:
    state.references = state.sources
    save_checkpoint(state.user_id, "synthesis", state.model_dump())
    return state


@retry(max_attempts=3, delay=2)
def post_processing_node(state: ResearchState) -> ResearchState:
    state.final_brief = FinalBrief(
        topic=state.topic,
        plan=state.plan,
        sources=state.summaries,
        references=state.references
    )
    save_checkpoint(state.user_id, "post_processing", state.model_dump())
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
