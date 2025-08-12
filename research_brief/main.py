from research_brief.schemas import BriefRequest, FinalBrief

async def generate_brief(request: BriefRequest) -> FinalBrief:
    # Later you'll replace this with LangGraph logic
    return FinalBrief(
        topic=request.topic,
        depth=request.depth,
        follow_up=request.follow_up,
        user_id=request.user_id,
        summary="Generated research brief goes here.",
        references=[]
    )
