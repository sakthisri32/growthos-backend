import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas, auth
from app.database import get_db
from app.config import settings

router = APIRouter(prefix="/api/ai", tags=["AI Coach"])


def _build_context(user: models.User) -> str:
    open_tasks = [t.title for t in user.tasks if not t.completed][:10]
    skills = [f"{s.name} ({s.progress_percent}%)" for s in user.skills][:10]
    goals = [g.title for g in user.goals if not g.completed][:10]
    return (
        f"Open tasks: {', '.join(open_tasks) or 'none'}\n"
        f"Skills in progress: {', '.join(skills) or 'none'}\n"
        f"Active goals: {', '.join(goals) or 'none'}"
    )


@router.post("/coach", response_model=schemas.AICoachResponse)
def ai_coach(
    payload: schemas.AICoachRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if not settings.ANTHROPIC_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="AI Coach isn't configured yet — set ANTHROPIC_API_KEY in the backend environment.",
        )

    import anthropic

    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    context = _build_context(current_user)

    system_prompt = (
        "You are GrowthOS's AI Coach. Given a user's available hours today and their "
        "current tasks/skills/goals, produce a focused, realistic plan. Respond ONLY "
        "with JSON: {\"plan\": \"<2-4 sentence plan in plain text>\", "
        "\"suggested_tasks\": [\"<short task 1>\", \"<short task 2>\", ...]} "
        "with at most 6 suggested_tasks."
    )
    user_prompt = (
        f"Hours available today: {payload.hours_available}\n"
        f"Focus area: {payload.focus_area or 'none specified'}\n"
        f"User note: {payload.message or 'none'}\n\n"
        f"{context}"
    )

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )

    raw_text = "".join(block.text for block in response.content if block.type == "text")
    try:
        cleaned = raw_text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        parsed = json.loads(cleaned)
        return schemas.AICoachResponse(plan=parsed["plan"], suggested_tasks=parsed.get("suggested_tasks", []))
    except Exception:
        # Fall back to returning the raw text as the plan if parsing fails.
        return schemas.AICoachResponse(plan=raw_text, suggested_tasks=[])
