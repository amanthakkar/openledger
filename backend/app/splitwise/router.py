from datetime import datetime

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.database import get_db
from app.plaid.service import decrypt_token, encrypt_token
from app.splitwise.models import SplitwiseBalance, SplitwiseConnection
from app.splitwise.schemas import SplitwiseConnectRequest
from app.splitwise.service import normalize_balances, splitwise_get_friends

router = APIRouter()


@router.post("/connect")
def connect(
    payload: SplitwiseConnectRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    token = payload.access_token.strip()
    if not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing Splitwise access token")
    token_type = payload.token_type.lower().strip()
    if token_type not in {"bearer", "api_key"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="token_type must be 'bearer' or 'api_key'")

    connection = db.scalar(select(SplitwiseConnection).where(SplitwiseConnection.user_id == user.id))
    encrypted = encrypt_token(f"{token_type}:{token}")
    if connection:
        connection.access_token_encrypted = encrypted
        connection.updated_at = datetime.utcnow()
    else:
        db.add(SplitwiseConnection(user_id=user.id, access_token_encrypted=encrypted, updated_at=datetime.utcnow()))
    db.commit()
    return {"message": "Splitwise token saved"}


@router.get("/balances")
def balances(
    sync: bool = True,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    connection = db.scalar(select(SplitwiseConnection).where(SplitwiseConnection.user_id == user.id))
    if not connection:
        return {"friends": [], "connected": False}

    if sync:
        try:
            raw = decrypt_token(connection.access_token_encrypted)
            parsed_type, parsed_token = raw.split(":", 1) if ":" in raw else ("bearer", raw)
            friends_payload = splitwise_get_friends(parsed_token, parsed_type)
            normalized = normalize_balances(friends_payload)
            db.execute(delete(SplitwiseBalance).where(SplitwiseBalance.user_id == user.id))
            for friend in normalized:
                db.add(
                    SplitwiseBalance(
                        user_id=user.id,
                        friend_name=friend["friend_name"],
                        friend_id=friend["friend_id"],
                        balance=friend["balance"],
                        updated_at=datetime.utcnow(),
                    )
                )
            db.commit()
        except httpx.HTTPStatusError as exc:
            db.rollback()
            detail = exc.response.text if exc.response is not None else str(exc)
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Splitwise error: {detail}") from exc

    rows = list(db.scalars(select(SplitwiseBalance).where(SplitwiseBalance.user_id == user.id)))
    return {
        "connected": True,
        "friends": [{"name": row.friend_name, "balance": float(row.balance)} for row in rows],
    }
