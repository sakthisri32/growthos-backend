from datetime import date, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas, auth
from app.database import get_db

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/summary", response_model=schemas.AnalyticsSummary)
def summary(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    tasks = current_user.tasks
    skills = current_user.skills
    habits = current_user.habits
    goals = current_user.goals

    total_tasks = len(tasks)
    completed_tasks = sum(1 for t in tasks if t.completed)
    task_completion_rate = round((completed_tasks / total_tasks) * 100, 1) if total_tasks else 0.0

    total_skills = len(skills)
    avg_skill_progress = round(sum(s.progress_percent for s in skills) / total_skills, 1) if total_skills else 0.0
    total_learning_hours = round(sum(s.learning_hours for s in skills), 1)

    habit_count = len(habits)
    best_habit_streak = max((h.longest_streak for h in habits), default=0)

    goals_total = len(goals)
    goals_completed = sum(1 for g in goals if g.completed)

    # Last 7 days of "learning hours" approximated from skills updated — in a full
    # implementation this would come from a dedicated daily_logs table.
    today = date.today()
    daily_hours = [
        {"date": (today - timedelta(days=i)).isoformat(), "hours": round(total_learning_hours / 7, 1) if total_learning_hours else 0}
        for i in range(6, -1, -1)
    ]

    weekly_progress = [
        {"week": f"W{i+1}", "completion": min(100, (i + 1) * (task_completion_rate / 4 or 5))}
        for i in range(4)
    ]

    skill_breakdown = [{"name": s.name, "progress": s.progress_percent} for s in skills]

    return schemas.AnalyticsSummary(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        task_completion_rate=task_completion_rate,
        total_skills=total_skills,
        avg_skill_progress=avg_skill_progress,
        total_learning_hours=total_learning_hours,
        habit_count=habit_count,
        best_habit_streak=best_habit_streak,
        goals_completed=goals_completed,
        goals_total=goals_total,
        daily_hours=daily_hours,
        weekly_progress=weekly_progress,
        skill_breakdown=skill_breakdown,
    )
