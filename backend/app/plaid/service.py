from datetime import datetime

import httpx
from cryptography.fernet import Fernet
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.plaid.models import Account, PlaidItem, Transaction


cipher = Fernet(settings.encryption_key.encode())


def encrypt_token(token: str) -> str:
    return cipher.encrypt(token.encode()).decode()


def decrypt_token(encrypted_token: str) -> str:
    return cipher.decrypt(encrypted_token.encode()).decode()


def plaid_base_url() -> str:
    env = settings.plaid_env.lower().strip()
    if env == "production":
        return "https://production.plaid.com"
    if env == "development":
        return "https://development.plaid.com"
    return "https://sandbox.plaid.com"


def plaid_configured() -> bool:
    return bool(settings.plaid_client_id and settings.plaid_secret)


def plaid_post(path: str, payload: dict) -> dict:
    body = {
        "client_id": settings.plaid_client_id,
        "secret": settings.plaid_secret,
        **payload,
    }
    with httpx.Client(timeout=30) as client:
        response = client.post(f"{plaid_base_url()}{path}", json=body)
    response.raise_for_status()
    return response.json()


def upsert_accounts(db: Session, user_id: int, plaid_item: PlaidItem, accounts: list[dict]) -> None:
    for record in accounts:
        existing = db.scalar(select(Account).where(Account.plaid_account_id == record["account_id"]))
        if existing:
            existing.name = record.get("name") or existing.name
            existing.official_name = record.get("official_name")
            existing.type = record.get("type") or existing.type
            existing.subtype = record.get("subtype")
            balances = record.get("balances", {})
            existing.current_balance = balances.get("current")
            existing.available_balance = balances.get("available")
            existing.currency = balances.get("iso_currency_code") or "USD"
            existing.updated_at = datetime.utcnow()
            continue

        balances = record.get("balances", {})
        db.add(
            Account(
                user_id=user_id,
                plaid_item_id=plaid_item.id,
                plaid_account_id=record["account_id"],
                name=record.get("name") or "Account",
                official_name=record.get("official_name"),
                type=record.get("type") or "unknown",
                subtype=record.get("subtype"),
                current_balance=balances.get("current"),
                available_balance=balances.get("available"),
                currency=balances.get("iso_currency_code") or "USD",
                updated_at=datetime.utcnow(),
            )
        )


def upsert_transactions(db: Session, user_id: int, rows: list[dict]) -> int:
    created = 0
    for row in rows:
        plaid_transaction_id = row.get("transaction_id")
        if not plaid_transaction_id:
            continue

        existing = db.scalar(select(Transaction).where(Transaction.plaid_transaction_id == plaid_transaction_id))
        account = db.scalar(select(Account).where(Account.plaid_account_id == row.get("account_id")))
        if not account:
            continue

        category = None
        subcategory = None
        pfc = row.get("personal_finance_category")
        if isinstance(pfc, dict):
            category = pfc.get("primary")
            subcategory = pfc.get("detailed")

        if existing:
            existing.date = datetime.fromisoformat(row["date"]).date()
            existing.merchant_name = row.get("merchant_name")
            existing.description = row.get("name")
            existing.amount = row.get("amount", 0)
            existing.category = category
            existing.subcategory = subcategory
            continue

        db.add(
            Transaction(
                user_id=user_id,
                account_id=account.id,
                plaid_transaction_id=plaid_transaction_id,
                date=datetime.fromisoformat(row["date"]).date(),
                merchant_name=row.get("merchant_name"),
                description=row.get("name"),
                amount=row.get("amount", 0),
                category=category,
                subcategory=subcategory,
                is_recurring=False,
                is_excluded=False,
            )
        )
        created += 1
    return created
