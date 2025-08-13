# tests/test_graph.py

from app.graph import workflow, ResearchState
from app.schemas import FinalBrief
from pathlib import Path
import json


def test_workflow_brief():
    state = ResearchState(
        topic="Test Topic",
        depth=1,
        follow_up=False,
        user_id="tester"
    )
    # workflow.invoke() returns a dict, so convert it to ResearchState
    result_dict = workflow.invoke(state)
    result = ResearchState.model_validate(result_dict)

    brief = result.final_brief
    assert isinstance(brief, FinalBrief)
    assert brief.topic == "Test Topic"
    assert len(brief.plan.steps) > 0, "Plan should have steps"

    # ✅ Additional check: Verify checkpoint file is created and contains the test user
    checkpoint_file = Path("checkpoints.json")
    assert checkpoint_file.exists(), "Checkpoints file should be created"
    with open(checkpoint_file) as f:
        data = json.load(f)
        assert "tester" in data, "Checkpoint for this user_id should exist"
        assert "state" in data["tester"], "Checkpoint should contain state data"


def test_retry_mechanism(monkeypatch):
    """
    Simulate a failure in one workflow node to ensure the retry decorator works.
    """
    call_count = {"count": 0}
    from app import graph

    original_search_node = graph.search_node

    def faulty_search_node(state):
        if call_count["count"] < 1:
            call_count["count"] += 1
            raise Exception("Simulated search failure")
        return original_search_node(state)

    monkeypatch.setattr(graph, "search_node", faulty_search_node)

    state = graph.ResearchState(
        topic="Retry Test",
        depth=1,
        follow_up=False,
        user_id="retry_user"
    )

    # workflow.invoke() returns a dict, so convert it to ResearchState
    result_dict = workflow.invoke(state)
    result = ResearchState.model_validate(result_dict)

    brief = result.final_brief
    assert isinstance(brief, FinalBrief)
    assert brief.topic == "Retry Test"

    # Restore original function
    monkeypatch.setattr(graph, "search_node", original_search_node)

    # ✅ Verify checkpoint contains retry_user
    checkpoint_file = Path("checkpoints.json")
    assert checkpoint_file.exists(), "Checkpoints file should be created"
    with open(checkpoint_file) as f:
        data = json.load(f)
        assert "retry_user" in data, "Checkpoint for this retry_user should exist"
