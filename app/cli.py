# app/cli.py

import typer
from app.graph import workflow, ResearchState

app = typer.Typer()

@app.command()
def brief(topic: str, depth: int = 2, follow_up: bool = False, user_id: str = "default"):
    state = ResearchState(topic=topic, depth=depth, follow_up=follow_up, user_id=user_id)
    result = workflow.invoke(state)
    print(result.final_brief.json(indent=2))

if __name__ == "__main__":
    app()
