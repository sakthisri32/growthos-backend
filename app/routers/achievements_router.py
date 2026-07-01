from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas, auth
from app.database import get_db

router = APIRouter(prefix="/api", tags=["Achievements & Notifications"])

BADGES = {
    "30_day_streak": ("30 Day Streak", "Kept any habit alive for 30 days straight."),
    "100_hours_coding": ("100 Hours Coding", "Logged 100+ learning hours on coding skills."),
    "python_master": ("Python Master", "Reached 90%+ progress on a Python skill."),
    "ai_explorer": ("AI Explorer", "Created your first AI/ML skill."),
    "startup_thinker": ("Startup Thinker", "Logged your first startup idea."),
}


@router.get("/achievements", response_model=list[schemas.AchievementOut])
def list_achievements(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Achievement).filter(models.Achievement.user_id == current_user.id).all()


@router.post("/achievements/check", response_model=list[schemas.AchievementOut])
def check_achievements(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    """Evaluates badge conditions against current data and unlocks any newly-earned badges."""
    unlocked_keys = {a.badge_key for a in current_user.achievements}
    newly_unlocked = []

    def unlock(key):
        if key not in unlocked_keys:
            title, desc = BADGES[key]
            badge = models.Achievement(user_id=current_user.id, badge_key=key, title=title, description=desc)
            db.add(badge)
            newly_unlocked.append(badge)

    if any(h.longest_streak >= 30 for h in current_user.habits):
        unlock("30_day_streak")
    if sum(s.learning_hours for s in current_user.skills) >= 100:
        unlock("100_hours_coding")
    if any(s.name.lower() == "python" and s.progress_percent >= 90 for s in current_user.skills):
        unlock("python_master")
    if any(s.category and "ai" in s.category.lower() for s in current_user.skills):
        unlock("ai_explorer")
    if len(current_user.startup_ideas) >= 1:
        unlock("startup_thinker")

    db.commit()
    for b in newly_unlocked:
        db.refresh(b)
    return newly_unlocked


@router.get("/notifications", response_model=list[schemas.NotificationOut])
def list_notifications(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return (
        db.query(models.Notification)
        .filter(models.Notification.user_id == current_user.id)
        .order_by(models.Notification.created_at.desc())
        .limit(50)
        .all()
    )


@router.put("/notifications/{notification_id}/read", response_model=schemas.NotificationOut)
def mark_read(notification_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    n = db.query(models.Notification).filter(models.Notification.id == notification_id, models.Notification.user_id == current_user.id).first()
    if not n:
        raise HTTPException(status_code=404, detail="Notification not found")
    n.is_read = True
    db.commit()
    db.refresh(n)
    return n
