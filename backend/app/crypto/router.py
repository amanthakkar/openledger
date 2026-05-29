from fastapi import APIRouter

router = APIRouter()


@router.post("/import")
def import_csv() -> dict[str, str]:
    return {"message": "crypto import placeholder"}


@router.get("/holdings")
def holdings() -> dict:
    return {
        "holdings": [
            {"symbol": "BTC", "quantity": 0.042, "value": 2840.12},
            {"symbol": "ETH", "quantity": 0.55, "value": 1712.40},
        ]
    }
