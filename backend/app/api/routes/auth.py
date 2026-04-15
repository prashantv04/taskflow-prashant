from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db import models
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(name: str, email: str, password: str, db: Session = Depends(get_db)):
    user = models.User(name=name, email=email, password=hash_password(password))
    db.add(user)
    db.commit()
    return {"message": "User created"}


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.password):
        return {"error": "Invalid credentials"}

    token = create_access_token({"user_id": str(user.id), "email": user.email})
    return {"access_token": token}