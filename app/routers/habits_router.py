import json
from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas, auth
from app.database import get_db

router = APIRouter(prefix="/api/habits", tags=["Habits"])


def _load_logs(habit: models.Habit) -> list:
    return json.loads(habit.logs) if habit.logs else []


def _save_logs(habit: models.Habit, logs: list):
    habit.logs = json.dumps(sorted(logs))


def _recompute_streak(logs: list) -> tuple:
    """Returns (current_streak, longest_streak) based on consecutive days ending today."""
    if not logs:
        return 0, 0
    days = sorted({date.fromisoformat(d) for d in logs})
    longest = current = 1
    for i in range(1, len(days)):
        if (days[i] - days[i - 1]).days == 1:
            current += 1
        else:
            current = 1
        longest = max(longest, current)

    today = date.today()
    if days[-1] == today or days[-1] == today - timedelta(days=1):
        streak = current
    else:
        streak = 0
    return streak, longest


@router.get("", response_model=list[schemas.HabitOut])
def list_habits(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Habit).filter(models.Habit.user_id == current_user.id).order_by(models.Habit.created_at.desc()).all()


@router.post("", response_model=schemas.HabitOut, status_code=201)
def create_habit(payload: schemas.HabitCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    habit = models.Habit(**payload.model_dump(), user_id=current_user.id, logs=json.dumps([]))
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit


@router.put("/{habit_id}", response_model=schemas.HabitOut)
def update_habit(habit_id: str, payload: schemas.HabitUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id, models.Habit.user_id == current_user.id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(habit, key, value)
    db.commit()
    db.refresh(habit)
    return habit


@router.delete("/{habit_id}", status_code=204)
def delete_habit(habit_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id, models.Habit.user_id == current_user.id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    db.delete(habit)
    db.commit()
    return None


@router.post("/{habit_id}/check-in", response_model=schemas.HabitOut)
def check_in(habit_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    """Marks the habit as done for today (idempotent) and recomputes streaks."""
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id, models.Habit.user_id == current_user.id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    logs = _load_logs(habit)
    today_str = date.today().isoformat()
    if today_str not in logs:
        logs.append(today_str)
    _save_logs(habit, logs)

    current_streak, longest_streak = _recompute_streak(logs)
    habit.current_streak = current_streak
    habit.longest_streak = max(habit.longest_streak, longest_streak)

    db.commit()
    db.refresh(habit)
    return habit
