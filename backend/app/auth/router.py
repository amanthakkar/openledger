from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.jwt import create_access_token, decode_token
from app.auth.models import User
from app.auth.schemas import LoginRequest, SignupRequest, UserResponse
from app.auth.service import hash_password, verify_password
from app.database import get_db

router = APIRouter()


@router.post("/signup")
def signup(payload: SignupRequest, response: Response, db: Session = Depends(get_db)) -> UserResponse:
    existing = db.scalar(select(User).where(User.email == payload.email.lower()))
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = User(email=payload.email.lower(), password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(str(user.id))
    response.set_cookie(
        key="openledger_access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24,
        path="/",
    )
    return UserResponse(id=user.id, email=user.email)


@router.post("/login")
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)) -> UserResponse:
    user = db.scalar(select(User).where(User.email == payload.email.lower()))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(str(user.id))
    response.set_cookie(
        key="openledger_access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24,
        path="/",
    )
    return UserResponse(id=user.id, email=user.email)


@router.get("/me")
def me(user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse(id=user.id, email=user.email)


@router.get("/session")
def session(user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse(id=user.id, email=user.email)


@router.post("/logout")
def logout(response: Response) -> dict[str, str]:
    response.delete_cookie("openledger_access_token", path="/")
    return {"message": "Logged out"}
