from datetime import date, timedelta


def recent_transactions() -> list[dict]:
    return [
        {"id": "tx_1", "date": "2026-05-16", "merchant": "Whole Foods", "category": "Groceries", "amount": -86.43},
        {"id": "tx_2", "date": "2026-05-16", "merchant": "Uber", "category": "Transport", "amount": -23.15},
        {"id": "tx_3", "date": "2026-05-15", "merchant": "Payroll", "category": "Income", "amount": 2400.00},
        {"id": "tx_4", "date": "2026-05-14", "merchant": "Netflix", "category": "Subscriptions", "amount": -19.99},
        {"id": "tx_5", "date": "2026-05-13", "merchant": "Shell", "category": "Transport", "amount": -52.04},
    ]


def spending_breakdown() -> list[dict]:
    return [
        {"category": "Groceries", "amount": 640},
        {"category": "Dining", "amount": 325},
        {"category": "Transport", "amount": 215},
        {"category": "Subscriptions", "amount": 89},
        {"category": "Utilities", "amount": 172},
    ]


def net_worth_history(days: int = 7) -> list[dict]:
    start = date.today() - timedelta(days=days - 1)
    base = 128_450
    deltas = [0, 80, -120, 240, 320, -40, 410]
    history = []
    running = base
    for idx in range(days):
        running += deltas[idx % len(deltas)]
        history.append({"date": (start + timedelta(days=idx)).isoformat(), "value": running})
    return history


def overview_payload() -> dict:
    assets = 163_200.50
    liabilities = 34_125.22
    net_worth = round(assets - liabilities, 2)
    previous = 128_180.00
    return {
        "summary": {
            "net_worth": net_worth,
            "assets": assets,
            "liabilities": liabilities,
            "change_1d": 410.0,
            "change_30d": round(net_worth - previous, 2),
        },
        "account_groups": [
            {"group": "Cash", "total": 18240.80},
            {"group": "Credit", "total": -5125.10},
            {"group": "Investments", "total": 132780.33},
            {"group": "Crypto", "total": 2179.37},
            {"group": "Debts", "total": -29000.12},
        ],
        "spending": spending_breakdown(),
        "recent_transactions": recent_transactions(),
    }
