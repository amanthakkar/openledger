from datetime import date, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.database import get_db
from app.plaid.models import Account, Transaction
from app.splitwise.models import SplitwiseBalance

router = APIRouter()


@router.get("/overview")
def overview(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    accounts = list(db.scalars(select(Account).where(Account.user_id == user.id)))
    transactions = list(
        db.scalars(select(Transaction).where(Transaction.user_id == user.id).order_by(desc(Transaction.date)).limit(10))
    )
    splitwise_balances = list(db.scalars(select(SplitwiseBalance).where(SplitwiseBalance.user_id == user.id)))

    assets = 0.0
    liabilities = 0.0
    groups: dict[str, float] = {"Cash": 0.0, "Credit": 0.0, "Investments": 0.0, "Crypto": 0.0, "Debts": 0.0}
    for account in accounts:
        bal = float(account.current_balance or 0)
        category = "Cash"
        if account.type == "credit":
            category = "Credit"
        elif account.type == "investment":
            category = "Investments"
        elif account.type in {"loan", "mortgage"}:
            category = "Debts"
        elif account.type == "crypto":
            category = "Crypto"

        groups[category] = groups.get(category, 0.0) + bal
        if bal >= 0:
            assets += bal
        else:
            liabilities += abs(bal)

    splitwise_net = round(sum(float(row.balance or 0) for row in splitwise_balances), 2)
    if splitwise_net >= 0:
        assets += splitwise_net
    else:
        liabilities += abs(splitwise_net)

    recent = [
        {
            "id": str(item.id),
            "date": item.date.isoformat(),
            "merchant": item.merchant_name or item.description or "Unknown",
            "category": item.category or "uncategorized",
            "amount": float(item.amount),
        }
        for item in transactions
    ]
    spending_map: dict[str, float] = {}
    for item in transactions:
        amount = float(item.amount)
        if amount > 0:
            continue
        key = item.category or "uncategorized"
        spending_map[key] = spending_map.get(key, 0.0) + abs(amount)

    return {
        "summary": {
            "net_worth": round(assets - liabilities, 2),
            "assets": round(assets, 2),
            "liabilities": round(liabilities, 2),
            "change_1d": 0.0,
            "change_30d": 0.0,
            "splitwise_net": splitwise_net,
        },
        "account_groups": [{"group": name, "total": round(total, 2)} for name, total in groups.items()],
        "spending": [{"category": name, "amount": round(total, 2)} for name, total in spending_map.items()],
        "recent_transactions": recent,
    }


@router.get("/net-worth")
def net_worth(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    accounts = list(db.scalars(select(Account).where(Account.user_id == user.id)))
    splitwise_balances = list(db.scalars(select(SplitwiseBalance).where(SplitwiseBalance.user_id == user.id)))
    current_assets = sum(max(float(a.current_balance or 0), 0) for a in accounts)
    current_liabilities = sum(abs(min(float(a.current_balance or 0), 0)) for a in accounts)
    splitwise_net = sum(float(row.balance or 0) for row in splitwise_balances)
    if splitwise_net >= 0:
        current_assets += splitwise_net
    else:
        current_liabilities += abs(splitwise_net)
    current = round(current_assets - current_liabilities, 2)

    points = []
    start = date.today() - timedelta(days=29)
    for idx in range(30):
        points.append({"date": (start + timedelta(days=idx)).isoformat(), "value": round(current - (29 - idx) * 8.5, 2)})
    return {"history": points}


@router.get("/spending")
def spending(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    transactions = list(db.scalars(select(Transaction).where(Transaction.user_id == user.id).order_by(desc(Transaction.date)).limit(200)))
    buckets: dict[str, float] = {}
    for row in transactions:
        amount = float(row.amount)
        if amount >= 0:
            continue
        category = row.category or "uncategorized"
        buckets[category] = buckets.get(category, 0.0) + abs(amount)
    categories = [{"category": key, "amount": round(value, 2)} for key, value in buckets.items()]
    return {"categories": categories}


@router.get("/transactions/recent")
def recent(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    items = list(db.scalars(select(Transaction).where(Transaction.user_id == user.id).order_by(desc(Transaction.date)).limit(20)))
    return {
        "items": [
            {
                "id": str(item.id),
                "date": item.date.isoformat(),
                "merchant": item.merchant_name or item.description or "Unknown",
                "category": item.category or "uncategorized",
                "amount": float(item.amount),
            }
            for item in items
        ]
    }
