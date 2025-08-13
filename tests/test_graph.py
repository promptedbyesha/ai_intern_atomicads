# tests/test_graph.py

from app.graph import workflow, ResearchState
from app.schemas import FinalBrief

def test_workflow_brief():
    state = ResearchState(
        topic="Test Topic",
        depth=1,
        follow_up=False,
        user_id="tester"
    )
    result = workflow.invoke(state)
    brief = result.final_brief
    assert isinstance(brief, FinalBrief)
    assert brief.topic == "Test Topic"
    assert len(brief.plan.steps) > 0, "Plan should have steps"
