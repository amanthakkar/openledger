from fastapi import Cookie, Depends
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.auth.jwt import decode_token
from app.auth.models import User
from app.database import get_db
from app.splitwise.models import SplitwiseConnection


def _ensure_local_user(db: Session) -> User:
    # Single-user local mode fallback:
    # 1) Prefer user with a Splitwise connection (existing configured account)
    # 2) Else use most recently created user
    # 3) Else create a local default user
    splitwise_user_id = db.scalar(select(SplitwiseConnection.user_id).order_by(desc(SplitwiseConnection.updated_at)))
    if splitwise_user_id:
        user = db.get(User, int(splitwise_user_id))
        if user:
            return user

    existing = db.scalar(select(User).order_by(desc(User.created_at)))
    if existing:
        return existing

    user = User(email="local@openledger.local", password_hash="local-mode-no-password")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_current_user(
    openledger_access_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
) -> User:
    if not openledger_access_token:
        return _ensure_local_user(db)

    payload = decode_token(openledger_access_token)
    if not payload or "sub" not in payload:
        return _ensure_local_user(db)

    user = db.get(User, int(payload["sub"]))
    if not user:
        return _ensure_local_user(db)

    return user
