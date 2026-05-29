import httpx


def splitwise_get_friends(token: str, token_type: str = "bearer") -> list[dict]:
    with httpx.Client(timeout=30) as client:
        response = client.get(
            "https://secure.splitwise.com/api/v3.0/get_friends",
            headers={"Authorization": f"Bearer {token}"},
        )
    response.raise_for_status()
    payload = response.json()
    return payload.get("friends", [])


def normalize_balances(friends_payload: list[dict]) -> list[dict]:
    normalized: list[dict] = []
    for friend in friends_payload:
        net = 0.0
        for balance in friend.get("balance", []):
            if balance.get("currency_code") == "USD":
                try:
                    net += float(balance.get("amount", 0))
                except (TypeError, ValueError):
                    continue
        normalized.append(
            {
                "friend_id": str(friend.get("id")),
                "friend_name": friend.get("first_name") or friend.get("email") or "Unknown",
                "balance": round(net, 2),
            }
        )
    return normalized
