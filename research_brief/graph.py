# research_brief/graph.py
from research_brief.schemas import FinalBrief, Reference

async def run_workflow(request) -> FinalBrief:
    # TODO: Replace with actual LangGraph node orchestration
    return FinalBrief(
        topic=request.topic,
        depth=request.depth,
        follow_up=request.follow_up,
        user_id=request.user_id,
        summary=f"Stub summary for topic '{request.topic}' until LangGraph is connected.",
        references=[
            Reference(url="https://example.com", title="Example Source")
        ]
    )
