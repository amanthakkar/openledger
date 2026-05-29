from datetime import datetime

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.database import get_db
from app.plaid.models import Account, PlaidItem
from app.plaid.schemas import PublicTokenExchangeRequest, SyncRequest
from app.plaid.service import decrypt_token, encrypt_token, plaid_configured, plaid_post, upsert_accounts, upsert_transactions

router = APIRouter()


@router.post("/link-token/create")
def create_link_token(user: User = Depends(get_current_user)) -> dict:
    if not plaid_configured():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Plaid credentials are not configured")

    try:
        response = plaid_post(
            "/link/token/create",
            {
                "client_name": "OpenLedger",
                "country_codes": ["US"],
                "language": "en",
                "products": ["transactions"],
                "user": {"client_user_id": str(user.id)},
            },
        )
        return {"link_token": response["link_token"], "expiration": response.get("expiration")}
    except httpx.HTTPStatusError as exc:
        detail = exc.response.text if exc.response is not None else str(exc)
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Plaid error: {detail}") from exc


@router.post("/item/public_token/exchange")
def exchange_public_token(
    payload: PublicTokenExchangeRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    if not plaid_configured():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Plaid credentials are not configured")

    try:
        exchanged = plaid_post("/item/public_token/exchange", {"public_token": payload.public_token})
        access_token = exchanged["access_token"]
        item_id = exchanged["item_id"]

        item_response = plaid_post("/item/get", {"access_token": access_token})
        institution_id = item_response["item"].get("institution_id") or "unknown"
        institution_name = "Unknown institution"

        if institution_id != "unknown":
            try:
                institution = plaid_post(
                    "/institutions/get_by_id",
                    {"institution_id": institution_id, "country_codes": ["US"]},
                )
                institution_name = institution.get("institution", {}).get("name") or institution_name
            except httpx.HTTPError:
                pass

        plaid_item = db.scalar(select(PlaidItem).where(PlaidItem.user_id == user.id, PlaidItem.institution_id == item_id))
        if plaid_item:
            plaid_item.access_token_encrypted = encrypt_token(access_token)
            plaid_item.institution_name = institution_name
            plaid_item.status = "healthy"
            plaid_item.last_synced_at = datetime.utcnow()
        else:
            plaid_item = PlaidItem(
                user_id=user.id,
                institution_name=institution_name,
                institution_id=item_id,
                access_token_encrypted=encrypt_token(access_token),
                status="healthy",
                last_synced_at=datetime.utcnow(),
            )
            db.add(plaid_item)
            db.flush()

        accounts_response = plaid_post("/accounts/get", {"access_token": access_token})
        upsert_accounts(db, user.id, plaid_item, accounts_response.get("accounts", []))
        db.commit()
        return {
            "message": "Plaid item connected",
            "item_id": plaid_item.id,
            "institution_name": institution_name,
            "accounts_added": len(accounts_response.get("accounts", [])),
        }
    except httpx.HTTPStatusError as exc:
        db.rollback()
        detail = exc.response.text if exc.response is not None else str(exc)
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Plaid error: {detail}") from exc


@router.post("/transactions/sync")
def sync_transactions(
    payload: SyncRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    if not plaid_configured():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Plaid credentials are not configured")

    query = select(PlaidItem).where(PlaidItem.user_id == user.id)
    if payload.item_id:
        query = query.where(PlaidItem.id == payload.item_id)
    items = list(db.scalars(query))
    if not items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No connected Plaid items")

    total_created = 0
    try:
        for item in items:
            access_token = decrypt_token(item.access_token_encrypted)
            cursor = item.cursor
            has_more = True
            while has_more:
                sync_response = plaid_post(
                    "/transactions/sync",
                    {"access_token": access_token, "cursor": cursor},
                )
                upsert_accounts(db, user.id, item, sync_response.get("accounts", []))
                total_created += upsert_transactions(db, user.id, sync_response.get("added", []))
                cursor = sync_response.get("next_cursor")
                has_more = bool(sync_response.get("has_more"))
            item.cursor = cursor
            item.last_synced_at = datetime.utcnow()
            item.status = "healthy"
        db.commit()
        return {"message": "Transactions synced", "new_transactions": total_created}
    except httpx.HTTPStatusError as exc:
        db.rollback()
        detail = exc.response.text if exc.response is not None else str(exc)
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Plaid error: {detail}") from exc


@router.get("/accounts")
def list_accounts(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    accounts = list(
        db.scalars(
            select(Account).where(Account.user_id == user.id).order_by(Account.updated_at.desc().nullslast())
        )
    )
    items = {item.id: item for item in db.scalars(select(PlaidItem).where(PlaidItem.user_id == user.id))}
    return {
        "accounts": [
            {
                "id": str(account.id),
                "institution": items.get(account.plaid_item_id).institution_name if items.get(account.plaid_item_id) else "Unknown",
                "name": account.name,
                "type": account.type,
                "subtype": account.subtype or "",
                "balance": float(account.current_balance or 0),
                "status": items.get(account.plaid_item_id).status if items.get(account.plaid_item_id) else "unknown",
            }
            for account in accounts
        ]
    }
