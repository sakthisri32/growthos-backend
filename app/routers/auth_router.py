from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas, auth
from app.database import get_db
from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=schemas.Token, status_code=status.HTTP_201_CREATED)
def register(payload: schemas.UserRegister, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email already exists")

    user = models.User(
        name=payload.name,
        email=payload.email,
        hashed_password=auth.hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # In production: send a verification email containing this token.
    verify_token = auth.create_special_token({"sub": user.id, "purpose": "verify"}, timedelta(hours=24))
    _ = verify_token  # send via email service

    token = auth.create_access_token({"sub": user.id})
    return schemas.Token(access_token=token, user=schemas.UserOut.model_validate(user))


@router.post("/login", response_model=schemas.Token)
def login(payload: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user or not user.hashed_password or not auth.verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    token = auth.create_access_token({"sub": user.id})
    return schemas.Token(access_token=token, user=schemas.UserOut.model_validate(user))


@router.post("/google", response_model=schemas.Token)
def google_login(payload: schemas.GoogleAuth, db: Session = Depends(get_db)):
    """
    Verifies the Google ID token and logs the user in, creating an account
    on first sign-in. Requires GOOGLE_CLIENT_ID to be set.
    """
    try:
        from google.oauth2 import id_token as google_id_token
        from google.auth.transport import requests as google_requests

        idinfo = google_id_token.verify_oauth2_token(
            payload.id_token, google_requests.Request(), settings.GOOGLE_CLIENT_ID
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Google token")

    google_id = idinfo["sub"]
    email = idinfo["email"]
    name = idinfo.get("name", email.split("@")[0])
    avatar = idinfo.get("picture")

    user = db.query(models.User).filter(models.User.google_id == google_id).first()
    if not user:
        user = db.query(models.User).filter(models.User.email == email).first()
        if user:
            user.google_id = google_id
        else:
            user = models.User(
                name=name, email=email, google_id=google_id, avatar_url=avatar, is_verified=True
            )
            db.add(user)
        db.commit()
        db.refresh(user)

    token = auth.create_access_token({"sub": user.id})
    return schemas.Token(access_token=token, user=schemas.UserOut.model_validate(user))


@router.post("/forgot-password")
def forgot_password(payload: schemas.ForgotPassword, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user:
        # Don't leak whether the email exists.
        return {"message": "If that email exists, a reset link has been sent."}

    reset_token = auth.create_special_token({"sub": user.id, "purpose": "reset"}, timedelta(minutes=30))
    # In production: email a link like {FRONTEND_URL}/reset-password?token=reset_token
    return {"message": "If that email exists, a reset link has been sent.", "dev_token": reset_token}


@router.post("/reset-password")
def reset_password(payload: schemas.ResetPassword, db: Session = Depends(get_db)):
    data = auth.decode_token(payload.token)
    if data.get("purpose") != "reset":
        raise HTTPException(status_code=400, detail="Invalid reset token")

    user = db.query(models.User).filter(models.User.id == data["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = auth.hash_password(payload.new_password)
    db.commit()
    return {"message": "Password updated successfully"}


@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    data = auth.decode_token(token)
    if data.get("purpose") != "verify":
        raise HTTPException(status_code=400, detail="Invalid verification token")

    user = db.query(models.User).filter(models.User.id == data["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_verified = True
    db.commit()
    return {"message": "Email verified successfully"}


@router.get("/me", response_model=schemas.UserOut)
def me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user
