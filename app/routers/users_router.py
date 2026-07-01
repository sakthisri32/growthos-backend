import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas, auth
from app.database import get_db

router = APIRouter(prefix="/api/users", tags=["Users / Settings"])


@router.get("/me", response_model=schemas.UserOut)
def get_profile(current_user: models.User = Depends(auth.get_current_user)):
    return current_user


@router.put("/me", response_model=schemas.UserOut)
def update_profile(payload: schemas.UserUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.post("/me/change-password")
def change_password(payload: schemas.PasswordChange, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    if not current_user.hashed_password or not auth.verify_password(payload.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    current_user.hashed_password = auth.hash_password(payload.new_password)
    db.commit()
    return {"message": "Password changed successfully"}


@router.get("/me/export")
def export_data(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    """Returns a full JSON export of the user's data across every module (for the Settings > Export Data action)."""
    def serialize(rows):
        return [{c.name: getattr(r, c.name) for c in r.__table__.columns} for r in rows]

    data = {
        "profile": {"name": current_user.name, "email": current_user.email},
        "tasks": serialize(current_user.tasks),
        "skills": serialize(current_user.skills),
        "habits": serialize(current_user.habits),
        "goals": serialize(current_user.goals),
        "journal": serialize(current_user.journal_entries),
        "projects": serialize(current_user.projects),
        "research": serialize(current_user.research_items),
        "startup_ideas": serialize(current_user.startup_ideas),
        "reading_list": serialize(current_user.reading_items),
        "achievements": serialize(current_user.achievements),
    }
    # default=str handles datetime/date serialization
    return json.loads(json.dumps(data, default=str))


@router.delete("/me")
def delete_account(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db.delete(current_user)
    db.commit()
    return {"message": "Account deleted"}
